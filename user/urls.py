from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    CustomUserUpdateDetailView,
    LoginView,
    RegisterView,
    update_profile_image,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", CustomUserUpdateDetailView.as_view(), name="profile"),
    path(
        "profile/update_profile_image/",
        update_profile_image,
        name="update-profile-image",
    ),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="user/change-password.html"
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="user/change-password-done.html"
        ),
        name="password_change_done",
    ),
    # reset password
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="user/reset-password.html"),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="user/reset-password-done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="user/reset-password-confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="user/reset-password-complete.html"
        ),
        name="password_reset_complete",
    ),
    # path("update_pack/", updatePack, name="update-pack"),
]
