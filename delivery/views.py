import json
from django.conf import settings

from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
import requests
from django.db.models import Q

from send_email.whatsapp_notif import send_notif_whats


from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.template.loader import get_template
from page.models import Contact
from user.models import CustomUser
from .models import DeliveryPoint, DeparturePoint, Package, PackageTracking
from django.contrib import messages
from django.core.mail import send_mail
from .forms import SendPackageForm


GOOGLE_MAP_API_KEY = settings.GOOGLE_MAP_API_KEY


class SendPackageView(CreateView):
    form_class = SendPackageForm
    template_name = "send-package.html"

    def get(self, request, *args, **kwargs):
        departures = DeparturePoint.objects.all()

        adress_ip = requests.get('http://ip-api.com/json')
        ip_data = json.loads(adress_ip.text)
        res = requests.get('http://ip-api.com/json/'+ip_data["query"])
        location_data_one = res.text
        location_data = json.loads(location_data_one)

        form = self.form_class()

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "GOOGLE_MAP_API_KEY": GOOGLE_MAP_API_KEY,
                "departures": departures,
                "data" : location_data
            },
        )

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        form = SendPackageForm(request.POST, request.FILES)
        if form.is_valid():
            departure_point = request.POST.get("id_departure_point")
            test = request.POST.get('mode_recup')
            print(test)
            arrival_point = request.POST.get("id_arrival_point")
            delivery_point = DeliveryPoint.objects.filter(
                Q(departure_point__name=departure_point)
                & Q(arrival_point=arrival_point)
            ).get()
            customer_first_name = form.cleaned_data["customer_first_name"]
            customer_last_name = form.cleaned_data["customer_last_name"]
            customer_phone = form.cleaned_data["customer_phone"]
            customer_email = form.cleaned_data["customer_email"]
            sender_phone = form.cleaned_data["sender_phone"]
            sender_email = form.cleaned_data["sender_email"]
            package_weigth = form.cleaned_data["package_weigth"]
            price = form.cleaned_data["price"]
            package_picture = form.cleaned_data["package_picture"]
            customer, created = Contact.objects.get_or_create(
                email=customer_email,
            )
            user, user_created = CustomUser.objects.get_or_create(
                email=sender_email,
            )
            if user_created:
                user.phone = sender_phone
                user.set_password("12345678")
                user.save()
            if created:
                customer.full_name = customer_first_name + " " + customer_last_name
                customer.phone = customer_phone
                customer.created_by = user
                customer.email = customer_email
                customer.save()
            package = Package.objects.create(
                amount=delivery_point.delivery_price,
                customer=customer,
                delivery_point=delivery_point,
                sender=user,
                weight=package_weigth,
                picture=package_picture,
                price=price,
            )
            package.save()
            send_notif_whats(customer.phone, )
            package_status_mail(customer_email, user.email)
            messages.success(
                request,
                "Votre Colis est envoyé",
            )
            PackageTracking.objects.create(
                tracking_code=package.tracking_number,
                note=package.get_status_display(),
                location=f"Votre colis est a {departure_point}",
            )

            if request.user.is_authenticated:
                return redirect("login")
            # rediriger sur whatsapp +221 78 428 39 07
            # if not user.pro_pack or not user.particular_pack:
            #     return redirect(
            #         "https://wa.me/+221784283907?text=Bonjour AfricaRelais, je veux m'inscrire a vos packs"
            #     )
            # else:
            #     return redirect(
            #         "https://wa.me/+221784283907?text=Bonjour votre colis a été enregistrée veuillez patienter"
            #     )
        else:
            messages.error(request, f"Colis non envoyé: {form.errors}")

        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )


def get_delivery_price(request):
    data = {}
    try:
        departure_point = request.POST.get("departure_point")
        arrival_point = request.POST.get("arrival_point")
        arrival = DeliveryPoint.objects.filter(
            Q(departure_point__name=departure_point) & Q(arrival_point=arrival_point)
        ).get()
        data["price"] = round(arrival.delivery_price)
        return JsonResponse(data)
    except Exception:
        data["price"] = 0
        if departure_point == arrival_point:
            data["price"] = 500
    return JsonResponse(data)


def package_status_mail(sender_email, customer_user):
    htmly = get_template("email/package-status.html")
    context = {"sender_email": sender_email, "customer_user": customer_user}
    to_emails = [sender_email, "ahmeth.amar@gmail.com"]
    subject, from_email = ("AfricaRelais", "ahmeth mbacke amar")
    html_content = htmly.render(context)
    msg = EmailMultiAlternatives(
        subject,
        html_content,
        from_email,
        to_emails,
    )
    msg.attach_alternative(
        html_content,
        "text/html",
    )
    msg.send(fail_silently=False)


def package_tracking(request):
    return render(
        request,
        "delivery/tracking.html",
    )


def tracking_results(request):
    tracking_number = request.GET.get("tracking_number")
    try:
        tracking = PackageTracking.objects.filter(tracking_code__iexact=tracking_number)
        return render(
            request,
            "delivery/tracking-results.html",
            {
                "tracking": tracking,
            },
        )
    except Exception:
        messages.error(request, "Une erreur innatendue s'est produtie")
        return redirect("delivery:package-tracking")


def mail(request):
    send_mail(
        "Hello from Africa-relais",
        "Notification des colis disponibles",
        "falloumbengue96@gmail.com",
        ["lixepef193@zherben.com"],
        fail_silently=False,
    )
    return render(request, "delivery/send-mail.html")


def relayer(request):
    return render(request, "delivery/relayer.html")
