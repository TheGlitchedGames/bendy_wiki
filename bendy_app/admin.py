from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import BendyUser, Character, Chapter


# ── BendyUser ─────────────────────────────────────────────────────────────────

@admin.register(BendyUser)
class BendyUserAdmin(UserAdmin):
    list_display: tuple[str, ...] = (
        "username", "email", "display_role_badge", "favorite_game",
        "ink_points", "is_banned", "is_active", "joined_at",
    )
    list_filter: tuple[str, ...] = ("role", "favorite_game", "is_banned",
                                    "is_active",
                                    "is_staff")
    search_fields: tuple[str, ...] = ("username", "email", "first_name",
                                      "last_name")
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
            '<span style="background:{};color:white;padding:2px 8px;'
            'border-radius:3px;font-size:11px">{}</span>',
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


# ── Character ─────────────────────────────────────────────────────────────────

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display: tuple[str, ...] = (
        "name", "display_game_badge", "display_role_badge", "character_type",
        "human_counterpart", "is_playable", "is_alive_end",
    )
    list_filter: tuple[str, ...] = (
        "game", "role", "character_type", "is_playable", "is_alive_end",
    )
    search_fields: tuple[str, ...] = (
        "name", "alias", "human_counterpart", "real_world_inspiration",
    )
    ordering: tuple[str, ...] = ("game", "name")
    prepopulated_fields: dict[str, tuple[str, ...]] = {"slug": ("name",)}
    readonly_fields: tuple[str, ...] = ("created_at", "updated_at")
    list_per_page: int = 25

    fieldsets = (
        (_("Identificación"), {
            "fields": ("name", "slug", "alias", "image"),
        }),
        (_("Clasificación"), {
            "fields": ("game", "role", "character_type"),
        }),
        (_("Descripción"), {
            "fields": ("description", "appearance", "personality",
                       "background"),
            "classes": ("collapse",),
        }),
        (_("Conexiones"), {
            "fields": (
                "human_counterpart", "real_world_inspiration",
                "voice_actor_batim", "voice_actor_batdr",
            ),
            "classes": ("collapse",),
        }),
        (_("Narrativa"), {
            "fields": (
                "appears_in_chapters", "iconic_quote", "quote_source",
                "is_alive_end", "is_playable",
            ),
            "classes": ("collapse",),
        }),
        (_("Metadatos"), {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    def display_game_badge(self, obj: Character) -> str:
        colors: dict[str, str] = {
            "batim": "#1a1a2e",
            "batdr": "#4a0e0e",
            "both": "#1a3a1a",
        }
        color: str = colors.get(obj.game, "#555")
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;'
            'border-radius:3px;font-size:11px;font-weight:bold">{}</span>',
            color,
            obj.get_game_display(),
        )

    display_game_badge.short_description = _("Juego")

    def display_role_badge(self, obj: Character) -> str:
        colors: dict[str, str] = {
            "protagonist": "#27ae60",
            "antagonist": "#c0392b",
            "secondary_antagonist": "#e67e22",
            "ally": "#2980b9",
            "neutral": "#7f8c8d",
            "mentioned": "#95a5a6",
        }
        color: str = colors.get(obj.role, "#7f8c8d")
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;'
            'border-radius:3px;font-size:11px">{}</span>',
            color,
            obj.get_role_display(),
        )

    display_role_badge.short_description = _("Rol")

    actions: list[str] = ["mark_batim", "mark_batdr", "mark_both"]

    @admin.action(description=_("Marcar como personajes de BATIM"))
    def mark_batim(self, request, queryset) -> None:
        count: int = queryset.update(game="batim")
        self.message_user(request,
                          f"{count} personaje(s) marcado(s) como BATIM.")

    @admin.action(description=_("Marcar como personajes de BATDR"))
    def mark_batdr(self, request, queryset) -> None:
        count: int = queryset.update(game="batdr")
        self.message_user(request,
                          f"{count} personaje(s) marcado(s) como BATDR.")

    @admin.action(description=_("Marcar como personajes de ambos juegos"))
    def mark_both(self, request, queryset) -> None:
        count: int = queryset.update(game="both")
        self.message_user(request,
                          f"{count} personaje(s) marcado(s) como Ambos.")


# ── Chapter ───────────────────────────────────────────────────────────────────

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display: tuple[str, ...] = (
        "display_game_badge", "number", "title", "art_theme",
        "release_date", "difficulty", "has_boss_fight",
        "has_stealth_sections", "approximate_duration_minutes",
    )
    list_filter: tuple[str, ...] = (
        "game", "art_theme", "difficulty",
        "has_boss_fight", "has_stealth_sections", "has_puzzle_sections",
    )
    search_fields: tuple[str, ...] = (
        "title", "synopsis", "main_villain", "boss_name",
        "new_characters_introduced",
    )
    ordering: tuple[str, ...] = ("game", "number")
    prepopulated_fields: dict[str, tuple[str, ...]] = {"slug": ("title",)}
    readonly_fields: tuple[str, ...] = ("created_at", "updated_at")
    list_per_page: int = 20
    date_hierarchy: str = "release_date"

    fieldsets = (
        (_("Identificación"), {
            "fields": ("game", "number", "title", "slug"),
        }),
        (_("Arte y temática"), {
            "fields": ("art_theme", "art_theme_explanation"),
        }),
        (_("Publicación"), {
            "fields": ("release_date", "last_update_date"),
        }),
        (_("Historia"), {
            "fields": (
                "synopsis", "aesthetics", "setting_description",
                "protagonist", "main_villain",
                "new_characters_introduced", "key_events", "lore_revelations",
            ),
            "classes": ("collapse",),
        }),
        (_("Gameplay"), {
            "fields": (
                "difficulty", "approximate_duration_minutes",
                "has_boss_fight", "boss_name",
                "has_stealth_sections", "has_puzzle_sections",
            ),
        }),
        (_("Música"), {
            "fields": ("composer", "soundtrack_notes"),
            "classes": ("collapse",),
        }),
        (_("Imágenes"), {
            "fields": ("cover_image", "background_image"),
            "classes": ("collapse",),
        }),
        (_("Comunidad"), {
            "fields": ("trivia", "reception_notes"),
            "classes": ("collapse",),
        }),
        (_("Metadatos"), {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    def display_game_badge(self, obj: Chapter) -> str:
        colors: dict[str, str] = {
            "batim": "#1a1a2e",
            "batdr": "#4a0e0e",
        }
        color: str = colors.get(obj.game, "#555")
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;'
            'border-radius:3px;font-size:11px;font-weight:bold">{}</span>',
            color,
            obj.get_game_display(),
        )

    display_game_badge.short_description = _("Juego")

    actions: list[str] = ["mark_batim", "mark_batdr"]

    @admin.action(description=_("Mover a BATIM"))
    def mark_batim(self, request, queryset) -> None:
        count: int = queryset.update(game="batim")
        self.message_user(request, f"{count} capítulo(s) movido(s) a BATIM.")

    @admin.action(description=_("Mover a BATDR"))
    def mark_batdr(self, request, queryset) -> None:
        count: int = queryset.update(game="batdr")
        self.message_user(request, f"{count} capítulo(s) movido(s) a BATDR.")
