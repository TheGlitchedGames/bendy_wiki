from django.urls import path

from bendy_app import views

app_name = "bendy"

urlpatterns = [
    path("", views.HomeView.as_view(), name='index'),

    path('characters/', views.CharacterListView.as_view(),
         name="character_list"),
    path("characters/crear/", views.CharacterCreateView.as_view(),
         name="character_create"),
    path("characters/<slug:slug>/", views.CharacterDetailView.as_view(),
         name="character_detail"),
    path("characters/<slug:slug>/editar/", views.CharacterUpdateView.as_view(

    ), name="character_update"),
    path("characters/<slug:slug>/eliminar",
         views.CharacterDeleteView.as_view(), name="character_delete")
]
