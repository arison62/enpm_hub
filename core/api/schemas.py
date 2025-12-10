from typing import Optional
from ninja import Schema, ModelSchema, Field
from core.models import User

# ==========================================
# Schémas d'authentification
# ==========================================

class LoginSchema(Schema):
    """Schéma d'entrée pour l'authentification (Matricule ou Email)"""
    login_id: str
    password: str
    
class TokenSchema(Schema):
    """Schéma de sortie après connexion réussie"""
    user_id: str
    access_token: str
    refresh_token: str
    role: str  # Important pour le RBAC côté client
    
class RefreshTokenSchema(Schema):
    """Schéma pour fournir un refresh token."""
    refresh: str

# ==========================================
# Schémas utilisateur
# ==========================================

class UserSchema(ModelSchema):
    """Schéma de sortie complet pour un utilisateur"""
    class Meta:
        model = User
        fields = (
            'id', 'nom', 'prenom', 'email', 
            'matricule', 'bio', 'telephone', 
            'travailleur', 'role', 'statut',
            'annee_sortie', 'domaine', 'photo_profile',
            'titre', 'est_actif', 'created_at', 'updated_at'
        )

class UserCreateSchema(ModelSchema):
    """Schéma pour la création d'un utilisateur."""
    class Meta:
        model = User
        fields = [
            'nom', 'prenom', 'email', 'matricule', 'statut', 'titre',
            'travailleur', 'annee_sortie', 'telephone', 'bio',
            'domaine', 'role'
        ]
        # Le mot de passe est généré automatiquement par le service

class UserUpdateSchema(Schema):
    """
    Schéma pour la mise à jour d'un utilisateur (tous les champs optionnels).
    """
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[str] = None
    matricule: Optional[str] = None
    statut: Optional[str] = None
    titre: Optional[str] = None
    travailleur: Optional[bool] = None
    annee_sortie: Optional[int] = None
    telephone: Optional[str] = None
    bio: Optional[str] = None
    domaine: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None  # Pour permettre le changement de mot de passe

class UserListSchema(ModelSchema):
    """Schéma simplifié pour les listes d'utilisateurs."""
    class Meta:
        model = User
        fields = [
            'id', 'nom', 'prenom', 'email', 'statut', 
            'role', 'est_actif', 'photo_profile', 'matricule'
        ]

# ==========================================
# Schémas pour upload de photo
# ==========================================

class PhotoUploadResponseSchema(Schema):
    """Schéma de réponse après upload de photo"""
    message: str
    photo_url: Optional[str] = None
    

# ==========================================
# Schema pour les filtres utilisateur
# ==========================================

class UserFilterSchema(Schema):
    """Schéma pour les filtres de recherche d'utilisateurs"""
    search: Optional[str] = Field(None, description="Recherche dans nom, prenom, email, matricule")
    role: Optional[str] = Field(None, description="Filtrer par rôle")
    statut: Optional[str] = Field(None, description="Filtrer par statut")
    est_actif: Optional[bool] = Field(None, description="Filtrer par statut actif")
    travailleur: Optional[bool] = Field(None, description="Filtrer par statut travailleur")