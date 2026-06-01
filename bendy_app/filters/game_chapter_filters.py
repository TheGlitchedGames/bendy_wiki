import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from bendy_app.models import Game, Chapter


# ── Game Filter ────────────────────────────────────────────────────────────────

class GameFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr="icontains",
        label=_("Título"),
        widget=forms.TextInput(attrs={
            "class": "bendy-input",
            "placeholder": "Buscar juego...",
        }),
    )

    release_year = django_filters.NumberFilter(
        label=_("Año de lanzamiento"),
        widget=forms.NumberInput(attrs={
            "class": "bendy-input",
            "placeholder": "Ej: 2017",
        }),
    )

    ordering = django_filters.OrderingFilter(
        fields=(
            ("release_year", "release_year"),
            ("title", "title"),
        ),
        label=_("Ordenar por"),
        widget=forms.Select(attrs={"class": "bendy-select"}),
    )

    class Meta:
        model = Game
        fields = ["title", "release_year"]


# ── Chapter Filter ─────────────────────────────────────────────────────────────

class ChapterFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr="icontains",
        label=_("Título"),
        widget=forms.TextInput(attrs={
            "class": "bendy-input",
            "placeholder": "Buscar capítulo...",
        }),
    )

    game = django_filters.ModelChoiceFilter(
        queryset=Game.objects.all(),
        label=_("Juego"),
        empty_label=_("Todos los juegos"),
        widget=forms.Select(attrs={"class": "bendy-select"}),
    )

    art_theme = django_filters.ChoiceFilter(
        choices=[("", _("Todos los temas"))] + Chapter.ART_THEME_CHOICES,
        label=_("Tema artístico"),
        widget=forms.Select(attrs={"class": "bendy-select"}),
    )

    difficulty = django_filters.ChoiceFilter(
        choices=[("", _("Todas las dificultades"))] + Chapter.DIFFICULTY_CHOICES,
        label=_("Dificultad"),
        widget=forms.Select(attrs={"class": "bendy-select"}),
    )

    has_boss_fight = django_filters.BooleanFilter(
        label=_("Con jefe"),
        widget=forms.CheckboxInput(attrs={"class": "bendy-checkbox"}),
    )

    has_stealth_sections = django_filters.BooleanFilter(
        label=_("Secciones de sigilo"),
        widget=forms.CheckboxInput(attrs={"class": "bendy-checkbox"}),
    )

    has_puzzle_sections = django_filters.BooleanFilter(
        label=_("Secciones de puzles"),
        widget=forms.CheckboxInput(attrs={"class": "bendy-checkbox"}),
    )

    ordering = django_filters.OrderingFilter(
        fields=(
            ("number", "number"),
            ("title", "title"),
            ("difficulty", "difficulty"),
            ("approximate_duration_minutes", "approximate_duration_minutes"),
        ),
        label=_("Ordenar por"),
        widget=forms.Select(attrs={"class": "bendy-select"}),
    )

    class Meta:
        model = Chapter
        fields = [
            "title", "game", "art_theme", "difficulty",
            "has_boss_fight", "has_stealth_sections", "has_puzzle_sections",
        ]