from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm,
)

from delivery_management.constants import (
    PARTICULAR,
    PROFESSIONNAL,
)

from .models import CustomUser


class CustomUserCreationForm(forms.Form):
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            {
                "class": "form-control",
                "placeholder": "Saisissez...",
            }
        ),
    )
    password2 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            {
                "class": "form-control",
                "placeholder": "Saisissez...",
            }
        ),
    )

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("email", "password1")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "avatar")


class CustomUserLoginForm(forms.Form):
    # email = forms.CharField(
    #     max_length=254,
    #     required=False,
    #     label="Entrez votre email",
    #     widget=forms.TextInput(
    #         {"class": "form-control", "placeholder": "Saisissez...", "type": "email"}
    #     ),
    # )
    phone = forms.CharField(
        max_length=254,
        label="Téléphone",
        widget=forms.TextInput(
            {
                "class": "form-control form-tel",
                "placeholder": "Saisissez...",
                "id": "phone",
                "type": "number",
                "required": "true",
            }
        ),
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            {
                "class": "form-control",
                "placeholder": "Saisissez...",
            }
        ),
    )


class SignUpForm(forms.ModelForm):
    USER_TYPE = (
        (PROFESSIONNAL, "Je suis Professionnel"),
        (PARTICULAR, "Je suis Particulier"),
    )
    user_type = forms.ChoiceField(
        choices=USER_TYPE,
        label="Vous etes?",
        widget=forms.Select(
            {
                "class": "form-control my-2 float-none",
                "placeholder": "Votre profil",
            }
        ),
    )
    first_name = forms.CharField(
        max_length=254,
        label="Prénom",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Saisissez...",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=254,
        label="Nom de famille",
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": "Saisissez...",
            }
        ),
    )
    phone = forms.CharField(
        max_length=254,
        label="Téléphone",
        widget=forms.TextInput(
            {
                "class": "form-control form-tel",
                "placeholder": "Saisissez...",
                "id": "phone",
                "type": "number",
                "required": "true",
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
                "placeholder": "Saisissez...",
                "type": "email",
            }
        ),
    )
    # address = forms.CharField(
    #     max_length=254,
    #     label="Quartier",
    #     widget=forms.TextInput(
    #         {
    #             "class": "form-control",
    #             "placeholder": "Saisissez...",
    #             "id": "pac-input",
    #         }
    #     ),
    # )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            {
                "class": "form-control password",
                "placeholder": "Saisissez...",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirmer le  mot de passe",
        widget=forms.PasswordInput(
            {
                "class": "form-control password",
                "placeholder": "Saisissez...",
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = [
            "user_type",
            "first_name",
            "last_name",
            "phone",
            "email",
            # "address",
            "password1",
            "password2",
        ]


class CustomUserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        label="Photo de profile",
    )

    class Meta:
        model = CustomUser
        fields = ("avatar",)


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
            "avatar",
        )


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.FileField(
        label="Photo de profile",
        widget=forms.FileInput(
            {
                "class": "opacity-0 position-absolute as-parent file-upload",
                "accept": "image/*",
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = ("avatar",)


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        max_length=80,
        label="Mot de passe actuel",
        widget=forms.PasswordInput(
            {
                "class": "form-control",
                "placeholder": "Saisissez...",
            }
        ),
    )
    new_password1 = forms.CharField(
        max_length=80,
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(
            {
                "class": "form-control",
                "placeholder": "Saisissez...",
            }
        ),
    )
    new_password2 = forms.CharField(
        max_length=80,
        label="Confirmation mot de passe",
        widget=forms.PasswordInput(
            {
                "class": "form-control",
                "placeholder": "Saisissez...",
            }
        ),
    )

    class Meta:
        model = CustomUser
