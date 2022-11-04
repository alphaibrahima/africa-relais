from django.db import models
from delivery_management.constants import (
    FACEBOOK,
    HOUR_OF_DAY_24,
    INSTAGRAM,
    LINKEDIN,
    TWITTER,
    WEEKDAYS,
    WHATSAPP,
    YOUTUBE,
)


class BaseTimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created"]


class Contact(BaseTimeStampedModel):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=60)
    address = models.CharField(max_length=160, null=True)
    created_by = models.ForeignKey(
        "user.CustomUser", models.SET_NULL, related_name="contact_created", null=True
    )

    def __str__(self) -> str:
        return self.full_name


class OpeningHours(models.Model):
    relay_point = models.ForeignKey(
        "page.RelayPoint",
        on_delete=models.CASCADE,
    )
    weekday_from = models.PositiveSmallIntegerField(choices=WEEKDAYS, unique=True)
    weekday_to = models.PositiveSmallIntegerField(choices=WEEKDAYS)
    from_hour = models.PositiveSmallIntegerField(choices=HOUR_OF_DAY_24)
    to_hour = models.PositiveSmallIntegerField(choices=HOUR_OF_DAY_24)

    def get_weekday_from_display(self):
        return WEEKDAYS[self.weekday_from]

    def get_weekday_to_display(self):
        return WEEKDAYS[self.weekday_to]


class RelayPoint(BaseTimeStampedModel):
    user = models.ForeignKey(
        "user.CustomUser",
        models.SET_NULL,
        related_name="point_created",
        null=True,
    )
    title = models.CharField(
        max_length=155,
        default="Dakar",
    )
    address = models.CharField(
        max_length=155,
        default="Dakar",
    )
    pluscode = models.CharField(
        max_length=155,
        default="Dakar",
    )
    phone = models.CharField(
        max_length=155,
        null=True,
    )
    email = models.CharField(
        max_length=155,
        null=True,
    )
    friday = models.CharField(
        max_length=155,
        default="8a.m  6p.m.",
    )
    saturday = models.CharField(
        max_length=155,
        default="8a.m  6p.m.",
    )
    sunday = models.CharField(
        max_length=155,
        default="8a.m  6p.m.",
    )
    monday = models.CharField(
        max_length=155,
        default="8a.m  6p.m.",
    )
    tuesday = models.CharField(
        max_length=155,
        default="8a.m  6p.m.",
    )
    wednesday = models.CharField(
        max_length=155,
        default="8a.m  6p.m.",
    )
    thursday = models.CharField(
        max_length=155,
        default="8a.m  6p.m.",
    )
    latitude = models.DecimalField(
        max_digits=30,
        decimal_places=7,
        default=14.71331,
    )
    longitude = models.DecimalField(
        max_digits=30,
        decimal_places=7,
        default=-17.45472,
    )
    name = models.CharField(max_length=155, default="Hlm")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Rate(BaseTimeStampedModel):
    """Class contenant les notes d'un point relais
    Args:
        BaseTimeStampedModel (Classe Abstraite): Recuperer le timestamp
    """

    client_name = models.CharField(max_length=155)
    client_email = models.CharField(max_length=155, null=True)
    relay_point = models.ForeignKey(
        "page.RelayPoint",
        on_delete=models.CASCADE,
        related_name="rates",
    )
    rate = models.IntegerField(default=0)


class ClientRealyPoint(BaseTimeStampedModel):
    """Class contenant les points relais d'un client
    Args:
        BaseTimeStampedModel (Classe Abstraite): Recuperer le timestamp
    """

    relay_point = models.ForeignKey(
        "page.RelayPoint",
        on_delete=models.CASCADE,
    )
    client = models.ForeignKey(
        "user.CustomUser",
        on_delete=models.CASCADE,
    )
    is_favorite = models.BooleanField(default=False)


class Carousel(models.Model):
    title = models.CharField(max_length=150, default="AfricaRelais")
    description = models.TextField(default="AfricaRelais")
    link_to = models.URLField(max_length=200, null=True, blank=True)
    link_text = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to="slides/", null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    PLATFORM_CHOICES = (
        (YOUTUBE, YOUTUBE),
        (LINKEDIN, LINKEDIN),
        (FACEBOOK, FACEBOOK),
        (WHATSAPP, WHATSAPP),
        (INSTAGRAM, INSTAGRAM),
        (TWITTER, TWITTER),
    )
    description = models.TextField()
    user_name = models.CharField(max_length=60)
    platfom = models.CharField(
        max_length=20, choices=PLATFORM_CHOICES, default=LINKEDIN
    )
    user_image = models.ImageField(upload_to="testimonial/user/", null=True, blank=True)
    user_title = models.CharField(max_length=60, null=True)
    capture = models.ImageField(upload_to="testimonial/capture/", null=True, blank=True)

    def __str__(self):
        return self.user_name
