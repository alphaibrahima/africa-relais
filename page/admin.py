from django.contrib import admin
from .models import Testimonial, RelayPoint, Rate, ClientRealyPoint, Carousel, Contact

# Register your models here.
@admin.register(RelayPoint)
class RealyPointAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "address",
        "phone",
        "email",
        "latitude",
        "longitude",
    ]


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "client_name",
        "rate",
        "relay_point",
    ]


@admin.register(ClientRealyPoint)
class ClientRealyPointAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "relay_point",
        "client",
        "is_favorite",
    ]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "full_name",
        "email",
        "phone",
        "address",
    ]


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "description",
        "image",
        "active",
    ]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user_title",
        "user_name",
        "description",
        "user_image",
        "platfom",
    ]
