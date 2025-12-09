from typing import Optional
from ninja import Schema, ModelSchema, Field
from core.models import User

# Schéma d'entrée pour la connexion
class LoginSchema(Schema):
    """Schéma d'entrée pour l'authentification (Matricule ou Email)"""
    login_id: str
    password: str
    
# Schéma de sortie pour le token
class TokenSchema(Schema):
    """Schéma de sortie après connexion réussie"""
    user_id: str
    access_token: str
    refresh_token: str
    role: str # Important pour le RBAC côté client
    
# Schéma de sortie pour le token
class RefreshTokenSchema(Schema):
    """Schéma pour fournir un refresh token."""
    refresh: str

# Schéma de sortie pour l'utilisateur
class UserSchema(ModelSchema):
    """Schéma de sortie simple pour un utilisateur (après authentification)"""
    class Meta:
        model = User
        fields = ('id', 'nom', 'prenom', 'email', 
                  'matricule', 'bio', 'telephone', 
                  'travailleur' ,'role', 'statut',
                  'annee_sortie', 'domaine', 'photo_profile',
                  'titre', 
                )

# ==========================================
# Schémas pour le CRUD Utilisateur
# ==========================================

class UserCreateSchema(ModelSchema):
    """Schéma pour la création d'un utilisateur."""
    class Meta:
        model = User
        fields = ['nom', 'prenom', 'email', 'matricule', 'statut', 'titre',
                  'travailleur', 'annee_sortie', 'telephone', 'bio',
                  'domaine', 'role']
        # Exclure 'password' car il est généré aléatoirement par le service

class UserUpdateSchema(Schema):
    """
    Schéma pour la mise à jour d'un utilisateur (tous les champs optionnels).
    Hérite de `Schema` pour une définition explicite et éviter les conflits.
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

class UserListSchema(ModelSchema):
    """Schéma simplifié pour les listes d'utilisateurs."""
    class Meta:
        model = User
        fields = ['id', 'nom', 'prenom', 'email', 'statut', 'role', 'est_actif']