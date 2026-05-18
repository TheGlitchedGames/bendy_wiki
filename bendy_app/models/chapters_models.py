from django.db import models
from django.utils.translation import gettext_lazy as _


class Chapter(models.Model):
    GAME_CHOICES: list[tuple[str, str]] = [
        ("batim", "Bendy and the Ink Machine"),
        ("batdr", "Bendy and the Dark Revival"),
    ]

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

    # Identificación
    game: models.CharField = models.CharField(
        verbose_name=_("Juego"),
        max_length=10,
        choices=GAME_CHOICES,
        default="batim",
    )
    number: models.PositiveSmallIntegerField = models.PositiveSmallIntegerField(
        verbose_name=_("Número de capítulo"),
    )
    title: models.CharField = models.CharField(
        verbose_name=_("Título"),
        max_length=150,
        help_text=_("Ej: Moving Pictures"),
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
        help_text=_(
            "Cada capítulo de BATIM hace referencia a una forma de arte"),
    )
    art_theme_explanation: models.TextField = models.TextField(
        verbose_name=_("Explicación del tema artístico"),
        blank=True,
    )

    # Fechas de lanzamiento
    release_date: models.DateField = models.DateField(
        verbose_name=_("Fecha de lanzamiento"),
        null=True,
        blank=True,
    )
    last_update_date: models.DateField = models.DateField(
        verbose_name=_("Fecha de última actualización"),
        null=True,
        blank=True,
        help_text=_("Si el capítulo fue remasterizado o actualizado"),
    )

    # Sinopsis y estética
    synopsis: models.TextField = models.TextField(
        verbose_name=_("Sinopsis"),
    )
    aesthetics: models.TextField = models.TextField(
        verbose_name=_("Estética y análisis visual"),
        blank=True,
    )
    setting_description: models.TextField = models.TextField(
        verbose_name=_("Descripción del escenario"),
        blank=True,
        help_text=_(
            "Descripción del entorno físico donde transcurre el capítulo"),
    )

    # Gameplay
    difficulty: models.CharField = models.CharField(
        verbose_name=_("Dificultad"),
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default="medium",
    )
    has_boss_fight: models.BooleanField = models.BooleanField(
        verbose_name=_("¿Tiene combate contra jefe?"),
        default=False,
    )
    boss_name: models.CharField = models.CharField(
        verbose_name=_("Nombre del jefe"),
        max_length=100,
        blank=True,
    )
    has_stealth_sections: models.BooleanField = models.BooleanField(
        verbose_name=_("¿Tiene secciones de sigilo?"),
        default=False,
    )
    has_puzzle_sections: models.BooleanField = models.BooleanField(
        verbose_name=_("¿Tiene secciones de puzles?"),
        default=False,
    )
    approximate_duration_minutes: models.PositiveSmallIntegerField = models.PositiveSmallIntegerField(
        verbose_name=_("Duración aproximada (minutos)"),
        null=True,
        blank=True,
    )

    # Narrativa
    protagonist: models.CharField = models.CharField(
        verbose_name=_("Protagonista"),
        max_length=100,
        default="Henry Stein",
    )
    main_villain: models.CharField = models.CharField(
        verbose_name=_("Villano principal"),
        max_length=100,
        blank=True,
    )
    new_characters_introduced: models.TextField = models.TextField(
        verbose_name=_("Nuevos personajes introducidos"),
        blank=True,
        help_text=_(
            "Lista de personajes que aparecen por primera vez en este capítulo"),
    )
    key_events: models.TextField = models.TextField(
        verbose_name=_("Eventos clave"),
        blank=True,
        help_text=_("Los momentos más importantes del capítulo"),
    )
    lore_revelations: models.TextField = models.TextField(
        verbose_name=_("Revelaciones de trasfondo"),
        blank=True,
        help_text=_(
            "Información nueva sobre la historia del mundo que se descubre en este capítulo"),
    )

    # Música
    soundtrack_notes: models.TextField = models.TextField(
        verbose_name=_("Notas sobre la banda sonora"),
        blank=True,
    )
    composer: models.CharField = models.CharField(
        verbose_name=_("Compositor"),
        max_length=100,
        blank=True,
        default="theMeatly",
    )

    # Imagen representativa
    cover_image: models.ImageField = models.ImageField(
        verbose_name=_("Imagen de portada"),
        upload_to="chapters/",
        blank=True,
        null=True,
    )
    background_image: models.ImageField = models.ImageField(
        verbose_name=_("Imagen de fondo"),
        upload_to="chapters/backgrounds/",
        blank=True,
        null=True,
    )

    # Trivia y curiosidades
    trivia: models.TextField = models.TextField(
        verbose_name=_("Curiosidades / Trivia"),
        blank=True,
    )
    reception_notes: models.TextField = models.TextField(
        verbose_name=_("Recepción / Polémica"),
        blank=True,
        help_text=_("Cómo reaccionó la comunidad al capítulo"),
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
        verbose_name: str = "Capítulo"
        verbose_name_plural: str = "Capítulos"
        ordering: list[str] = ["game", "number"]
        unique_together: list[tuple[str, str]] = [("game", "number")]

    def __str__(self) -> str:
        return f"[{self.get_game_display()}] Capítulo {self.number}: {self.title}"

    @property
    def full_title(self) -> str:
        return f"Chapter {self.number}: {self.title}"
