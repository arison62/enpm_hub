

# organizations/api/schemas.py
from ninja.schema import Schema
from ninja import ModelSchema
from typing import Optional, List
from datetime import date, datetime
from pydantic import UUID4, EmailStr
from core.api.schemas import SecteurActiviteSimple
from users.api.schemas import ProfilBaseOut, PaginationMetaSchema, ProfilCreate
from organizations.models import Organisation, MembreOrganisation, AbonnementOrganisation


# ==========================================
# SCHÉMAS ORGANISATION
# ==========================================

class OrganisationOut(ModelSchema):
    """Schéma de sortie simple pour une organisation"""
    logo: Optional[str] = None
    pays: Optional[str] = None
    pays_nom: Optional[str] = None
    secteur_activite: Optional[SecteurActiviteSimple] = None

    class Meta:
        model = Organisation
        fields = [
            'id', 'nom_organisation', 'type_organisation', 'secteur_activite',
            'adresse', 'ville', 'pays', 'email_general', 'telephone_general',
            'description', 'date_creation', 'statut', 'slug', 'logo',
            'created_at', 'updated_at'
        ]

    @staticmethod
    def resolve_logo(obj):
        return obj.logo.url if obj.logo else None
    
    @staticmethod
    def resolve_pays(obj):
        return obj.pays.code if obj.pays else None
    
    @staticmethod
    def resolve_pays_nom(obj):
        return obj.pays.name if obj.pays else None
    
    @staticmethod
    def resolve_secteur_activite(obj):
        return {
            "id": obj.secteur_activite.id,
            "nom": obj.secteur_activite.nom,
            "code": obj.secteur_activite.code
        }


class OrganisationCompleteOut(OrganisationOut):
    """Schéma complet avec statistiques"""
    logo: Optional[str] = None
    nombre_membres: Optional[int] = 0
    nombre_abonnes: Optional[int] = 0
    est_suivi: Optional[bool] = False

    @staticmethod
    def resolve_logo(obj):
        return obj.logo.url if obj.logo else None
    
    @staticmethod
    def resolve_membres_count(obj):
        return getattr(obj, 'membres_count', 0)
    
    @staticmethod
    def resolve_abonnes_count(obj):
        return getattr(obj, 'abonnes_count', 0)


class OrganisationCreate(Schema):
    """Schéma pour création d'organisation"""
    nom_organisation: str
    type_organisation: str
    secteur_activite_id: Optional[UUID4] = None
    adresse: Optional[str] = None
    ville: Optional[str] = None
    pays: Optional[str] = None
    email_general: Optional[str] = None
    telephone_general: Optional[str] = None
    description: Optional[str] = None
    date_creation: Optional[date] = None


class MembersOrganisationCreate(Schema):
    """Schéma pour ajout de membres"""
    email: EmailStr
    role_systeme: str = 'user'
    role_organisation: str = "employe"
    profil: ProfilCreate
    

class OrgansisationCreateWithMembers(OrganisationCreate):
    membres : List[MembersOrganisationCreate]

class OrganisationUpdate(Schema):
    """Schéma pour mise à jour d'organisation"""
    nom_organisation: Optional[str] = None
    type_organisation: Optional[str] = None
    secteur_activite: Optional[UUID4] = None
    adresse: Optional[str] = None
    ville: Optional[str] = None
    pays: Optional[str] = None
    email_general: Optional[str] = None
    telephone_general: Optional[str] = None
    description: Optional[str] = None
    date_creation: Optional[date] = None
    slug: Optional[str] = None


class OrganisationStatusUpdate(Schema):
    """Schéma pour mise à jour du statut"""
    statut: str


class OrganisationFilter(Schema):
    """Schéma pour filtres de recherche d'organisations"""
    search: Optional[str] = None
    pays: Optional[str] = None
    secteur_activite: Optional[str] = None
    type_organisation: Optional[str] = None
    ville: Optional[str] = None


class OrganisationListResponse(Schema):
    """Réponse paginée pour liste d'organisations"""
    items: List[OrganisationCompleteOut]
    meta: PaginationMetaSchema


class OrganisationStats(Schema):
    """Schéma pour statistiques d'une organisation"""
    membres_count: int
    admins_count: int
    followers_count: int


class OrganisationGlobalStats(Schema):
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

class MembreOrganisationOut(ModelSchema):
    """Schéma de sortie pour un membre"""
    profil_nom: str
    organisation_nom: str

    class Meta:
        model = MembreOrganisation
        fields = [
            'id', 'role_organisation', 'est_actif',
            'date_joindre', 'created_at'
        ]

    @staticmethod
    def resolve_profil_nom(obj):
        return obj.profil.nom_complet
    
    @staticmethod
    def resolve_organisation_nom(obj):
        return obj.organisation.nom_organisation



class MembreOrganisationCreate(Schema):
    """Schéma pour ajout d'un membre"""
    profil_id: UUID4
    role_organisation: str
    poste: Optional[UUID4] = None


class MembreOrganisationUpdate(Schema):
    """Schéma pour mise à jour d'un membre"""
    role_organisation: Optional[str] = None
    poste: Optional[UUID4] = None
    est_actif: Optional[bool] = None


class MembreFilter(Schema):
    """Schéma pour filtres de recherche de membres"""
    search: Optional[str] = None
    role_organisation: Optional[str] = None


class MembreListResponse(Schema):
    """Réponse paginée pour liste de membres"""
    items: List[MembreOrganisationOut]
    meta: PaginationMetaSchema


# ==========================================
# SCHÉMAS ABONNEMENTS
# ==========================================

class AbonnementOrganisationOut(ModelSchema):
    """Schéma de sortie pour un abonnement"""
    profil: ProfilBaseOut
    organisation: OrganisationOut
    
    class Meta:
        model = AbonnementOrganisation
        fields = ['id', 'date_abonnement']


class Follower(Schema):
    """Schéma simplifié pour un abonné"""
    profil: ProfilBaseOut
    date_abonnement: datetime


class FollowerListResponse(Schema):
    """Réponse paginée pour liste d'abonnés"""
    items: List[ProfilBaseOut]
    meta: PaginationMetaSchema


class FollowingListResponse(Schema):
    """Réponse paginée pour liste d'organisations suivies"""
    items: List[OrganisationCompleteOut]
    meta: PaginationMetaSchema


# ==========================================
# SCHÉMAS LOGO
# ==========================================

class LogoUploadResponse(Schema):
    """Réponse après upload de logo"""
    message: str = "Logo de l'organisation mis à jour avec succès"
    logo_url: Optional[str] = None


# ==========================================
# SCHÉMAS MESSAGES
# ==========================================


class FollowResponse(Schema):
    """Réponse après abonnement"""
    message: str
    organisation: OrganisationOut


class UnfollowResponse(Schema):
    """Réponse après désabonnement"""
    message: str = "Vous ne suivez plus cette organisation"