from typing import Any

import sweetify
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, \
    UpdateView, DeleteView

from bendy_app.filters import CharacterFilter
from bendy_app.filters.game_chapter_filters import GameFilter, ChapterFilter
from bendy_app.forms import CharacterForm, GameForm, ChapterForm
from bendy_app.mixins import BreadcrumbMixin, EditorRequiredMixin
from bendy_app.models import Game, Character, Chapter


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

# ══════════════════════════════════════════════════════════════════════════════
# GAME VIEWS
# ══════════════════════════════════════════════════════════════════════════════

class GameListView(BreadcrumbMixin, ListView):
    """
    Lista de juegos con filtrado y estadísticas.
    URL: /games/
    """

    model = Game
    template_name = "games/game_list.html"
    context_object_name = "games"
    paginate_by = 12
    breadcrumbs = [
        {"label": "Inicio", "url": "/"},
        {"label": "Juegos", "url": None},
    ]

    def get_queryset(self):
        qs = Game.objects.all()
        self.filterset = GameFilter(self.request.GET, queryset=qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filterset"] = self.filterset
        ctx["total_count"] = self.filterset.qs.count()

        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["has_active_filters"] = any(v for v in params.values())
        return ctx


class GameDetailView(BreadcrumbMixin, DetailView):
    """
    Detalle de un juego con sus capítulos y personajes.
    URL: /games/<slug>/
    """

    model = Game
    template_name = "games/game_detail.html"
    context_object_name = "game"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_breadcrumbs(self):
        return [
            {"label": "Inicio", "url": "/"},
            {"label": "Juegos", "url": reverse_lazy("bendy:game_list")},
            {"label": self.object.title, "url": None},
        ]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        game: Game = self.object

        ctx["chapters"] = game.chapters.order_by("number")
        ctx["characters"] = (
            Character.objects.filter(primary_game=game)
            .order_by("name")[:12]
        )
        ctx["total_characters"] = Character.objects.filter(
            primary_game=game).count()
        ctx["total_chapters"] = game.chapters.count()

        # Color temático por juego
        ctx["game_color"] = {
            "batim": "#1a1a2e",
            "batdr": "#4a0e0e",
        }.get(game.key, "#2c1a0a")
        ctx["game_accent"] = {
            "batim": "#aab0e0",
            "batdr": "#e08080",
        }.get(game.key, "#d4aa47")

        return ctx


class GameCreateView(EditorRequiredMixin, BreadcrumbMixin, SuccessMessageMixin,
                     CreateView):
    """
    Creación de un juego. Solo accesible para editores y admins.
    URL: /games/crear/
    """

    model = Game
    form_class = GameForm
    template_name = "games/game_form.html"
    success_message = "¡Juego «%(title)s» añadido al archivo del Estudio!"
    breadcrumbs = [
        {"label": "Inicio", "url": "/"},
        {"label": "Juegos", "url": reverse_lazy("bendy:game_list")},
        {"label": "Nuevo juego", "url": None},
    ]

    def get_success_url(self):
        return reverse_lazy("bendy:game_detail",
                            kwargs={"slug": self.object.slug})

    def form_invalid(self, form):
        sweetify.error(
            self.request,
            "Error al crear el juego",
            text="Revisa los campos marcados en rojo.",
            timer=4000,
        )
        return super().form_invalid(form)


class GameUpdateView(EditorRequiredMixin, BreadcrumbMixin, SuccessMessageMixin,
                     UpdateView):
    """
    Edición de un juego existente.
    URL: /games/<slug>/editar/
    """

    model = Game
    form_class = GameForm
    template_name = "games/game_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_message = "Juego «%(title)s» actualizado correctamente."

    def get_breadcrumbs(self):
        return [
            {"label": "Inicio", "url": "/"},
            {"label": "Juegos", "url": reverse_lazy("bendy:game_list")},
            {"label": self.object.title,
             "url": reverse_lazy("bendy:game_detail",
                                 kwargs={"slug": self.object.slug})},
            {"label": "Editar", "url": None},
        ]

    def get_success_url(self):
        return reverse_lazy("bendy:game_detail",
                            kwargs={"slug": self.object.slug})

    def form_invalid(self, form):
        sweetify.error(
            self.request,
            "Error al actualizar el juego",
            text="Revisa los campos marcados en rojo.",
            timer=4000,
        )
        return super().form_invalid(form)


class GameDeleteView(EditorRequiredMixin, BreadcrumbMixin, DeleteView):
    """
    Eliminación de un juego con confirmación.
    URL: /games/<slug>/eliminar/
    """

    model = Game
    template_name = "games/game_confirm_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("bendy:game_list")

    def get_breadcrumbs(self) -> list[dict[str, Any]]:
        return [
            {"label": "Inicio", "url": "/"},
            {"label": "Juegos", "url": reverse_lazy("bendy:game_list")},
            {"label": self.object.title,
             "url": reverse_lazy("bendy:game_detail",
                                 kwargs={"slug": self.object.slug})},
            {"label": "Eliminar", "url": None},
        ]

    def post(self, request, *args, **kwargs):
        title = self.get_object().title
        response = super().post(request, *args, **kwargs)
        sweetify.success(
            request,
            "Juego eliminado",
            text=f"«{title}» ha sido borrado del archivo.",
            timer=4000,
        )
        return response


# ══════════════════════════════════════════════════════════════════════════════
# CHAPTER VIEWS
# ══════════════════════════════════════════════════════════════════════════════

class ChapterListView(BreadcrumbMixin, ListView):
    """
    Lista paginada de capítulos con filtrado.
    URL: /chapters/
    """

    model = Chapter
    template_name = "chapters/chapter_list.html"
    context_object_name = "chapters"
    paginate_by = 10
    breadcrumbs = [
        {"label": "Inicio", "url": "/"},
        {"label": "Capítulos", "url": None},
    ]

    def get_queryset(self):
        qs = Chapter.objects.select_related("game").order_by("game", "number")
        self.filterset = ChapterFilter(self.request.GET, queryset=qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filterset"] = self.filterset
        ctx["total_count"] = self.filterset.qs.count()
        ctx["active_filters"] = self._get_active_filters()

        ctx["batim_count"] = Chapter.objects.filter(game__key="batim").count()
        ctx["batdr_count"] = Chapter.objects.filter(game__key="batdr").count()

        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["has_active_filters"] = any(v for v in params.values())
        return ctx

    def _get_active_filters(self) -> list[dict]:
        labels = {
            "title": "Título",
            "game": "Juego",
            "art_theme": "Tema",
            "difficulty": "Dificultad",
            "has_boss_fight": "Con jefe",
            "has_stealth_sections": "Sigilo",
            "has_puzzle_sections": "Puzles",
            "ordering": "Orden",
        }
        return [
            {"key": k, "label": l, "value": self.request.GET.get(k, "")}
            for k, l in labels.items()
            if self.request.GET.get(k, "")
        ]


class ChapterDetailView(BreadcrumbMixin, DetailView):
    """
    Detalle de un capítulo.
    URL: /chapters/<slug>/
    """

    model = Chapter
    template_name = "chapters/chapter_detail.html"
    context_object_name = "chapter"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_breadcrumbs(self):
        return [
            {"label": "Inicio", "url": "/"},
            {"label": "Capítulos", "url": reverse_lazy("bendy:chapter_list")},
            {"label": self.object.full_title, "url": None},
        ]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        chapter: Chapter = self.object

        # Navegación entre capítulos del mismo juego
        siblings = Chapter.objects.filter(game=chapter.game).order_by("number")
        numbers = list(siblings.values_list("number", flat=True))
        idx = numbers.index(chapter.number)
        ctx["prev_chapter"] = siblings[idx - 1] if idx > 0 else None
        ctx["next_chapter"] = siblings[idx + 1] if idx < len(
            numbers) - 1 else None

        ctx["game_color"] = {
            "batim": "#1a1a2e",
            "batdr": "#4a0e0e",
        }.get(chapter.game.key, "#2c1a0a")
        ctx["game_accent"] = {
            "batim": "#aab0e0",
            "batdr": "#e08080",
        }.get(chapter.game.key, "#d4aa47")

        ctx["difficulty_color"] = {
            "introductory": "#27ae60",
            "easy": "#2ecc71",
            "medium": "#f39c12",
            "hard": "#e67e22",
            "boss_heavy": "#c0392b",
        }.get(chapter.difficulty, "#7f8c8d")

        return ctx


class ChapterCreateView(EditorRequiredMixin, BreadcrumbMixin,
                        SuccessMessageMixin, CreateView):
    """
    Creación de un capítulo. Solo accesible para editores y admins.
    URL: /chapters/crear/
    """

    model = Chapter
    form_class = ChapterForm
    template_name = "chapters/chapter_form.html"
    success_message = "¡Capítulo «%(title)s» creado con éxito en el archivo del Estudio!"
    breadcrumbs = [
        {"label": "Inicio", "url": "/"},
        {"label": "Capítulos", "url": reverse_lazy("bendy:chapter_list")},
        {"label": "Nuevo capítulo", "url": None},
    ]

    def get_success_url(self):
        return reverse_lazy("bendy:chapter_detail",
                            kwargs={"slug": self.object.slug})

    def form_invalid(self, form):
        sweetify.error(
            self.request,
            "Error al crear el capítulo",
            text="Revisa los campos marcados en rojo.",
            timer=4000,
        )
        return super().form_invalid(form)


class ChapterUpdateView(EditorRequiredMixin, BreadcrumbMixin,
                        SuccessMessageMixin, UpdateView):
    """
    Edición de un capítulo existente.
    URL: /chapters/<slug>/editar/
    """

    model = Chapter
    form_class = ChapterForm
    template_name = "chapters/chapter_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_message = "Capítulo «%(title)s» actualizado correctamente."

    def get_breadcrumbs(self):
        return [
            {"label": "Inicio", "url": "/"},
            {"label": "Capítulos", "url": reverse_lazy("bendy:chapter_list")},
            {"label": self.object.full_title,
             "url": reverse_lazy("bendy:chapter_detail",
                                 kwargs={"slug": self.object.slug})},
            {"label": "Editar", "url": None},
        ]

    def get_success_url(self):
        return reverse_lazy("bendy:chapter_detail",
                            kwargs={"slug": self.object.slug})

    def form_invalid(self, form):
        sweetify.error(
            self.request,
            "Error al actualizar el capítulo",
            text="Revisa los campos marcados en rojo.",
            timer=4000,
        )
        return super().form_invalid(form)


class ChapterDeleteView(EditorRequiredMixin, BreadcrumbMixin, DeleteView):
    """
    Eliminación de un capítulo con confirmación.
    URL: /chapters/<slug>/eliminar/
    """

    model = Chapter
    template_name = "chapters/chapter_confirm_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("bendy:chapter_list")

    def get_breadcrumbs(self) -> list[dict[str, Any]]:
        return [
            {"label": "Inicio", "url": "/"},
            {"label": "Capítulos", "url": reverse_lazy("bendy:chapter_list")},
            {"label": self.object.full_title,
             "url": reverse_lazy("bendy:chapter_detail",
                                 kwargs={"slug": self.object.slug})},
            {"label": "Eliminar", "url": None},
        ]

    def post(self, request, *args, **kwargs):
        title = self.get_object().full_title
        response = super().post(request, *args, **kwargs)
        sweetify.success(
            request,
            "Capítulo eliminado",
            text=f"«{title}» ha sido borrado del archivo.",
            timer=4000,
        )
        return response