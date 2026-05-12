from typing import Any

import sweetify
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView

from bendy_app.forms import (
    BendyLoginForm,
    BendyRegisterForm,
    BendyProfileUpdateForm,
    BendyPasswordChangeForm,
)
from bendy_app.models import BendyUser


class LoginView(TemplateView):
    template_name: str = "auth_app/login.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["form"] = BendyLoginForm()
        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("bendy:index")
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form: BendyLoginForm = BendyLoginForm(data=request.POST)
        if form.is_valid():
            user: BendyUser | None = form.get_user()
            if user is not None:
                if user.is_banned:
                    sweetify.error(
                        request,
                        "Acceso denegado",
                        text="Tu cuenta ha sido suspendida. Contacta con un administrador.",
                        persistent=True,
                        icon="error",
                    )
                    return self.render_to_response(self.get_context_data(form=form))
                login(request, user)
                if not form.cleaned_data.get("remember_me"):
                    request.session.set_expiry(0)
                sweetify.success(
                    request,
                    f"¡Bienvenido de nuevo, {user.display_name}!",
                    text="Has iniciado sesión en el Estudio de Tinta.",
                    timer=3000,
                    icon="success",
                )
                next_url: str = request.GET.get("next", reverse_lazy("bendy:index"))
                return redirect(next_url)
        sweetify.error(
            request,
            "Error de acceso",
            text="Usuario o contraseña incorrectos. Vuelve a intentarlo.",
            timer=4000,
        )
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        if "form" not in kwargs:
            context["form"] = BendyLoginForm()
        else:
            context["form"] = kwargs["form"]
        return context


class RegisterView(TemplateView):
    template_name: str = "auth_app/register.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("bendy:index")
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form: BendyRegisterForm = BendyRegisterForm(data=request.POST)
        if form.is_valid():
            user: BendyUser = form.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            sweetify.success(
                request,
                "¡Registro completado!",
                text=f"Bienvenido al Estudio de Tinta, {user.username}. Tu historia comienza ahora.",
                timer=5000,
                icon="success",
            )
            return redirect("bendy:index")
        sweetify.error(
            request,
            "Error en el registro",
            text="Por favor, corrige los errores en el formulario.",
            timer=4000,
        )
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["form"] = kwargs.get("form", BendyRegisterForm())
        return context


class LogoutView(TemplateView):
    template_name: str = "auth_app/login.html"

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        username: str = request.user.username if request.user.is_authenticated else ""
        logout(request)
        sweetify.info(
            request,
            "Sesión cerrada",
            text=f"Hasta pronto, {username}. El estudio te espera.",
            timer=3000,
            icon="info",
        )
        return redirect("bendy:index")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return self.post(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, DetailView):
    model: type[BendyUser] = BendyUser
    template_name: str = "auth_app/profile.html"
    context_object_name: str = "profile_user"
    slug_field: str = "username"
    slug_url_kwarg: str = "username"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["is_own_profile"] = self.request.user == self.get_object()
        return context


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    template_name: str = "auth_app/profile_edit.html"

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form: BendyProfileUpdateForm = BendyProfileUpdateForm(
            data=request.POST,
            files=request.FILES,
            instance=request.user,
        )
        if form.is_valid():
            form.save()
            sweetify.success(
                request,
                "Perfil actualizado",
                text="Tus datos han sido guardados exitosamente.",
                timer=3000,
            )
            return redirect("bendy:profile", username=request.user.username)
        sweetify.error(
            request,
            "Error al guardar",
            text="Revisa los campos e inténtalo de nuevo.",
            timer=4000,
        )
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["form"] = kwargs.get("form",
                                     BendyProfileUpdateForm(instance=self.request.user))
        return context


class PasswordChangeView(LoginRequiredMixin, TemplateView):
    template_name: str = "auth_app/password_change.html"

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form: BendyPasswordChangeForm = BendyPasswordChangeForm(user=request.user,
                                                                data=request.POST)
        if form.is_valid():
            user: BendyUser = form.save()
            update_session_auth_hash(request, user)
            sweetify.success(
                request,
                "Contraseña actualizada",
                text="Tu contraseña ha sido cambiada con éxito.",
                timer=3000,
            )
            return redirect("bendy:profile", username=request.user.username)
        sweetify.error(
            request,
            "Error al cambiar contraseña",
            text="Verifica que los datos sean correctos.",
            timer=4000,
        )
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["form"] = kwargs.get("form",
                                     BendyPasswordChangeForm(user=self.request.user))
        return context


class UserListView(LoginRequiredMixin, ListView):
    model: type[BendyUser] = BendyUser
    template_name: str = "auth_app/user_list.html"
    context_object_name: str = "users"
    paginate_by: int = 20

    def get_queryset(self):
        return BendyUser.objects.filter(is_active=True, is_banned=False).order_by(
            "-ink_points")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["total_users"] = BendyUser.objects.filter(is_active=True).count()
        return context


class DeleteAccountView(LoginRequiredMixin, TemplateView):
    template_name: str = "auth_app/delete_account.html"

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user: BendyUser = request.user
        confirm: str = request.POST.get("confirm_username", "")
        if confirm != user.username:
            sweetify.error(
                request,
                "Confirmación incorrecta",
                text="El nombre de usuario no coincide.",
                timer=4000,
            )
            return self.render_to_response(self.get_context_data())
        logout(request)
        user.delete()
        sweetify.success(
            request,
            "Cuenta eliminada",
            text="Tu cuenta ha sido eliminada permanentemente.",
            timer=5000,
        )
        return redirect("bendy:index")
