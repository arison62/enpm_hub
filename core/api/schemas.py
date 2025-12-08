from ninja import Schema, ModelSchema
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