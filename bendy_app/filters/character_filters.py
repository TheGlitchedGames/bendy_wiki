import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from bendy_app.models import Character, Game


class CharacterFilter(django_filters.FilterSet):
    class CharacterFilter(django_filters.FilterSet):
        name = django_filters.CharFilter(
            lookup_expr="icontains",
            label=_("Nombre"),
            widget=forms.TextInput,  # ✅ class only
            extra={"widget": forms.TextInput(attrs={
                "class": "bendy-input",
                "placeholder": "Buscar personaje..."
            })}
        )

        primary_game = django_filters.ModelChoiceFilter(
            queryset=Game.objects.all(),
            label=_("Juego"),
            empty_label=_("Todos los juegos"),
            widget=forms.Select,
            extra={"widget": forms.Select(attrs={"class": "bendy-select"})}
        )

        role = django_filters.ChoiceFilter(
            choices=[("", _("Todos los roles"))] + Character.ROLE_CHOICES,
            label=_("Rol"),
            widget=forms.Select,
            extra={"widget": forms.Select(attrs={"class": "bendy-select"})}
        )

        character_type = django_filters.ChoiceFilter(
            choices=[("", _("Todos los tipos"))] + Character.TYPE_CHOICES,
            label=_("Tipo"),
            widget=forms.Select,
            extra={"widget": forms.Select(attrs={"class": "bendy-select"})}
        )

        is_playable = django_filters.BooleanFilter(
            label=_("Solo jugables"),
            widget=forms.CheckboxInput,
            extra={"widget": forms.CheckboxInput(
                attrs={"class": "bendy-checkbox"})}
        )

        is_alive_end = django_filters.BooleanFilter(
            label=_("Sobrevive al final"),
            widget=forms.CheckboxInput,
            extra={"widget": forms.CheckboxInput(
                attrs={"class": "bendy-checkbox"})}
        )

        ordering = django_filters.OrderingFilter(
            fields=(
                ("name", "name"),
                ("primary_game", "primary_game"),
                ("role", "role"),
            ),
            label=_("Ordenar por"),
            widget=forms.Select,
            extra={"widget": forms.Select(attrs={"class": "bendy-select"})}
        )

    class Meta:
        model = Character
        fields = ["name", "primary_game", "role", "character_type", "is_playable", "is_alive_end"]