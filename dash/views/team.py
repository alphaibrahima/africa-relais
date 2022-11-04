from django.db.models.aggregates import Count, Sum
from django.http import HttpResponseBadRequest
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic import UpdateView

from dash.forms.team import (
    AddRealyPointForm,
    AssignDelivermenForm,
    UpdateRealyPointForm,
)
from delivery.models import Package, PackageTracking
from delivery_management.constants import IN_PROGRESS
from page.models import Contact, RelayPoint
from send_email.views import assign_deliverymen_email
from user.decorators import team_required
from user.models import CustomUser, Pack
from user.forms import (
    ChangePasswordForm,
    CustomUserProfileForm,
    CustomUserUpdateForm,
)
from django.contrib import messages


@method_decorator([team_required], name="dispatch")
class TeamDashboardView(View):
    template_name = "team/dashboard.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        abonnement = Pack.objects.aggregate(Count("id"))["id__count"]
        packages = Package.objects.aggregate(Count("id"))["id__count"]
        relaypoint = RelayPoint.objects.aggregate(Count("id"))["id__count"]
        income_deliverman = Package.objects.aggregate(Sum("amount"))["amount__sum"]
        income_realypoint = Package.objects.aggregate(Sum("amount"))["amount__sum"]
        total_incom = (
            income_deliverman + income_realypoint
            if income_deliverman and income_realypoint
            else 0
        )
        all_package = Package.objects.all()[:3]
        total_delivermen = CustomUser.objects.deliverymen().count()
        deliverman = Package.objects.all()

        context = {
            "user": user,
            "packages": packages,
            "all_package": all_package,
            "relaypoint": relaypoint,
            "total_delivermen": total_delivermen,
            "total_incom": total_incom,
            "abonnement": abonnement,
            "income_deliverman": income_deliverman,
            "income_realypoint": income_realypoint,
            "deliverman": deliverman,
        }
        return render(request, self.template_name, context=context)


@method_decorator([team_required], name="dispatch")
class CustomUserUpdateDetailView(UpdateView, DetailView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    avatar_form = CustomUserProfileForm
    password_form = ChangePasswordForm
    template_name = "team/profile.html"

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
            return redirect("dashboard:team-profile")

        password_form = self.password_form(user, request.POST)
        if password_form.is_valid():
            password_form.save()
            messages.success(request, "Mot de passe modifiée avec succes")
            return redirect("dashboard:team-profile")
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


@method_decorator([team_required], name="dispatch")
class PackageListView(View):
    template_name = "team/package-list.html"
    queryset = CustomUser.objects.deliverymen()
    form_class = AssignDelivermenForm

    def get(self, request, *args, **kwargs):
        packages = Package.objects.all()
        deliverymen = self.queryset
        form = self.form_class
        context = {"packages": packages, "deliverymen": deliverymen, "form": form}
        return render(request, self.template_name, context=context)

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


@method_decorator([team_required], name="dispatch")
class DeliveryManManagement(View):
    template_name = "team/deliverymen.html"
    queryset = CustomUser.objects.deliverymen()

    def get(self, request, *args, **kwargs):
        deliverymen = self.queryset
        return render(
            request,
            self.template_name,
            {
                "deliverymen": deliverymen,
            },
        )


@method_decorator([team_required], name="dispatch")
class RevenusListView(View):
    template_name = "team/revenus-list.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)


@method_decorator([team_required], name="dispatch")
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


@method_decorator([team_required], name="dispatch")
class RealyPointListView(UpdateView, DetailView):
    form_class = AddRealyPointForm
    realypoint_form = UpdateRealyPointForm
    template_name = "team/relaypoint-list.html"

    def get(self, request, *args, **kwargs):
        relay_point = RelayPoint.objects.all()
        form = self.form_class()
        context = {"relay_point": relay_point, "form": form}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST)
        if form.is_valid():
            relaypoint = form.save(commit=False)
            relaypoint.user = user
            relaypoint.save()
            messages.success(request, "Point relais créé avec succes")
            return redirect("dashboard:team-relaypoint-liste")
        context = {"form": form, "form_update": "form_update"}
        return render(request, self.template_name, context=context)


@method_decorator([team_required], name="dispatch")
class UpdateRealyPointView(UpdateView, DetailView):
    template_name = "team/update_realypoint.html"
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
            return redirect("dashboard:team-relaypoint-liste")
        context = {"form": form}
        return render(request, self.template_name, context=context)


@team_required
def deleteRealyPoint(request, pk):
    data = {}
    try:
        relay_point = get_object_or_404(RelayPoint, id=pk)
        if request.is_ajax():
            relay_point.delete()
            data["messages"] = "Point relais supprimé avec succés"
            return JsonResponse(data)
    except Exception:
        data["error"] = "Une erreur innatendue s'est produite"
        return HttpResponseBadRequest(data, content_type="application/json")


@method_decorator([team_required], name="dispatch")
class DelivermanListView(View):
    template_name = "team/deliverman-list.html"
    queryset = CustomUser.objects.deliverymen()

    def get(self, request, *args, **kwargs):
        deliverymen = self.queryset
        return render(
            request,
            self.template_name,
            {
                "deliverymen": deliverymen,
            },
        )


@team_required
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


dashboard = TeamDashboardView.as_view()
user_update = CustomUserUpdateDetailView.as_view()
address_book_list = ContactManagement.as_view()
package_list = PackageListView.as_view()
revenus_list = RevenusListView.as_view()
relay_point = RealyPointListView.as_view()
deliverman = DelivermanListView.as_view()
update_realypoint = UpdateRealyPointView.as_view()
delete_realypoint = deleteRealyPoint
