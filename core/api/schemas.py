# core/api/schemas.py
from ninja import Field, ModelSchema, Schema
from typing import Optional
from pydantic import EmailStr, field_validator
from core.models import AnneePromotion, ReseauSocial, User, AuditLog


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
    user: "UserOut"


class RefreshTokenSchema(Schema):
    """Schéma pour rafraîchir le token"""
    refresh: str


class EmailSchema(Schema):
    """Schéma simple pour les opérations basées sur l'email."""
    email: str
    
class PaginationMetaSchema(Schema):
    """Métadonnées de pagination"""
    page: int
    page_size: int
    total_items: int
    total_pages: int

# ==========================================
# SCHÉMAS POUR AnneePromotion
# ==========================================

class AnneePromotionOut(ModelSchema):
    class Meta:
        model = AnneePromotion
        fields = ['id', 'annee', 'libelle', 'description', 'est_active', 'ordre_affichage', 'created_at', 'updated_at']

# ==========================================
# SCHÉMAS POUR ReseauSocial
# ==========================================

class ReseauSocialOut(ModelSchema):
    class Meta:
        model = ReseauSocial
        fields = ['id', 'nom', 'url_base', 'type_reseau', 'pattern_validation', 'placeholder_exemple', 'est_actif', 'ordre_affichage', 'created_at', 'updated_at']


# ==========================================
# SCHÉMAS POUR User
# ==========================================

class UserOut(ModelSchema):
    class Meta:
        model = User
        fields = ['id', 'email', 'role_systeme', 'last_login', 'est_actif', 'is_staff', 'created_at', 'updated_at', 'deleted', 'deleted_at']
        # Excluded sensitive fields like mot_de_passe, groups, user_permissions

class UserCreate(Schema):
    email: EmailStr
    password: Optional[str] = None  # For create_user with or without password
    role_systeme: str = 'user'
    est_actif: bool = True
    is_staff: bool = False

    @field_validator('role_systeme')
    def validate_role(cls, v):
        if v not in [choice[0] for choice in User.ROLE_SYSTEME_CHOICES]:
            raise ValueError('Invalid role')
        return v

class UserUpdate(ModelSchema):
    class Meta:
        model = User
        fields = ['email', 'role_systeme', 'est_actif', 'is_staff']
        fields_optional = '__all__'
        # Password update should be handled separately, not included here for security

# ==========================================
# SCHÉMAS POUR AuditLog
# ==========================================

class AuditLogOut(ModelSchema):
    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'action', 'entity_type', 'entity_id', 'old_values', 'new_values', 'ip_address', 'user_agent', 'created_at', 'updated_at']
        # AuditLog is typically read-only, no create/update schemas needed for API exposure
