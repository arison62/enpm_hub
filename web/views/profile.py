from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from inertia import defer, render as render_inertia
from django.views import View
from users.services.user_service import user_service
from users.api.schemas import UserCompleteOut

def get_user_by_slug(slug):
    user = user_service.get_user_by_slug(slug)
    if not user:
        raise Http404("Utilisateur non trouvé")
    user_data = UserCompleteOut.from_orm(user).model_dump()
    return user_data

@method_decorator(xframe_options_exempt, name='dispatch')
class ProfileView(View):
    def get(self, request, slug):
        return render_inertia(request, "home/profile/Profile", {
            "user": defer(lambda: get_user_by_slug(slug))
        })