from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path(
        "process/<int:order_pk>/<int:user_id>/", views.payment_process, name="process"
    ),
    path("done/", views.payment_done, name="done"),
    path("canceled/", views.payment_canceled, name="canceled"),
]
