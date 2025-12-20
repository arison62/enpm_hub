from django.urls import path
from .views.home import home
from .views.auth import LoginView


urlpatterns = [
    path('', home),
    path('login/', LoginView.as_view(), name='login'),
]
