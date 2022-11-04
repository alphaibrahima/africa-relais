from django import forms
from django.utils.translation import gettext_lazy as _

from coupons.models import Coupon


class CouponApplyForm(forms.Form):
    code = forms.CharField(
        label=_("Coupon"),
        widget=forms.TextInput(
            {"placeholder": "Votre code promo", "class": "form-control"}
        ),
    )


class AddCouponForm(forms.ModelForm):
    code = forms.CharField(
        label=_("Code Promo"),
        widget=forms.TextInput(
            {"placeholder": "Votre code promo", "class": "form-control m-2"}
        ),
    )
    discount = forms.CharField(
        label=_("Reduction en %"),
        widget=forms.NumberInput(
            {"placeholder": "Reduction en pourcentage", "class": "form-control m-2"}
        ),
    )
    valid_from = forms.DateField(
        label=_("Date de début"),
        widget=forms.DateInput(
            {
                "placeholder": "20/12/21",
                "class": "form-control m-2",
                "type": "date",
            }
        ),
    )
    valid_to = forms.DateField(
        label=_("Date d'expiration"),
        widget=forms.DateInput(
            {
                "placeholder": "21/12/22",
                "class": "form-control m-2",
                "type": "date",
            }
        ),
    )

    class Meta:
        model = Coupon
        fields = (
            "code",
            "discount",
            "valid_from",
            "valid_to",
        )
