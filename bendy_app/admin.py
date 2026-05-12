from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import BendyUser


@admin.register(BendyUser)
class BendyUserAdmin(UserAdmin):
    list_display: tuple[str, ...] = (
        "username", "email", "display_role_badge", "favorite_game",
        "ink_points", "is_banned", "is_active", "joined_at",
    )
    list_filter: tuple[str, ...] = ("role", "favorite_game", "is_banned", "is_active",
                                    "is_staff")
    search_fields: tuple[str, ...] = ("username", "email", "first_name", "last_name")
    ordering: tuple[str, ...] = ("-joined_at",)
    readonly_fields: tuple[str, ...] = ("joined_at", "updated_at", "ink_points")
    list_per_page: int = 25
    list_editable: tuple[str, ...] = ("is_banned",)

    fieldsets = (
        (_("Credenciales"), {"fields": ("username", "password")}),
        (_("Información personal"), {
            "fields": ("first_name", "last_name", "email", "bio", "avatar"),
        }),
        (_("Configuración de Bendy Wiki"), {
            "fields": ("role", "favorite_game", "ink_points", "is_banned"),
            "classes": ("collapse",),
        }),
        (_("Permisos"), {
            "fields": ("is_active", "is_staff", "is_superuser", "groups",
                       "user_permissions"),
            "classes": ("collapse",),
        }),
        (_("Fechas importantes"), {
            "fields": ("last_login", "joined_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role",
                       "favorite_game"),
        }),
    )

    def display_role_badge(self, obj: BendyUser) -> str:
        colors: dict[str, str] = {
            "admin": "#c0392b",
            "editor": "#e67e22",
            "reader": "#27ae60",
        }
        color: str = colors.get(obj.role, "#7f8c8d")
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:3px;font-size:11px">{}</span>',
            color,
            obj.get_role_display(),
        )

    display_role_badge.short_description = _("Rol")

    actions: list[str] = ["ban_users", "unban_users", "promote_to_editor"]

    @admin.action(description=_("Banear usuarios seleccionados"))
    def ban_users(self, request, queryset) -> None:
        count: int = queryset.update(is_banned=True, is_active=False)
        self.message_user(request, f"{count} usuario(s) baneado(s).")

    @admin.action(description=_("Desbanear usuarios seleccionados"))
    def unban_users(self, request, queryset) -> None:
        count: int = queryset.update(is_banned=False, is_active=True)
        self.message_user(request, f"{count} usuario(s) desbaneado(s).")

    @admin.action(description=_("Promover a Editor"))
    def promote_to_editor(self, request, queryset) -> None:
        count: int = queryset.update(role="editor")
        self.message_user(request, f"{count} usuario(s) promovido(s) a Editor.")
