from typing import Any

import sweetify
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import (
    BendyLoginForm,
    BendyPasswordChangeForm,
    BendyProfileUpdateForm,
    BendyRegisterForm,
)
from .mixins import BannedUserMixin
from .models import BendyUser


# ── Login ─────────────────────────────────────────────────────────────────────

class LoginView(TemplateView):
    """
    Vista de inicio de sesión.
    Usa TemplateView + manejo manual de POST para poder integrar Sweetify.
    """

    template_name: str = "auth_app/login.html"

    def get(self, request: HttpRequest, *args: Any,
            **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("bendy:index")
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any,
             **kwargs: Any) -> HttpResponse:
        form = BendyLoginForm(data=request.POST, request=request)
        if form.is_valid():
            user: BendyUser = form.get_user()
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
            text=
            form.errors.get("__all__", ["Usuario o contraseña incorrectos."])[
                0],
            timer=4000,
        )
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = kwargs.get("form", BendyLoginForm())
        return context


# ── Register ──────────────────────────────────────────────────────────────────

class RegisterView(TemplateView):
    """Vista de registro de nuevos usuarios."""

    template_name: str = "auth_app/register.html"

    def get(self, request: HttpRequest, *args: Any,
            **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("bendy:index")
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any,
             **kwargs: Any) -> HttpResponse:
        form = BendyRegisterForm(data=request.POST)
        if form.is_valid():
            user: BendyUser = form.save()
            login(request, user,
                  backend="django.contrib.auth.backends.ModelBackend")
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
        context = super().get_context_data(**kwargs)
        context["form"] = kwargs.get("form", BendyRegisterForm())
        return context


# ── Logout ────────────────────────────────────────────────────────────────────

class LogoutView(TemplateView):
    template_name: str = "auth_app/login.html"

    def post(self, request: HttpRequest, *args: Any,
             **kwargs: Any) -> HttpResponse:
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

    def get(self, request: HttpRequest, *args: Any,
            **kwargs: Any) -> HttpResponse:
        return self.post(request, *args, **kwargs)


# ── Profile — Detail ──────────────────────────────────────────────────────────

class ProfileView(BannedUserMixin, DetailView):
    """
    Perfil público de un usuario.
    Usa BannedUserMixin (mixin personalizado) para proteger la vista.
    """

    model = BendyUser
    template_name: str = "auth_app/profile.html"
    context_object_name: str = "profile_user"
    slug_field: str = "username"
    slug_url_kwarg: str = "username"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["is_own_profile"] = self.request.user == self.get_object()
        return context


# ── Profile — Update ──────────────────────────────────────────────────────────

class ProfileUpdateView(BannedUserMixin, SuccessMessageMixin, UpdateView):
    """
    Edición del perfil propio. Usa UpdateView + ModelForm + SuccessMessageMixin.
    """

    model = BendyUser
    form_class = BendyProfileUpdateForm
    template_name: str = "auth_app/profile_edit.html"
    success_message: str = "Perfil actualizado correctamente."

    def get_object(self, queryset=None) -> BendyUser:
        # El usuario solo puede editar su propio perfil
        return self.request.user

    def get_success_url(self) -> str:
        return reverse_lazy("auth:profile",
                            kwargs={"username": self.request.user.username})

    def form_invalid(self, form) -> HttpResponse:
        sweetify.error(
            self.request,
            "Error al guardar",
            text="Revisa los campos e inténtalo de nuevo.",
            timer=4000,
        )
        return super().form_invalid(form)


# ── Password Change ───────────────────────────────────────────────────────────

class PasswordChangeView(BannedUserMixin, TemplateView):
    """Vista para cambio de contraseña con Sweetify."""

    template_name: str = "auth_app/password_change.html"

    def post(self, request: HttpRequest, *args: Any,
             **kwargs: Any) -> HttpResponse:
        form = BendyPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user: BendyUser = form.save()
            update_session_auth_hash(request, user)
            sweetify.success(
                request,
                "Contraseña actualizada",
                text="Tu contraseña ha sido cambiada con éxito.",
                timer=3000,
            )
            return redirect("auth:profile", username=request.user.username)
        sweetify.error(
            request,
            "Error al cambiar contraseña",
            text="Verifica que los datos sean correctos.",
            timer=4000,
        )
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = kwargs.get("form", BendyPasswordChangeForm(
            user=self.request.user))
        return context


# ── User List ─────────────────────────────────────────────────────────────────

class UserListView(BannedUserMixin, ListView):
    """Ranking de usuarios por puntos de tinta."""

    model = BendyUser
    template_name: str = "auth_app/user_list.html"
    context_object_name: str = "users"
    paginate_by: int = 20

    def get_queryset(self):
        return BendyUser.objects.filter(is_active=True,
                                        is_banned=False).order_by(
            "-ink_points"
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["total_users"] = BendyUser.objects.filter(
            is_active=True).count()
        return context


# ── Delete Account ────────────────────────────────────────────────────────────

class DeleteAccountView(BannedUserMixin, DeleteView):
    """
    Eliminación de la propia cuenta. Usa DeleteView con confirmación.
    """

    model = BendyUser
    template_name: str = "auth_app/delete_account.html"
    success_url = reverse_lazy("bendy:index")

    def get_object(self, queryset=None) -> BendyUser:
        return self.request.user

    def post(self, request: HttpRequest, *args: Any,
             **kwargs: Any) -> HttpResponse:
        confirm: str = request.POST.get("confirm_username", "")
        if confirm != request.user.username:
            sweetify.error(
                request,
                "Confirmación incorrecta",
                text="El nombre de usuario no coincide.",
                timer=4000,
            )
            return self.render_to_response(self.get_context_data())
        logout(request)
        # Llamamos a delete() directamente porque ya deslogueamos
        self.get_object().delete()
        sweetify.success(
            request,
            "Cuenta eliminada",
            text="Tu cuenta ha sido eliminada permanentemente.",
            timer=5000,
        )
        return redirect(self.success_url)
