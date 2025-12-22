from inertia import render as render_inertia
from django.views import View
from core.services.user_service import user_service

class ProfileView(View):
    def get(self, request, slug):
        user = user_service.get_user_by_slug(slug)
        return render_inertia(request, "home/profile/Profile", {"user": user})