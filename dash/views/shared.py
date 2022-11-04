from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render
from notifications.signals import notify


from django.contrib.auth.decorators import login_required


@login_required
def dashboard_view(request):
    user = request.user
    if user.is_staff:
        return redirect("dashboard:staff-dashboard")
    elif user.is_deliveryman():
        return redirect("dashboard:dashboard-deliverman")
    elif user.is_professionnal():
        return redirect("dashboard:professionnal-dashboard")
    elif user.is_particular():
        return redirect("dashboard:particular-dashboard")
    elif user.is_team():
        return redirect("dashboard:team-dashboard")
    elif user.is_realypoint():
        return redirect("dashboard:dashboard-realypoint")
    else:
        return HttpResponseForbidden()


@login_required
def get_notifications(request):
    user = request.user
    unread = user.notifications.unread()
    # active = user.notifications.active()
    sen = user.notifications.sent()
    notify.send(user, recipient=user, verb="Chargement de la page")
    return render(
        request,
        "notifications.html",
        {
            "user": user,
            "sen": sen,
            "unread": unread,
        },
    )
