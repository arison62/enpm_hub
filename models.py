# core/models.py
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from django.apps import apps

# ==========================================
# 1. MANAGERS
# ==========================================
class SoftDeleteManager(models.Manager):
    """Manager qui filtre par défaut les objets supprimés (Soft Delete)"""
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class AllObjectsManager(models.Manager):
    """Manager pour accéder à tous les objets, y compris supprimés (Admin/Audit)"""
    def get_queryset(self):
        return super().get_queryset()
    
class CustomUserManager(BaseUserManager):
    """Manager personnalisé pour la gestion des utilisateurs"""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('L\'adresse email est obligatoire'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('est_actif', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role_systeme', 'super_admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        user = self.create_user(email, password, **extra_fields)
        Profil = apps.get_model('users', 'Profil')
        Profil.objects.create(user=user, nom_complet=extra_fields.get('nom_complet', 'Super Admin'))
        return user
       


# ==========================================
# 2. MODÈLE DE BASE (Abstract)
# ==========================================
class ENSPMHubBaseModel(models.Model):
    """
    Modèle de base pour tous les modèles du projet.
    Intègre UUID, Timestamps et Soft Delete.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de création"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Date de modification"))

    # Soft Delete
    deleted = models.BooleanField(default=False, verbose_name=_("Supprimé"))
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Date de suppression"))

    # Managers
    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True

    def soft_delete(self):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted', 'deleted_at'])

    def restore(self):
        self.deleted = False
        self.deleted_at = None
        self.save(update_fields=['deleted', 'deleted_at'])

# ==========================================
# 1. RÉFÉRENCES ACADÉMIQUES
# ==========================================

class AnneePromotion(ENSPMHubBaseModel):
    """
    Années de sortie valides pour les alumni.
    Permet un contrôle strict et facilite les statistiques par promotion.
    """
    annee = models.SmallIntegerField(
        unique=True,
        validators=[MinValueValidator(1950), MaxValueValidator(2100)],
        verbose_name=_("Année")
    )
    libelle = models.CharField(
        max_length=50,
        verbose_name=_("Libellé"),
        help_text=_("Ex: Promotion 2020, Promo 2020, etc.")
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Informations supplémentaires sur cette promotion")
    )
    est_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Permet de désactiver temporairement une année")
    )
    ordre_affichage = models.IntegerField(
        default=0,
        verbose_name=_("Ordre d'affichage"),
        help_text=_("Plus petit = affiché en premier")
    )

    class Meta:
        verbose_name = _("Année de promotion")
        verbose_name_plural = _("Années de promotion")
        db_table = 'annee_promotion'
        ordering = ['-annee']

    def __str__(self):
        return f"{self.libelle} ({self.annee})"


class Domaine(ENSPMHubBaseModel):
    """
    Domaines d'études et de spécialisation.
    Ex: Génie Civil, Génie Informatique, Génie Mécanique, etc.
    """
    nom = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=_("Nom"),
        help_text=_("Nom complet du domaine")
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("Code"),
        help_text=_("Code court: GCI, GIM, GEL, etc.")
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Présentation du domaine, débouchés, compétences")
    )
    categorie = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("Catégorie"),
        help_text=_("Ex: Génie, Santé, Sciences Sociales")
    )
    est_actif = models.BooleanField(
        default=True,
        verbose_name=_("Actif")
    )
    ordre_affichage = models.IntegerField(
        default=0,
        verbose_name=_("Ordre d'affichage")
    )

    class Meta:
        verbose_name = _("Domaine")
        verbose_name_plural = _("Domaines")
        db_table = 'domaine'
        ordering = ['ordre_affichage', 'nom']

    def __str__(self):
        return f"{self.nom} ({self.code})"


class Filiere(ENSPMHubBaseModel):
    """
    Filières spécifiques au sein des domaines.
    Ex: Domaine "Génie Informatique" → Filières: IA, Cybersécurité, etc.
    """
    NIVEAU_CHOICES = [
        ('licence', 'Licence'),
        ('ingenieur', 'Ingénieur'),
        ('master', 'Master'),
        ('doctorat', 'Doctorat'),
        ('autre', 'Autre'),
    ]

    domaine = models.ForeignKey(
        Domaine,
        on_delete=models.CASCADE,
        related_name='filieres',
        verbose_name=_("Domaine")
    )
    nom = models.CharField(
        max_length=150,
        verbose_name=_("Nom de la filière")
    )
    code = models.CharField(
        max_length=20,
        verbose_name=_("Code")
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description")
    )
    niveau = models.CharField(
        max_length=50,
        choices=NIVEAU_CHOICES,
        verbose_name=_("Niveau")
    )
    duree_annees = models.SmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Durée (années)")
    )
    est_actif = models.BooleanField(
        default=True,
        verbose_name=_("Active")
    )
    ordre_affichage = models.IntegerField(
        default=0,
        verbose_name=_("Ordre d'affichage")
    )

    class Meta:
        verbose_name = _("Filière")
        verbose_name_plural = _("Filières")
        db_table = 'filiere'
        unique_together = ('domaine', 'code')
        ordering = ['domaine', 'ordre_affichage', 'nom']

    def __str__(self):
        return f"{self.domaine.code} - {self.nom}"


# ==========================================
# 2. RÉFÉRENCES PROFESSIONNELLES
# ==========================================

class SecteurActivite(ENSPMHubBaseModel):
    """
    Secteurs d'activité économique pour les organisations.
    Supporte une hiérarchie (secteur parent → sous-secteurs).
    """
    nom = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=_("Nom du secteur")
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("Code"),
        help_text=_("Ex: TECH, BTP, SANTE, FINANCE")
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description")
    )
    categorie_parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='sous_secteurs',
        verbose_name=_("Secteur parent"),
        help_text=_("Permet une hiérarchie: Technologie > Informatique > IA")
    )
    icone = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("Icône")
    )
    est_actif = models.BooleanField(
        default=True,
        verbose_name=_("Actif")
    )
    ordre_affichage = models.IntegerField(
        default=0,
        verbose_name=_("Ordre d'affichage")
    )

    class Meta:
        verbose_name = _("Secteur d'activité")
        verbose_name_plural = _("Secteurs d'activité")
        db_table = 'secteur_activite'
        ordering = ['ordre_affichage', 'nom']

    def __str__(self):
        if self.categorie_parent:
            return f"{self.categorie_parent.nom} > {self.nom}"
        return self.nom

    @property
    def nom_complet(self):
        """Retourne le chemin complet dans la hiérarchie"""
        if self.categorie_parent:
            return f"{self.categorie_parent.nom_complet} > {self.nom}"
        return self.nom


class Poste(ENSPMHubBaseModel):
    """
    Intitulés de postes standardisés.
    Évite les variations: "Développeur", "Dev", "Software Engineer".
    """
    NIVEAU_CHOICES = [
        ('junior', 'Junior'),
        ('intermediaire', 'Intermédiaire'),
        ('senior', 'Senior'),
        ('lead', 'Lead'),
        ('manager', 'Manager'),
        ('directeur', 'Directeur'),
        ('vp', 'Vice-Président'),
        ('c_level', 'C-Level'),
    ]

    titre = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=_("Titre du poste")
    )
    categorie = models.CharField(
        max_length=50,
        verbose_name=_("Catégorie"),
        help_text=_("Ex: Technique, Management, Commercial, RH")
    )
    niveau = models.CharField(
        max_length=50,
        choices=NIVEAU_CHOICES,
        null=True,
        blank=True,
        verbose_name=_("Niveau hiérarchique")
    )
    secteur = models.ForeignKey(
        SecteurActivite,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='postes',
        verbose_name=_("Secteur d'activité")
    )
    synonymes = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Synonymes"),
        help_text=_("Liste des variantes: ['Dev', 'Développeur', 'Software Engineer']")
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description")
    )
    est_actif = models.BooleanField(
        default=True,
        verbose_name=_("Actif")
    )
    ordre_affichage = models.IntegerField(
        default=0,
        verbose_name=_("Ordre d'affichage")
    )

    class Meta:
        verbose_name = _("Poste")
        verbose_name_plural = _("Postes")
        db_table = 'poste'
        ordering = ['categorie', 'ordre_affichage', 'titre']

    def __str__(self):
        return self.titre


# ==========================================
# 3. RÉFÉRENCES FINANCIÈRES
# ==========================================

class Devise(ENSPMHubBaseModel):
    """
    Devises monétaires pour les salaires et prix de formation.
    Permet la conversion et l'affichage cohérent.
    """
    code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_("Code"),
        help_text=_("Code ISO 4217: XAF, EUR, USD")
    )
    nom = models.CharField(
        max_length=100,
        verbose_name=_("Nom complet")
    )
    symbole = models.CharField(
        max_length=10,
        verbose_name=_("Symbole"),
        help_text=_("FCFA, €, $")
    )
    taux_change_usd = models.DecimalField(
        max_digits=15,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name=_("Taux de change USD"),
        help_text=_("1 USD = X devise (mis à jour régulièrement)")
    )
    date_mise_a_jour_taux = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Date mise à jour du taux")
    )
    est_active = models.BooleanField(
        default=True,
        verbose_name=_("Active")
    )
    ordre_affichage = models.IntegerField(
        default=0,
        verbose_name=_("Ordre d'affichage"),
        help_text=_("XAF en premier pour le Cameroun")
    )

    class Meta:
        verbose_name = _("Devise")
        verbose_name_plural = _("Devises")
        db_table = 'devise'
        ordering = ['ordre_affichage', 'nom']

    def __str__(self):
        return f"{self.code} ({self.symbole})"


# ==========================================
# 4. RÉFÉRENCES TITRES & HONORIFIQUES
# ==========================================

class TitreHonorifique(ENSPMHubBaseModel):
    """
    Titres honorifiques et académiques.
    Ex: Dr., Prof., Ing., M., Mme
    """
    TYPE_TITRE_CHOICES = [
        ('academique', 'Académique'),
        ('professionnel', 'Professionnel'),
        ('honorifique', 'Honorifique'),
        ('civilite', 'Civilité'),
    ]

    titre = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("Titre"),
        help_text=_("Abréviation: Dr., Prof., Ing.")
    )
    nom_complet = models.CharField(
        max_length=100,
        verbose_name=_("Nom complet"),
        help_text=_("Docteur, Professeur, Ingénieur")
    )
    type_titre = models.CharField(
        max_length=20,
        choices=TYPE_TITRE_CHOICES,
        verbose_name=_("Type de titre")
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Explication du titre, conditions d'obtention")
    )
    est_actif = models.BooleanField(
        default=True,
        verbose_name=_("Actif")
    )
    ordre_affichage = models.IntegerField(
        default=0,
        verbose_name=_("Ordre d'affichage")
    )

    class Meta:
        verbose_name = _("Titre honorifique")
        verbose_name_plural = _("Titres honorifiques")
        db_table = 'titre_honorifique'
        ordering = ['ordre_affichage', 'titre']

    def __str__(self):
        return f"{self.titre} ({self.nom_complet})"


# ==========================================
# 5. RÉFÉRENCES RÉSEAUX SOCIAUX
# ==========================================

class ReseauSocial(ENSPMHubBaseModel):
    """
    Réseaux sociaux et plateformes professionnelles.
    Plus flexible que des choices hardcodés.
    """
    TYPE_RESEAU_CHOICES = [
        ('professionnel', 'Professionnel'),
        ('social', 'Social'),
        ('academique', 'Académique'),
        ('technique', 'Technique'),
        ('portfolio', 'Portfolio'),
    ]

    nom = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Nom"),
        help_text=_("LinkedIn, Facebook, GitHub, etc.")
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("Code"),
        help_text=_("linkedin, facebook, github (minuscules, sans espaces)")
    )
    url_base = models.URLField(
        verbose_name=_("URL de base"),
        help_text=_("https://linkedin.com/in/, https://github.com/")
    )
    icone = models.CharField(
        max_length=50,
        verbose_name=_("Icône"),
        help_text=_("Classe Font Awesome: fab fa-linkedin")
    )
    couleur_brand = models.CharField(
        max_length=7,
        verbose_name=_("Couleur de marque"),
        help_text=_("Code hexadécimal: #0077B5 pour LinkedIn")
    )
    type_reseau = models.CharField(
        max_length=20,
        choices=TYPE_RESEAU_CHOICES,
        verbose_name=_("Type de réseau")
    )
    pattern_validation = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Pattern de validation"),
        help_text=_("Expression régulière pour valider l'URL")
    )
    placeholder_exemple = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Exemple de placeholder"),
        help_text=_("Ex: votre-nom ou username")
    )
    est_actif = models.BooleanField(
        default=True,
        verbose_name=_("Actif")
    )
    ordre_affichage = models.IntegerField(
        default=0,
        verbose_name=_("Ordre d'affichage")
    )

    class Meta:
        verbose_name = _("Réseau social")
        verbose_name_plural = _("Réseaux sociaux")
        db_table = 'reseau_social'
        ordering = ['ordre_affichage', 'nom']

    def __str__(self):
        return self.nom



# ==========================================
# 3. AUTHENTIFICATION : USER
# ==========================================
class User(AbstractBaseUser, PermissionsMixin, ENSPMHubBaseModel):
    """Modèle d'authentification minimal"""
    ROLE_SYSTEME_CHOICES = [
        ('user', 'Utilisateur'),
        ('admin_site', 'Administrateur site'),
        ('super_admin', 'Super Administrateur'),
    ]

    email = models.EmailField(unique=True, verbose_name=_("Adresse email"))
    mot_de_passe = models.CharField(max_length=255, editable=False, null=True, blank=True)  # Django gère déjà le hash
    role_systeme = models.CharField(max_length=20, choices=ROLE_SYSTEME_CHOICES, default='user',
                                    verbose_name=_("Rôle système"))
    last_login = models.DateTimeField(null=True, blank=True, verbose_name=_("Dernière connexion"))
    est_actif = models.BooleanField(default=True, verbose_name=_("Compte actif"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Accès admin Django"))

    # Permissions Django
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name="ensp_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name="ensp_user_set",
        related_query_name="user",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
        db_table = 'users'

    def __str__(self):
        return self.email

    @property
    def is_active(self):
        return self.est_actif and not self.deleted




class AuditLog(ENSPMHubBaseModel):
    """Journal d'audit pour la traçabilité complète des actions."""

    class AuditAction(models.TextChoices):
        CREATE = 'CREATE', _('Create')
        UPDATE = 'UPDATE', _('Update')
        DELETE = 'DELETE', _('Delete')
        VIEW = 'VIEW', _('View')
        ACCESS_DENIED = 'ACCESS_DENIED', _('Access denied')

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs',
        verbose_name=_("Utilisateur")
    )
    action = models.CharField(
        max_length=20,
        choices=AuditAction.choices,
        verbose_name=_('Action'),
        db_index=True
    )

    # Informations sur l'entité concernée
    entity_type = models.CharField(
        max_length=100,
        verbose_name=_('Type d\'entité'),
        db_index=True
    )
    entity_id = models.UUIDField(verbose_name=_('ID de l\'entité'), db_index=True)

    # Détails des changements
    old_values = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_('Anciennes valeurs')
    )
    new_values = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_('Nouvelles valeurs')
    )

    # Informations de connexion
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_('Adresse IP')
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name=_('User agent')
    )

    class Meta:
        verbose_name = _("Journal d'audit")
        verbose_name_plural = _("Journaux d'audit")
        db_table = 'audit_log'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.action} on {self.entity_type} "


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
        verbose_name = _("Lien réseau social utilisateur")
        db_table = 'lien_reseau_social_profil'
        indexes = [
            models.Index(fields=['nom_complet']),
            models.Index(fields=['statut_global', '-created_at']),
            models.Index(fields=['domaine', 'annee_sortie']),
        ]
      

    def __str__(self):
        return f"{self.reseau.nom} - {self.profil.nom_complet}"


# opportunities/models.py
from django.db import models
from core.models import ENSPMHubBaseModel
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


class Stage(ENSPMHubBaseModel):
    """Modèle pour les offres de stage"""
    TYPE_STAGE_CHOICES = [
        ('ouvrier', 'Ouvrier'),
        ('academique', 'Académique'),
        ('professionnel', 'Professionnel')
    ]
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente de validation'),
        ('active', 'Active'),
        ('expiree', 'Expirée'),
        ('pourvue', 'Pourvue'),
        ('rejetee', 'Rejetée')
    ]

    # Relations
    createur_profil = models.ForeignKey(
        'users.Profil',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='stages_crees',
        verbose_name=_("Créateur")
    )
    organisation = models.ForeignKey(
        'organizations.Organisation',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='stages',
        verbose_name=_("Organisation")
    )
    
    # Informations principales
    titre = models.CharField(max_length=255, verbose_name=_("Titre du stage"))
    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Slug"),
        help_text=_("Identifiant unique pour les URLs")
    )
    nom_structure = models.CharField(max_length=255, verbose_name=_("Nom de la structure"))
    description = models.TextField(verbose_name=_("Description"))
    type_stage = models.CharField(max_length=20, choices=TYPE_STAGE_CHOICES, verbose_name=_("Type de stage"))
    
    # Localisation
    adresse = models.CharField(max_length=150, verbose_name=_("Lieu"))
    ville = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Ville"))
    pays = CountryField(null=True, blank=True, verbose_name=_("Pays"))
    
    # Contact
    email_contact = models.EmailField(null=True, blank=True, verbose_name=_("Email de contact"))
    telephone_contact = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Téléphone"))
    
    # Liens
    lien_offre_original = models.URLField(null=True, blank=True, verbose_name=_("Lien offre originale"))
    lien_candidature = models.URLField(null=True, blank=True, verbose_name=_("Lien candidature"))
    
    # Dates
    date_debut = models.DateField(null=True, blank=True, verbose_name=_("Date de début"))
    date_fin = models.DateField(null=True, blank=True, verbose_name=_("Date de fin"))
    date_publication = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de publication"))
    
    # Statut et validation
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente', verbose_name=_("Statut"))
    est_valide = models.BooleanField(default=False, verbose_name=_("Validé"))
    validateur_profil = models.ForeignKey(
        'users.Profil',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='stages_valides',
        verbose_name=_("Validateur")
    )
    date_validation = models.DateTimeField(null=True, blank=True, verbose_name=_("Date de validation"))
    commentaire_validation = models.TextField(null=True, blank=True, verbose_name=_("Commentaire de validation"))

    class Meta:
        verbose_name = _("Stage")
        verbose_name_plural = _("Stages")
        db_table = 'stage'
        ordering = ['-date_publication']
        indexes = [
            models.Index(fields=['statut', '-date_publication']),
            models.Index(fields=['ville', 'pays']),
            models.Index(fields=['type_stage', 'statut']),
        ]

    def __str__(self):
        return self.titre


class Emploi(ENSPMHubBaseModel):
    """Modèle pour les offres d'emploi"""
    TYPE_EMPLOI_CHOICES = [
        ('temps_plein_terrain', 'Temps plein terrain'),
        ('temps_partiel_terrain', 'Temps partiel terrain'),
        ('temps_plein_ligne', 'Temps plein en ligne'),
        ('temps_partiel_ligne', 'Temps partiel en ligne'),
        ('freelance', 'Freelance'),
        ('contrat', 'Contrat')
    ]
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente de validation'),
        ('active', 'Active'),
        ('expiree', 'Expirée'),
        ('pourvue', 'Pourvue'),
        ('rejetee', 'Rejetée')
    ]

    # Relations
    createur_profil = models.ForeignKey(
        'users.Profil',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='emplois_crees',
        verbose_name=_("Créateur")
    )
    organisation = models.ForeignKey(
        'organizations.Organisation',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='emplois',
        verbose_name=_("Organisation")
    )
    
    # Informations principales
    titre = models.CharField(max_length=255, verbose_name=_("Titre du poste"))
    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Slug")
    )
    nom_structure = models.CharField(max_length=255, verbose_name=_("Nom de la structure"))
    description = models.TextField(verbose_name=_("Description"))
    type_emploi = models.CharField(
        max_length=40,
        choices=TYPE_EMPLOI_CHOICES,
        null=True,
        blank=True,
        verbose_name=_("Type d'emploi")
    )
    
    # Localisation
    adresse = models.CharField(max_length=150, verbose_name=_("Lieu"))
    ville = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Ville"))
    pays = CountryField(null=True, blank=True, verbose_name=_("Pays"))

    
    # Contact
    email_contact = models.EmailField(null=True, blank=True, verbose_name=_("Email de contact"))
    telephone_contact = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Téléphone"))
    
    # Liens
    lien_offre_original = models.URLField(null=True, blank=True, verbose_name=_("Lien offre originale"))
    lien_candidature = models.URLField(null=True, blank=True, verbose_name=_("Lien candidature"))
    
    # Dates
    date_publication = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de publication"))
    date_expiration = models.DateField(null=True, blank=True, verbose_name=_("Date d'expiration"))
    
    # Salaire
    salaire_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salaire_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    devise = models.ForeignKey(
        'core.Devise',
        on_delete=models.PROTECT,
        related_name='emplois',
        verbose_name=_("Devise")
    )
    # Statut et validation
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente', verbose_name=_("Statut"))
    est_valide = models.BooleanField(default=False, verbose_name=_("Validé"))
    validateur_profil = models.ForeignKey(
        'users.Profil',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='emplois_valides',
        verbose_name=_("Validateur")
    )
    date_validation = models.DateTimeField(null=True, blank=True, verbose_name=_("Date de validation"))
    commentaire_validation = models.TextField(null=True, blank=True, verbose_name=_("Commentaire de validation"))

    class Meta:
        verbose_name = _("Emploi")
        verbose_name_plural = _("Emplois")
        db_table = 'emploi'
        ordering = ['-date_publication']
        indexes = [
            models.Index(fields=['statut', 'est_valide'], name='emploi_statut_est_valide'),
            models.Index(fields=['date_publication'], name='emploi_date_publication'),   
        ]

    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Validation des salaires
        if self.salaire_min and self.salaire_max:
            if self.salaire_min > self.salaire_max:
                raise ValidationError({
                    'salaire_max': _("Le salaire maximum doit être supérieur au minimum")
                })
        
        # Validation de la devise si salaire présent
        if (self.salaire_min or self.salaire_max) and not self.devise:
            raise ValidationError({
                'devise': _("La devise est obligatoire si un salaire est spécifié")
            })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.titre


class Formation(ENSPMHubBaseModel):
    """Modèle pour les formations"""
    TYPE_FORMATION_CHOICES = [
        ('en_ligne', 'En ligne'),
        ('presentiel', 'Présentiel'),
        ('hybride', 'Hybride')
    ]
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente de validation'),
        ('active', 'Active'),
        ('expiree', 'Expirée'),
        ('annulee', 'Annulée'),
        ('rejetee', 'Rejetée')
    ]

    # Relations
    createur_profil = models.ForeignKey(
        'users.Profil',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='formations_creees',
        verbose_name=_("Créateur")
    )
    organisation = models.ForeignKey(
        'organizations.Organisation',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='formations',
        verbose_name=_("Organisation")
    )
    
    # Informations principales
    titre = models.CharField(max_length=255, verbose_name=_("Titre de la formation"))
    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Slug")
    )
    nom_structure = models.CharField(max_length=255, verbose_name=_("Nom de la structure"))
    description = models.TextField(verbose_name=_("Description"))
    type_formation = models.CharField(
        max_length=20,
        choices=TYPE_FORMATION_CHOICES,
        verbose_name=_("Type de formation")
    )
    
    # Localisation
    adresse = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("Lieu"))
    ville = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Ville"))
    pays = CountryField(null=True, blank=True, verbose_name=_("Pays"))
    
    # Contact
    email_contact = models.EmailField(null=True, blank=True, verbose_name=_("Email de contact"))
    telephone_contact = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Téléphone"))
    
    # Liens
    lien_formation = models.URLField(null=True, blank=True, verbose_name=_("Lien de la formation"))
    lien_inscription = models.URLField(null=True, blank=True, verbose_name=_("Lien d'inscription"))
    
    # Dates
    date_debut = models.DateField(null=True, blank=True, verbose_name=_("Date de début"))
    date_fin = models.DateField(null=True, blank=True, verbose_name=_("Date de fin"))
    date_publication = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de publication"))
    
    # Prix
    est_payante = models.BooleanField(default=False, verbose_name=_("Formation payante"))
    prix = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    devise = models.ForeignKey(
        'core.Devise',
        on_delete=models.PROTECT,
        related_name='formations',
        verbose_name=_("Devise")
    )
    # Durée
    duree_heures = models.IntegerField(null=True, blank=True, verbose_name=_("Durée en heures"))
    
    # Statut et validation
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente', verbose_name=_("Statut"))
    est_valide = models.BooleanField(default=False, verbose_name=_("Validé"))
    validateur_profil = models.ForeignKey(
        'users.Profil',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='formations_validees',
        verbose_name=_("Validateur")
    )
    date_validation = models.DateTimeField(null=True, blank=True, verbose_name=_("Date de validation"))
    commentaire_validation = models.TextField(null=True, blank=True, verbose_name=_("Commentaire de validation"))

    class Meta:
        verbose_name = _("Formation")
        verbose_name_plural = _("Formations")
        db_table = 'formation'
        ordering = ['-date_publication']

    def __str__(self):
        return self.titre
    
    
# organizations/models.py
from django.db import models
from core.models import ENSPMHubBaseModel
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

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
    secteur_activite = models.ForeignKey(
        'core.SecteurActivite',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='organisations',
        verbose_name=_("Secteur d'activité")
    )
    adresse = models.TextField(null=True, blank=True, verbose_name=_("Adresse"))
    ville = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Ville"))
    pays = CountryField(null=True, blank=True, verbose_name=_("Pays"))
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
        'users.Profil',
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
    poste = models.ForeignKey(
        'core.Poste',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='membres',
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
        'users.Profil',
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


 
    
