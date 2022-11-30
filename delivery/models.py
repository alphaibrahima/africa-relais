from django.db import models
from delivery_management.constants import (
    ECONOMIQUE,
    EXPRESS,
    HOME,
    PREPARING,
    ARRIVED,
    RECEIVED,
    RELAY_POINT,
    IN_PROGRESS,
    STANDARDS,
)
from delivery_management.utils import generate_key

from page.models import BaseTimeStampedModel


class Package(BaseTimeStampedModel):
    DELIVERY_STATUS_CHOICES = (
        (PREPARING, "En préparation"),
        (ARRIVED, "Arrivé au point relais"),
        (IN_PROGRESS, "En cours de livraison"),
        (RECEIVED, "Reçu par le client"),
    )
    DELIVERY_MODE_CHOICES = (
        (HOME, "Domicile"),
        (RELAY_POINT, "Point relais"),
    )
    DELIVERY_TYPE_CHOICES = (
        (STANDARDS, "Standards"),
        (EXPRESS, "Express"),
        (ECONOMIQUE, "Economique"),
    )
    status = models.CharField(
        max_length=155, choices=DELIVERY_STATUS_CHOICES, default=PREPARING
    )
    mode = models.CharField(
        max_length=155,
        choices=DELIVERY_MODE_CHOICES,
        default=HOME,
    )
    pack = models.CharField(
        max_length=155, choices=DELIVERY_TYPE_CHOICES, default=STANDARDS
    )
    weight = models.DecimalField(max_digits=6, decimal_places=2, default=5)
    # prix de l'article
    price = models.DecimalField(max_digits=6, decimal_places=2, default=5)
    picture = models.ImageField(
        upload_to="packages/%Y/%m%d",
        null=True,
        blank=True,
    )
    # Expediteur
    sender = models.ForeignKey("user.CustomUser", models.SET_NULL, null=True)
    # livreur
    delivered_by = models.ForeignKey(
        "user.CustomUser",
        models.SET_NULL,
        null=True,
        related_name="deliveries",
    )
    delivery_point = models.ForeignKey(
        "delivery.DeliveryPoint",
        models.SET_NULL,
        null=True,
        related_name="delivery_points",
    )
    # destinataire
    customer = models.ForeignKey("page.Contact", models.SET_NULL, null=True)
    # montant a payer
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    tracking_number = models.CharField(
        max_length=8,
        null=True,
    )

    def __str__(self):
        if not self.delivered_by:
            return ""
        return str(self.delivered_by)


    def _get_unique_tracking_number(self):
        unique_tracking_number = self.tracking_number
        while Package.objects.filter(tracking_number=unique_tracking_number).exists():
            unique_tracking_number = generate_key()
        return unique_tracking_number

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = self._get_unique_tracking_number()
        super().save(*args, **kwargs)


class Bill(BaseTimeStampedModel):
    client_name = models.CharField(max_length=155)
    client_phone = models.CharField(max_length=155)
    package = models.ForeignKey("delivery.Package", models.SET_NULL, null=True)
    paid = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.client_name


class PackageTracking(BaseTimeStampedModel):
    note = models.CharField(max_length=60)
    location = models.CharField(max_length=60)
    tracking_code = models.CharField(
        max_length=8,
        null=True,
    )

    def __str__(self):
        return self.note


class DeparturePoint(BaseTimeStampedModel):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class DeliveryPoint(BaseTimeStampedModel):
    departure_point = models.ForeignKey(
        "delivery.DeparturePoint",
        on_delete=models.CASCADE,
    )
    arrival_point = models.CharField(
        max_length=150,
    )
    delivery_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    transporter_commission = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    africarelais_commission = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    relayer_commission = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )

    class Meta:
        unique_together = (
            "departure_point",
            "arrival_point",
        )

    def __str__(self):
        return f"Depart: {self.departure_point.name} | Arrivee: {self.arrival_point}"


"""
Recuperer les liste des status
a la creation:
    note = "Votre colis a ete renseigne sur AfricaRelais
a la demande du livreur de venir
    note = Votre colis est en preparation
a l'acceptation
    note = votre colis est avec le livreur Modou
a la livraison
    note = Votre colis est lovre par
"""
