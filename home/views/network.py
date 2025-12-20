from inertia import render as render_inertia
from django.views import View


class NetworkView(View):
    def get(self, request):
        return render_inertia(request, "home/Network", None, {
            "seo_title" : "ENSPM Hub - Réseau des Alumni, Étudiants et Partenaires",
            "seo_description" : "ENSPM Hub - Plateforme de mise en relation des alumni, étudiants et partenaires de l'École Nationale Supérieure Polytechnique de Maroua."
        })


