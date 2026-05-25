from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, \
    PasswordChangeForm
from django.utils.translation import gettext_lazy as _

from .models import BendyUser

# Clase de widget reutilizable para no repetir attrs
_INPUT = lambda placeholder="", type_="text": forms.TextInput(attrs={
    "class": "bendy-input", "placeholder": placeholder, "autocomplete": type_
})


class BendyLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Usuario o Email"),
        widget=forms.TextInput(attrs={
            "class": "bendy-input",
            "placeholder": "Tu nombre de archivador...",
            "autocomplete": "username",
        }),
    )
    password = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput(attrs={
            "class": "bendy-input",
            "placeholder": "Contraseña secreta...",
            "autocomplete": "current-password",
        }),
    )
    remember_me = forms.BooleanField(
        label=_("Recordarme"),
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "bendy-checkbox"}),
    )

    class Meta:
        model = BendyUser
        fields = ["username", "password", "remember_me"]

    # clean_<field>: normaliza el nombre de usuario a minúsculas
    def clean_username(self) -> str:
        username: str = self.cleaned_data.get("username", "").strip()
        return username.lower()

    # clean(): validación cruzada — bloquea usuarios baneados antes del login
    def clean(self) -> dict:
        cleaned_data = super().clean()
        user = self.get_user()
        if user is not None and getattr(user, "is_banned", False):
            raise forms.ValidationError(
                _("Tu cuenta ha sido suspendida. Contacta con un administrador.")
            )
        return cleaned_data


class BendyRegisterForm(UserCreationForm):
    username = forms.CharField(
        label=_("Nombre de usuario"),
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "bendy-input",
            "placeholder": "Elige tu nombre en el estudio...",
        }),
    )
    email = forms.EmailField(
        label=_("Correo electrónico"),
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "bendy-input",
            "placeholder": "tu@email.com",
        }),
    )
    first_name = forms.CharField(
        label=_("Nombre"),
        required=False,
        widget=forms.TextInput(attrs={
            "class": "bendy-input",
            "placeholder": "Tu nombre real (opcional)",
        }),
    )
    last_name = forms.CharField(
        label=_("Apellidos"),
        required=False,
        widget=forms.TextInput(attrs={
            "class": "bendy-input",
            "placeholder": "Tus apellidos (opcional)",
        }),
    )
    password1 = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput(attrs={
            "class": "bendy-input",
            "placeholder": "Crea tu contraseña secreta...",
        }),
    )
    password2 = forms.CharField(
        label=_("Confirmar contraseña"),
        widget=forms.PasswordInput(attrs={
            "class": "bendy-input",
            "placeholder": "Repite tu contraseña...",
        }),
    )
    favorite_game = forms.ChoiceField(
        label=_("Juego favorito"),
        choices=[
            ("batim", "Bendy and the Ink Machine"),
            ("batdr", "Bendy and the Dark Revival"),
            ("both", "Ambos"),
        ],
        widget=forms.Select(attrs={"class": "bendy-select"}),
    )
    terms = forms.BooleanField(
        label=_("Acepto los términos y condiciones"),
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "bendy-checkbox"}),
    )

    class Meta:
        model = BendyUser
        fields = [
            "username", "email", "first_name", "last_name",
            "password1", "password2", "favorite_game",
        ]

    # clean_<field>: verifica unicidad del email de forma case-insensitive
    def clean_email(self) -> str:
        email: str = self.cleaned_data.get("email", "").strip()
        if BendyUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                _("Este correo electrónico ya está registrado."))
        return email.lower()

    # clean_<field>: normaliza el username y comprueba caracteres reservados
    def clean_username(self) -> str:
        username: str = self.cleaned_data.get("username", "").strip()
        forbidden = {"admin", "root", "superuser", "bendy", "system"}
        if username.lower() in forbidden:
            raise forms.ValidationError(
                _("Este nombre de usuario está reservado. Elige otro.")
            )
        return username

    # clean(): validación cruzada nombre + apellido (al menos uno, si no es anónimo)
    def clean(self) -> dict:
        cleaned_data = super().clean()
        first_name: str = cleaned_data.get("first_name", "").strip()
        last_name: str = cleaned_data.get("last_name", "").strip()
        # Si rellena uno, debe rellenar el otro
        if bool(first_name) != bool(last_name):
            msg = _(
                "Si rellenas el nombre, debes rellenar también los apellidos, y viceversa.")
            self.add_error("first_name", msg)
            self.add_error("last_name", msg)
        return cleaned_data

    def save(self, commit: bool = True) -> BendyUser:
        user: BendyUser = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.favorite_game = self.cleaned_data["favorite_game"]
        if commit:
            user.save()
        return user


class BendyProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = BendyUser
        fields = ["first_name", "last_name", "email", "bio", "avatar",
                  "favorite_game"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "bendy-input"}),
            "last_name": forms.TextInput(attrs={"class": "bendy-input"}),
            "email": forms.EmailInput(attrs={"class": "bendy-input"}),
            "bio": forms.Textarea(attrs={
                "class": "bendy-textarea", "rows": 4,
                "placeholder": "Cuéntanos sobre ti...",
            }),
            "avatar": forms.FileInput(attrs={"class": "bendy-file-input"}),
            "favorite_game": forms.Select(attrs={"class": "bendy-select"}),
        }

    # clean_<field>: unicidad de email excluyendo el usuario actual
    def clean_email(self) -> str:
        email: str = self.cleaned_data.get("email", "").strip()
        qs = BendyUser.objects.filter(email__iexact=email).exclude(
            pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                _("Este correo electrónico ya está en uso."))
        return email.lower()

    # clean(): comprueba que la bio no contenga URLs si el usuario es lector
    def clean(self) -> dict:
        cleaned_data = super().clean()
        bio: str = cleaned_data.get("bio", "")
        role: str = getattr(self.instance, "role", "reader")
        if role == "reader" and ("http://" in bio or "https://" in bio):
            self.add_error(
                "bio",
                _("Los lectores no pueden incluir enlaces en la biografía."),
            )
        return cleaned_data


class BendyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Contraseña actual"),
        widget=forms.PasswordInput(attrs={
            "class": "bendy-input",
            "placeholder": "Tu contraseña actual...",
            "autocomplete": "current-password",
        }),
    )
    new_password1 = forms.CharField(
        label=_("Nueva contraseña"),
        widget=forms.PasswordInput(attrs={
            "class": "bendy-input",
            "placeholder": "Nueva contraseña...",
            "autocomplete": "new-password",
        }),
    )
    new_password2 = forms.CharField(
        label=_("Confirmar nueva contraseña"),
        widget=forms.PasswordInput(attrs={
            "class": "bendy-input",
            "placeholder": "Repite la nueva contraseña...",
            "autocomplete": "new-password",
        }),
    )

    # clean(): verifica que la nueva contraseña sea diferente a la actual
    def clean(self) -> dict:
        cleaned_data = super().clean()
        old_password: str = cleaned_data.get("old_password", "")
        new_password: str = cleaned_data.get("new_password1", "")
        if old_password and new_password and old_password == new_password:
            raise forms.ValidationError(
                _("La nueva contraseña no puede ser igual a la actual.")
            )
        return cleaned_data
