# core/middleware/maintenance.py
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs à toujours ignorer (admin, API, et la page de maintenance elle-même)
        if (
            request.path.startswith('/admin/')
            or request.path.startswith('/api/')
            or request.path == reverse('maintenance') 
            or request.path == '/maintenance/' 
        ):
            return self.get_response(request)

        # Vérifie si le mode maintenance est activé
        if getattr(settings, 'MAINTENANCE_MODE', False):
            return HttpResponseRedirect(reverse('maintenance'))

        return self.get_response(request)