import weasyprint
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from user.decorators import particular_required
from django.template.loader import render_to_string
from django.views.generic.base import View
from delivery.models import Bill, Package
from page.models import Contact, RelayPoint
from django.db.models.aggregates import Count
from user.forms import ChangePasswordForm, CustomUserUpdateForm, UpdateProfileForm
from user.models import CustomUser


@method_decorator([particular_required], name="dispatch")
class ParticularDashboardView(View):
    template_name = "particular/dashboard.html"
    queryset = Contact.objects.filter()[:2]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        packages = Package.objects.filter(sender=request.user).aggregate(Count("id"))[
            "id__count"
        ]
        relaypoint = RelayPoint.objects.count()
        all_package = Package.objects.filter(sender=request.user)[:2]
        contacts = self.queryset

        context = {
            "user": user,
            "packages": packages,
            "all_package": all_package,
            "relaypoint": relaypoint,
            "contacts": contacts,
        }
        return render(request, self.template_name, context=context)


@particular_required
def profile(request):
    user = request.user
    if request.method == "POST":
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Information particulier mise a jour avec succes")
            return redirect("dashboard:particular-profile")
        else:
            messages.error(request, f"{form.errors}")
            return redirect("dashboard:particular-profile")
    else:
        form = CustomUserUpdateForm(instance=user)
    return render(request, "particular/profile.html", {"form": form})


@method_decorator([particular_required], name="dispatch")
class CustomUserUpdateDetailView(UpdateView, DetailView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    avatar_form = UpdateProfileForm
    password_form = ChangePasswordForm
    template_name = "particular/profile.html"

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
            return redirect("dashboard:particular-profile")
        password_form = self.password_form(user, request.POST)
        if password_form.is_valid():
            password_form.save()
            messages.success(request, "Mot de passe modifiée avec succes")
            return redirect("dashboard:particular-profile")
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


@method_decorator([particular_required], name="dispatch")
class RevenusListView(View):
    template_name = "particular/revenus-list.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)


@method_decorator([particular_required], name="dispatch")
class PackageListView(View):
    template_name = "particular/package-list.html"

    def get(self, request, *args, **kwargs):
        packages = Package.objects.filter(sender=request.user)
        context = {"packages": packages}
        return render(request, self.template_name, context=context)


@method_decorator([particular_required], name="dispatch")
class AddressBookView(View):
    template_name = "particular/address-book.html"
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


@method_decorator([particular_required], name="dispatch")
class BillListView(View):
    template_name = "particular/bill-list.html"

    def get(self, request, *args, **kwargs):
        packages = Package.objects.all()
        bills = Bill.objects.all()
        context = {"packages": packages, "bills": bills}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)


@method_decorator([particular_required], name="dispatch")
class BillView(View):
    template_name = "particular/bill.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        bill_id = self.kwargs["pk"]
        bill = Bill.objects.get(id=bill_id)
        package = Package.objects.get(id=bill_id)
        delivery = Package.objects.filter().count()
        price = package.amount
        context = {
            "user": user,
            "bill": bill,
            "package": package,
            "price": price,
            "delivery": delivery,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)


@particular_required
def bill_to_pdf(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    package = Package.objects.get(id=bill_id)
    delivery = Package.objects.filter().count()
    price = bill.amount + package.price
    html = render_to_string(
        "particular/pdf.html",
        {"bill": bill, "package": package, "delivery": delivery, "price": price},
    )
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename=bill_{bill.id}.pdf"
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[
            weasyprint.CSS(
                "https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css"
            )
        ],
    )
    return response


@particular_required
def Express(request):
    return render(request, "particular/express.html")


@particular_required
def pay(request):
    return render(request, "particular/paiement/compte-paiement.html")


@particular_required
def choice_pay(request):
    return render(request, "particular/paiement/choix-compte.html")


@particular_required
def bank_pay(request):
    return render(request, "particular/paiement/paiement-bancaire.html")


@particular_required
def wave_pay(request):
    return render(request, "particular/paiement/paiement-wave.html")


@particular_required
def orange_money_pay(request):
    return render(request, "particular/paiement/paiement-orange-money.html")


@particular_required
def free_money_pay(request):
    return render(request, "particular/paiement/paiement-free.html")


@particular_required
def dunya_money_pay(request):
    return render(request, "particular/paiement/paiement-dunya.html")


dashboard = ParticularDashboardView.as_view()
revenus_list = RevenusListView.as_view()
package_list = PackageListView.as_view()
address_book_list = AddressBookView.as_view()
bill_list = BillListView.as_view()
bill = BillView.as_view()
user_update = CustomUserUpdateDetailView.as_view()
pdf = bill_to_pdf
express = Express
paiement_part = pay
choice = choice_pay
wave = wave_pay
bancaire = bank_pay
orange = orange_money_pay
free = free_money_pay
dunya = dunya_money_pay
