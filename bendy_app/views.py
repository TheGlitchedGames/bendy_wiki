from typing import Any

import sweetify
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, \
    UpdateView, DeleteView

from bendy_app.filters import CharacterFilter
from bendy_app.forms import CharacterForm
from bendy_app.mixins import BreadcrumbMixin, EditorRequiredMixin
from bendy_app.models import Game, Character


# Home

class HomeView(TemplateView):
    """Página de inicio con estadísticas y últimos contribuidores."""

    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        from auth_app.models import BendyUser

        context = super().get_context_data(**kwargs)
        context["top_contributors"] = BendyUser.objects.filter(
            is_active=True, is_banned=False
        ).order_by("-ink_points")[:5]
        context["recent_users"] = BendyUser.objects.filter(
            is_active=True
        ).order_by("-joined_at")[:5]
        context["games"] = Game.objects.all()
        return context


# Character - List

class CharacterListView(BreadcrumbMixin, ListView):
    """
    Lista paginada de personajes con filtrado mediante django-filter.
    URL: /characters/
    """

    model = Character
    template_name = "characters/character_list.html"
    context_object_name = "characters"
    paginate_by = 12
    breadcrumbs = [
        {"label": "Inicio", "url": "/"},
        {"label": "Personajes", "url": None}
    ]

    def get_queryset(self):
        qs = Character.objects.select_related("primary_game").all()
        self.filterset = CharacterFilter(self.request.GET, queryset=qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filterset"] = self.filterset
        ctx["total_count"] = self.filterset.qs.count()
        ctx["active_filters"] = self._get_active_filters()

        # Contadores por juego para las pills del header
        ctx["batim_count"] = Character.objects.filter(
            primary_game__key="batim"
        ).count()
        ctx["batdr_count"] = Character.objects.filter(
            primary_game__key="batdr"
        ).count()

        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["has_active_filters"] = any(v for v in params.values())
        return ctx

    def _get_active_filters(self) -> list[dict]:
        labels = {
            "name": "Nombre",
            "primary_game": 'Juego',
            'role': 'Rol',
            'character_type': 'Tipo',
            'is_playable': 'Jugable',
            'is_alive_end': 'Sobrevive',
            'ordering': 'Orden'
        }
        return [
            {"key": k, "label": l, "value": self.request.GET.get(k, "")}
            for k, l in labels.items()
            if self.request.GET.get(k, "")
        ]


class CharacterDetailView(BreadcrumbMixin, DetailView):
    """
    Detalle de un personaje.
    URL: /characters/<slug>/
    """

    model = Character
    template_name = "characters/character_detail.html"
    context_object_name = "character"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_breadcrumbs(self):
        return [
            {"label": "Inicio", "url": "/"},
            {"label": "Personajes",
             "url": reverse_lazy("bendy:character_list")},
            {"label": self.object.name, "url": None}
        ]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        character: Character = self.object

        ctx["related_characters"] = (
            Character.objects.filter(primary_game=character.primary_game)
            .exclude(pk=character.pk)
            .order_by("name")[:6]
        )
        ctx["role_color"] = {
            "protagonist": "#27ae60",
            "antagonist": "#c0392b",
            "secondary_antagonist": "#e67e22",
            "ally": "#2980b9",
            "neutral": "#7f8c8d",
            "mentioned": "#95a5a6",
        }.get(character.role, "#7f8c8d")
        ctx["game_color"] = {
            "batim": "#1a1a2e",
            "batdr": "#4a0e0e",
        }.get(character.primary_game.key, "#555")
        return ctx


# Character - Create

class CharacterCreateView(EditorRequiredMixin, BreadcrumbMixin,
                          SuccessMessageMixin, CreateView):
    """
    Creació de un personaje. Solo accesible para editores y admins.
    Usa SuccessMessageMixin para mostrar un toast tras guardar.
    URL: /characters/crear/
    """

    model = Character
    form_class = CharacterForm
    template_name = "characters/character_form.html"
    success_message = ("¡Personaje «%(name)s» creado con éxito en el archivo "
                       "del Estudio!")
    breadcrumbs = [
        {"label": "Inicio", "url": "/"},
        {"label": "Personajes", "url": reverse_lazy("bendy:character_list")},
        {"label": "Nuevo personaje", "url": None}
    ]

    def get_success_url(self):
        return reverse_lazy("bendy:character_detail", kwargs={'slug':
                                                                  self.object.slug})

    def form_invalid(self, form):
        sweetify.error(
            self.request,
            'Error al crear el personaje',
            text='Revisa los campos marcados en rojo.',
            timer=4000
        )
        return super().form_invalid(form)


# Character - Update

class CharacterUpdateView(EditorRequiredMixin, BreadcrumbMixin,
                          SuccessMessageMixin, UpdateView):
    """
    Edición de un personaje existente,
    URL: /characters/<slug>/editar/
    """

    model = Character
    form_class = CharacterForm
    template_name = "characters/character_form.html"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_message = 'Personaje «%(name)s» actualizado correctamente.'

    def get_breadcrumbs(self):
        return [
            {"label": "Inicio", "url": "/"},
            {"label": "Personajes",
             "url": reverse_lazy("bendy:character_list")},
            {"label": self.object.name,
             "url": reverse_lazy("bendy:character_detail",
                                 kwargs={"slug": self.object.slug})},
            {"label": "Editar", "url": None}
        ]

    def get_success_url(self):
        return reverse_lazy('bendy:character_detail', kwargs={'slug':
                                                                  self.object.slug})

    def form_invalid(self, form):
        sweetify.error(
            self.request,
            "Error al actualizar",
            text="Revisa los campos marcados en rojo.",
            timer=4000
        )
        return super().form_invalid(form)


# Character - Delete

class CharacterDeleteView(EditorRequiredMixin, BreadcrumbMixin, DeleteView):
    """
    Eliminación de un personaje con confirmación.
    URL: /characters/<slug>/eliminar/
    """

    model = Character
    template_name = 'characters/character_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('bendy:character_list')

    def get_breadcrumbs(self) -> list[dict[str, Any]]:
        return [
            {"label": "Inicio", "url": "/"},
            {"label": "Personajes",
             "url": reverse_lazy("bendy:character_list")},
            {"label": self.object.name,
             "url": reverse_lazy("bendy:character_detail",
                                 kwargs={"slug": self.object.slug})},
            {"label": "Eliminar", "url": None}
        ]

    def post(self, request, *args, **kwargs):
        name = self.get_object().name
        response = super().post(request, *args, **kwargs)
        sweetify.success(
            request,
            'Personaje eliminado',
            text=f"«{name}» ha sido borrado del archivo.",
            timer=4000
        )
        return response
