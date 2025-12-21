# core/api/schemas.py
from math import ceil
from typing import Optional, List
from ninja import Schema, Field, ModelSchema
from pydantic import UUID4
from datetime import datetime
from core.models import User, Profil, LienReseauSocial


# ==========================================
# 1. Schémas d'authentification
# ==========================================
class LoginSchema(Schema):
    """Schéma d'entrée pour l'authentification (email uniquement)"""
    email: str = Field(..., description="Adresse email de l'utilisateur")
    password: str = Field(..., description="Mot de passe")


class TokenSchema(Schema):
    """Schéma de sortie après connexion réussie"""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    user: "UserSchema"


class RefreshTokenSchema(Schema):
    """Schéma pour rafraîchir le token"""
    refresh: str


class EmailSchema(Schema):
    """Schéma simple pour les opérations basées sur l'email."""
    email: str


# ==========================================
# 2. Schémas Profil (données riches)
# ==========================================
class ProfilOutSchema(ModelSchema):
    """Schéma de sortie pour le Profil (inclut l'URL de la photo)"""
    photo_profil: Optional[str] = None  # On expose l'URL

    class Meta:
        model = Profil
        fields = [
            'id', 'nom_complet', 'matricule', 'titre', 'statut_global', 'slug',
            'travailleur', 'annee_sortie', 'telephone', 'domaine',
            'bio', 'photo_profil'
        ]

    @staticmethod
    def resolve_photo_profil(obj):
        return obj.photo_profil.url if obj.photo_profil else None


class ProfilCreateSchema(Schema):
    """Schéma pour création du Profil (lors de la création utilisateur)"""
    nom_complet: str
    matricule: Optional[str] = None
    titre: Optional[str] = None
    statut_global: Optional[str] = "etudiant"
    travailleur: Optional[bool] = False
    annee_sortie: Optional[int] = None
    telephone: Optional[str] = None
    domaine: Optional[str] = None
    bio: Optional[str] = None


class ProfilUpdateSchema(Schema):
    """Schéma pour mise à jour partielle du Profil"""
    nom_complet: Optional[str] = None
    matricule: Optional[str] = None
    titre: Optional[str] = None
    statut_global: Optional[str] = None
    travailleur: Optional[bool] = None
    annee_sortie: Optional[int] = None
    telephone: Optional[str] = None
    domaine: Optional[str] = None
    bio: Optional[str] = None


# ==========================================
# 3. Schémas Utilisateur complets
# ==========================================

class UserSchema(Schema):
    """
    Schéma retourné login
    """
    id: UUID4
    email: str
    role_systeme: str
    est_actif: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class UserDetailSchema(Schema):
    """Schéma complet retourné get me"""
    id: UUID4
    email: str
    role_systeme: str
    est_actif: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    profil: ProfilOutSchema

# ==========================================
# 4. Schémas Admin (création/mise à jour complète)
# ==========================================
class UserCreateAdminSchema(Schema):
    """Pour création par un admin"""
    email: str
    role_systeme: Optional[str] = "user"
    profil: ProfilCreateSchema


class UserUpdateAdminSchema(Schema):
    """Pour mise à jour par un admin"""
    email: Optional[str] = None
    role_systeme: Optional[str] = None
    est_actif: Optional[bool] = None

    profil: Optional[ProfilUpdateSchema] = None


# ==========================================
# 5. Schémas Photo de profil
# ==========================================
class PhotoUploadResponseSchema(Schema):
    """Réponse après upload réussi de photo"""
    message: str = "Photo de profil mise à jour avec succès"
    photo_profil: Optional[str] = None


class PhotoDeleteResponseSchema(Schema):
    """Réponse après suppression de photo"""
    message: str = "Photo de profil supprimée avec succès"


# ==========================================
# 6. Filtres de recherche
# ==========================================
class UserFilterSchema(Schema):
    """Filtres pour endpoint de liste utilisateurs"""
    search: Optional[str] = Field(
        None,
        description="Recherche dans nom complet, email, matricule, téléphone, domaine"
    )
    role_systeme: Optional[str] = Field(None, description="Filtrer par rôle système")
    statut_global: Optional[str] = Field(None, description="Filtrer par statut (etudiant, alumni, etc.)")
    est_actif: Optional[bool] = Field(None, description="Filtrer par compte actif")
    travailleur: Optional[bool] = Field(None, description="Filtrer par statut travailleur")




# ==========================================
# SCHÉMAS RÉSEAUX SOCIAUX
# ==========================================

class LienReseauSocialSchema(ModelSchema):
    """Schéma de sortie pour un lien réseau social"""
    class Meta:
        model = LienReseauSocial
        fields = ['id', 'nom_reseau', 'url', 'est_actif', 'created_at']


class LienReseauSocialCreateSchema(Schema):
    """Schéma pour création d'un lien réseau social"""
    nom_reseau: str = Field(
        ..., 
        description="Nom du réseau (LinkedIn, GitHub, etc.)"
    )
    url: str = Field(..., description="URL du profil")


class LienReseauSocialUpdateSchema(Schema):
    """Schéma pour mise à jour d'un lien réseau social"""
    url: Optional[str] = Field(None, description="Nouvelle URL")
    est_actif: Optional[bool] = Field(None, description="Statut actif/inactif")


# ==========================================
# SCHÉMAS MOT DE PASSE
# ==========================================

class ChangePasswordSchema(Schema):
    """Schéma pour changement de mot de passe par l'utilisateur"""
    old_password: str = Field(..., description="Ancien mot de passe")
    new_password: str = Field(
        ..., 
        min_length=8,
        description="Nouveau mot de passe (min. 8 caractères)"
    )


class ResetPasswordSchema(Schema):
    """Schéma pour réinitialisation de mot de passe par admin"""
    new_password: Optional[str] = Field(
        None,
        min_length=8,
        description="Nouveau mot de passe (généré automatiquement si non fourni)"
    )


class PasswordResponseSchema(Schema):
    """Schéma de réponse après réinitialisation de mot de passe"""
    message: str
    temporary_password: Optional[str] = None


# ==========================================
# SCHÉMAS PROFIL COMPLET (avec réseaux sociaux)
# ==========================================

class ProfilCompleteSchema(ModelSchema):
    """Schéma de sortie complet du Profil avec réseaux sociaux"""
    photo_profil: Optional[str] = None
    liens_reseaux: List[LienReseauSocialSchema] = []

    class Meta:
        model = Profil
        fields = [
            'id', 'nom_complet', 'matricule', 'titre', 'statut_global',
            'travailleur', 'annee_sortie', 'telephone', 'domaine',
            'bio', 'photo_profil', 'slug', 'created_at', 'updated_at'
        ]

    @staticmethod
    def resolve_photo_profil(obj):
        return obj.photo_profil.url if obj.photo_profil else None
    
    @staticmethod
    def resolve_liens_reseaux(obj):
        return [
            LienReseauSocialSchema.from_orm(lien) 
            for lien in obj.liens_reseaux.filter(est_actif=True)
        ]


class UserCompleteSchema(Schema):
    """Schéma utilisateur complet avec profil et réseaux sociaux"""
    id: UUID4
    email: str
    role_systeme: str
    est_actif: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    profil: ProfilCompleteSchema


# ==========================================
# SCHÉMAS LISTE PAGINÉE
# ==========================================

class PaginationMetaSchema(Schema):
    """Métadonnées de pagination"""
    page: int
    page_size: int
    total_items: int
    total_pages: int


class UserListResponseSchema(Schema):
    """Réponse paginée pour liste d'utilisateurs"""
    items: List[UserCompleteSchema]
    meta: PaginationMetaSchema


# ==========================================
# SCHÉMAS STATISTIQUES
# ==========================================

class UserStatisticsSchema(Schema):
    """Schéma pour les statistiques utilisateurs"""
    total_users: int
    active_users: int
    inactive_users: int
    deleted_users: int
    by_role: dict
    by_status: dict


# ==========================================
# SCHÉMAS GESTION COMPTE
# ==========================================

class ToggleStatusSchema(Schema):
    """Schéma pour activer/désactiver un compte"""
    est_actif: bool = Field(..., description="True pour activer, False pour désactiver")


class SlugUpdateSchema(Schema):
    """Schéma pour mise à jour du slug personnalisé"""
    slug: str = Field(
        ..., 
        min_length=3,
        max_length=100,
        description="Nouveau slug personnalisé (sera slugifié automatiquement)"
    )

# ==========================================
# 7. Schémas d'erreur standardisés
# ==========================================
class MessageSchema(Schema):
    """Schéma de réponse pour les messages simples (erreurs, succès)."""
    detail: str


class FieldErrorSchema(Schema):
    """Détail d'une erreur de validation pour un champ spécifique."""
    field: str
    message: str


class ValidationErrorSchema(Schema):
    """Schéma pour les erreurs de validation (422)."""
    detail: str = "Erreur de validation."
    errors: List[FieldErrorSchema]
