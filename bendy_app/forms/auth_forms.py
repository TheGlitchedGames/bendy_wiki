from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, \
    PasswordChangeForm
from django.utils.translation import gettext_lazy as _

from bendy_app.models import BendyUser


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
        model: type[BendyUser] = BendyUser
        fields: list[str] = ["username", "password", "remember_me"]


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
        model: type[BendyUser] = BendyUser
        fields: list[str] = [
            "username", "email", "first_name", "last_name",
            "password1", "password2", "favorite_game",
        ]

    def clean_email(self) -> str:
        email: str = self.cleaned_data.get("email", "")
        if BendyUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("Este correo electrónico ya está registrado."))
        return email.lower()

    def save(self, commit: bool = True) -> BendyUser:
        user: BendyUser = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.favorite_game = self.cleaned_data["favorite_game"]
        if commit:
            user.save()
        return user


class BendyProfileUpdateForm(forms.ModelForm):
    class Meta:
        model: type[BendyUser] = BendyUser
        fields: list[str] = ["first_name", "last_name", "email", "bio", "avatar",
                             "favorite_game"]
        widgets: dict = {
            "first_name": forms.TextInput(attrs={"class": "bendy-input"}),
            "last_name": forms.TextInput(attrs={"class": "bendy-input"}),
            "email": forms.EmailInput(attrs={"class": "bendy-input"}),
            "bio": forms.Textarea(attrs={"class": "bendy-textarea", "rows": 4,
                                         "placeholder": "Cuéntanos sobre ti..."}),
            "avatar": forms.FileInput(attrs={"class": "bendy-file-input"}),
            "favorite_game": forms.Select(attrs={"class": "bendy-select"}),
        }

    def clean_email(self) -> str:
        email: str = self.cleaned_data.get("email", "")
        qs = BendyUser.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(_("Este correo electrónico ya está en uso."))
        return email.lower()


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
