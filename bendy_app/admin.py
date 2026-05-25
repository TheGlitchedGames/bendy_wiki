from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Character, Chapter, Game


# ── Game ──────────────────────────────────────────────────────────────────────

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("key", "title", "release_year")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "key")
    ordering = ("release_year",)


# ── Character ─────────────────────────────────────────────────────────────────

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = (
        "name", "display_game_badge", "display_role_badge",
        "character_type", "human_counterpart", "is_playable", "is_alive_end",
    )
    list_filter = ("primary_game", "role", "character_type", "is_playable", "is_alive_end")
    search_fields = ("name", "alias", "human_counterpart", "real_world_inspiration")
    ordering = ("primary_game", "name")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 25
    filter_horizontal = ("extra_games",)

    fieldsets = (
        (_("Identificación"), {"fields": ("name", "slug", "alias", "image")}),
        (_("Clasificación"), {"fields": ("primary_game", "extra_games", "role", "character_type")}),
        (_("Descripción"), {
            "fields": ("description", "appearance", "personality", "background"),
            "classes": ("collapse",),
        }),
        (_("Conexiones"), {
            "fields": ("human_counterpart", "real_world_inspiration", "voice_actor_batim", "voice_actor_batdr"),
            "classes": ("collapse",),
        }),
        (_("Narrativa"), {
            "fields": ("appears_in_chapters", "iconic_quote", "quote_source", "is_alive_end", "is_playable"),
            "classes": ("collapse",),
        }),
        (_("Metadatos"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def display_game_badge(self, obj: Character) -> str:
        colors = {"batim": "#1a1a2e", "batdr": "#4a0e0e"}
        color = colors.get(obj.primary_game.key, "#555")
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;'
            'border-radius:3px;font-size:11px;font-weight:bold">{}</span>',
            color, obj.primary_game.title,
        )
    display_game_badge.short_description = _("Juego principal")

    def display_role_badge(self, obj: Character) -> str:
        colors = {
            "protagonist": "#27ae60", "antagonist": "#c0392b",
            "secondary_antagonist": "#e67e22", "ally": "#2980b9",
            "neutral": "#7f8c8d", "mentioned": "#95a5a6",
        }
        color = colors.get(obj.role, "#7f8c8d")
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;'
            'border-radius:3px;font-size:11px">{}</span>',
            color, obj.get_role_display(),
        )
    display_role_badge.short_description = _("Rol")


# ── Chapter ───────────────────────────────────────────────────────────────────

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = (
        "display_game_badge", "number", "title", "art_theme",
        "release_date", "difficulty", "has_boss_fight",
        "has_stealth_sections", "approximate_duration_minutes",
    )
    list_filter = ("game", "art_theme", "difficulty", "has_boss_fight", "has_stealth_sections")
    search_fields = ("title", "synopsis", "main_villain", "boss_name", "new_characters_introduced")
    ordering = ("game", "number")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "release_date"

    fieldsets = (
        (_("Identificación"), {"fields": ("game", "number", "title", "slug")}),
        (_("Arte y temática"), {"fields": ("art_theme", "art_theme_explanation")}),
        (_("Publicación"), {"fields": ("release_date", "last_update_date")}),
        (_("Historia"), {
            "fields": ("synopsis", "aesthetics", "setting_description", "protagonist",
                       "main_villain", "new_characters_introduced", "key_events", "lore_revelations"),
            "classes": ("collapse",),
        }),
        (_("Gameplay"), {
            "fields": ("difficulty", "approximate_duration_minutes", "has_boss_fight",
                       "boss_name", "has_stealth_sections", "has_puzzle_sections"),
        }),
        (_("Música"), {"fields": ("composer", "soundtrack_notes"), "classes": ("collapse",)}),
        (_("Imágenes"), {"fields": ("cover_image", "background_image"), "classes": ("collapse",)}),
        (_("Comunidad"), {"fields": ("trivia", "reception_notes"), "classes": ("collapse",)}),
        (_("Metadatos"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def display_game_badge(self, obj: Chapter) -> str:
        colors = {"batim": "#1a1a2e", "batdr": "#4a0e0e"}
        color = colors.get(obj.game.key, "#555")
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;'
            'border-radius:3px;font-size:11px;font-weight:bold">{}</span>',
            color, obj.game.title,
        )
    display_game_badge.short_description = _("Juego")