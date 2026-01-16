from inertia import render as render_inertia
from django.views import View

class OpportunitiesView(View):
    def get(self, request):
        return render_inertia(request, "home/opportunities/Opportunities", None, {
            "seo_title" : "ENSPM Hub - Opportunités",
            "seo_description": "ENSPM Hub - Reseau d'opportnuites de formation et emploi."
        })


