from django.urls import path
from django.utils.translation import gettext_lazy as _
from . import views

app_name = "order"

urlpatterns = [
    path(_("create/"), views.order_create, name="order_create"),
    path(
        "create-mobile-order/<int:user_id>/<int:course_id>/",
        views.create_mobile_order,
        name="mobile_create_order",
    ),
    path(
        "admin/order/<int:order_id>/",
        views.admin_order_detail,
        name="admin_order_detail",
    ),
    path(
        "admin/order/<int:order_id>/pdf/", views.admin_order_pdf, name="admin_order_pdf"
    ),
]
