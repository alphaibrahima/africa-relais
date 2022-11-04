import weasyprint
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from user.models import CustomUser
from .models import Order

# from .tasks import order_created


def order_create(request):
    # user = request.user
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        order = Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
        )
        obj, created = CustomUser.objects.get_or_create(
            email=email,
        )
        if created:
            obj.set_password("12345678")
        obj.phone = phone
        obj.first_name = first_name
        obj.last_name = last_name
        if not obj.is_teacher:
            obj.is_student = True
        obj.save()
        # if cart.coupon:
        #     order.coupon = cart.coupon
        #     order.discount = cart.coupon.discount
        # order.save()
        # for item in cart:
        #     OrderItem.objects.create(
        #         order=order,
        #         course=item["course"],
        #         price=item["price"],
        #         quantity=item["quantity"],
        #     )
        # clear the cart
        # launch asynchronous task
        # order_created.delay(order.id)
        # set the order in the session
        # redirect for payment
        return redirect(
            reverse(
                "payment:process",
                kwargs={
                    "order_pk": order.id,
                    "user_id": obj.id,
                },
            )
        )

    return redirect("cart:cart_detail")


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "admin/orders/order/detail.html", {"order": order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string("orders/order/pdf.html", {"order": order})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename=order_{order.id}.pdf"
    weasyprint.HTML(string=html).write_pdf(
        response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + "/css/pdf.css")]
    )
    return response
