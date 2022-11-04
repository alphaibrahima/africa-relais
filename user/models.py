from django.db import models
from django.contrib.auth.models import AbstractUser

from user.managers import CustomUserManager
from delivery_management.constants import (
    DELIVERYMAN,
    PARTICULAR,
    PROFESSIONNAL,
    TEAM,
    REALYPOINT,
)


class CustomUser(AbstractUser):

    USER_TYPE = (
        (TEAM, "Responsable"),
        (DELIVERYMAN, "Relayeur"),
        (PROFESSIONNAL, "Professionnel"),
        (PARTICULAR, "Particulier"),
        (REALYPOINT, "Point relais"),
    )
    username = None
    email = models.EmailField(
        unique=True,
        null=True,
    )
    phone = models.CharField(
        max_length=60,
        unique=True,
    )
    city = models.CharField(max_length=60, default="Dakar")
    address = models.CharField(max_length=155, blank=True, null=True)
    avatar = models.ImageField(
        upload_to="avatars/%Y/%m%d",
        null=True,
        blank=True,
    )
    entrprise = models.ForeignKey(
        "user.Entreprise",
        models.SET_NULL,
        null=True,
        blank=True,
    )
    pro_pack = models.ForeignKey(
        "user.ProPack",
        models.SET_NULL,
        null=True,
        blank=True,
    )
    particular_pack = models.ForeignKey(
        "user.ParticularPack",
        models.SET_NULL,
        null=True,
        blank=True,
    )
    user_type = models.CharField(
        max_length=155,
        choices=USER_TYPE,
        default=PARTICULAR,
    )

    objects = CustomUserManager()

    class Meta:
        ordering = ["-date_joined"]

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def is_team(self):
        if self.user_type == TEAM:
            return True
        return False

    def is_professionnal(self):
        if self.user_type == PROFESSIONNAL:
            return True
        return False

    def is_deliveryman(self):
        if self.user_type == DELIVERYMAN:
            return True
        return False

    def is_particular(self):
        if self.user_type == PARTICULAR:
            return True
        return False

    def is_realypoint(self):
        if self.user_type == REALYPOINT:
            return True
        return False

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = None
        super().save(*args, **kwargs)


class Feature(models.Model):
    title = models.CharField(max_length=160)
    # prix
    # nombre de livraison
    # zone

    def __str__(self) -> str:
        return self.title


class Pack(models.Model):
    title = models.CharField(max_length=25, default="Standards")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    features = models.ManyToManyField("user.Feature")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)


class ProPack(Pack):
    pass


class ParticularPack(Pack):
    pass


class Transaction(models.Model):
    EXPENSE = 0
    REVENU = 1
    TRANSACTION_TYPE = (
        (EXPENSE, "Dépense"),
        (REVENU, "Revenue"),
    )
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE)
    account = models.ForeignKey("user.Account", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.amount)


class Account(models.Model):
    user = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.email


class Entreprise(models.Model):
    ONE_MAN = "1"
    SMALL = "1-10"
    MEDIUM = "10-50"
    LARGE = "50-100"
    OTHER = "Other"
    COMPANY_SIZE = (
        (ONE_MAN, "Je suis solo entrepreneur"),
        (SMALL, "1 à 10 employés"),
        (MEDIUM, "10 à 50 employés"),
        (LARGE, "50 à 100 employés"),
        (OTHER, "Plus de 100 employés"),
    )
    size = models.CharField(max_length=60, choices=COMPANY_SIZE, default=ONE_MAN)
    name = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
