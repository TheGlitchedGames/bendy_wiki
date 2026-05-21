from __future__ import annotations

from django.views.generic import ListView, DetailView
from django.db.models import QuerySet

from ..models import Character
from ..filters import CharacterFilter


class CharacterListView(ListView):
    """
    Lista paginada de personajes con filtrado mediante django-filter.
    URL: /characters/
    """
    model = Character
    template_name = "characters/character_list.html"
    context_object_name = "characters"
    paginate_by = 12

    def get_queryset(self) -> QuerySet[Character]:
        qs = Character.objects.all()
        self.filterset = CharacterFilter(self.request.GET, queryset=qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filterset"] = self.filterset
        ctx["total_count"] = self.filterset.qs.count()
        ctx["active_filters"] = self._get_active_filters()

        # Contadores por juego para las pills del header
        ctx["batim_count"] = Character.objects.filter(game__in=["batim",
                                                                "both"]).count()
        ctx["batdr_count"] = Character.objects.filter(game__in=["batdr",
                                                                "both"]).count()

        # ¿Hay algún filtro activo? (excluyendo page y ordering vacío)
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["has_active_filters"] = any(v for v in params.values())

        return ctx

    def _get_active_filters(self) -> list[dict]:
        """Devuelve lista de filtros activos para mostrar pills eliminables."""
        labels = {
            "name": "Nombre",
            "game": "Juego",
            "role": "Rol",
            "character_type": "Tipo",
            "is_playable": "Jugable",
            "is_alive_end": "Sobrevive",
            "ordering": "Orden"
        }
        active = []
        for key, label in labels.items():
            val = self.request.GET.get(key, "")
            if val:
                active.append({"key": key, "label": label, "value": val})
        return active


class CharacterDetailView(DetailView):
    """
    Detalle de un personaje.
    URL: /characters/<slug>/
    """
    model = Character
    template_name = "characters/character_detail.html"
    context_object_name = "character"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        character: Character = self.object

        # Personajes relacionados: mísmo juego, excluyendo el actual
        ctx["related_characters"] = (
            Character.objects
            .filter(game__in=[character.game, "both"])
            .exclude(pk=character.pk)
            .order_by("name")[:6]
        )

        # Colores de badge según rol
        ctx["role_color"] = {
            "protagonist": "#27ae60",
            "antagonist": "#c0392b",
            "secondary_antagonist": "#e67e22",
            "ally": "#2980b9",
            "neutral": "#7f8c8d",
            "mentioned": "#95a5a6",
        }.get(character.role, "#7f8c8d")

        # Colores de badge según juego
        ctx["game_color"] = {
            "batim": "#1a1a2e",
            "batdr": "#4a0e0e",
            "both": "#1a3a1a",
        }.get(character.game, "#555")

        return ctx