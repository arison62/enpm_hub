from django.urls import path
from .index import AdminView
from .users import UsersView


urlpatterns = [
   path('', AdminView.as_view(), name='admin'),
   path('/users', UsersView.as_view(), name='admin_users'),
]
