import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from bendy_app.models import Character


class CharacterFilter(django_filters.FilterSet):
    """
    Filtro para el listado de personajes.
    """
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label=_("Nombre"),
        widget=forms.TextInput(attrs={
            "class": "bendy-input",
            "placeholder": "Buscar personaje..."
        })
    )

    game = django_filters.ChoiceFilter(
        choices=[("", "Todos los juegos")] + Character.GAME_CHOICES,
        empty_label=None,
        label=_("Juego"),
        widget=forms.Select(attrs={"class": "bendy-select"})
    )

    role = django_filters.ChoiceFilter(
        choices=[("", "Todos los roles")] + Character.ROLE_CHOICES,
        empty_label=None,
        label=_("Rol"),
        widget=forms.Select(attrs={"class": "bendy-select"})
    )

    character_type = django_filters.ChoiceFilter(
        choices=[("", "Todos los tipos")] + Character.TYPE_CHOICES,
        empty_label=None,
        label=_("Tipo"),
        widget=forms.Select(attrs={"class": "bendy-select"})
    )

    is_playable = django_filters.BooleanFilter(
        label=_("Solo jugables"),
        widget=forms.CheckboxInput(attrs={"class": "bendy-checkbox"})
    )

    is_alive_end = django_filters.BooleanFilter(
        label=_("Sobrevive al final"),
        widget=forms.CheckboxInput(attrs={"class": "bendy-checkbox"})
    )

    ordering = django_filters.OrderingFilter(
        fields=(
        ("name", "name"),
        ("game", "game"),
        ("role", "role")
        ),
        field_labels={
            "name": "Nombre (A→Z)",
            "-name": "Nombre (Z→A)",
            "game": "Juego",
            "role": "Rol"
        },
        label=_("Ordenar por"),
        widget=forms.Select(attrs={"class": "bendy-select"})
    )

    class Meta:
        model = Character
        fields = ["name", "game", "role", "character_type", "is_playable",
                  "is_alive_end"]