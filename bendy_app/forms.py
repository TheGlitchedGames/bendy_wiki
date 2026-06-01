from django import forms
from django.utils.translation import gettext_lazy as _

from bendy_app.models import Character, Chapter, Game


class CharacterForm(forms.ModelForm):
    """Formulario para crear y editar personajes."""

    class Meta:
        model = Character
        fields = [
            'name', 'slug', 'alias', 'primary_game', 'extra_games',
            'role', 'character_type', 'description', 'appearance',
            'personality', 'background', 'human_counterpart',
            'voice_actor_batim', 'voice_actor_batdr', 'real_world_inspiration',
            'appears_in_chapters', 'iconic_quote', 'quote_source',
            'is_alive_end', 'is_playable', 'image'
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "bendy-input",
                                           "placeholder": "Nombre del personaje"}),
            "slug": forms.TextInput(attrs={"class": "bendy-input",
                                           "placeholder": "nombre-del-personaje"}),
            "alias": forms.TextInput(attrs={"class": "bendy-input"}),
            "primary_game": forms.Select(attrs={"class": "bendy-select"}),
            "extra_games": forms.CheckboxSelectMultiple(),
            "role": forms.Select(attrs={"class": "bendy-select"}),
            "character_type": forms.Select(attrs={"class": "bendy-select"}),
            "description": forms.Textarea(
                attrs={"class": "bendy-textarea", "rows": 4}),
            "appearance": forms.Textarea(
                attrs={"class": "bendy-textarea", "rows": 3}),
            "personality": forms.Textarea(
                attrs={"class": "bendy-textarea", "rows": 3}),
            "background": forms.Textarea(
                attrs={"class": "bendy-textarea", "rows": 3}),
            "human_counterpart": forms.TextInput(
                attrs={"class": "bendy-input"}),
            "voice_actor_batim": forms.TextInput(
                attrs={"class": "bendy-input"}),
            "voice_actor_batdr": forms.TextInput(
                attrs={"class": "bendy-input"}),
            "real_world_inspiration": forms.TextInput(
                attrs={"class": "bendy-input"}),
            "appears_in_chapters": forms.TextInput(
                attrs={"class": "bendy-input", "placeholder": "1, 2, 3"}),
            "iconic_quote": forms.Textarea(
                attrs={"class": "bendy-textarea", "rows": 2}),
            "quote_source": forms.TextInput(attrs={"class": "bendy-input"}),
            "image": forms.FileInput(attrs={"class": "bendy-file-input"})
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError(_('El nombre debe tener al menos 2 '
                                          'caracteres.'))
        return name

    def clean_slug(self):
        slug = self.cleaned_data.get('slug', '').strip().lower()
        qs = Character.objects.filter(slug=slug)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(_('Ya existe un personaje con este '
                                          'slug.'))
        return slug

    def clean(self):
        cleaned_data = super().clean()
        primary_game = cleaned_data.get('primary_game')
        extra_games = cleaned_data.get('extra_games')

        # El juego principal no puede estar también en "extra_games"
        if primary_game and extra_games and primary_game in extra_games:
            self.add_error(
                "extra_games",
                _('El juego principal no puede aparecer también en "También '
                  'aparece en".')
            )
        return cleaned_data


class ChapterForm(forms.ModelForm):
    """Formulario para crear y editar capítulos."""

    class Meta:
        model = Chapter
        fields = [
            "game", "number", "title", "slug", "art_theme",
            "art_theme_explanation",
            "release_date", "last_update_date", "synopsis", "aesthetics",
            "setting_description", "difficulty", "has_boss_fight", "boss_name",
            "has_stealth_sections", "has_puzzle_sections",
            "approximate_duration_minutes", "protagonist", "main_villain",
            "new_characters_introduced", "key_events", "lore_revelations",
            "composer", "soundtrack_notes", "cover_image", "background_image",
            "trivia", "reception_notes"
        ]
        widgets = {
            "game": forms.Select(attrs={"class": "bendy-select"}),
            "number": forms.NumberInput(attrs={"class": "bendy-input"}),
            "title": forms.TextInput(attrs={"class": "bendy-input"}),
            "slug": forms.TextInput(attrs={"class": "bendy-input"}),
            "art_theme": forms.Select(attrs={"class": "bendy-select"}),
            "art_theme_explanation": forms.Textarea(
                attrs={"class": "bendy-textarea", "rows": 3}),
            "release_date": forms.DateInput(
                attrs={"class": "bendy-input", "type": "date"}),
            "last_update_date": forms.DateInput(
                attrs={"class": "bendy-input", "type": "date"}),
            "synopsis": forms.Textarea(
                attrs={"class": "bendy-textarea", "rows": 4}),
            "aesthetics": forms.Textarea(
                attrs={"class": "bendy-textarea", "rows": 3}),
            "setting_description": forms.Textarea(
                attrs={"class": "bendy-textarea", "rows": 3}),
            "difficulty": forms.Select(attrs={"class": "bendy-select"}),
            "boss_name": forms.TextInput(attrs={"class": "bendy-input"}),
            "approximate_duration_minutes": forms.NumberInput(
                attrs={"class": "bendy-input"}),
            "protagonist": forms.TextInput(attrs={"class": "bendy-input"}),
            "main_villain": forms.TextInput(attrs={"class": "bendy-input"}),
            "new_characters_introduced": forms.Textarea(
                attrs={"class": "bendy-textarea", "rows": 2}),
            "key_events": forms.Textarea(
                attrs={"class": "bendy-textarea", "rows": 3}),
            "lore_revelations": forms.Textarea(
                attrs={"class": "bendy-textarea", "rows": 3}),
            "composer": forms.TextInput(attrs={"class": "bendy-input"}),
            "soundtrack_notes": forms.Textarea(
                attrs={"class": "bendy-textarea", "rows": 2}),
            "cover_image": forms.FileInput(attrs={"class": "bendy-file-input"}),
            "background_image": forms.FileInput(
                attrs={"class": "bendy-file-input"}),
            "trivia": forms.Textarea(
                attrs={"class": "bendy-textarea", "rows": 3}),
            "reception_notes": forms.Textarea(
                attrs={"class": "bendy-textarea", "rows": 3})
        }

    def clean_number(self) -> int:
        number: int = self.cleaned_data.get('number')
        if number is not None and number < 1:
            raise forms.ValidationError(_("El número de capítulo debe ser "
                                          "mayor de 0."))
        return number

    def clean(self) -> dict:
        cleaned_data = super().clean()
        game = cleaned_data.get('game')
        number = cleaned_data.get('number')
        has_boss = cleaned_data.get('has_boss_fight')
        boss_name = cleaned_data.get('boss_name', '').strip()

        # Unicidad (game, number) al crear o editar
        if game and number is not None:
            qs = Chapter.objects.filter(game=game, number=number)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(
                    _('Ya existe un capítulo %(number)s para ese juego.'),
                    params={"number": number}
                )

        # Si hay jefe, el nombre es obligatorio
        if has_boss and not boss_name:
            self.add_error('boss_name', _('Si hay combate contra jefe, '
                                          'indica su nombre.'))

        return cleaned_data


class GameForm(forms.ModelForm):
    """Formulario para crear y editar juegos."""

    class Meta:
        model = Game
        fields = ["key", "title", "slug", "release_year", "short_description",
                  "cover_image"]
        widgets = {
            "key": forms.Select(attrs={"class": "bendy-select"}),
            "title": forms.TextInput(attrs={
                "class": "bendy-input",
                "placeholder": "Ej: Bendy and the Ink Machine",
            }),
            "slug": forms.TextInput(attrs={
                "class": "bendy-input",
                "placeholder": "bendy-and-the-ink-machine",
            }),
            "release_year": forms.NumberInput(attrs={
                "class": "bendy-input",
                "placeholder": "Ej: 2017",
            }),
            "short_description": forms.Textarea(attrs={
                "class": "bendy-textarea",
                "rows": 4,
                "placeholder": "Descripción breve del juego...",
            }),
            "cover_image": forms.FileInput(attrs={"class": "bendy-file-input"}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug", "").strip().lower()
        qs = Game.objects.filter(slug=slug)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(_("Ya existe un juego con este slug."))
        return slug

    def clean_key(self):
        key = self.cleaned_data.get("key", "").strip()
        qs = Game.objects.filter(key=key)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(_("Ya existe un juego con esta clave."))
        return key

    def clean_release_year(self):
        year = self.cleaned_data.get("release_year")
        if year is not None and (year < 1900 or year > 2100):
            raise forms.ValidationError(_("Introduce un año válido."))
        return year