from inertia import render as render_inertia
from django.views import View


class NetworkView(View):
    def get(self, request):
        return render_inertia(request, "home/Network")

def network(request):
    return render_inertia(request, "home/Network")

