from django.urls import path, include
from rest_framework.routers import DefaultRouter

from bendy_app.api_views import GameViewSet

router = DefaultRouter()
router.register(r"games", GameViewSet, basename="game")

urlpatterns = [
    path("", include(router.urls))
]