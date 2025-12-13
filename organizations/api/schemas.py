# organizations/api/schemas.py
from ninja import Schema, ModelSchema
from typing import Optional, List
from datetime import date
from pydantic import UUID4
from core.models import User
from organizations.models import Organisation, MembreOrganisation, AbonnementOrganisation

class OrganisationOutSchema(ModelSchema):
    logo: Optional[str] = None

    class Meta:
        model = Organisation
        fields = "__all__"

    @staticmethod
    def resolve_logo(obj):
        return obj.logo.url if obj.logo else None

class OrganisationCreateSchema(Schema):
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

class OrganisationStatusUpdateSchema(Schema):
    statut: str

class MembreOrganisationOutSchema(ModelSchema):
    class Meta:
        model = MembreOrganisation
        fields = "__all__"

class MembreOrganisationCreateSchema(Schema):
    profil_id: UUID4
    role_organisation: str
    poste: Optional[str] = None

class MembreOrganisationUpdateSchema(Schema):
    role_organisation: Optional[str] = None
    poste: Optional[str] = None
    est_actif: Optional[bool] = None

class AbonnementOrganisationOutSchema(ModelSchema):
    class Meta:
        model = AbonnementOrganisation
        fields = "__all__"
