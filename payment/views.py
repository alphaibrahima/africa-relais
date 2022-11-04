import paydunya
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from course.models import Course

# from .tasks import payment_completed
# from course.tasks import enroll_course
from order.models import Order
from payment.services.paydunya import (
    get_invoice,
    get_items,
    get_user_and_course,
    invoice_confirmation,
)
from userlogs.models import UserLog
from users.models import CustomUser

# Activer le mode 'test'. Le debug est à False par défaut
paydunya.debug = settings.DEBUG

# Configurer les clés d'API
paydunya.api_keys = settings.PAYDUNYA_ACCESS_TOKENS


def payment_process(request, order_pk=None, user_id=None):
    session_order_id = request.session.get("order_id")
    order_id = session_order_id if session_order_id else order_pk
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    items = get_items(order.items.all())
    order_item_first = order.items.all()[0]
    custom_data = get_user_and_course(
        order_item_first.course.id,
        user_id,
    )
    try:
        successful, response = get_invoice(
            items,
            total_cost,
            request.get_host(),
            custom_data=custom_data,
        )
        if successful:
            # payment_completed.delay(order.id)
            return redirect(response.get("response_text"))
    except Exception:
        messages.error(
            request, f"Une erreur s'est produit, veuillez ressayer {response}"
        )
    return redirect("cart:cart_detail")


def payment_done(request):
    try:
        token = request.GET.get("token")
        successful, response = invoice_confirmation(token)
        if successful:
            # userID, courseID
            course_id = response.get("custom_data").get("course_id")
            user_id = response.get("custom_data").get("user_id")
            student = CustomUser.objects.get(pk=user_id)
            course = Course.objects.get(pk=course_id)
            student.courses_enrolled.add(course)
            # enroll_course.delay(student.email, course.title)
            UserLog.objects.create(
                action=f"Enrolled {course} course",
                user_type="Student",
                user=student,
            )
            messages.success(request, "Cours acheté avec succes...")
            if course.is_live:
                return redirect("course:live_courses_thanks")
            return redirect(f"/courses/{course.slug}/overview")
    except Exception as e:
        messages.error(request, f"Paiement non complète {e}")
    return redirect("cart:cart_detail")


def payment_canceled(request):
    return render(request, "payment/canceled.html")
