from inertia import render as render_inertia
from django.views import View

class ProfileView(View):
    def get(self, request, slug):
        return render_inertia(request, "home/Profile")