from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=60,
        label="Prénom",
        required=True,
        error_messages={"required": "Le Prenom doit être renseigné."},
        widget=forms.TextInput(
            {
                "placeholder": "Ex: Modou",
                "class": "form-control",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=60,
        label="Nom",
        required=True,
        error_messages={"required": "Le Nom doit être renseigné."},
        widget=forms.TextInput(
            {
                "placeholder": "Ex: Ndiaye",
                "class": "form-control",
            }
        ),
    )
    email = forms.CharField(
        max_length=60,
        label="Email",
        required=True,
        error_messages={"required": "Le Prenom doit être renseigné."},
        widget=forms.EmailInput(
            {
                "placeholder": "Ex: your@gmail.com",
                "class": "form-control",
            }
        ),
    )
    phone = forms.CharField(
        max_length=60,
        label="Numéro de téléphone",
        required=True,
        error_messages={"required": "Le telephone doit être renseigné."},
        widget=forms.TextInput(
            {
                "placeholder": "Ex: 763772260",
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = Order
        fields = ["first_name", "last_name", "email", "phone"]
