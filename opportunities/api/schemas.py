# opportunities/api/schemas.py
from ninja.schema import Schema
from ninja import ModelSchema
from typing import Optional, List
from datetime import date
from decimal import Decimal

from pydantic import UUID4
from core.api.schemas import DeviseSimple
from users.api.schemas import ProfilBaseOut, PaginationMetaSchema
from organizations.api.schemas import OrganisationOut
from opportunities.models import Stage, Emploi, Formation


# ==========================================
# SCHÉMAS STAGE
# ==========================================

class StageOut(ModelSchema):
    """Schéma de sortie pour un stage"""
    createur_profil: Optional[ProfilBaseOut] = None
    organisation: Optional[OrganisationOut] = None
    validateur_profil: Optional[ProfilBaseOut] = None
    pays: Optional[str]
    pays_nom: Optional[str]


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
        return obj.pays.code if obj.pays else None
    
    @staticmethod
    def resolve_pays_nom(obj):
        return obj.pays.name if obj.pays else None
    

class StageCreate(Schema):
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


class StageUpdate(Schema):
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


class StageFilter(Schema):
    """Filtres pour recherche de stages"""
    search: Optional[str] = None
    type_stage: Optional[str] = None
    lieu: Optional[str] = None
    ville: Optional[str] = None
    pays: Optional[str] = None
    statut: Optional[str] = None


class StageListResponse(Schema):
    """Réponse paginée pour liste de stages"""
    items: List[StageOut]
    meta: PaginationMetaSchema


class StageValidation(Schema):
    """Schéma pour validation d'un stage"""
    approved: bool
    commentaire: Optional[str] = None


class StageStatusUpdate(Schema):
    """Schéma pour mise à jour du statut"""
    statut: str


class StageStats(Schema):
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

class EmploiOut(ModelSchema):
    """Schéma de sortie pour un emploi"""
    createur_profil: Optional[ProfilBaseOut] = None
    organisation: Optional[OrganisationOut] = None
    validateur_profil: Optional[ProfilBaseOut] = None
    pays: Optional[str]
    pays_nom: Optional[str]
    devise: Optional[DeviseSimple]

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
        return obj.pays.code if obj.pays else None
    
    @staticmethod
    def resolve_pays_nom(obj):
        return obj.pays.name if obj.pays else None
    
    @staticmethod
    def resolve_devise(obj):
        return {
            'code': obj.devise.code,
            'nom': obj.devise.nom,
            'symbole': obj.devise.symbole
        }

class EmploiCreate(Schema):
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


class EmploiUpdate(Schema):
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


class EmploiFilter(Schema):
    """Filtres pour recherche d'emplois"""
    search: Optional[str] = None
    type_emploi: Optional[str] = None
    lieu: Optional[str] = None
    ville: Optional[str] = None
    pays: Optional[str] = None
    statut: Optional[str] = None


class EmploiListResponse(Schema):
    """Réponse paginée pour liste d'emplois"""
    items: List[EmploiOut]
    meta: PaginationMetaSchema


class EmploiValidation(Schema):
    """Schéma pour validation d'un emploi"""
    approved: bool
    commentaire: Optional[str] = None


class EmploiStatusUpdate(Schema):
    """Schéma pour mise à jour du statut"""
    statut: str


class EmploiStats(Schema):
    """Statistiques des emplois"""
    total_emplois: int
    active_emplois: int
    pending_emplois: int
    by_type: dict


# ==========================================
# SCHÉMAS FORMATION
# ==========================================

class FormationOut(ModelSchema):
    """Schéma de sortie pour une formation"""
    createur_profil: Optional[ProfilBaseOut] = None
    organisation: Optional[OrganisationOut] = None
    validateur_profil: Optional[ProfilBaseOut] = None
    pays: Optional[str]
    pays_nom: Optional[str]
    devise: Optional[DeviseSimple]

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
        return obj.pays.code if obj.pays else None
    
    @staticmethod
    def resolve_pays_nom(obj):
        return obj.pays.name if obj.pays else None
    
    @staticmethod
    def resolve_devise(obj):
        return {
            'code': obj.devise.code,
            'nom': obj.devise.nom,
            'symbole': obj.devise.symbole
        }
        
class FormationCreate(Schema):
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
    devise: Optional[UUID4]
    duree_heures: Optional[int] = None


class FormationUpdate(Schema):
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
    devise: Optional[UUID4] = None
    duree_heures: Optional[int] = None
    slug: Optional[str] = None


class FormationFilter(Schema):
    """Filtres pour recherche de formations"""
    search: Optional[str] = None
    type_formation: Optional[str] = None
    est_payante: Optional[bool] = None
    ville: Optional[str] = None
    pays: Optional[str] = None
    statut: Optional[str] = None


class FormationListResponse(Schema):
    """Réponse paginée pour liste de formations"""
    items: List[FormationOut]
    meta: PaginationMetaSchema


class FormationValidation(Schema):
    """Schéma pour validation d'une formation"""
    approved: bool
    commentaire: Optional[str] = None


class FormationStatusUpdate(Schema):
    """Schéma pour mise à jour du statut"""
    statut: str


class FormationStats(Schema):
    """Statistiques des formations"""
    total_formations: int
    active_formations: int
    pending_formations: int
    by_type: dict
    gratuites: int
    payantes: int

