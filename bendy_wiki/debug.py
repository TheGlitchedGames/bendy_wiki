"""
Callback personalizado para django-debug-toolbar.

El callback por defecto de la toolbar asume que las plantillas son Django
Templates y busca el tag {% debug_toolbar %}. Como este proyecto usa Jinja2,
la toolbar se inyecta directamente en el HTML sin tag especial; solo
necesitamos decidir si mostrarla o no.

Referencia: https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#show-toolbar-callback
"""
from django.conf import settings
from django.http import HttpRequest


def show_toolbar(request: HttpRequest) -> bool:
    """
    Muestra el panel de debug si:
        - DEBUG está activo, Y
        - la petición de una IP en INTERNAL_IPS.

    Se puede añadir condiciones adicionales aquí.
    """
    if not settings.DEBUG:
        return False
    return request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS
