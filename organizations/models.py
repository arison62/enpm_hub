# organizations/models.py
from django.db import models
from core.models import ENSPMHubBaseModel
from django.utils.translation import gettext_lazy as _


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

    nom_organisation = models.CharField(max_length=255, verbose_name=_("Nom de l'organisation"))
    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Slug"),
        db_index=True,
        help_text=_("Identifiant unique pour les URLs (ex: ensp-maroua-x7r2p9)")
    )
    type_organisation = models.CharField(
        max_length=30,
        choices=TYPE_ORGANISATION_CHOICES,
        verbose_name=_("Type d'organisation")
    )
    secteur_activite = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name=_("Secteur d'activité")
    )
    adresse = models.TextField(null=True, blank=True, verbose_name=_("Adresse"))
    ville = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Ville"))
    pays = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Pays"))
    email_general = models.EmailField(null=True, blank=True, verbose_name=_("Email général"))
    telephone_general = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name=_("Téléphone général")
    )
    logo = models.ImageField(
        upload_to='logos_organisations/',
        null=True,
        blank=True,
        verbose_name=_("Logo")
    )
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    date_creation = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date de création de l'organisation")
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente',
        verbose_name=_("Statut")
    )

    class Meta:
        verbose_name = _("Organisation")
        verbose_name_plural = _("Organisations")
        db_table = 'organisation'
        ordering = ['nom_organisation']

    def __str__(self):
        return self.nom_organisation


class MembreOrganisation(ENSPMHubBaseModel):
    ROLE_CHOICES = [
        ('employe', 'Employé'),
        ('administrateur_page', 'Administrateur page'),
    ]

    profil = models.ForeignKey(
        'core.Profil',
        on_delete=models.CASCADE,
        related_name='membres_organisations',
        verbose_name=_("Profil")
    )
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name='membres',
        verbose_name=_("Organisation")
    )
    role_organisation = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default='employe',
        verbose_name=_("Rôle dans l'organisation")
    )
    poste = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name=_("Poste")
    )
    est_actif = models.BooleanField(default=True, verbose_name=_("Membre actif"))
    date_joindre = models.DateField(auto_now_add=True, verbose_name=_("Date d'adhésion"))
    
    class Meta:
        verbose_name = _("Membre organisation")
        verbose_name_plural = _("Membres organisations")
        db_table = 'membre_organisation'
        unique_together = ('profil', 'organisation', 'est_actif')
        ordering = ['profil__nom_complet']

    def __str__(self):
        return f"{self.profil} - {self.organisation}"


class AbonnementOrganisation(ENSPMHubBaseModel):
    profil = models.ForeignKey(
        'core.Profil',
        on_delete=models.CASCADE,
        related_name='abonnements',
        verbose_name=_("Profil")
    )
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name='abonnes',
        verbose_name=_("Organisation")
    )
    date_abonnement = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date d'abonnement")
    )

    class Meta:
        verbose_name = _("Abonnement organisation")
        verbose_name_plural = _("Abonnements organisations")
        db_table = 'abonnement_organisation'
        unique_together = ('profil', 'organisation')
        ordering = ['-date_abonnement']

    def __str__(self):
        return f"{self.profil} suit {self.organisation}"

