from django import forms

from page.models import RelayPoint
from user.models import CustomUser


class AddRealyPointForm(forms.ModelForm):
    title = forms.CharField(
        max_length=80,
        label="Titre :",
        widget=forms.TextInput({"class": "form-control", "placeholder": "Titre"}),
    )
    address = forms.CharField(
        max_length=80,
        label="Adresse :",
        widget=forms.TextInput({"class": "form-control", "placeholder": "Adresse"}),
    )
    pluscode = forms.CharField(
        max_length=80,
        label="Pluscode :",
        widget=forms.TextInput({"class": "form-control", "placeholder": "Pluscode"}),
    )
    phone = forms.CharField(
        max_length=80,
        label="Numéro de téléphone :",
        widget=forms.TextInput(
            {"class": "form-control", "placeholder": "Numéro de téléphone"}
        ),
    )
    friday = forms.CharField(
        max_length=80,
        label="Vendredi :",
        widget=forms.TextInput({"class": "form-control", "placeholder": "8a.m  6p.m."}),
    )
    saturday = forms.CharField(
        max_length=80,
        label="Samedi :",
        widget=forms.TextInput({"class": "form-control", "placeholder": "8a.m  6p.m."}),
    )
    sunday = forms.CharField(
        max_length=80,
        label="Dimanche :",
        widget=forms.TextInput({"class": "form-control", "placeholder": "8a.m  6p.m."}),
    )
    monday = forms.CharField(
        max_length=80,
        label="Lundi :",
        widget=forms.TextInput({"class": "form-control", "placeholder": "8a.m  6p.m."}),
    )
    tuesday = forms.CharField(
        max_length=80,
        label="Mardi :",
        widget=forms.TextInput({"class": "form-control", "placeholder": "8a.m  6p.m."}),
    )
    wednesday = forms.CharField(
        max_length=80,
        label="Mercredi :",
        widget=forms.TextInput({"class": "form-control", "placeholder": "8a.m  6p.m."}),
    )
    thursday = forms.CharField(
        max_length=80,
        label="Jeudi :",
        widget=forms.TextInput({"class": "form-control", "placeholder": "8a.m  6p.m."}),
    )
    latitude = forms.CharField(
        max_length=80,
        label="Latitude :",
        widget=forms.TextInput({"class": "form-control", "placeholder": "Latitude"}),
    )
    longitude = forms.CharField(
        max_length=80,
        label="Longitude :",
        widget=forms.TextInput({"class": "form-control", "placeholder": "Longitude"}),
    )
    name = forms.CharField(
        max_length=80,
        label="Nom point relais :",
        widget=forms.TextInput({"class": "form-control", "placeholder": "Name"}),
    )

    class Meta:
        model = RelayPoint
        fields = (
            "title",
            "address",
            "pluscode",
            "phone",
            "friday",
            "saturday",
            "sunday",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "latitude",
            "longitude",
            "name",
        )


class UpdateRealyPointForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=80,
        label="Numéro de téléphone :",
        widget=forms.TextInput(
            {"class": "form-control", "placeholder": "Numéro de téléphone"}
        ),
    )
    address = forms.CharField(
        max_length=80,
        label="Adresse :",
        widget=forms.TextInput({"class": "form-control", "placeholder": "Adresse"}),
    )
    city = forms.CharField(
        max_length=80,
        label="City :",
        widget=forms.TextInput({"class": "form-control", "placeholder": "Ville"}),
    )
    country = forms.CharField(
        max_length=80,
        label="Pays :",
        widget=forms.TextInput({"class": "form-control", "placeholder": "Pays"}),
    )
    county = forms.CharField(
        max_length=80,
        label="county :",
        widget=forms.TextInput({"class": "form-control", "placeholder": "Département"}),
    )
    email = forms.CharField(
        max_length=80,
        label="Email :",
        widget=forms.TextInput({"class": "form-control", "placeholder": "Email"}),
    )
    latitude = forms.CharField(
        max_length=80,
        label="Latitude :",
        widget=forms.TextInput({"class": "form-control", "placeholder": "Latitude"}),
    )
    longitude = forms.CharField(
        max_length=80,
        label="Longitude :",
        widget=forms.TextInput({"class": "form-control", "placeholder": "Longitude"}),
    )

    class Meta:
        model = RelayPoint
        fields = (
            "phone",
            "address",
            "city",
            "country",
            "county",
            "email",
            "latitude",
            "longitude",
        )


class AddRealyPointsForm(forms.Form):
    excel_file = forms.FileField(label="Excel File", required=False)


class AssignDelivermenForm(forms.Form):
    delivermen = forms.ModelChoiceField(
        CustomUser.objects.deliverymen(),
        label="Livreur",
        widget=forms.Select(
            {
                "class": "form-control",
                "placeholder": "Livreur",
            }
        ),
    )
