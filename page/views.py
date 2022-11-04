from django.conf import settings

from django.http.response import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from delivery.models import DeparturePoint
from page.forms import PriceSimulationForm
from .models import Carousel, ClientRealyPoint, RelayPoint, Testimonial


GOOGLE_MAP_API_KEY = settings.GOOGLE_MAP_API_KEY


def index(request):
    user = request.user
    form = PriceSimulationForm
    testimonials = Testimonial.objects.all()
    carousels = Carousel.objects.filter(active=True)
    departures = DeparturePoint.objects.all()
    context = {
        "form": form,
        "user": user,
        "carousels": carousels,
        "testimonials": testimonials,
        "departures": departures,
    }
    return render(request, "index.html", context)


def simulation(request):
    user = request.user
    form = PriceSimulationForm
    departures = DeparturePoint.objects.all()
    context = {
        "form": form,
        "user": user,
        "departures": departures,
    }
    return render(request, "simulation.html", context)


def relay(request):
    all_relay_point = RelayPoint.objects.filter(is_active=True)
    relay_point = RelayPoint.objects.filter(is_active=True)
    query = request.GET.get("address", None)
    departures = DeparturePoint.objects.all()
    if query:
        relay_point = RelayPoint.objects.filter(
            Q(name__iexact=query) | Q(address__iexact=query)
        )
    relay_point_to_list = list(relay_point.values("id", "title"))
    return render(
        request,
        "relay.html",
        {
            "relay_point": relay_point,
            "departures": departures,
            "all_relay_point": all_relay_point,
            "query": query,
            "GOOGLE_MAP_API_KEY": GOOGLE_MAP_API_KEY,
            "relay_point_to_list": {"data": relay_point_to_list},
        },
    )


def get_relay_points(request):
    query = request.GET.get("address", None)
    if query:
        relay_point_to_list = list(
            RelayPoint.objects.filter(
                Q(address__iexact=query) | Q(name__iexact=query)
            ).values(
                "id",
                "title",
                "latitude",
                "longitude",
            )
        )
    else:
        relay_point_to_list = list(
            RelayPoint.objects.filter(is_active=True).values(
                "id",
                "title",
                "latitude",
                "longitude",
            )
        )
    print("relay_point_to_list ", relay_point_to_list)
    return JsonResponse(data={"data": relay_point_to_list}, safe=False)


def result(request):
    query = request.GET.get("q")
    if query:
        relay_point = RelayPoint.objects.filter(adress__iexact=query)
    count = len(query)
    return render(
        request,
        "result.html",
        {"relay_point": relay_point, "count": count, "query": query},
    )


def favorite_ajax(request):
    data = {"success ": False}
    if request.is_ajax():
        realy_id = request.POST["relay_point"]
        relay_point = get_object_or_404(RelayPoint, pk=int(realy_id))
        clientRelayPoint = ClientRealyPoint.objects.create(
            relay_point=relay_point, client=request.user
        )
        print(clientRelayPoint)
    data = {"success": True}
    return JsonResponse(data)


def subscription(request):
    return render(request, "subscription.html")


def about(request):
    return render(request, "about.html")


def faq(request):
    return render(request, "copywriting/faq.html")


def mention_legal(request):
    return render(request, "copywriting/mention-legal.html")


def fraud(request):
    return render(request, "copywriting/fraud.html")


def contact(request):
    return render(request, "copywriting/contact.html")


def suivi_liv(request):
    return render(request, "copywriting/suivi-livreur.html")


def condi_vent(request):
    return render(request, "copywriting/condition-vente.html")


def rembourse(request):
    return render(request, "copywriting/remboursement.html")


def protection(request):
    return render(request, "copywriting/protection.html")
