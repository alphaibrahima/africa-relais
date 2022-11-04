from django import forms
from .models import Package


class SendPackageForm(forms.Form):

    WEIGHT = (
        ("1.0", "1KG"),
        ("2.0", "2KG"),
        ("3.0", "3KG"),
        ("4.0", "4KG"),
        ("5.0", "5KG"),
    )
    sender_first_name = forms.CharField(
        max_length=254,
        label="Prénom",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Prénom",
            }
        ),
    )
    sender_last_name = forms.CharField(
        max_length=254,
        label="Nom de famille",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Nom",
            }
        ),
    )
    sender_phone = forms.CharField(
        max_length=20,
        label="Téléphone",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Telephone",
            }
        ),
    )
    sender_email = forms.CharField(
        max_length=50,
        label="Email",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Email",
            }
        ),
    )
    package_weigth = forms.ChoiceField(
        choices=WEIGHT,
        label="Poinds(en KG)",
        widget=forms.Select(
            {
                "class": "form-control",
                "placeholder": "Poids en Kg",
            }
        ),
    )
    package_picture = forms.ImageField(
        label="Photo",
        widget=forms.FileInput(
            {
                "class": "form-control form-control-sm",
                "accept": "image/*",
            }
        ),
    )
    customer_first_name = forms.CharField(
        max_length=254,
        label="Prénom",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Prénom",
            }
        ),
    )
    customer_last_name = forms.CharField(
        max_length=254,
        label="Nom de famille",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Nom",
            }
        ),
    )
    customer_phone = forms.CharField(
        max_length=20,
        label="Téléphone",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Telephone",
            }
        ),
    )
    customer_email = forms.CharField(
        max_length=50,
        label="Email",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Email",
            }
        ),
    )




