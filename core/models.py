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
        extra_fields.setdefault('role', 'super_admin')
        extra_fields.setdefault('statut', 'personnel_technique') # Valeur par défaut cohérente

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
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de création"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Date de modification"))
    
    # Soft Delete
    deleted = models.BooleanField(default=False, verbose_name=_("Supprimé"))
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Date de suppression"))

    # Managers
    objects = SoftDeleteManager()      # Par défaut : cache les supprimés
    all_objects = AllObjectsManager()  # Accès total : admin/audit

    class Meta:
        abstract = True

    def soft_delete(self):
        """Effectue une suppression logique"""
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Restaure un élément supprimé"""
        self.deleted = False
        self.deleted_at = None
        self.save()

# ==========================================
# 3. MODÈLE UTILISATEUR
# ==========================================

class User(AbstractBaseUser, PermissionsMixin, ENSPMHubBaseModel):
    """
    Modèle utilisateur personnalisé adapté aux besoins ENSPM Hub.
    Remplace le modèle User par défaut de Django.
    """
    
    # Choix basés sur database.md et tasks.md
    STATUT_CHOICES = [
        ('etudiant', 'Étudiant'),
        ('enseignant', 'Enseignant'),
        ('directeur', 'Directeur'),
        ('partenaire', 'Partenaire'),
        ('personnel_admin', 'Personnel Administratif'),
        ('personnel_technique', 'Personnel Technique'),
    ]

    ROLE_CHOICES = [
        ('user', 'Utilisateur'),
        ('admin', 'Administrateur'),
        ('super_admin', 'Super Administrateur'),
    ]

    # Champs d'identification
    nom = models.CharField(max_length=255, verbose_name=_("Nom"))
    prenom = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Prenon de l'utilisateur"))
    email = models.EmailField(unique=True, verbose_name=_("Adresse email"))
    matricule = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name=_("Matricule"))
    
    # Informations métier
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, verbose_name=_("Statut"))
    titre = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Titre (ex: Ing., Dr.)"))
    travailleur = models.BooleanField(default=False, verbose_name=_("Est travailleur"))
    annee_sortie = models.SmallIntegerField(null=True, blank=True, verbose_name=_("Année de sortie"))
    telephone = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Téléphone"))
    bio = models.TextField(null=True, blank=True, verbose_name=_("Description sur l'utilisateur"))
    photo_profile = models.ImageField(upload_to="profils/", blank=True, null=True)
    domaine = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Domaine d'étude"))
    
    # Rôles et Permissions
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user', verbose_name=_("Rôle système"))
    
    # Champs Django requis (PermissionsMixin & AbstractBaseUser)
    est_actif = models.BooleanField(default=True, verbose_name=_("Compte actif")) # Remplace is_active
    is_staff = models.BooleanField(default=False, verbose_name=_("Accès admin Django")) # Requis pour l'admin Django
    
    # Configuration du modèle
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom']

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
        db_table = 'user'
        
    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.email})"

    @property
    def is_active(self):
        """Alias pour que Django Admin fonctionne avec notre champ 'est_actif'"""
        return self.est_actif and not self.deleted