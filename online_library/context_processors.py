from django.utils.translation import get_language

from .translations import get_ui_text


def ui_text(request):
    return {
        "active_language": (get_language() or "kk").split("-")[0],
        "ui": get_ui_text(get_language()),
    }
