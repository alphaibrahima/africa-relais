import csv

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.db.models.aggregates import Count, Sum
from django.views.generic import View
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from coupons.forms import AddCouponForm
from coupons.models import Coupon
from dash.forms.staff import (
    PackCreationForm,
    TeamCreationForm,
    TeamUpdateForm,
    UpdateDeliverymenForm,
    AssignCouponToPersonForm,
)
from dash.forms.team import AddRealyPointForm, AssignDelivermenForm
from delivery.models import (
    Bill,
    DeliveryPoint,
    DeparturePoint,
    Package,
    PackageTracking,
)
from delivery_management.constants import TEAM
from delivery_management.utils import decode_utf8
from page.models import Contact, RelayPoint
from delivery_management.constants import IN_PROGRESS, ARRIVED
from send_email.views import assign_deliverymen_email
from user.decorators import staff_required
from dash.forms.team import AddRealyPointsForm
from user.forms import ChangePasswordForm, CustomUserUpdateForm, UpdateProfileForm
from user.models import CustomUser, Pack


@method_decorator([staff_required], name="dispatch")
class StaffView(View):
    template_name = "staff/dashboard.html"
    queryset = CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        income_delivery = Package.objects.all()
        all_package = Package.objects.all()[:3]
        income_deliverman = Package.objects.aggregate(Sum("amount"))["amount__sum"]
        income_realypoint = Package.objects.aggregate(Sum("amount"))["amount__sum"]
        total_incom = (
            income_deliverman + income_realypoint
            if income_deliverman and income_realypoint
            else 0
        )
        total_pack = Pack.objects.aggregate(Count("id"))["id__count"]
        total_realypoint = RelayPoint.objects.aggregate(Count("id"))["id__count"]
        total_users = self.queryset.count()
        total_delivermen = CustomUser.objects.deliverymen().count()

        context = {
            "all_package": all_package,
            "income_delivery": income_delivery,
            "income_deliverman": income_deliverman,
            "income_realypoint": income_realypoint,
            "total_incom": total_incom,
            "total_pack": total_pack,
            "total_users": total_users,
            "total_delivermen": total_delivermen,
            "total_realypoint": total_realypoint,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)


@staff_required
def profile(request):
    user = request.user
    if request.method == "POST":
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Information mise a jour avec succes")
            return redirect("dashboard:staff-dashboard")
        else:
            messages.error(request, f"{form.errors}")
            print("form.errors ", form.errors)
            return redirect("dashboard:staff-dashboard")
    else:
        form = CustomUserUpdateForm(instance=user)
    return render(request, "staff/profile.html", {"form": form})


@method_decorator([staff_required], name="dispatch")
class CustomUserUpdateDetailView(UpdateView, DetailView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    avatar_form = UpdateProfileForm
    password_form = ChangePasswordForm
    template_name = "staff/profile.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(instance=user)
        relay = request.user.point_created.all()
        password_form = self.password_form(user=user)
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "user": user,
                "relay": relay,
                "password_form": password_form,
            },
        )

    def post(self, request, *args, **kwargs):
        user = request.user
        relay = request.user.point_created.all()
        form = self.form_class(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Information modifiée avec succes")
            return redirect("dashboard:staff-profile")
        password_form = self.password_form(user, request.POST)
        if password_form.is_valid():
            password_form.save()
            messages.success(request, "Mot de passe modifiée avec succes")
            return redirect("dashboard:staff-profile")
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "user": user,
                "relay": relay,
                "password_form": password_form,
            },
        )


@method_decorator([staff_required], name="dispatch")
class ProMember(View):
    template_name = "staff/pro.html"
    queryset = CustomUser.objects.professionnals

    def get(self, request, *args, **kwargs):
        professionals = self.queryset()
        return render(
            request,
            self.template_name,
            {
                "professionals": professionals,
            },
        )


@method_decorator([staff_required], name="dispatch")
class TeamMember(View):
    template_name = "staff/team.html"
    form_class = TeamCreationForm
    queryset = CustomUser.objects.teams

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        members = self.queryset()
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "members": members,
            },
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        members = self.queryset()
        context = {"form": form, "members": members}
        if form.is_valid():
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            if password1 == password2:
                team_member = form.save(commit=False)
                team_member.user_type = TEAM
                team_member.set_password(password1)
                team_member.save()
                return redirect("dashboard:team-member")
            else:
                messages.error(
                    request, "Les deux mots de passe ne sont pas identiques!"
                )
                return redirect("dashboard:team-member")
        else:
            context["errors"] = form.errors
        return render(request, self.template_name, context)


@staff_required
def delete_team_member(request, pk):
    data = {}
    try:
        team_member = get_object_or_404(CustomUser, id=pk)
        if request.is_ajax():
            team_member.delete()
            data["message"] = "Responsable supprimé avec succés"
            return JsonResponse(data)
    except Exception:
        data["error"] = "Une erreur innatendue s'est produite"
        return HttpResponseBadRequest(data, content_type="application/json")


@method_decorator([staff_required], name="dispatch")
class UpdateTeamMemberView(UpdateView, DetailView):
    template_name = "staff/update_team.html"
    team_member_form = TeamUpdateForm

    def get(self, request, *args, **kwargs):
        user = request.user
        member = get_object_or_404(CustomUser, id=kwargs["pk"])
        form = self.team_member_form(instance=member)
        context = {"form": form, "user": user, "member": member}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        user = request.user
        member = get_object_or_404(CustomUser, id=kwargs["pk"])
        form = self.team_member_form(request.POST, instance=member)
        if form.is_valid():
            memberteam = form.save()
            memberteam.user = user
            memberteam.save()
            messages.success(request, "Information modifiée avec succes")
            return redirect("dashboard:team-member")
        context = {"form": form}
        return render(request, self.template_name, context=context)


@method_decorator([staff_required], name="dispatch")
class PackManagement(View):
    template_name = "staff/pack.html"
    form_class = PackCreationForm
    queryset = Pack.objects.all

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        packs = self.queryset()
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "packs": packs,
            },
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        packs = self.queryset()
        context = {"form": form, "packs": packs}
        if form.is_valid():
            form.save()
            return redirect("dashboard:pack-management")
        else:
            context["errors"] = form.errors
        return render(request, self.template_name, context)


@method_decorator([staff_required], name="dispatch")
class UserManagement(View):
    template_name = "staff/users.html"
    queryset = CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        users = self.queryset
        return render(
            request,
            self.template_name,
            {
                "users": users,
            },
        )


@method_decorator([staff_required], name="dispatch")
class UpdateUserView(UpdateView, DetailView):
    template_name = "staff/update-users.html"
    user_form = CustomUserUpdateForm

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=kwargs["pk"])
        form = self.user_form(instance=user)
        context = {
            "form": form,
            "user": user,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=kwargs["pk"])
        form = self.user_form(request.POST, instance=user)
        if form.is_valid():
            customer_user = form.save()
            customer_user.user = user
            customer_user.save()
            messages.success(request, "Information modifiée avec succes")
            return redirect("dashboard:user-management")
        context = {"form": form}
        return render(request, self.template_name, context=context)


@method_decorator([staff_required], name="dispatch")
class RealyPointListView(View):
    realypoint_form = AddRealyPointForm
    template_name = "staff/relaypoint-list.html"

    def get(self, request, *args, **kwargs):
        relay_point = RelayPoint.objects.all()
        form = self.realypoint_form()
        context = {"relay_point": relay_point, "form": form}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.realypoint_form(request.POST)
        if form.is_valid():
            relaypoint = form.save(commit=False)
            relaypoint.user = user
            relaypoint.save()
            messages.success(request, "Point relais créé avec succes")

        if form.is_valid:
            form = AddRealyPointsForm(request.POST, request.FILES)
            excel_file = request.FILES["excel_file"]
            products_file = csv.reader(decode_utf8(excel_file))
            next(products_file)  # Skip header row
            for row in products_file:
                RelayPoint.objects.create(
                    title=row[0],
                    address=row[1],
                    pluscode=row[2],
                    phone=row[3],
                    friday=row[4],
                    saturday=row[5],
                    sunday=row[6],
                    monday=row[7],
                    tuesday=row[8],
                    wednesday=row[9],
                    thursday=row[10],
                    latitude=row[11].replace(",", "."),
                    longitude=row[12].replace(",", "."),
                    name=row[13],
                )
            return redirect("dashboard:realypoint-management")
        context = {"form": form}
        return render(request, self.template_name, context=context)


@method_decorator([staff_required], name="dispatch")
class UpdateRealyPointView(UpdateView, DetailView):
    template_name = "staff/update_realypoint.html"
    realypoint_form = AddRealyPointForm

    def get(self, request, *args, **kwargs):
        user = request.user
        relay = get_object_or_404(RelayPoint, id=kwargs["pk"])
        form = self.realypoint_form(instance=relay)
        relay_point = RelayPoint.objects.all()
        context = {
            "relay_point": relay_point,
            "form": form,
            "user": user,
            "relay": relay,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        user = request.user
        relay = get_object_or_404(RelayPoint, id=kwargs["pk"])
        form = self.realypoint_form(request.POST, instance=relay)
        if form.is_valid():
            relaypoint = form.save()
            relaypoint.user = user
            relaypoint.save()
            messages.success(request, "Information modifiée avec succes")
            return redirect("dashboard:realypoint-management")
        context = {"form": form}
        return render(request, self.template_name, context=context)


@staff_required
def deleteRealyPoint(request, pk):
    data = {}
    try:
        relay_point = get_object_or_404(RelayPoint, id=pk)
        if request.is_ajax():
            relay_point.delete()
            data["message"] = "Point relais supprimé avec succés"
            return JsonResponse(data)
    except Exception:
        data["error"] = "Une erreur innatendue s'est produite"
        return HttpResponseBadRequest(data, content_type="application/json")


@method_decorator([staff_required], name="dispatch")
class BillManagement(View):
    template_name = "staff/bills.html"
    queryset = Bill.objects.all()

    def get(self, request, *args, **kwargs):
        bills = self.queryset
        return render(
            request,
            self.template_name,
            {
                "bills": bills,
            },
        )


@method_decorator([staff_required], name="dispatch")
class PackageManagement(View):
    template_name = "staff/packages.html"
    queryset = Package.objects.all()
    form_class = AssignDelivermenForm

    def get(self, request, *args, **kwargs):
        packages = self.queryset
        form = self.form_class
        return render(
            request,
            self.template_name,
            {"packages": packages, "form": form},
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            delivermen = form.cleaned_data["delivermen"]
            package_id = request.POST.get("package_id")
            package = get_object_or_404(Package, pk=int(package_id))
            package.delivered_by = delivermen
            package.status = IN_PROGRESS
            package.save()
            assign_deliverymen_email(delivermen.email)
            PackageTracking.objects.create(
                tracking_code=package.tracking_number,
                note=package.get_status_display(),
                location=f"Votre colis est {package.sender_zone.title}",
            )
            return redirect("dashboard:team-package-list")
        else:
            messages.error(f"Erreur: {form.errors}")
        return render(request, self.template_name)


@method_decorator([staff_required], name="dispatch")
class ContactManagement(View):
    template_name = "staff/contacts.html"
    queryset = Contact.objects.all()

    def get(self, request, *args, **kwargs):
        contacts = self.queryset
        return render(
            request,
            self.template_name,
            {
                "contacts": contacts,
            },
        )


@method_decorator([staff_required], name="dispatch")
class DeliveryManagement(View):
    template_name = "staff/deliveries.html"
    queryset = Package.objects.filter(status=ARRIVED)

    def get(self, request, *args, **kwargs):
        deliveries = self.queryset
        return render(
            request,
            self.template_name,
            {
                "deliveries": deliveries,
            },
        )


@method_decorator([staff_required], name="dispatch")
class DeliveryManManagement(View):
    template_name = "staff/deliverymen.html"
    queryset = CustomUser.objects.deliverymen()

    def get(self, request, *args, **kwargs):
        deliverymen = self.queryset
        return render(
            request,
            self.template_name,
            {"deliverymen": deliverymen},
        )


@method_decorator([staff_required], name="dispatch")
class UpdateDeliverymen(UpdateView, DetailView):
    template_name = "staff/update_deliverymen.html"
    realypoint_form = UpdateDeliverymenForm

    def get(self, request, *args, **kwargs):
        user = request.user
        deliverymen = get_object_or_404(CustomUser, id=kwargs["pk"])
        form = self.realypoint_form(instance=deliverymen)
        context = {
            "form": form,
            "user": user,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        user = request.user
        deliverymen = get_object_or_404(CustomUser, id=kwargs["pk"])
        form = self.realypoint_form(request.POST, instance=deliverymen)
        if form.is_valid():
            deliveryman = form.save()
            deliveryman.user = user
            deliveryman.save()
            messages.success(request, "Information modifiée avec succes")
            return redirect("dashboard:delivery_man_management")
        context = {"form": form}
        return render(request, self.template_name, context=context)


@method_decorator([staff_required], name="dispatch")
class CouponView(View):
    template_name = "staff/list-coupon.html"
    form_class = AddCouponForm
    form_coupon = AssignCouponToPersonForm
    queryset = Coupon.objects.all

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        coupons = self.queryset()
        assign_form = self.form_coupon()
        return render(
            request,
            self.template_name,
            {"form": form, "coupons": coupons, "assign_form": assign_form},
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form_assign = self.form_coupon(request.POST)
        context = {"form": form, "form_assign": form_assign}

        if form.is_valid():
            discount = form.save(commit=False)
            discount.active = True
            discount.save()
            messages.info(request, "Votre Coupon as éte bien enregistrée.")
            return redirect("dashboard:coupon-list")
        if form_assign.is_valid():
            customer = form_assign.cleaned_data["customer"]
            coupon_id = request.POST.get("coupon_id")
            coupon = get_object_or_404(Coupon, pk=int(coupon_id))
            coupon = customer
            coupon.save()
            messages.info(
                request,
                f"Votre Coupon as éte bien assignée a l'utilisateur {customer}",
            )
            return redirect("dashboard:coupon-list")
        else:
            context["errors"] = form.errors
        return render(request, self.template_name, context)


@method_decorator([staff_required], name="dispatch")
class RelayPointRate(View):
    template_name = "staff/rates.html"

    def get(self, request, *args, **kwargs):
        relay_point_id = kwargs["relay_point_id"]
        relay_point = get_object_or_404(RelayPoint, pk=relay_point_id)
        rates = relay_point.rates.all()
        return render(
            request,
            self.template_name,
            {
                "rates": rates,
                "relay_point": relay_point,
            },
        )


@staff_required
def desactivate_realypoint(request, relay_id):
    data = {}
    try:
        realypoint = get_object_or_404(RelayPoint, pk=relay_id)
        if request.is_ajax():
            realypoint.is_active = False
            realypoint.save()
            data["message"] = "Compté desactivé"
            return JsonResponse(data)
    except Exception:
        data["error"] = "Une erreur innatendue s'est produite"
        return HttpResponseBadRequest(data, content_type="application/json")


@staff_required
def deactivate_user_account(request, user_id):
    data = {}
    try:
        user = get_object_or_404(CustomUser, pk=user_id)
        if request.is_ajax():
            user.is_active = False
            user.save()
            data["message"] = "Compté desactivé"
            return JsonResponse(data)
    except Exception:
        data["error"] = "Une erreur innatendue s'est produite"
        return HttpResponseBadRequest(data, content_type="application/json")


@staff_required
def activate_user_account(request, user_id):
    data = {}
    try:
        user = get_object_or_404(CustomUser, pk=user_id)
        if request.is_ajax():
            user.is_active = True
            user.save()
            data["message"] = "Compté activé"
            return JsonResponse(data)
    except Exception:
        data["error"] = "Une erreur innatendue s'est produite"
        return HttpResponseBadRequest(data, content_type="application/json")


@staff_required
def delete_user_account(request, user_id):
    data = {}
    try:
        user = get_object_or_404(CustomUser, pk=user_id)
        if request.is_ajax():
            user.delete()
            data["message"] = "Compté supprimé"
            return JsonResponse(data)
    except Exception:
        data["error"] = "Une erreur innatendue s'est produite"
        return HttpResponseBadRequest(data, content_type="application/json")


@staff_required
def test_upload_departure_arrival(request):
    if request.method == "POST":
        excel_file = request.FILES["point_csv_file"]
        products_file = csv.reader(decode_utf8(excel_file))
        next(products_file)  # Skip header row
        for row in products_file:
            dept = DeparturePoint.objects.get(name=row[0])
            DeliveryPoint.objects.create(
                departure_point=dept,
                arrival_point=row[1],
                delivery_price=row[2],
                transporter_commission=row[3],
                relayer_commission=row[4],
                africarelais_commission=row[5],
            )
            print(dept)
        return HttpResponse("Done")
        # print(row[0])
        # print(row[1])
        # print(row[2])
        # print(row[3])
        # print(row[4])
        # print(row[5])


dashboard = StaffView.as_view()
user_update = CustomUserUpdateDetailView.as_view()
team_member = TeamMember.as_view()
pro_member = ProMember.as_view()
pack_management = PackManagement.as_view()
user_management = UserManagement.as_view()
bill_management = BillManagement.as_view()
package_management = PackageManagement.as_view()
contact_management = ContactManagement.as_view()
delivery_management = DeliveryManagement.as_view()
realypoint_management = RealyPointListView.as_view()
delivery_man_management = DeliveryManManagement.as_view()
relay_point_rate = RelayPointRate.as_view()
update_realypoint = UpdateRealyPointView.as_view()
delete_relaypoint = deleteRealyPoint
coupons = CouponView.as_view()
# upload_realypoint = upload_file
update_team = UpdateTeamMemberView.as_view()
update_deliverymen = UpdateDeliverymen.as_view()

update_user = UpdateUserView.as_view()
