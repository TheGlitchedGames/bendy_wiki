from rest_framework import serializers

from bendy_app.models import Game


class GameSerializer(serializers.ModelSerializer):
    """Serializer completo para el modelo Game."""

    class Meta:
        model = Game
        fields = [
            "id",
            "key",
            "title",
            "slug",
            "release_year",
            "short_description",
            "cover_image"
        ]