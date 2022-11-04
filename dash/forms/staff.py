from django import forms
from user.models import CustomUser, Pack
from django.contrib.auth.forms import UserCreationForm


class TeamCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=254,
        label="Prénom",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Prénom",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=254,
        label="Nom de famille",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Nom de famille",
            }
        ),
    )
    address = forms.CharField(
        max_length=254,
        label="Adresse",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Adresse complète",
            }
        ),
    )
    city = forms.CharField(
        max_length=254,
        label="Ville",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Ville",
            }
        ),
    )
    phone = forms.CharField(
        max_length=254,
        label="Téléphone",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Numéro de Téléphone",
            }
        ),
    )
    email = forms.CharField(
        max_length=254,
        required=False,
        label="E-mail",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "adresse email",
            }
        ),
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            {
                "class": "form-control",
                "placeholder": "Mot de passe",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirmation Mot de passe",
        widget=forms.PasswordInput(
            {
                "class": "form-control",
                "placeholder": "Mot de passe",
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "city",
            "password1",
            "password2",
        )


class TeamUpdateForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=254,
        label="Prénom",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Prénom",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=254,
        label="Nom de famille",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Nom de famille",
            }
        ),
    )
    address = forms.CharField(
        max_length=254,
        label="Adresse",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Adresse complète",
            }
        ),
    )
    city = forms.CharField(
        max_length=254,
        label="Ville",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Ville",
            }
        ),
    )
    phone = forms.CharField(
        max_length=254,
        label="Téléphone",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Numéro de Téléphone",
            }
        ),
    )
    email = forms.CharField(
        max_length=254,
        label="E-mail",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "adresse email",
            }
        ),
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            {
                "class": "form-control",
                "placeholder": "Mot de passe",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirmation Mot de passe",
        widget=forms.PasswordInput(
            {
                "class": "form-control",
                "placeholder": "Mot de passe",
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "city",
            "password1",
            "password2",
        )


class UpdateDeliverymenForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=254,
        label="Prénom",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Prénom",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=254,
        label="Nom de famille",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Nom de famille",
            }
        ),
    )
    address = forms.CharField(
        max_length=254,
        label="Adresse",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Adresse complète",
            }
        ),
    )
    address = forms.CharField(
        max_length=254,
        label="Ville",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Ville",
            }
        ),
    )
    phone = forms.CharField(
        max_length=254,
        label="Téléphone",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Numéro de Téléphone",
            }
        ),
    )
    email = forms.CharField(
        max_length=254,
        label="E-mail",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "adresse email",
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
        )


class PackCreationForm(forms.ModelForm):
    title = forms.CharField(
        max_length=254,
        label="Nom du pack",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Nom du pack",
            }
        ),
    )
    price = forms.CharField(
        max_length=254,
        label="Prix",
        widget=forms.NumberInput(
            {
                "class": "form-control",
                "placeholder": "Prix",
            }
        ),
    )

    class Meta:
        model = Pack
        fields = (
            "title",
            "price",
        )


class AssignCouponToPersonForm(forms.Form):
    customer = forms.ModelChoiceField(
        CustomUser.objects.all(),
        label="Personne",
        widget=forms.Select(
            {
                "class": "form-control",
                "placeholder": "Personne",
            }
        ),
    )


class CustomUserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=80,
        label="Prénom",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Saisissez...",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=80,
        label="Nom de famille",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Saisissez...",
            }
        ),
    )
    email = forms.CharField(
        max_length=80,
        label="E-mail",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Saisissez...",
            }
        ),
    )
    address = forms.CharField(
        max_length=80,
        label="Address",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Saisissez...",
            }
        ),
    )
    phone = forms.CharField(
        max_length=80,
        label="Numéro de téléphone",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Saisissez...",
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
        )
