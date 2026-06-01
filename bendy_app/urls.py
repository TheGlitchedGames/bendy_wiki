from django.urls import path

from bendy_app import views

app_name = "bendy"

urlpatterns = [
    # ── Home ──────────────────────────────────────────────────────────────────
    path("", views.HomeView.as_view(), name="index"),

    # ── Characters ────────────────────────────────────────────────────────────
    path("characters/", views.CharacterListView.as_view(), name="character_list"),
    path("characters/crear/", views.CharacterCreateView.as_view(), name="character_create"),
    path("characters/<slug:slug>/", views.CharacterDetailView.as_view(), name="character_detail"),
    path("characters/<slug:slug>/editar/", views.CharacterUpdateView.as_view(), name="character_update"),
    path("characters/<slug:slug>/eliminar/", views.CharacterDeleteView.as_view(), name="character_delete"),

    # ── Games ─────────────────────────────────────────────────────────────────
    path("games/", views.GameListView.as_view(), name="game_list"),
    path("games/crear/", views.GameCreateView.as_view(), name="game_create"),
    path("games/<slug:slug>/", views.GameDetailView.as_view(), name="game_detail"),
    path("games/<slug:slug>/editar/", views.GameUpdateView.as_view(), name="game_update"),
    path("games/<slug:slug>/eliminar/", views.GameDeleteView.as_view(), name="game_delete"),

    # ── Chapters ──────────────────────────────────────────────────────────────
    path("chapters/", views.ChapterListView.as_view(), name="chapter_list"),
    path("chapters/crear/", views.ChapterCreateView.as_view(), name="chapter_create"),
    path("chapters/<slug:slug>/", views.ChapterDetailView.as_view(), name="chapter_detail"),
    path("chapters/<slug:slug>/editar/", views.ChapterUpdateView.as_view(), name="chapter_update"),
    path("chapters/<slug:slug>/eliminar/", views.ChapterDeleteView.as_view(), name="chapter_delete"),
]