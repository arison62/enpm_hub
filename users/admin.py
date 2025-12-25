from django.contrib import admin
from .models import LienReseauSocialProfil

class LienReseauSocialProfilAdmin(admin.ModelAdmin):
    list_display = ('profil', 'reseau', 'url', 'est_actif')