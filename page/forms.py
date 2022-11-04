from django import forms
from delivery.models import DeparturePoint
from delivery_management.constants import (
    HOME,
    REALYPOINT,
)


class PriceSimulationForm(forms.Form):
    departure_point = forms.ModelChoiceField(
        DeparturePoint.objects.all(),
        label="Quartier",
        widget=forms.Select(
            {
                "class": "form-control",
                "placeholder": "Médina",
            }
        ),
    )
    arrival_point = forms.ModelChoiceField(
        DeparturePoint.objects.all(),
        label="Quartier",
        widget=forms.Select(
            {
                "class": "form-control",
                "placeholder": "Quartier",
            }
        ),
    )
    DELIVERY_MODE = (
        (REALYPOINT, "Point relais"),
        (HOME, "Domicile"),
    )
    mode = forms.ChoiceField(
        choices=DELIVERY_MODE,
        label="Mode de livraison",
        widget=forms.Select(
            {
                "class": "form-control my-2 float-none",
                "placeholder": "Mode de livraison",
            }
        ),
    )
