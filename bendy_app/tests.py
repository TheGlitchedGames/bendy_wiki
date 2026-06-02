"""
Tests para bendy_app
Cubre: modelos Game / Character / Chapter, vistas y la API REST.
"""

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

User = get_user_model()


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_user(username="testuser", password="Pass1234!", role="reader",
              **kwargs):
    return User.objects.create_user(
        username=username,
        email=f"{username}@example.com",
        password=password,
        role=role,
        **kwargs,
    )


def make_editor(username="editor"):
    return make_user(username=username, role="editor")


def make_batim():
    from bendy_app.models import Game
    return Game.objects.create(
        key="batim",
        title="Bendy and the Ink Machine",
        slug="bendy-and-the-ink-machine",
        release_year=2017,
        short_description="Classic ink horror.",
    )


def make_batdr():
    from bendy_app.models import Game
    return Game.objects.create(
        key="batdr",
        title="Bendy and the Dark Revival",
        slug="bendy-and-the-dark-revival",
        release_year=2022,
        short_description="Dark Revival horror.",
    )


def make_character(game, name="Bendy", slug="bendy", role="antagonist",
                   character_type="toon"):
    from bendy_app.models import Character
    return Character.objects.create(
        primary_game=game,
        name=name,
        slug=slug,
        role=role,
        character_type=character_type,
        description="Ink demon mascot.",
    )


def make_chapter(game, number=1, title="Moving Pictures", slug=None,
                 difficulty="introductory"):
    from bendy_app.models import Chapter
    if slug is None:
        slug = f"{game.key}-chapter-{number}-{title.lower().replace(' ', '-')}"
    return Chapter.objects.create(
        game=game,
        number=number,
        title=title,
        slug=slug,
        synopsis="First chapter synopsis.",
        difficulty=difficulty,
    )


# ══════════════════════════════════════════════════════════════════════════════
# TEST 1 — Solo los editores (no lectores, no anónimos) pueden crear juegos
# Verifica el control de acceso del EditorRequiredMixin de una sola vez.
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.django_db
def test_game_create_access_by_role():
    client = Client()
    reader = make_user(username="reader_gc")
    editor = make_editor(username="editor_gc")
    url = reverse("bendy:game_create")

    # Anónimo → redirigido al login
    response = client.get(url)
    assert response.status_code != 200

    # Lector → redirigido al índice
    client.force_login(reader)
    response = client.get(url)
    assert response.url == reverse("bendy:index")

    # Editor → acceso permitido
    client.force_login(editor)
    response = client.get(url)
    assert response.status_code == 200


# ══════════════════════════════════════════════════════════════════════════════
# TEST 2 — La vista de detalle de capítulo expone los capítulos anterior y siguiente
# Prueba la lógica de navegación entre capítulos, clave para la UX.
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.django_db
def test_chapter_detail_prev_next_navigation():
    client = Client()
    game = make_batim()
    ch1 = make_chapter(game, number=1, slug="batim-ch1")
    ch2 = make_chapter(game, number=2, title="The Old Song", slug="batim-ch2")

    response = client.get(
        reverse("bendy:chapter_detail", kwargs={"slug": "batim-ch2"}))
    assert response.status_code == 200
    assert response.context["prev_chapter"] == ch1
    assert response.context["next_chapter"] is None

    response = client.get(
        reverse("bendy:chapter_detail", kwargs={"slug": "batim-ch1"}))
    assert response.context["prev_chapter"] is None


# ══════════════════════════════════════════════════════════════════════════════
# TEST 3 — La API REST de juegos es de solo lectura
# Garantiza que ningún usuario pueda crear/modificar datos a través de la API.
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.django_db
def test_game_api_is_read_only():
    client = Client()
    make_batim()
    user = make_user(username="api_user")

    # GET público funciona
    response = client.get("/api/games/")
    assert response.status_code == 200

    # POST anónimo → 403
    response = client.post("/api/games/", {"key": "batim", "title": "X"})
    assert response.status_code == 403

    # POST autenticado → 405 Method Not Allowed
    client.force_login(user)
    response = client.post(
        "/api/games/",
        {"key": "batdr", "title": "Y"},
        content_type="application/json",
    )
    assert response.status_code == 405


# ══════════════════════════════════════════════════════════════════════════════
# TEST 4 — El formulario de personaje rechaza que el juego principal esté en
#          juegos extra y valida slugs duplicados
# Verifica las dos reglas de negocio más importantes de CharacterForm.
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.django_db
def test_character_form_business_rules():
    from bendy_app.forms import CharacterForm

    game = make_batim()
    base = {
        "name": "Bendy",
        "slug": "bendy-form",
        "primary_game": game.pk,
        "role": "antagonist",
        "character_type": "toon",
        "description": "Ink Demon mascot.",
        "extra_games": [],
    }

    # Juego principal repetido en extra_games → inválido
    form = CharacterForm(data={**base, "extra_games": [game.pk]})
    assert not form.is_valid()
    assert "extra_games" in form.errors

    # Slug duplicado → inválido
    make_character(game, name="Existing", slug="bendy-form")
    form = CharacterForm(data=base)
    assert not form.is_valid()
    assert "slug" in form.errors

    # Formulario limpio → válido
    form = CharacterForm(data={**base, "slug": "bendy-clean"})
    assert form.is_valid(), form.errors


# ══════════════════════════════════════════════════════════════════════════════
# TEST 5 — El comando populate_bendy_data es idempotente y usa update_or_create
# Evita duplicados al ejecutarse varias veces; vital para el fixture del proyecto.
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.django_db
def test_populate_command_is_idempotent():
    from django.core.management import call_command
    from bendy_app.models import Character, Chapter, Game

    call_command("populate_bendy_data", verbosity=0)
    first_game_count = Game.objects.count()
    first_char_count = Character.objects.count()
    first_chap_count = Chapter.objects.count()

    # Segunda ejecución no debe duplicar registros
    call_command("populate_bendy_data", verbosity=0)
    assert Game.objects.count() == first_game_count
    assert Character.objects.count() == first_char_count
    assert Chapter.objects.count() == first_chap_count
    assert first_game_count == 2
