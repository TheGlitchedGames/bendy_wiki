from django.db import models
from django.utils.translation import gettext_lazy as _


class Character(models.Model):
    GAME_CHOICES: list[tuple[str, str]] = [
        ("batim", "Bendy and the Ink Machine"),
        ("batdr", "Bendy and the Dark Revival"),
        ("both", "Ambos"),
    ]

    ROLE_CHOICES: list[tuple[str, str]] = [
        ("protagonist", "Protagonista"),
        ("antagonist", "Antagonista"),
        ("secondary_antagonist", "Antagonista secundario"),
        ("ally", "Aliado"),
        ("neutral", "Neutral"),
        ("mentioned", "Solo mencionado"),
    ]

    TYPE_CHOICES: list[tuple[str, str]] = [
        ("human", "Humano"),
        ("toon", "Personaje de dibujos animados"),
        ("ink_monster", "Monstruo de tinta"),
        ("hybrid", "Híbrido"),
        ("spirit", "Espíritu/Alma"),
    ]

    # Identificación
    name: models.CharField = models.CharField(
        verbose_name=_("Nombre"),
        max_length=100,
    )
    slug: models.SlugField = models.SlugField(
        verbose_name=_("Slug"),
        unique=True,
        help_text=_(
            "Identificador único para URLs (ej: bendy-the-dancing-demon)"),
    )
    alias: models.CharField = models.CharField(
        verbose_name=_("Alias / Apodo"),
        max_length=200,
        blank=True,
        help_text=_("Otros nombres por los que se conoce al personaje"),
    )

    # Clasificación
    game: models.CharField = models.CharField(
        verbose_name=_("Juego"),
        max_length=10,
        choices=GAME_CHOICES,
        default="batim",
        help_text=_("En qué juego(s) aparece este personaje"),
    )
    role: models.CharField = models.CharField(
        verbose_name=_("Rol"),
        max_length=30,
        choices=ROLE_CHOICES,
        default="secondary_antagonist",
    )
    character_type: models.CharField = models.CharField(
        verbose_name=_("Tipo de personaje"),
        max_length=20,
        choices=TYPE_CHOICES,
        default="toon",
    )

    # Descripción
    description: models.TextField = models.TextField(
        verbose_name=_("Descripción general"),
        help_text=_("Historia y contexto del personaje"),
    )
    appearance: models.TextField = models.TextField(
        verbose_name=_("Apariencia"),
        blank=True,
        help_text=_("Descripción física del personaje"),
    )
    personality: models.TextField = models.TextField(
        verbose_name=_("Personalidad"),
        blank=True,
    )
    background: models.TextField = models.TextField(
        verbose_name=_("Trasfondo"),
        blank=True,
        help_text=_(
            "Historia previa del personaje antes de los eventos del juego"),
    )

    # Relaciones con humanos reales (si aplica)
    human_counterpart: models.CharField = models.CharField(
        verbose_name=_("Contraparte humana"),
        max_length=100,
        blank=True,
        help_text=_(
            "Nombre del humano en el que está basado (ej: Susie Campbell → Twisted Alice)"),
    )
    voice_actor_batim: models.CharField = models.CharField(
        verbose_name=_("Actor de voz (BATIM)"),
        max_length=100,
        blank=True,
    )
    voice_actor_batdr: models.CharField = models.CharField(
        verbose_name=_("Actor de voz (BATDR)"),
        max_length=100,
        blank=True,
    )

    # Inspiración
    real_world_inspiration: models.CharField = models.CharField(
        verbose_name=_("Inspiración del mundo real"),
        max_length=200,
        blank=True,
        help_text=_(
            "En qué personaje real o histórico está basado (ej: Betty Boop → Alice Angel)"),
    )

    # Capítulos en los que aparece
    appears_in_chapters: models.CharField = models.CharField(
        verbose_name=_("Aparece en capítulos"),
        max_length=100,
        blank=True,
        help_text=_("Ej: '1, 2, 3' o 'Todos'"),
    )

    # Cita icónica
    iconic_quote: models.TextField = models.TextField(
        verbose_name=_("Cita icónica"),
        blank=True,
    )
    quote_source: models.CharField = models.CharField(
        verbose_name=_("Fuente de la cita"),
        max_length=100,
        blank=True,
        help_text=_("De qué parte del juego proviene la cita"),
    )

    # Estado
    is_alive_end: models.BooleanField = models.BooleanField(
        verbose_name=_("¿Sobrevive al final?"),
        default=False,
        null=True,
        blank=True,
    )
    is_playable: models.BooleanField = models.BooleanField(
        verbose_name=_("¿Es jugable?"),
        default=False,
    )

    # Imagen
    image: models.ImageField = models.ImageField(
        verbose_name=_("Imagen"),
        upload_to="characters/",
        blank=True,
        null=True,
    )

    # Metadata
    created_at: models.DateTimeField = models.DateTimeField(
        verbose_name=_("Creado el"),
        auto_now_add=True,
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        verbose_name=_("Actualizado el"),
        auto_now=True,
    )

    class Meta:
        verbose_name: str = "Personaje"
        verbose_name_plural: str = "Personajes"
        ordering: list[str] = ["game", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.get_game_display()})"

    @property
    def is_ink_creature(self) -> bool:
        return self.character_type in ("toon", "ink_monster", "hybrid")
