# core/models.py
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


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

        return self.create_user(email, password, **extra_fields)


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
# 3. AUTHENTIFICATION : USER & PROFIL
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


class Profil(ENSPMHubBaseModel):
    """Profil riche lié 1:1 à User"""
    STATUT_GLOBAL_CHOICES = [
        ('etudiant', 'Étudiant'),
        ('alumni', 'Alumni'),
        ('enseignant', 'Enseignant'),
        ('personnel_admin', 'Personnel Administratif'),
        ('personnel_technique', 'Personnel Technique'),
        ('partenaire', 'Partenaire'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    nom_complet = models.CharField(max_length=255, verbose_name=_("Nom complet"))
    matricule = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name=_("Matricule"))
    titre = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Titre (Dr., Prof., etc.)"))
    statut_global = models.CharField(max_length=30, choices=STATUT_GLOBAL_CHOICES, verbose_name=_("Statut global"))
    travailleur = models.BooleanField(default=False, verbose_name=_("Travailleur"))
    annee_sortie = models.SmallIntegerField(null=True, blank=True, verbose_name=_("Année de sortie"))
    telephone = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Téléphone"))
    photo_profil = models.ImageField(upload_to='photos_profils/', null=True, blank=True, verbose_name=_("Photo de profil"))
    domaine = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Domaine"))
    bio = models.TextField(null=True, blank=True, verbose_name=_("Bio"))

    class Meta:
        verbose_name = _("Profil")
        db_table = 'profil'

    def __str__(self):
        return self.nom_complet or self.user.email
    

# ==========================================
# 4. RÉSEAUX SOCIAUX
# ==========================================
class LienReseauSocial(ENSPMHubBaseModel):
    NOM_RESEAU_CHOICES = [
        ('LinkedIn', 'LinkedIn'),
        ('Facebook', 'Facebook'),
        ('Twitter', 'Twitter'),
        ('Instagram', 'Instagram'),
        ('GitHub', 'GitHub'),
        ('ResearchGate', 'ResearchGate'),
        ('GoogleScholar', 'Google Scholar'),
        ('SiteWeb', 'Site Web'),
        ('Portfolio', 'Portfolio'),
    ]

    profil = models.ForeignKey(Profil, on_delete=models.CASCADE, related_name='liens_reseaux')
    nom_reseau = models.CharField(max_length=50, choices=NOM_RESEAU_CHOICES)
    url = models.URLField(verbose_name=_("URL"))
    est_actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Lien réseau social")
        db_table = 'lien_reseau_social'

    def __str__(self):
        return f"{self.nom_reseau} - {self.url}"



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
