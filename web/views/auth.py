from django.views import View
from inertia import render as inertia_render

class LoginView(View):
    def get(self, request):
        return inertia_render(request, 'auth/Login')

class PasswordResetView(View):
    def get(self, request):
        return inertia_render(request, 'auth/PasswordReset')