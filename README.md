# 🎬 Bendy Wiki — El Estudio de Tinta

> Wiki no oficial de **Bendy and the Ink Machine** y **Bendy and the Dark Revival**, construida con Django 6.

---

## Tabla de contenidos

1. [Descripción del proyecto](#descripción-del-proyecto)
2. [Stack tecnológico](#stack-tecnológico)
3. [Requisitos previos](#requisitos-previos)
4. [Instalación en Windows (PowerShell)](#instalación-en-windows-powershell)
5. [Variables de entorno](#variables-de-entorno)
6. [Estructura del proyecto](#estructura-del-proyecto)
7. [Aplicaciones](#aplicaciones)
8. [Modelos](#modelos)
9. [Vistas y URLs](#vistas-y-urls)
10. [API REST](#api-rest)
11. [Sistema de permisos y roles](#sistema-de-permisos-y-roles)
12. [Tests](#tests)
13. [Comandos de gestión](#comandos-de-gestión)
14. [Archivos estáticos y media](#archivos-estáticos-y-media)
15. [Django Admin](#django-admin)
16. [Despliegue](#despliegue)

---

## Descripción del proyecto

**Bendy Wiki** es una aplicación web desarrollada en Django que actúa como enciclopedia colaborativa del universo de
Bendy. Permite a los usuarios registrados consultar y (si tienen el rol adecuado) editar información sobre:

- Los dos juegos principales: *BATIM* y *BATDR*
- Personajes, con toda su ficha narrativa
- Capítulos, con mecánicas de juego, lore y trivia
- Una comunidad de usuarios con sistema de puntos de tinta

---

## Stack tecnológico

| Capa               | Tecnología                   |
|--------------------|------------------------------|
| Framework          | Django 6                     |
| Base de datos      | SQLite (desarrollo)          |
| Autenticación      | Django Auth + django-allauth |
| API REST           | Django REST Framework        |
| Formularios        | Django Forms + crispy-forms  |
| Filtros            | django-filter                |
| Notificaciones     | sweetify (SweetAlert2)       |
| Archivos estáticos | WhiteNoise                   |
| Templates          | Django Templates             |
| CSS/JS             | Bootstrap 5 + CSS propio     |
| Debug              | django-debug-toolbar         |

---

## Requisitos previos

- **Python 3.11+**
- **pip**
- **Git**

Comprueba las versiones instaladas en PowerShell:

```powershell
python --version
pip --version
git --version
```

---

## Instalación en Windows (PowerShell)

### 1 — Clonar el repositorio

```powershell
git clone https://github.com/tu-usuario/bendy-wiki.git
Set-Location bendy-wiki
```

### 2 — Crear y activar el entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

> Si PowerShell bloquea la ejecución de scripts, ejecuta primero:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### 3 — Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 4 — Configurar variables de entorno

Crea el archivo `.env` en la raíz del proyecto:

```powershell
Copy-Item .env.example .env
notepad .env
```

Contenido mínimo del `.env`:

```env
SECRET_KEY=django-insecure-cambia-esto-en-produccion
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5 — Aplicar migraciones

```powershell
python manage.py migrate
```

### 6 — Poblar la base de datos con datos de ejemplo

```powershell
python manage.py populate_bendy_data
```

### 7 — Crear un superusuario

```powershell
python manage.py createsuperuser
```

### 8 — Recopilar archivos estáticos

```powershell
python manage.py collectstatic --noinput
```

### 9 — Ejecutar el servidor de desarrollo

```powershell
python manage.py runserver
```

Abre tu navegador en `http://127.0.0.1:8000`.

---

## Variables de entorno

| Variable        | Descripción                          | Valor por defecto            |
|-----------------|--------------------------------------|------------------------------|
| `SECRET_KEY`    | Clave secreta de Django              | Valor inseguro de desarrollo |
| `DEBUG`         | Modo debug                           | `True`                       |
| `ALLOWED_HOSTS` | Hosts permitidos, separados por coma | `localhost,127.0.0.1`        |

---

## Estructura del proyecto

```
bendy-wiki/
│
├── auth_app/               # Autenticación, registro, perfiles
│   ├── models.py           # BendyUser (AbstractUser extendido)
│   ├── views.py            # Login, Register, Logout, Profile…
│   ├── forms.py            # Formularios de autenticación
│   ├── urls.py             # /auth/…
│   ├── mixins.py           # BannedUserMixin
│   └── tests.py            # Tests de la app
│
├── bendy_app/              # Lógica principal de la wiki
│   ├── models.py           # Game, Character, Chapter
│   ├── views.py            # CRUD completo
│   ├── forms.py            # GameForm, CharacterForm, ChapterForm
│   ├── urls.py             # URLs de la wiki
│   ├── api_views.py        # ViewSets de DRF
│   ├── api_urls.py         # /api/…
│   ├── serializers.py      # GameSerializer
│   ├── filters/            # django-filter FilterSets
│   ├── mixins.py           # EditorRequiredMixin, BreadcrumbMixin
│   └── management/
│       └── commands/
│           └── populate_bendy_data.py
│
├── bendy_wiki/             # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   ├── jinja2.py
│   └── debug.py
│
├── templates/              # Plantillas Django
│   ├── base.html
│   ├── home/
│   ├── auth_app/
│   ├── characters/
│   ├── chapters/
│   ├── games/
│   └── partials/
│
├── static/                 # CSS y JS propios
│   ├── css/
│   └── js/
│
├── media/                  # Archivos subidos por usuarios (no en git)
├── staticfiles/            # Salida de collectstatic (no en git)
├── manage.py
├── requirements.txt
└── .env                    # Variables de entorno (no en git)
```

---

## Aplicaciones

### `auth_app`

Gestiona todo lo relacionado con usuarios:

- Modelo `BendyUser` que extiende `AbstractUser`
- Sistema de roles: `reader`, `editor`, `admin`
- Puntos de tinta (`ink_points`)
- Protección contra usuarios baneados (`BannedUserMixin`)
- Vistas de login, registro, logout, perfil, edición de perfil, cambio de contraseña y eliminación de cuenta

### `bendy_app`

Núcleo de la wiki:

- Modelos `Game`, `Character` y `Chapter`
- CRUD completo protegido con `EditorRequiredMixin`
- API REST de solo lectura (DRF)
- Filtros avanzados con `django-filter`
- Comando de gestión para poblar datos iniciales

---

## Modelos

### `BendyUser`

```python
# Campos añadidos sobre AbstractUser
role          = CharField  # reader | editor | admin
bio           = TextField
avatar        = ImageField
favorite_game = CharField  # batim | batdr | both
ink_points    = PositiveIntegerField
is_banned     = BooleanField
joined_at     = DateTimeField (auto)
updated_at    = DateTimeField (auto)
```

**Propiedad útil:**

```python
user.display_name  # Devuelve get_full_name() o username
```

### `Game`

```python
key              = CharField  # batim | batdr (único)
title            = CharField
slug             = SlugField  (único)
release_year     = PositiveSmallIntegerField
short_description = TextField
cover_image      = ImageField
```

### `Character`

```python
primary_game     = ForeignKey(Game)
extra_games      = ManyToManyField(Game)  # juegos secundarios
name             = CharField
slug             = SlugField (único)
role             = CharField  # protagonist | antagonist | ally | …
character_type   = CharField  # human | toon | ink_monster | …
description      = TextField
# … appearance, personality, background, voice actors, etc.
is_playable      = BooleanField
is_alive_end     = BooleanField (nullable)
```

**Propiedad útil:**

```python
character.is_ink_creature  # True si toon, ink_monster o hybrid
```

### `Chapter`

```python
game             = ForeignKey(Game)
number           = PositiveSmallIntegerField
title            = CharField
slug             = SlugField (único)
art_theme        = CharField  # animation | music | literature | …
difficulty       = CharField  # introductory | easy | medium | hard | boss_heavy
has_boss_fight   = BooleanField
has_stealth_sections = BooleanField
has_puzzle_sections  = BooleanField
synopsis         = TextField
# … key_events, lore_revelations, trivia, etc.
```

**Restricción de unicidad:** `(game, number)` — no puede haber dos capítulos con el mismo número en el mismo juego.

**Propiedad útil:**

```python
chapter.full_title  # "Chapter 1: Moving Pictures"
```

---

## Vistas y URLs

### URLs de `auth_app` — prefijo `/`

| URL                                  | Nombre                 | Vista                |
|--------------------------------------|------------------------|----------------------|
| `/auth/login/`                       | `auth:login`           | `LoginView`          |
| `/auth/register/`                    | `auth:register`        | `RegisterView`       |
| `/auth/logout/`                      | `auth:logout`          | `LogoutView`         |
| `/auth/profile/<username>/`          | `auth:profile`         | `ProfileView`        |
| `/auth/profile/<username>/edit/`     | `auth:profile_edit`    | `ProfileUpdateView`  |
| `/auth/profile/<username>/password/` | `auth:password_change` | `PasswordChangeView` |
| `/auth/users/`                       | `auth:user_list`       | `UserListView`       |
| `/auth/delete-account/`              | `auth:delete_account`  | `DeleteAccountView`  |

### URLs de `bendy_app` — prefijo `/`

| URL                            | Nombre                   | Vista                 |
|--------------------------------|--------------------------|-----------------------|
| `/`                            | `bendy:index`            | `HomeView`            |
| `/games/`                      | `bendy:game_list`        | `GameListView`        |
| `/games/crear/`                | `bendy:game_create`      | `GameCreateView`      |
| `/games/<slug>/`               | `bendy:game_detail`      | `GameDetailView`      |
| `/games/<slug>/editar/`        | `bendy:game_update`      | `GameUpdateView`      |
| `/games/<slug>/eliminar/`      | `bendy:game_delete`      | `GameDeleteView`      |
| `/characters/`                 | `bendy:character_list`   | `CharacterListView`   |
| `/characters/crear/`           | `bendy:character_create` | `CharacterCreateView` |
| `/characters/<slug>/`          | `bendy:character_detail` | `CharacterDetailView` |
| `/characters/<slug>/editar/`   | `bendy:character_update` | `CharacterUpdateView` |
| `/characters/<slug>/eliminar/` | `bendy:character_delete` | `CharacterDeleteView` |
| `/chapters/`                   | `bendy:chapter_list`     | `ChapterListView`     |
| `/chapters/crear/`             | `bendy:chapter_create`   | `ChapterCreateView`   |
| `/chapters/<slug>/`            | `bendy:chapter_detail`   | `ChapterDetailView`   |
| `/chapters/<slug>/editar/`     | `bendy:chapter_update`   | `ChapterUpdateView`   |
| `/chapters/<slug>/eliminar/`   | `bendy:chapter_delete`   | `ChapterDeleteView`   |

---

## API REST

La API es de **solo lectura** y está disponible en `/api/`.

### Endpoints

| Método | URL                | Descripción            | Auth         |
|--------|--------------------|------------------------|--------------|
| `GET`  | `/api/games/`      | Lista todos los juegos | No requerida |
| `GET`  | `/api/games/<id>/` | Detalle de un juego    | No requerida |

### Ejemplo de respuesta — `GET /api/games/`

```json
[
  {
    "id": 1,
    "key": "batim",
    "title": "Bendy and the Ink Machine",
    "slug": "bendy-and-the-ink-machine",
    "release_year": 2017,
    "short_description": "Juego de terror...",
    "cover_image": null
  }
]
```

### Consumir la API desde PowerShell

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/games/" -Method Get
```

---

## Sistema de permisos y roles

| Rol                 | Descripción                | Puede crear/editar contenido |
|---------------------|----------------------------|------------------------------|
| `reader`            | Usuario básico             | ❌                            |
| `editor`            | Contribuidor               | ✅                            |
| `admin`             | Administrador de contenido | ✅                            |
| `is_staff` (Django) | Acceso al admin panel      | ✅                            |

El mixin `EditorRequiredMixin` protege todas las vistas de creación, edición y eliminación. Un usuario `reader`
autenticado que intente acceder a estas rutas es redirigido a la portada.

```python
# bendy_app/mixins.py
class EditorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (
            user.is_staff or getattr(user, "role", "") in ("editor", "admin")
        )
```

---

## Tests

Los tests están organizados en dos archivos:

- `auth_app/tests.py` — Modelos, formularios y vistas de autenticación
- `bendy_app/tests.py` — Modelos, formularios, vistas, API y comando de gestión

### Ejecutar todos los tests

```powershell
python manage.py test
```

### Ejecutar tests de una app concreta

```powershell
python manage.py test auth_app
python manage.py test bendy_app
```

### Ejecutar una clase de test específica

```powershell
python manage.py test auth_app.tests.BendyUserModelTests
python manage.py test bendy_app.tests.GameAPITests
```

### Ejecutar un test individual

```powershell
python manage.py test auth_app.tests.BendyUserModelTests.test_display_name_returns_full_name_when_available
```

### Ver cobertura de tests (requiere `coverage`)

```powershell
pip install coverage
coverage run manage.py test
coverage report
coverage html   # genera htmlcov/index.html
```

---

## Comandos de gestión

### `populate_bendy_data`

Puebla la base de datos con los juegos, personajes y capítulos canónicos de BATIM y BATDR.

```powershell
# Insertar/actualizar datos
python manage.py populate_bendy_data

# Borrar todo y volver a insertar
python manage.py populate_bendy_data --clear
```

### Otros comandos Django útiles

```powershell
# Crear migraciones tras cambiar modelos
python manage.py makemigrations

# Aplicar migraciones pendientes
python manage.py migrate

# Abrir la shell de Django
python manage.py shell

# Listar todas las URLs del proyecto
python manage.py show_urls   # requiere django-extensions

# Exportar datos a JSON
python manage.py dumpdata bendy_app --indent 2 > bendy_data.json

# Importar datos desde JSON
python manage.py loaddata bendy_data.json
```

---

## Archivos estáticos y media

En **desarrollo** Django sirve automáticamente los archivos estáticos y de media gracias a la configuración en
`bendy_wiki/urls.py`.

En **producción**, ejecuta:

```powershell
python manage.py collectstatic --noinput
```

Los archivos se copian a `staticfiles/` y son servidos por **WhiteNoise** sin necesidad de configurar un servidor web
adicional para estáticos.

Los archivos subidos por usuarios (avatares, imágenes de personajes…) se almacenan en `media/`. En producción deberías
servirlos desde un CDN o un servidor de objetos (S3, etc.).

---

## Django Admin

Accede al panel de administración en `http://127.0.0.1:8000/admin/`.

Funcionalidades registradas:

| Modelo      | Acciones personalizadas                                        |
|-------------|----------------------------------------------------------------|
| `BendyUser` | Banear/desbanear usuarios, promover a Editor                   |
| `Game`      | CRUD completo con slug autocompletado                          |
| `Character` | Filtros por juego, rol y tipo; gestión de M2M                  |
| `Chapter`   | Filtros por juego, dificultad y mecánicas; jerarquía por fecha |

---

## Despliegue

### Checklist antes de producción

```powershell
# Verificar configuración de seguridad
python manage.py check --deploy
```

Puntos críticos en `settings.py`:

```python
DEBUG = False
SECRET_KEY = "clave-larga-aleatoria-segura"
ALLOWED_HOSTS = ["tu-dominio.com"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        # ... configuración de PostgreSQL
    }
}
```

### Reemplazar SQLite por PostgreSQL

```powershell
pip install psycopg2-binary
```

```env
DATABASE_URL=postgres://usuario:contraseña@localhost:5432/bendy_wiki
```

---

## Licencia

Este proyecto es una obra de fans. **Bendy**, *Bendy and the Ink Machine* y *Bendy and the Dark Revival* son marcas
registradas de **Joey Drew Studios Inc. / Kindly Beast**. Todo el contenido original pertenece a sus respectivos
propietarios.