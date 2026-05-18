from django.db import models
from django.utils.translation import gettext_lazy as _


class Character(models.Model):
    GAME_CHOICES = [
        ("batim", "Bendy and the Ink Machine"),
        ("batdr", "Bendy and the Dark Revival"),
        ("both", "Ambos")
    ]

    ROLE_CHOICES = [
        ("protagonist", "Protagonista"),
        ("antagonist", "Antagonista"),
        ("secondary_antagonist", "Antagonista secundario"),
        ("ally", "Aliado"),
        ("neutral", "Neutral"),
        ("mentioned", "Solo mencionado")
    ]

    TYPE_CHOICES = [
        ("human", "Humano"),
        ("toon", "Personaje de dibujos animados"),
        ("ink_monster", "Monstruo de tinta"),
        ("hybrid", "Híbrido"),
        ("spirit", "Espíritu/Alma")
    ]

    # Identificación
    name = models.CharField(
        verbose_name=_('Nombre'),
        max_length=100
    )
    slug = models.SlugField(
        verbose_name=_('Slug'),
        unique=True,
        help_text=_('Identificador único para URLs (ej: bendy-the-dancing-demon)')
    )
    alias = models.CharField(
        verbose_name=_('Alias'),
        max_length=200,
        blank=True,
        help_text=_('Otros nombre por los que se conoce al personaje')
    )

    # Clasificación
    game = models.CharField(
        verbose_name=_('Juego'),
        max_length=10,
        choices=GAME_CHOICES,
        default='batim',
        help_text=_('En qué juego(s) aparece este personaje')
    )
    role = models.CharField