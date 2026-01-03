from django.urls import path
from .views.home import HomeView, index
from .views.internships import InternshipsView
from .views.network import NetworkView
from .views.opportunites import OpportunitiesView
from .views.chat import ChatView
from .views.auth import LoginView
from .views.profile import ProfileView


urlpatterns = [
    path('', index),
    path('home', HomeView.as_view(), name='home'),
    path('network', NetworkView.as_view(), name='network'),
    path('opportunities', OpportunitiesView.as_view(), name='opportunities'),
    path('chat', ChatView.as_view(), name="chat"),
    path('internships', InternshipsView.as_view(), name="internships"),
    path('profile/<slug:slug>', ProfileView.as_view(), name="profile"),
    path('login', LoginView.as_view(), name='login'),
]
