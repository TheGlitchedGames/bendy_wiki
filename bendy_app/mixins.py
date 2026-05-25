from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect


class EditorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (
            user.is_staff or getattr(user, "role", "") in ("editor", "admin")
        )

    def handle_no_permission(self):
        # Si no está autenticado, LoginRequiredMixin lo redirige al login.
        # Si está autenticado pero sin rol, lo mandamos al inicio.
        if self.request.user.is_authenticated:
            return redirect('bendy:index')
        return super().handle_no_permission()


class BreadcrumbMixin:
    breadcrumbs: list[dict[str, Any]] = []

    def get_breadcrumbs(self) -> list[dict[str, Any]]:
        return self.breadcrumbs

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = self.get_breadcrumbs()
        return context