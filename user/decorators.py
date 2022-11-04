import requests

from functools import wraps

from django.conf import settings
from django.contrib import messages

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def staff_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="login"
):
    """Decorator for views that checks that the logged in user is a staff/admin,
    redirects to the log-in page if necessary."""
    actual_decorator = user_passes_test(
        lambda user: user.is_active and user.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def superuser_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="login"
):
    """Decorator for views that checks that the logged in user is a superuser,
    redirects to the log-in page if necessary."""
    actual_decorator = user_passes_test(
        lambda user: user.is_active and user.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def team_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="login"
):
    """Decorator for views that checks that the logged in user is a team,
    redirects to the log-in page if necessary."""
    actual_decorator = user_passes_test(
        lambda user: user.is_active and user.is_team,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def deliveryman_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="login"
):
    """Decorator for views that checks that the logged in user is a deliveryman,
    redirects to the log-in page if necessary."""
    actual_decorator = user_passes_test(
        lambda user: user.is_active and user.is_deliveryman,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def realypoint_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="login"
):
    """Decorator for views that checks that the logged in user is a realypoint,
    redirects to the log-in page if necessary."""
    actual_decorator = user_passes_test(
        lambda user: user.is_active and user.is_realypoint(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def professionnal_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="login"
):
    """Decorator for views that checks that the logged in user is a professionnal,
    redirects to the log-in page if necessary."""
    actual_decorator = user_passes_test(
        lambda user: user.is_active and user.is_professionnal(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def particular_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="login"
):
    """Decorator for views that checks that the logged in user is a particular,
    redirects to the log-in page if necessary."""
    actual_decorator = user_passes_test(
        lambda user: user.is_active and user.is_particular(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def check_recaptcha(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == "POST":
            recaptcha_response = request.POST.get("g-recaptcha-response")
            data = {
                "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                "response": recaptcha_response,
            }
            r = requests.post(
                "https://www.google.com/recaptcha/api/siteverify", data=data
            )
            result = r.json()
            if result["success"]:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request, "ReCaptcha invalide, veuillez réessayer")
        return view_func(request, *args, **kwargs)

    return _wrapped_view
