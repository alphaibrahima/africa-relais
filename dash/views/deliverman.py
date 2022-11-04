import json
from django.db.models.aggregates import Count, Sum
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from page.models import Contact, RelayPoint
from user.decorators import deliveryman_required
from user.forms import ChangePasswordForm, CustomUserUpdateForm, UpdateProfileForm
from django.contrib import messages
from delivery.models import Package

from user.models import CustomUser


@deliveryman_required
def DelivermanDashboard(request):
    packages = Package.objects.filter(delivered_by=request.user).aggregate(Count("id"))[
        "id__count"
    ]
    income_deliverman = request.user.deliveries.aggregate(Sum("amount"))["amount__sum"]
    all_package = Package.objects.filter(delivered_by=request.user)[:3]
    all_price = Package.objects.all()
    deliverman = Package.objects.all()
    context = {
        "packages": packages,
        "income_deliverman": income_deliverman,
        "all_package": all_package,
        "all_price": all_price,
        "deliverman": deliverman,
    }
    return render(request, "deliverman/dashboard.html", context)


@deliveryman_required
def Profile(request):
    user = request.user
    if request.method == "POST":
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Information livreur mise a jour avec succes")
            return redirect("dashboard:deliverman-profile")
        else:
            messages.error(request, f"{form.errors}")
            return redirect("dashboard:deliverman-profile")
    else:
        form = CustomUserUpdateForm(instance=user)
    return render(request, "deliverman/profile.html", {"form": form})


@method_decorator([deliveryman_required], name="dispatch")
class CustomUserUpdateDetailView(UpdateView, DetailView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    avatar_form = UpdateProfileForm
    password_form = ChangePasswordForm
    template_name = "deliverman/profile.html"

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
            return redirect("dashboard:deliverman-profile")
        password_form = self.password_form(user, request.POST)
        if password_form.is_valid():
            password_form.save()
            messages.success(request, "Mot de passe modifiée avec succes")
            return redirect("dashboard:deliverman-profile")
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


@deliveryman_required
def revenue(request):
    return render(request, "deliverman/revenue.html")


@method_decorator([deliveryman_required], name="dispatch")
class AddressBookView(View):
    template_name = "deliverman/address-book.html"
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


@deliveryman_required
def history(request):
    packages = Package.objects.filter(delivered_by=request.user)
    return render(request, "deliverman/history.html", {"packages": packages})


@deliveryman_required
def income_statistique(request):
    dataset = (
        Package.objects.values("amount")
        .annotate(revenue_count=Count("amount"))
        .order_by("amount")
    )

    categories = list()
    revenue = list()

    for entry in dataset:
        categories.append("%s Class" % entry["price"])
        revenue.append(entry["revenue_count"])

    return render(
        request,
        "deliverman/dashboard.html",
        {
            "categories": json.dumps(categories),
            "revenue": json.dumps(revenue),
        },
    )


@method_decorator([deliveryman_required], name="dispatch")
class Realypoint_ListView(View):
    template_name = "deliverman/list_relypoint.html"

    def get(self, request, *args, **kwargs):
        realypoint = RelayPoint.objects.all()
        return render(request, self.template_name, {"realypoint": realypoint})


user_update = CustomUserUpdateDetailView.as_view()
realypoint_list = Realypoint_ListView.as_view()
