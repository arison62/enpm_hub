# users/models.py
from django.db import models
from core.models import ENSPMHubBaseModel
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

class Profil(ENSPMHubBaseModel):
    STATUT_GLOBAL_CHOICES = [
        ('etudiant', 'Étudiant'),
        ('alumni', 'Alumni'),
        ('enseignant', 'Enseignant'),
        ('personnel_admin', 'Personnel Administratif'),
        ('personnel_technique', 'Personnel Technique'),
        ('partenaire', 'Partenaire'),
    ]
    user = models.OneToOneField("core.User", on_delete=models.CASCADE, related_name='profil')
    nom_complet = models.CharField(max_length=255, verbose_name=_("Nom complet"))
    matricule = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name=_("Matricule"), db_index=True)
    
    titre = models.ForeignKey(
        'core.TitreHonorifique',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='profils',
        verbose_name=_("Titre")
    )
    
    statut_global = models.CharField(max_length=30, choices=STATUT_GLOBAL_CHOICES, verbose_name=_("Statut global"))
    travailleur = models.BooleanField(default=False, verbose_name=_("Travailleur"))
    
    annee_sortie = models.ForeignKey(
        'core.AnneePromotion',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='profils',
        verbose_name=_("Promotion")
    )
    
    adresse = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Adresse"))
    telephone = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Téléphone"))
    
    ville = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Ville"))
    
    pays = CountryField(null=True, blank=True, verbose_name=_("Pays"))
    
    photo_profil = models.ImageField(upload_to='photos_profils/', null=True, blank=True, verbose_name=_("Photo de profil"))
    
    domaine = models.ForeignKey(
        'core.Domaine',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='profils',
        verbose_name=_("Domaine")
    )
    
    bio = models.TextField(null=True, blank=True, verbose_name=_("Bio"))
    slug = models.SlugField(unique=True, null=True, blank=True, verbose_name=_("Slug"), db_index=True)

    class Meta:
        verbose_name = _("Profil")
        db_table = 'profil'

    def __str__(self):
        return self.nom_complet or self.user.email
    
class LienReseauSocialProfil(ENSPMHubBaseModel):
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE, related_name='liens_reseaux')
    
    reseau = models.ForeignKey(
        'core.ReseauSocial',
        on_delete=models.CASCADE,
        related_name='liens',
        verbose_name=_("Réseau social")
    )
    
    url = models.URLField(verbose_name=_("URL"))
    est_actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _("Lien de résseau social")
        db_table = 'lien_reseau_social_profil'

    def __str__(self):
        return f"{self.reseau.nom} - {self.profil.nom_complet}"
