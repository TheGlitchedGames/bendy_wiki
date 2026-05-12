from django.contrib.messages import get_messages
from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import gettext as _
from jinja2 import Environment


def environment(**options) -> Environment:
    env = Environment(**options)
    env.globals.update({
        "static": static,
        "url": reverse,
        "get_messages": get_messages,
        "_": _,
    })
    env.filters["static"] = lambda path: static(path)
    return env