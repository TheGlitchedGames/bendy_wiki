from django.db import models
from django.utils.translation import gettext_lazy as _


class Game(models.Model):
    """Representa cada uno de los juegos del universo de Bendy."""

    GAME_KEY_CHOICES = [
        ("batim", "Bendy and the Ink Machine"),
        ('batdr', 'Bendy and the Dark Revival')
    ]

    key = models.CharField(
        verbose_name=_('Clave'),
        max_length=10,
        choices=GAME_KEY_CHOICES,
        unique=True,
        help_text=_("Identificador corto del juego (batim / batdr)")
    )

    title = models.CharField(
        verbose_name=_("Título"),
        max_length=100
    )
    release_year = models.PositiveSmallIntegerField(
        verbose_name=_('Año de lanzamiento'),
        null=True,
        blank=True
    )
    short_description = models.TextField(
        verbose_name=_('Descripción corta'),
        blank=True
    )
    cover_image = models.ImageField(
        verbose_name=_('Imagen de Portada'),
        upload_to='games/',
        blank=True
    )
    slug = models.SlugField(
        verbose_name=_("Slug"),
        unique=True
    )

    class Meta:
        verbose_name = "Juego"
        verbose_name_plural = "Juegos"
        ordering = ["release_year"]

    def __str__(self):
        return self.title


# ── Character ─────────────────────────────────────────────────────────────────

class Character(models.Model):
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

    # FK al juego principal; un personaje puede aparecer en ambos juegos,
    # por lo que también existe la M2M `extra_games`.
    primary_game: models.ForeignKey = models.ForeignKey(
        Game,
        verbose_name=_("Juego principal"),
        on_delete=models.PROTECT,
        related_name="characters",
        help_text=_("Juego en el que el personaje tiene mayor protagonismo"),
    )
    extra_games: models.ManyToManyField = models.ManyToManyField(
        Game,
        verbose_name=_("También aparece en"),
        related_name="secondary_characters",
        blank=True,
    )

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
    )

    # Clasificación
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
    )
    appearance: models.TextField = models.TextField(
        verbose_name=_("Apariencia"),
        blank=True,
    )
    personality: models.TextField = models.TextField(
        verbose_name=_("Personalidad"),
        blank=True,
    )
    background: models.TextField = models.TextField(
        verbose_name=_("Trasfondo"),
        blank=True,
    )

    # Relaciones con humanos reales
    human_counterpart: models.CharField = models.CharField(
        verbose_name=_("Contraparte humana"),
        max_length=100,
        blank=True,
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
    real_world_inspiration: models.CharField = models.CharField(
        verbose_name=_("Inspiración del mundo real"),
        max_length=200,
        blank=True,
    )

    # Narrativa
    appears_in_chapters: models.CharField = models.CharField(
        verbose_name=_("Aparece en capítulos"),
        max_length=100,
        blank=True,
        help_text=_("Ej: '1, 2, 3' o 'Todos'"),
    )
    iconic_quote: models.TextField = models.TextField(
        verbose_name=_("Cita icónica"),
        blank=True,
    )
    quote_source: models.CharField = models.CharField(
        verbose_name=_("Fuente de la cita"),
        max_length=100,
        blank=True,
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
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name: str = "Personaje"
        verbose_name_plural: str = "Personajes"
        ordering: list[str] = ["primary_game", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.primary_game})"

    @property
    def is_ink_creature(self) -> bool:
        return self.character_type in ("toon", "ink_monster", "hybrid")


# ── Chapter ───────────────────────────────────────────────────────────────────

class Chapter(models.Model):
    ART_THEME_CHOICES: list[tuple[str, str]] = [
        ("animation", "Animación / Dibujo"),
        ("music", "Música"),
        ("literature", "Literatura / Voz y diálogos"),
        ("scenography", "Escenografía / Diseño de producción"),
        ("film", "Séptimo arte / Cine"),
        ("none", "Sin tema artístico explícito"),
    ]

    DIFFICULTY_CHOICES: list[tuple[str, str]] = [
        ("introductory", "Introductorio"),
        ("easy", "Fácil"),
        ("medium", "Medio"),
        ("hard", "Difícil"),
        ("boss_heavy", "Con múltiples jefes"),
    ]

    # FK al juego
    game: models.ForeignKey = models.ForeignKey(
        Game,
        verbose_name=_("Juego"),
        on_delete=models.PROTECT,
        related_name="chapters",
    )

    # Identificación
    number: models.PositiveSmallIntegerField = models.PositiveSmallIntegerField(
        verbose_name=_("Número de capítulo"),
    )
    title: models.CharField = models.CharField(
        verbose_name=_("Título"),
        max_length=150,
    )
    slug: models.SlugField = models.SlugField(
        verbose_name=_("Slug"),
        unique=True,
    )

    # Arte y temática
    art_theme: models.CharField = models.CharField(
        verbose_name=_("Tema artístico"),
        max_length=20,
        choices=ART_THEME_CHOICES,
        default="none",
    )
    art_theme_explanation: models.TextField = models.TextField(
        verbose_name=_("Explicación del tema artístico"),
        blank=True,
    )

    # Fechas
    release_date: models.DateField = models.DateField(null=True, blank=True)
    last_update_date: models.DateField = models.DateField(null=True, blank=True)

    # Sinopsis y estética
    synopsis: models.TextField = models.TextField(verbose_name=_("Sinopsis"))
    aesthetics: models.TextField = models.TextField(blank=True)
    setting_description: models.TextField = models.TextField(blank=True)

    # Gameplay
    difficulty: models.CharField = models.CharField(
        max_length=20, choices=DIFFICULTY_CHOICES, default="medium"
    )
    has_boss_fight: models.BooleanField = models.BooleanField(default=False)
    boss_name: models.CharField = models.CharField(max_length=100, blank=True)
    has_stealth_sections: models.BooleanField = models.BooleanField(
        default=False)
    has_puzzle_sections: models.BooleanField = models.BooleanField(
        default=False)
    approximate_duration_minutes: models.PositiveSmallIntegerField = (
        models.PositiveSmallIntegerField(null=True, blank=True)
    )

    # Narrativa
    protagonist: models.CharField = models.CharField(
        max_length=100, default="Henry Stein"
    )
    main_villain: models.CharField = models.CharField(max_length=100,
                                                      blank=True)
    new_characters_introduced: models.TextField = models.TextField(blank=True)
    key_events: models.TextField = models.TextField(blank=True)
    lore_revelations: models.TextField = models.TextField(blank=True)

    # Música
    soundtrack_notes: models.TextField = models.TextField(blank=True)
    composer: models.CharField = models.CharField(
        max_length=100, blank=True, default="theMeatly"
    )

    # Imágenes
    cover_image: models.ImageField = models.ImageField(
        upload_to="chapters/", blank=True, null=True
    )
    background_image: models.ImageField = models.ImageField(
        upload_to="chapters/backgrounds/", blank=True, null=True
    )

    # Trivia
    trivia: models.TextField = models.TextField(blank=True)
    reception_notes: models.TextField = models.TextField(blank=True)

    # Metadata
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name: str = "Capítulo"
        verbose_name_plural: str = "Capítulos"
        ordering: list[str] = ["game", "number"]
        unique_together: list[tuple[str, str]] = [("game", "number")]

    def __str__(self) -> str:
        return f"[{self.game}] Capítulo {self.number}: {self.title}"

    @property
    def full_title(self) -> str:
        return f"Chapter {self.number}: {self.title}"