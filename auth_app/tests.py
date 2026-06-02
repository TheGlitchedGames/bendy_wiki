"""
Tests para auth_app
Cubre: modelos, formularios y vistas de autenticación.
"""

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

User = get_user_model()


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_user(username="testuser", password="SecurePass123!", role="reader",
              **kwargs):
    return User.objects.create_user(
        username=username,
        email=f"{username}@example.com",
        password=password,
        role=role,
        **kwargs,
    )


# ══════════════════════════════════════════════════════════════════════════════
# TEST 1 — Un usuario baneado no puede iniciar sesión
# El BannedUserMixin y el formulario de login deben bloquearlo en ambas capas.
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.django_db
def test_banned_user_cannot_login():
    from django.test import RequestFactory
    from auth_app.forms import BendyLoginForm

    user = make_user(username="banned", password="Pass1234!")
    user.is_banned = True
    user.save()

    # Capa de formulario: debe producir error de validación
    factory = RequestFactory()
    request = factory.post("/auth/login/")
    form = BendyLoginForm(
        request=request,
        data={"username": "banned", "password": "Pass1234!"},
    )
    form.is_valid()
    assert "__all__" in form.errors

    # Capa de vista: debe quedarse en la página de login (200, no redirección)
    client = Client()
    response = client.post(reverse("auth:login"), {
        "username": "banned",
        "password": "Pass1234!",
    })
    assert response.status_code == 200


# ══════════════════════════════════════════════════════════════════════════════
# TEST 2 — El registro crea el usuario con los datos correctos y redirige
# Flujo completo de alta: POST válido → usuario en BD → redirect al índice.
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.django_db
def test_register_creates_user_and_redirects():
    client = Client()
    response = client.post(reverse("auth:register"), {
        "username": "brandnew",
        "email": "brandnew@example.com",
        "password1": "Str0ng!Pass99",
        "password2": "Str0ng!Pass99",
        "favorite_game": "batdr",
        "terms": True,
    })
    assert response.status_code == 302
    assert response.url == reverse("bendy:index")
    user = User.objects.get(username="brandnew")
    assert user.favorite_game == "batdr"


# ══════════════════════════════════════════════════════════════════════════════
# TEST 3 — El formulario de registro rechaza nombres de usuario reservados
#          y correos duplicados
# Protege la integridad de los datos desde la capa de validación.
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.django_db
def test_register_form_rejects_reserved_usernames_and_duplicate_email():
    from auth_app.forms import BendyRegisterForm

    base = {
        "password1": "Str0ng!Pass",
        "password2": "Str0ng!Pass",
        "favorite_game": "batim",
        "terms": True,
    }

    # Nombres reservados
    for reserved in ("admin", "root", "bendy", "system"):
        form = BendyRegisterForm(data={
            **base,
            "username": reserved,
            "email": f"{reserved}@example.com",
        })
        assert not form.is_valid(), f"'{reserved}' debería ser rechazado"
        assert "username" in form.errors

    # Email duplicado
    make_user(username="existing", email="taken@example.com")
    form = BendyRegisterForm(data={
        **base,
        "username": "newuser",
        "email": "taken@example.com",
    })
    assert not form.is_valid()
    assert "email" in form.errors


# ══════════════════════════════════════════════════════════════════════════════
# TEST 4 — Eliminar cuenta requiere confirmación exacta del nombre de usuario
# Evita borrados accidentales; la acción es irreversible.
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.django_db
def test_delete_account_requires_exact_username_confirmation():
    client = Client()
    user = make_user(username="deletecandidate", password="Del3te!")
    client.force_login(user)
    url = reverse("auth:delete_account")

    # Confirmación incorrecta → cuenta intacta
    response = client.post(url, {"confirm_username": "wrong_name"})
    assert response.status_code == 200
    assert User.objects.filter(username="deletecandidate").exists()

    # Confirmación correcta → cuenta eliminada y redirige al índice
    response = client.post(url, {"confirm_username": "deletecandidate"})
    assert response.url == reverse("bendy:index")
    assert not User.objects.filter(username="deletecandidate").exists()


# ══════════════════════════════════════════════════════════════════════════════
# TEST 5 — La lista de usuarios excluye baneados y está ordenada por ink_points
# Comprueba filtrado y ordenación que afectan directamente a la pantalla de ranking.
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.django_db
def test_user_list_excludes_banned_and_orders_by_ink_points():
    client = Client()
    viewer = make_user(username="viewer")
    make_user(username="rich", ink_points=999)
    make_user(username="poor", ink_points=1)
    banned = make_user(username="banned_one")
    banned.is_banned = True
    banned.save()

    client.force_login(viewer)
    response = client.get(reverse("auth:user_list"))
    assert response.status_code == 200

    usernames = [u.username for u in response.context["users"]]
    assert "banned_one" not in usernames
    assert "rich" in usernames

    points = [u.ink_points for u in response.context["users"]]
    assert points == sorted(points, reverse=True)
