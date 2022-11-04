from django.urls import path

from .views import (
    about,
    condi_vent,
    contact,
    faq,
    favorite_ajax,
    fraud,
    get_relay_points,
    index,
    mention_legal,
    protection,
    relay,
    rembourse,
    result,
    simulation,
    subscription,
    suivi_liv,
)

app_name = "page"

urlpatterns = [
    path("", index, name="home"),
    path("relay/", relay, name="relay"),
    path("get-relay-points/", get_relay_points, name="get_relay_points"),
    path("simulation/", simulation, name="simulation"),
    path("relay/result/", result, name="results"),
    path("favorite_ajax/", favorite_ajax, name="favoriteAjax"),
    path("subscription/", subscription, name="subscription"),
    path("about/", about, name="about"),
    path("faq/", faq, name="faq_page"),
    path("mention-legal", mention_legal, name="mention-legal-page"),
    path("signalement-fraud", fraud, name="fraud-page"),
    path("contactez-nous", contact, name="contact-page"),
    path("suivi-livreur/", suivi_liv, name="suivi-liv-page"),
    path("condition-vente/", condi_vent, name="vente-page"),
    path("reclamation/", rembourse, name="reclamation-page"),
    path("protection-données", protection, name="protection-page"),
]
