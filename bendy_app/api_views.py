from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from bendy_app.models import Game
from bendy_app.serializers import GameSerializer


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para el modelo Game.

    Endpoints generados automáticamente:
      GET /api/games/       → lista de juegos
      GET /api/games/{id}/  → detalle de un juego
    """

    queryset = Game.objects.all().order_by("release_year")
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]