from django.http import Http404, HttpRequest, HttpResponseNotFound
from inertia import render as inertia_render
from django.conf import settings


def maintenance(request: HttpRequest):
    if getattr(settings, 'MAINTENANCE_MODE', False):
        return inertia_render(request, 'devops/Maintenance')
    return not_found(request, Http404) # type: ignore


def forbidden(request: HttpRequest, exception: Exception):
    return inertia_render(request, "errors/403")

def not_found(request: HttpRequest, exception: Exception):
    return inertia_render(request, "errors/404")

def server_error(request: HttpRequest):
    return inertia_render(request, "errors/500")