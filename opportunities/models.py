# opportunities/models.py
from django.db import models
from core.models import ENSPMHubBaseModel
from django.utils.translation import gettext_lazy as _


# ==========================================
# 7. OFFRES & FORMATIONS
# ==========================================
# Stages, Emplois, Formations
class Stage(ENSPMHubBaseModel):
    TYPE_STAGE_CHOICES = [
        ('ouvrier', 'Ouvrier'), 
        ('academique', 'Académique'), 
        ('professionnel', 'Professionnel')
    ]
    
    STATUT_CHOICES = [
        ('active', 'Active'), 
        ('expiree', 'Expirée'), 
        ('pourvue', 'Pourvue')
    ]

    createur_profil = models.ForeignKey('core.Profil', null=True, blank=True, on_delete=models.SET_NULL)
    organisation = models.ForeignKey('organizations.Organisation', null=True, blank=True, on_delete=models.SET_NULL)
    titre = models.CharField(max_length=255)
    lieu = models.CharField(max_length=150)
    nom_structure = models.CharField(max_length=255)
    description = models.TextField()
    type_stage = models.CharField(max_length=20, choices=TYPE_STAGE_CHOICES)
    email_contact = models.EmailField(null=True, blank=True)
    telephone_contact = models.CharField(max_length=20, null=True, blank=True)
    lien_offre_original = models.URLField(null=True, blank=True)
    lien_candidature = models.URLField(null=True, blank=True)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='active')

    class Meta:
        db_table = 'stage'


class Emploi(ENSPMHubBaseModel):
    TYPE_EMPLOI_CHOICES = [  # À compléter selon besoins réels
        ('temps_plein_terrain', 'Temps plein terrain'),
        ('temps_partiel_terrain', 'Temps partiel terrain'),
        ('temps_plein_ligne', 'Temps plein ligne'),
    ]
    STATUT_CHOICES = [
        ('active', 'Active'),
        ('expiree', 'Expirée'), 
        ('pourvue', 'Pourvue')
    ]

    createur_profil = models.ForeignKey('core.Profil', null=True, blank=True, on_delete=models.SET_NULL)
    organisation = models.ForeignKey('organizations.Organisation', null=True, blank=True, on_delete=models.SET_NULL)
    titre = models.CharField(max_length=255)
    lieu = models.CharField(max_length=150)
    nom_structure = models.CharField(max_length=255)
    description = models.TextField()
    type_emploi = models.CharField(max_length=40, choices=TYPE_EMPLOI_CHOICES, null=True, blank=True)
    email_contact = models.EmailField(null=True, blank=True)
    telephone_contact = models.CharField(max_length=20, null=True, blank=True)
    lien_offre_original = models.URLField(null=True, blank=True)
    lien_candidature = models.URLField(null=True, blank=True)
    date_publication = models.DateField(auto_now_add=True)
    date_expiration = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='active')

    class Meta:
        db_table = 'emploi'


class Formation(ENSPMHubBaseModel):
    TYPE_FORMATION_CHOICES = [
        ('en_ligne', 'En ligne'), 
        ('presentiel', 'Présentiel'), 
        ('hybride', 'Hybride')
    ]

    createur_profil = models.ForeignKey('core.Profil', null=True, blank=True, on_delete=models.SET_NULL)
    organisation = models.ForeignKey('organizations.Organisation', null=True, blank=True, on_delete=models.SET_NULL)
    titre = models.CharField(max_length=255)
    lieu = models.CharField(max_length=150, null=True, blank=True)
    nom_structure = models.CharField(max_length=255)
    description = models.TextField()
    type_formation = models.CharField(max_length=20, choices=TYPE_FORMATION_CHOICES)
    est_payante = models.BooleanField(default=False)
    email_contact = models.EmailField(null=True, blank=True)
    telephone_contact = models.CharField(max_length=20, null=True, blank=True)
    lien_formation = models.URLField(null=True, blank=True)
    lien_inscription = models.URLField(null=True, blank=True)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    devise = models.CharField(max_length=10, default='XAF')
    est_valide = models.BooleanField(default=False)

    class Meta:
        db_table = 'formation'


class ValidationFormation(ENSPMHubBaseModel):
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='validations')
    validateur_profil = models.ForeignKey('core.Profil', on_delete=models.CASCADE)
    est_approuve = models.BooleanField()
    commentaire = models.TextField(null=True, blank=True)
    date_validation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'validation_formation'