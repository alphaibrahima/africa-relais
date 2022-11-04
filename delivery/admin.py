from django.contrib import admin
from .models import DeliveryPoint, DeparturePoint, Package, Bill, PackageTracking


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = [
        "tracking_number",
        "delivery_point",
        "amount",
        "pack",
        "mode",
    ]


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "client_name",
        "client_phone",
        "paid",
    ]


admin.site.register(PackageTracking)
admin.site.register(DeliveryPoint)
admin.site.register(DeparturePoint)
