from django.shortcuts import render, redirect
from django.db.models.aggregates import Count, Sum
from django.views.generic import View
from django.utils.decorators import method_decorator
from page.models import Contact
from user.decorators import realypoint_required
from django.views.generic import UpdateView, DetailView

from delivery.models import Package
from user.models import CustomUser
from user.forms import (
    ChangePasswordForm,
    CustomUserProfileForm,
    CustomUserUpdateForm,
)
from django.contrib import messages


@method_decorator([realypoint_required], name="dispatch")
class RealyPointDashboardView(View):
    template_name = "realypoint/dashboard.html"
    queryset = Contact.objects.filter()[:2]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        allPackages = Package.objects.filter(sender=user)
        packages = Package.objects.aggregate(Count("id"))["id__count"]
        income_realypoint = Package.objects.aggregate(Sum("amount"))["amount__sum"]
        contacts = self.queryset
        context = {
            "user": user,
            "allPackages": allPackages,
            "packages": packages,
            "income_realypoint": income_realypoint,
            "contacts": contacts,
        }
        return render(request, self.template_name, context=context)


@method_decorator([realypoint_required], name="dispatch")
class PackageListView(View):
    template_name = "realypoint/package-list.html"

    def get(self, request, *args, **kwargs):
        packages = Package.objects.filter(sender=request.user)
        context = {"packages": packages}
        return render(request, self.template_name, context=context)


@method_decorator([realypoint_required], name="dispatch")
class CustomUserUpdateDetailView(UpdateView, DetailView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    avatar_form = CustomUserProfileForm
    password_form = ChangePasswordForm
    template_name = "realypoint/profile.html"

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
            return redirect("dashboard:realypoint-profile")

        password_form = self.password_form(user, request.POST)
        if password_form.is_valid():
            password_form.save()
            messages.success(request, "Mot de passe modifiée avec succes")
            return redirect("dashboard:realypoint-profile")
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


class RevenusListView(View):
    template_name = "realypoint/revenue.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)


@realypoint_required
def parcel_reception(request):
    return render(request, "realypoint/reception.html")


@realypoint_required
def schedule(request):
    return render(request, "realypoint/horaire.html")


dashboard = RealyPointDashboardView.as_view()
profile = CustomUserUpdateDetailView.as_view()
package = PackageListView.as_view()
revenue = RevenusListView.as_view()
