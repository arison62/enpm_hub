# core/api/schemas.py
from typing import Optional, List
from ninja import Schema, Field, ModelSchema
from pydantic import UUID4
from datetime import datetime
from core.models import User, Profil


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


# ==========================================
# 2. Schémas Profil (données riches)
# ==========================================
class ProfilOutSchema(ModelSchema):
    """Schéma de sortie pour le Profil (inclut l'URL de la photo)"""
    photo_profil: Optional[str] = None  # On expose l'URL

    class Meta:
        model = Profil
        fields = [
            'nom_complet', 'matricule', 'titre', 'statut_global',
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


