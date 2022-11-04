from django.urls import path

from .views import (
    relayer,
    SendPackageView,
    get_delivery_price,
    package_tracking,
    tracking_results,
)

app_name = "delivery"

urlpatterns = [
    path(
        "send-package/",
        SendPackageView.as_view(),
        name="send-package",
    ),
    path("tracking/", package_tracking, name="package-tracking"),
    path(
        "tracking/results/",
        tracking_results,
        name="tracking-results",
    ),
    path(
        "get-delivery-price/",
        get_delivery_price,
        name="get_delivery_price",
    ),
    path(
        "relayer/",
        relayer,
        name="relayer_page",
    ),
]
