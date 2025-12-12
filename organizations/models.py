# organizations/models.py
from django.db import models
from core.models import ENSPMHubBaseModel
from django.utils.translation import gettext_lazy as _


# ==========================================
# 5. ORGANISATIONS
# ==========================================
class Organisation(ENSPMHubBaseModel):
    TYPE_ORGANISATION_CHOICES = [
        ('entreprise', 'Entreprise'),
        ('ong', 'ONG'),
        ('institution_publique', 'Institution publique'),
        ('startup', 'Startup'),
        ('universite', 'Université'),
        ('gouvernement', 'Gouvernement'),
        ('autre', 'Autre'),
        ('association', 'Association'),
    ]
    STATUT_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('en_attente', 'En attente'),
    ]

    nom_organisation = models.CharField(max_length=255)
    type_organisation = models.CharField(max_length=30, choices=TYPE_ORGANISATION_CHOICES)
    secteur_activite = models.CharField(max_length=150, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    ville = models.CharField(max_length=100, null=True, blank=True)
    pays = models.CharField(max_length=100, null=True, blank=True)
    email_general = models.EmailField(null=True, blank=True)
    telephone_general = models.CharField(max_length=20, null=True, blank=True)
    logo = models.ImageField(upload_to='logos_organisations/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date_creation = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    class Meta:
        verbose_name = _("Organisation")
        db_table = 'organisation'

    def __str__(self):
        return self.nom_organisation
    
    
    
class MembreOrganisation(ENSPMHubBaseModel):
    ROLE_CHOICES = [
        ('employe', 'Employé'),
        ('administrateur_page', 'Administrateur page'),
    ]

    profil = models.ForeignKey('core.Profil', on_delete=models.CASCADE, related_name='membres_organisations')
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='membres')
    role_organisation = models.CharField(max_length=30, choices=ROLE_CHOICES, default='employe')
    poste = models.CharField(max_length=150, null=True, blank=True)
    est_actif = models.BooleanField(default=True)
    date_joindre = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Membre organisation")
        db_table = 'membre_organisation'
        unique_together = ('profil', 'organisation', 'est_actif')  # Un profil ne peut être membre actif qu'une fois

    def __str__(self):
        return f"{self.profil} - {self.organisation}"


class AbonnementOrganisation(ENSPMHubBaseModel):
    profil = models.ForeignKey('core.Profil', on_delete=models.CASCADE, related_name='abonnements')
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='abonnés')
    date_abonnement = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Abonnement organisation")
        db_table = 'abonnement_organisation'
        unique_together = ('profil', 'organisation')

    def __str__(self):
        return f"{self.profil} suit {self.organisation}"