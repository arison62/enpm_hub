from inertia import render as render_inertia
from django.views import View

class InternshipsView(View):
    def get(self, request):
        return render_inertia(request, "home/Internships")


