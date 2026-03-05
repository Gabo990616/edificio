from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve

EXEMPT_PREFIXES = (
    "/admin/",
    "/static/",
    "/media/",
    "/login/",
)

EXEMPT_URL_NAMES = {
    "login",
    "logout",
}


class LoginRequiredMiddleware:
    """
    Requiere usuario autenticado para cualquier ruta,
    excepto las exentas.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # exenciones por prefijo
        if path.startswith(EXEMPT_PREFIXES):
            return self.get_response(request)

        # exenciones por nombre de url
        try:
            match = resolve(path)
            if match.url_name in EXEMPT_URL_NAMES:
                return self.get_response(request)
        except Exception:
            pass

        # si no está logueado -> login + next
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.get_full_path()}")

        return self.get_response(request)
