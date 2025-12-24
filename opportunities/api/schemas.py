# opportunities/api/schemas.py
from ninja.schema import Schema
from ninja import ModelSchema
from typing import Optional, List
from datetime import date
from decimal import Decimal
from users.api.schemas import ProfilBaseOut, PaginationMetaSchema
from organizations.api.schemas import OrganisationOutSchema
from opportunities.models import Stage, Emploi, Formation


# ==========================================
# SCHÉMAS STAGE
# ==========================================

class StageOutSchema(ModelSchema):
    """Schéma de sortie pour un stage"""
    createur_profil: Optional[ProfilBaseOut] = None
    organisation: Optional[OrganisationOutSchema] = None
    validateur_profil: Optional[ProfilBaseOut] = None


    class Meta:
        model = Stage
        fields = [
            'id', 'titre', 'slug', 'nom_structure', 'description', 'type_stage',
            'adresse', 'ville', 'pays', 'email_contact', 'telephone_contact',
            'lien_offre_original', 'lien_candidature', 'date_debut', 'date_fin',
            'date_publication', 'statut', 'est_valide', 'date_validation',
            'commentaire_validation', 'created_at', 'updated_at'
        ]

    @staticmethod
    def resolve_pays(obj):
        return obj.pays.name

class StageCreateSchema(Schema):
    """Schéma pour création d'un stage"""
    titre: str
    nom_structure: str
    description: str
    type_stage: str
    lieu: str
    ville: Optional[str] = None
    pays: Optional[str] = None
    email_contact: Optional[str] = None
    telephone_contact: Optional[str] = None
    lien_offre_original: Optional[str] = None
    lien_candidature: Optional[str] = None
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None


class StageUpdateSchema(Schema):
    """Schéma pour mise à jour d'un stage"""
    titre: Optional[str] = None
    nom_structure: Optional[str] = None
    description: Optional[str] = None
    type_stage: Optional[str] = None
    lieu: Optional[str] = None
    ville: Optional[str] = None
    pays: Optional[str] = None
    email_contact: Optional[str] = None
    telephone_contact: Optional[str] = None
    lien_offre_original: Optional[str] = None
    lien_candidature: Optional[str] = None
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    slug: Optional[str] = None


class StageFilterSchema(Schema):
    """Filtres pour recherche de stages"""
    search: Optional[str] = None
    type_stage: Optional[str] = None
    lieu: Optional[str] = None
    ville: Optional[str] = None
    pays: Optional[str] = None
    statut: Optional[str] = None


class StageListResponseSchema(Schema):
    """Réponse paginée pour liste de stages"""
    items: List[StageOutSchema]
    meta: PaginationMetaSchema


class StageValidationSchema(Schema):
    """Schéma pour validation d'un stage"""
    approved: bool
    commentaire: Optional[str] = None


class StageStatusUpdateSchema(Schema):
    """Schéma pour mise à jour du statut"""
    statut: str


class StageStatsSchema(Schema):
    """Statistiques des stages"""
    total_stages: int
    active_stages: int
    pending_stages: int
    expired_stages: int
    pourvue_stages: int
    by_type: dict


# ==========================================
# SCHÉMAS EMPLOI
# ==========================================

class EmploiOutSchema(ModelSchema):
    """Schéma de sortie pour un emploi"""
    createur_profil: Optional[ProfilBaseOut] = None
    organisation: Optional[OrganisationOutSchema] = None
    validateur_profil: Optional[ProfilBaseOut] = None

    class Meta:
        model = Emploi
        fields = [
            'id', 'titre', 'slug', 'nom_structure', 'description', 'type_emploi',
            'adresse', 'ville', 'pays', 'email_contact', 'telephone_contact',
            'lien_offre_original', 'lien_candidature', 'date_publication',
            'date_expiration', 'salaire_min', 'salaire_max', 'devise',
            'statut', 'est_valide', 'date_validation', 'commentaire_validation',
            'created_at', 'updated_at'
        ]

    @staticmethod
    def resolve_pays(obj):
        return obj.pays.name

class EmploiCreateSchema(Schema):
    """Schéma pour création d'un emploi"""
    titre: str
    nom_structure: str
    description: str
    type_emploi: Optional[str] = None
    lieu: str
    ville: Optional[str] = None
    pays: Optional[str] = None
    email_contact: Optional[str] = None
    telephone_contact: Optional[str] = None
    lien_offre_original: Optional[str] = None
    lien_candidature: Optional[str] = None
    date_expiration: Optional[date] = None
    salaire_min: Optional[Decimal] = None
    salaire_max: Optional[Decimal] = None
    devise: Optional[str] = 'XAF'


class EmploiUpdateSchema(Schema):
    """Schéma pour mise à jour d'un emploi"""
    titre: Optional[str] = None
    nom_structure: Optional[str] = None
    description: Optional[str] = None
    type_emploi: Optional[str] = None
    lieu: Optional[str] = None
    ville: Optional[str] = None
    pays: Optional[str] = None
    email_contact: Optional[str] = None
    telephone_contact: Optional[str] = None
    lien_offre_original: Optional[str] = None
    lien_candidature: Optional[str] = None
    date_expiration: Optional[date] = None
    salaire_min: Optional[Decimal] = None
    salaire_max: Optional[Decimal] = None
    devise: Optional[str] = None
    slug: Optional[str] = None


class EmploiFilterSchema(Schema):
    """Filtres pour recherche d'emplois"""
    search: Optional[str] = None
    type_emploi: Optional[str] = None
    lieu: Optional[str] = None
    ville: Optional[str] = None
    pays: Optional[str] = None
    statut: Optional[str] = None


class EmploiListResponseSchema(Schema):
    """Réponse paginée pour liste d'emplois"""
    items: List[EmploiOutSchema]
    meta: PaginationMetaSchema


class EmploiValidationSchema(Schema):
    """Schéma pour validation d'un emploi"""
    approved: bool
    commentaire: Optional[str] = None


class EmploiStatusUpdateSchema(Schema):
    """Schéma pour mise à jour du statut"""
    statut: str


class EmploiStatsSchema(Schema):
    """Statistiques des emplois"""
    total_emplois: int
    active_emplois: int
    pending_emplois: int
    by_type: dict


# ==========================================
# SCHÉMAS FORMATION
# ==========================================

class FormationOutSchema(ModelSchema):
    """Schéma de sortie pour une formation"""
    createur_profil: Optional[ProfilBaseOut] = None
    organisation: Optional[OrganisationOutSchema] = None
    validateur_profil: Optional[ProfilBaseOut] = None

    class Meta:
        model = Formation
        fields = [
            'id', 'titre', 'slug', 'nom_structure', 'description', 'type_formation',
            'adresse', 'ville', 'pays', 'email_contact', 'telephone_contact',
            'lien_formation', 'lien_inscription', 'date_debut', 'date_fin',
            'date_publication', 'est_payante', 'prix', 'devise', 'duree_heures',
            'statut', 'est_valide', 'date_validation', 'commentaire_validation',
            'created_at', 'updated_at'
        ]

    @staticmethod
    def resolve_pays(obj):
        return obj.pays.name

class FormationCreateSchema(Schema):
    """Schéma pour création d'une formation"""
    titre: str
    nom_structure: str
    description: str
    type_formation: str
    lieu: Optional[str] = None
    ville: Optional[str] = None
    pays: Optional[str] = None
    email_contact: Optional[str] = None
    telephone_contact: Optional[str] = None
    lien_formation: Optional[str] = None
    lien_inscription: Optional[str] = None
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    est_payante: bool = False
    prix: Optional[Decimal] = None
    devise: Optional[str] = 'XAF'
    duree_heures: Optional[int] = None


class FormationUpdateSchema(Schema):
    """Schéma pour mise à jour d'une formation"""
    titre: Optional[str] = None
    nom_structure: Optional[str] = None
    description: Optional[str] = None
    type_formation: Optional[str] = None
    lieu: Optional[str] = None
    ville: Optional[str] = None
    pays: Optional[str] = None
    email_contact: Optional[str] = None
    telephone_contact: Optional[str] = None
    lien_formation: Optional[str] = None
    lien_inscription: Optional[str] = None
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    est_payante: Optional[bool] = None
    prix: Optional[Decimal] = None
    devise: Optional[str] = None
    duree_heures: Optional[int] = None
    slug: Optional[str] = None


class FormationFilterSchema(Schema):
    """Filtres pour recherche de formations"""
    search: Optional[str] = None
    type_formation: Optional[str] = None
    est_payante: Optional[bool] = None
    ville: Optional[str] = None
    pays: Optional[str] = None
    statut: Optional[str] = None


class FormationListResponseSchema(Schema):
    """Réponse paginée pour liste de formations"""
    items: List[FormationOutSchema]
    meta: PaginationMetaSchema


class FormationValidationSchema(Schema):
    """Schéma pour validation d'une formation"""
    approved: bool
    commentaire: Optional[str] = None


class FormationStatusUpdateSchema(Schema):
    """Schéma pour mise à jour du statut"""
    statut: str


class FormationStatsSchema(Schema):
    """Statistiques des formations"""
    total_formations: int
    active_formations: int
    pending_formations: int
    by_type: dict
    gratuites: int
    payantes: int


# ==========================================
# SCHÉMAS COMMUNS
# ==========================================

class MessageSchema(Schema):
    """Schéma pour messages simples"""
    detail: str