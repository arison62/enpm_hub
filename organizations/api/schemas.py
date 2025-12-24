# organizations/api/schemas.py
from ninja.schema import Schema
from ninja import ModelSchema
from typing import Optional, List
from datetime import date, datetime
from pydantic import UUID4
from users.api.schemas import ProfilBaseOut, PaginationMetaSchema
from organizations.models import Organisation, MembreOrganisation, AbonnementOrganisation


# ==========================================
# SCHÉMAS ORGANISATION
# ==========================================

class OrganisationOutSchema(ModelSchema):
    """Schéma de sortie simple pour une organisation"""
    logo: Optional[str] = None

    class Meta:
        model = Organisation
        fields = [
            'id', 'nom_organisation', 'type_organisation', 'secteur_activite',
            'adresse', 'ville', 'pays', 'email_general', 'telephone_general',
            'description', 'date_creation', 'statut', 'slug',
            'created_at', 'updated_at'
        ]

    @staticmethod
    def resolve_logo(obj):
        return obj.logo.url if obj.logo else None


class OrganisationCompleteSchema(ModelSchema):
    """Schéma complet avec statistiques"""
    logo: Optional[str] = None
    membres_count: Optional[int] = 0
    abonnes_count: Optional[int] = 0

    class Meta:
        model = Organisation
        fields = [
            'id', 'nom_organisation', 'type_organisation', 'secteur_activite',
            'adresse', 'ville', 'pays', 'email_general', 'telephone_general',
            'description', 'date_creation', 'statut', 'slug',
            'created_at', 'updated_at'
        ]

    @staticmethod
    def resolve_logo(obj):
        return obj.logo.url if obj.logo else None
    
    @staticmethod
    def resolve_membres_count(obj):
        return getattr(obj, 'membres_count', 0)
    
    @staticmethod
    def resolve_abonnes_count(obj):
        return getattr(obj, 'abonnes_count', 0)


class OrganisationCreateSchema(Schema):
    """Schéma pour création d'organisation"""
    nom_organisation: str
    type_organisation: str
    secteur_activite: Optional[str] = None
    adresse: Optional[str] = None
    ville: Optional[str] = None
    pays: Optional[str] = None
    email_general: Optional[str] = None
    telephone_general: Optional[str] = None
    description: Optional[str] = None
    date_creation: Optional[date] = None


class OrganisationUpdateSchema(Schema):
    """Schéma pour mise à jour d'organisation"""
    nom_organisation: Optional[str] = None
    type_organisation: Optional[str] = None
    secteur_activite: Optional[str] = None
    adresse: Optional[str] = None
    ville: Optional[str] = None
    pays: Optional[str] = None
    email_general: Optional[str] = None
    telephone_general: Optional[str] = None
    description: Optional[str] = None
    date_creation: Optional[date] = None
    slug: Optional[str] = None


class OrganisationStatusUpdateSchema(Schema):
    """Schéma pour mise à jour du statut"""
    statut: str


class OrganisationFilterSchema(Schema):
    """Schéma pour filtres de recherche d'organisations"""
    search: Optional[str] = None
    pays: Optional[str] = None
    secteur_activite: Optional[str] = None
    type_organisation: Optional[str] = None
    ville: Optional[str] = None


class OrganisationListResponseSchema(Schema):
    """Réponse paginée pour liste d'organisations"""
    items: List[OrganisationCompleteSchema]
    meta: PaginationMetaSchema


class OrganisationStatsSchema(Schema):
    """Schéma pour statistiques d'une organisation"""
    membres_count: int
    admins_count: int
    followers_count: int


class OrganisationGlobalStatsSchema(Schema):
    """Schéma pour statistiques globales"""
    total_organisations: int
    active_organisations: int
    pending_organisations: int
    inactive_organisations: int
    deleted_organisations: int
    by_type: dict
    top_organisations: List[dict]


# ==========================================
# SCHÉMAS MEMBRES
# ==========================================

class MembreOrganisationOutSchema(ModelSchema):
    """Schéma de sortie pour un membre"""
    profil: ProfilBaseOut

    class Meta:
        model = MembreOrganisation
        fields = [
            'id', 'role_organisation', 'poste', 'est_actif',
            'date_joindre', 'created_at'
        ]


class MembreOrganisationCreateSchema(Schema):
    """Schéma pour ajout d'un membre"""
    profil_id: UUID4
    role_organisation: str
    poste: Optional[str] = None


class MembreOrganisationUpdateSchema(Schema):
    """Schéma pour mise à jour d'un membre"""
    role_organisation: Optional[str] = None
    poste: Optional[str] = None
    est_actif: Optional[bool] = None


class MembreFilterSchema(Schema):
    """Schéma pour filtres de recherche de membres"""
    search: Optional[str] = None
    role_organisation: Optional[str] = None


class MembreListResponseSchema(Schema):
    """Réponse paginée pour liste de membres"""
    items: List[MembreOrganisationOutSchema]
    meta: PaginationMetaSchema


# ==========================================
# SCHÉMAS ABONNEMENTS
# ==========================================

class AbonnementOrganisationOutSchema(ModelSchema):
    """Schéma de sortie pour un abonnement"""
    profil: ProfilBaseOut
    organisation: OrganisationOutSchema
    
    class Meta:
        model = AbonnementOrganisation
        fields = ['id', 'date_abonnement']


class FollowerSchema(Schema):
    """Schéma simplifié pour un abonné"""
    profil: ProfilBaseOut
    date_abonnement: datetime


class FollowerListResponseSchema(Schema):
    """Réponse paginée pour liste d'abonnés"""
    items: List[ProfilBaseOut]
    meta: PaginationMetaSchema


class FollowingListResponseSchema(Schema):
    """Réponse paginée pour liste d'organisations suivies"""
    items: List[OrganisationCompleteSchema]
    meta: PaginationMetaSchema


# ==========================================
# SCHÉMAS LOGO
# ==========================================

class LogoUploadResponseSchema(Schema):
    """Réponse après upload de logo"""
    message: str = "Logo de l'organisation mis à jour avec succès"
    logo_url: Optional[str] = None


# ==========================================
# SCHÉMAS MESSAGES
# ==========================================

class MessageSchema(Schema):
    """Schéma pour messages simples"""
    detail: str


class FollowResponseSchema(Schema):
    """Réponse après abonnement"""
    message: str
    organisation: OrganisationOutSchema


class UnfollowResponseSchema(Schema):
    """Réponse après désabonnement"""
    message: str = "Vous ne suivez plus cette organisation"