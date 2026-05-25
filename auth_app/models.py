from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class BendyUser(AbstractUser):
    """Usuario personalizado para Bendy Wiki."""

    ROLE_CHOICES: list[tuple[str, str]] = [
        ("reader", "Lector"),
        ("editor", "Editor"),
        ("admin", "Administrador"),
    ]

    GAME_CHOICES: list[tuple[str, str]] = [
        ("batim", "Bendy and the Ink Machine"),
        ("batdr", "Bendy and the Dark Revival"),
        ("both", "Ambos"),
    ]

    role: models.CharField = models.CharField(
        verbose_name=_("Rol"),
        max_length=10,
        choices=ROLE_CHOICES,
        default="reader",
    )
    bio: models.TextField = models.TextField(
        verbose_name=_("Biografía"),
        blank=True,
    )
    avatar: models.ImageField = models.ImageField(
        verbose_name=_("Avatar"),
        upload_to="avatars/",
        blank=True,
        null=True,
    )
    favorite_game: models.CharField = models.CharField(
        verbose_name=_("Juego favorito"),
        max_length=10,
        choices=GAME_CHOICES,
        default="both",
    )
    ink_points: models.PositiveIntegerField = models.PositiveIntegerField(
        verbose_name=_("Puntos de tinta"),
        default=0,
    )
    is_banned: models.BooleanField = models.BooleanField(
        verbose_name=_("¿Baneado?"),
        default=False,
    )
    joined_at: models.DateTimeField = models.DateTimeField(
        verbose_name=_("Fecha de registro"),
        auto_now_add=True,
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        verbose_name=_("Última actualización"),
        auto_now=True,
    )

    class Meta:
        verbose_name: str = "Usuario"
        verbose_name_plural: str = "Usuarios"
        ordering: list[str] = ["-joined_at"]

    @property
    def display_name(self) -> str:
        return self.get_full_name() or self.username

    def __str__(self) -> str:
        return f"{self.username} ({self.get_role_display()})"