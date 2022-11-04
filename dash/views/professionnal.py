from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.db.models.aggregates import Count, Sum
from page.models import Contact, RelayPoint
from user.decorators import professionnal_required
from user.forms import (
    ChangePasswordForm,
    CustomUserUpdateForm,
    UpdateProfileForm,
)
from django.contrib import messages

from delivery.models import Package
from user.models import Account, CustomUser


@method_decorator([professionnal_required], name="dispatch")
class ProfessionnalDashboardView(View):
    template_name = "professionnal/dashboard.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        packages = Package.objects.filter(sender=request.user).aggregate(Count("id"))[
            "id__count"
        ]
        all_packages = Package.objects.filter(sender=user)
        income_professionnal = request.user.deliveries.aggregate(Sum("amount"))[
            "amount__sum"
        ]
        contacts = Contact.objects.filter(created_by=user)[:4]
        context = {
            "user": user,
            "packages": packages,
            "all_packages": all_packages,
            "income_professionnal": income_professionnal,
            "contacts": contacts,
        }
        return render(request, self.template_name, context=context)


@professionnal_required
def profile(request):
    user = request.user
    if request.method == "POST":
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Information entreprise mise a jour avec succes")
            return redirect("dashboard:professionnal-profile")
        else:
            messages.error(request, f"{form.errors}")
            return redirect("dashboard:professionnal-profile")
    else:
        form = CustomUserUpdateForm(instance=user)
    return render(request, "professionnal/profile.html", {"form": form})


@method_decorator([professionnal_required], name="dispatch")
class CustomUserUpdateDetailView(UpdateView, DetailView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    avatar_form = UpdateProfileForm
    password_form = ChangePasswordForm
    # social_form = UpdateSocialForm
    # bio_form = UpdateBioForm
    template_name = "professionnal/profile.html"

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
            return redirect("dashboard:professionnal-profile")
        password_form = self.password_form(user, request.POST)
        if password_form.is_valid():
            password_form.save()
            messages.success(request, "Mot de passe modifiée avec succes")
            return redirect("dashboard:professionnal-profile")
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


@method_decorator([professionnal_required], name="dispatch")
class AddressBookView(View):
    template_name = "professionnal/address-book.html"
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


@method_decorator([professionnal_required], name="dispatch")
class PackageListView(View):
    template_name = "professionnal/package-list.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        packages = Package.objects.filter(sender=user)
        print("tester", packages)
        return render(request, self.template_name, {"packages": packages})

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)


@method_decorator([professionnal_required], name="dispatch")
class RevenusListView(View):
    template_name = "professionnal/revenus-list.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)


@method_decorator([professionnal_required], name="dispatch")
class AccountView(View):
    template_name = "professionnal/account.html"

    def get(self, request, *args, **kwargs):
        account = Account.objects.filter(user=request.user)
        return render(request, self.template_name, {"account": account})

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)


@method_decorator([professionnal_required], name="dispatch")
class Relypoint_ListView(View):
    template_name = "professionnal/relypoint_list.html"

    def get(self, request, *args, **kwargs):
        relypoint = RelayPoint.objects.all()
        return render(request, self.template_name, {"relypoint": relypoint})


@professionnal_required
def pay_pro(request):
    return render(request, "professionnal/paiement/compte-paiement.html")


@professionnal_required
def choice_pay_pro(request):
    return render(request, "professionnal/paiement/choix-compte.html")


@professionnal_required
def bank_pay_pro(request):
    return render(request, "professionnal/paiement/paiement-bancaire.html")


@professionnal_required
def wave_pay_pro(request):
    return render(request, "professionnal/paiement/paiement-wave.html")


@professionnal_required
def orange_money_pay_pro(request):
    return render(request, "professionnal/paiement/paiement-orange-money.html")


@professionnal_required
def free_money_pay_pro(request):
    return render(request, "professionnal/paiement/paiement-free.html")


@professionnal_required
def dunya_money_pay_pro(request):
    return render(request, "professionnal/paiement/paiement-dunya.html")


dashboard = ProfessionnalDashboardView.as_view()
address_book_list = AddressBookView.as_view()
package_list = PackageListView.as_view()
revenus_list = RevenusListView.as_view()
user_update = CustomUserUpdateDetailView.as_view()
account = AccountView.as_view()
rely_list = Relypoint_ListView.as_view()
paiement_pro = pay_pro
choice_pro = choice_pay_pro
bancaire_pro = bank_pay_pro
wave_pro = wave_pay_pro
orange_pro = orange_money_pay_pro
free_pro = free_money_pay_pro
dunya_pro = dunya_money_pay_pro
