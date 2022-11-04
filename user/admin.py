from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Entreprise, Feature, CustomUser, Pack, Transaction


from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active", "user_type")
    list_filter = (
        "is_staff",
        "is_active",
        "user_type",
    )
    list_editable = (
        "is_active",
        "user_type",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "avatar",
                    "first_name",
                    "last_name",
                    "phone",
                    "address",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


# Register your models here.


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
    ]


@admin.register(Pack)
class PackAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "price",
    ]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "amount",
    ]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
    ]


@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "size",
        "name",
    ]
