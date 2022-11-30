from django.http.response import JsonResponse
from django.conf import settings

from send_email.views import send_new_register_email
from send_email.whatsapp_notif import send_notif_whats, send_notif_infobip
from .forms import (
    ChangePasswordForm,
    CustomUserUpdateForm,
    SignUpForm,
    UpdateProfileForm,
)
from django.utils.http import url_has_allowed_host_and_scheme
from .models import CustomUser
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from user.forms import CustomUserLoginForm
from django.views.generic import View, UpdateView, DetailView

GOOGLE_MAP_API_KEY = settings.GOOGLE_MAP_API_KEY


class LoginView(View):
    form_class = CustomUserLoginForm
    template_name = "user/login.html"

    def get(self, request, **kwargs):
        form = self.form_class()
        user = request.user
        if user.is_authenticated:
            return redirect("page:home")
        return render(request, self.template_name, {"form": form})

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        next_ = request.GET.get("next")
        next_post = request.POST.get("next")
        redirect_path = next_ or next_post if next_ or next_post else "/"
        if form.is_valid():
            phone = form.cleaned_data.get("phone")
            password = form.cleaned_data.get("password")
            user = authenticate(request, phone=phone, password=password)
            if user is not None:
                auth_login(request, user)
                if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
                    return redirect(redirect_path)
                else:
                    return redirect("dashboard:dashboard")
            else:
                messages.error(request, "Information incorrecte")
                return redirect("login")
        return render(request, self.template_name, {"form": form})


class RegisterView(View):
    form_class = SignUpForm
    template_name = "user/register.html"

    def get(self, request, **kwargs):
        form = self.form_class()
        user = request.user
        if user.is_authenticated:
            return redirect("page:home")
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "GOOGLE_MAP_API_KEY": GOOGLE_MAP_API_KEY,
            },
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        # body ="Nous sommes heureux de vous accueillir dans la communauté d’AfricaRelais. AfricaRelais est une plateforme de mise en relation collaborative entre particuliers et/ou entreprises pour la livraison de colis dans la région de Dakar via points relais. Nous avons hâte de vous retrouver sur nos différentes plateformes. En tant que membre de la communauté, vous pouvez : Sur serviceclient@africarelais.com : Poser des questions à nos équipes, faire des réclamations et/ou suggestion sur le service. Les suggestions feront l’objet d’une étude par les équipes d’AfricaRelais. Nous rejoindre sur : Facebook : https://web.facebook.com/AfricaRelais?_rdc=1&_rdr Instagram Nous contacter via WhatsApp au +221 784283907 Afin de finaliser votre inscription à notre service, cliquez sur le lien suivant : Communauté AfricaRelais.",

        if form.is_valid():
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            phone = form.cleaned_data.get("phone")
            phonetw = f"whatsapp:+221{phone}"
            print(first_name)
            # body =f"Bonjour  \n Nous sommes heureux de vous accueillir {phone} {first_name} dans la communauté d’AfricaRelais. AfricaRelais est une plateforme de mise en relation collaborative entre particuliers et/ou entreprises pour la livraison de colis dans la région de Dakar via points relais. Nous avons hâte de vous retrouver sur nos différentes plateformes. En tant que membre de la communauté, vous pouvez : Sur serviceclient@africarelais.com : Poser des questions à nos équipes, faire des réclamations et/ou suggestion sur le service. Les suggestions feront l’objet d’une étude par les équipes d’AfricaRelais. Nous rejoindre sur : Facebook : https://web.facebook.com/AfricaRelais?_rdc=1&_rdr Instagram Nous contacter via WhatsApp au +221 784283907 Afin de finaliser votre inscription à notre service, cliquez sur le lien suivant : Communauté AfricaRelais.",

            mail_to_lower = email.lower()
            password = form.cleaned_data.get("password1")
            password2 = form.cleaned_data.get("password2")
            if password == password2:
                if email and CustomUser.objects.filter(email=mail_to_lower).exists():
                    messages.error(request, "Cet Email est déja utilisé")
                    return redirect("register")
                else:
                    user = form.save(commit=False)
                    user.set_password(password)
                    user.save()
                    if user is not None:
                        auth_login(
                            request,
                            user,
                            backend="django.contrib.auth.backends.ModelBackend",
                        )
                        send_new_register_email(email, first_name, last_name)
                        # send_notif_whats(phonetw, body)
                        # send_notif_infobip(phonetw, body)
                        messages.success(request, "Compte crée avec succes...")
                        return redirect("login")
            else:
                messages.error(request, "Les mots de passe ne sont pas identiques")
                return redirect("register")
        else:
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "GOOGLE_MAP_API_KEY": GOOGLE_MAP_API_KEY,
                },
            )


class CustomUserUpdateDetailView(UpdateView, DetailView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    avatar_form = UpdateProfileForm
    password_form = ChangePasswordForm
    template_name = "profile.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(instance=user)
        relay = request.user.point_created.all()
        password_form = self.password_form(user=user)
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "user": user,
                "relay": relay,
                "password_form": password_form,
            },
        )

    def post(self, request, *args, **kwargs):
        user = request.user
        relay = request.user.point_created.all()
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Information modifiée avec succes")
            return redirect("profile")
        password_form = self.password_form(request.POST, user=user)
        if password_form.is_valid():
            password_form.save()
            messages.success(request, "Mot de passe modifiée avec succes")
            return redirect("profile")
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "user": user,
                "relay": relay,
                "password_form": password_form,
            },
        )


def update_profile_image(request):
    avatar_form = UpdateProfileForm(
        request.POST or None, request.FILES or None, instance=request.user
    )
    try:
        if request.is_ajax() and avatar_form.is_valid():
            avatar = avatar_form.save(commit=False)
            avatar.save()
            return JsonResponse(
                {"code": "201", "message": "Profile mis a jour", "is_success": True}
            )
    except Exception:
        return JsonResponse(
            {"code": "500", "message": "Une erreur s'est produite", "is_success": False}
        )
