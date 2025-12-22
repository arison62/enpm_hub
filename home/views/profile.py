from django.http import Http404
from inertia import defer, render as render_inertia
from django.views import View
from core.services.user_service import user_service
from core.api.schemas import UserCompleteSchema

def get_user_by_slug(slug):
    user = user_service.get_user_by_slug(slug)
    if not user:
        raise Http404("Utilisateur non trouvé")
    user_data = UserCompleteSchema.from_orm(user).model_dump()
    return user_data

class ProfileView(View):
    def get(self, request, slug):
        return render_inertia(request, "home/profile/Profile", {
            "user": defer(lambda: get_user_by_slug(slug))
        })