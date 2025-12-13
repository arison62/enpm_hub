# organizations/api/views.py
from typing import List
from ninja import Router, File, UploadedFile
from ninja.pagination import paginate
from django.http import HttpRequest
from pydantic import UUID4
from core.services.auth_service import jwt_auth
from core.api.schemas import MessageSchema, ValidationErrorSchema
from organizations.services.organisation_service import organisation_service
from organizations.services.membre_service import membre_service
from organizations.services.abonnement_service import abonnement_service
from core.api.schemas import ProfilOutSchema
from .schemas import (
    OrganisationOutSchema,
    OrganisationCreateSchema,
    OrganisationUpdateSchema,
    OrganisationStatusUpdateSchema,
    MembreOrganisationOutSchema,
    MembreOrganisationCreateSchema,
    MembreOrganisationUpdateSchema,
    AbonnementOrganisationOutSchema,
)

organizations_router = Router(tags=["Organisations"])

@organizations_router.post(
    "/",
    response={201: OrganisationOutSchema, 400: MessageSchema, 401: MessageSchema, 422: ValidationErrorSchema},
    auth=jwt_auth,
    summary="Proposer la création d'une nouvelle organisation"
)
def create_organisation_endpoint(request: HttpRequest, payload: OrganisationCreateSchema):
    """
    Permet à un utilisateur authentifié de créer une nouvelle organisation.
    L'organisation est créée avec le statut 'en_attente' et nécessite l'approbation d'un admin.
    """
    new_organisation = organisation_service.create_organisation(
        acting_user=request.auth,  # type: ignore
        data=payload.dict()
    )
    return 201, new_organisation

@organizations_router.get(
    "/",
    response={200: List[OrganisationOutSchema], 422: ValidationErrorSchema},
    summary="Lister les organisations actives"
)
@paginate
def list_organisations_endpoint(request: HttpRequest):
    # Filters can be added here, e.g. filters: Query[OrganisationFilterSchema]
    organisations = organisation_service.list_organisations(filters={})
    return organisations

@organizations_router.get(
    "/pending",
    response={200: List[OrganisationOutSchema], 401: MessageSchema, 403: MessageSchema},
    auth=jwt_auth,
    summary="Lister les organisations en attente d'approbation (admin uniquement)"
)
def list_pending_organisations_endpoint(request: HttpRequest):
    organisations = organisation_service.list_pending_organisations(acting_user=request.auth) # type: ignore
    return organisations

@organizations_router.get(
    "/{org_id}",
    response={200: OrganisationOutSchema, 404: MessageSchema},
    summary="Obtenir les détails d'une organisation"
)
def get_organisation_endpoint(request: HttpRequest, org_id: UUID4):
    organisation = organisation_service.get_organisation_by_id(org_id)
    return organisation

@organizations_router.put(
    "/{org_id}",
    response={200: OrganisationOutSchema, 400: MessageSchema, 401: MessageSchema, 403: MessageSchema, 404: MessageSchema, 422: ValidationErrorSchema},
    auth=jwt_auth,
    summary="Mettre à jour une organisation"
)
def update_organisation_endpoint(request: HttpRequest, org_id: UUID4, payload: OrganisationUpdateSchema):
    updated_organisation = organisation_service.update_organisation(
        acting_user=request.auth,  # type: ignore
        org_id=org_id,
        data=payload.dict(exclude_unset=True)
    )
    return updated_organisation

@organizations_router.patch(
    "/{org_id}/status",
    response={200: OrganisationOutSchema, 400: MessageSchema, 401: MessageSchema, 403: MessageSchema, 404: MessageSchema, 422: ValidationErrorSchema},
    auth=jwt_auth,
    summary="Changer le statut d'une organisation (admin uniquement)"
)
def update_organisation_status_endpoint(request: HttpRequest, org_id: UUID4, payload: OrganisationStatusUpdateSchema):
    updated_organisation = organisation_service.update_organisation_status(
        acting_user=request.auth,  # type: ignore
        org_id=org_id,
        new_status=payload.statut
    )
    return updated_organisation

@organizations_router.post(
    "/{org_id}/logo",
    response={200: OrganisationOutSchema, 400: MessageSchema, 401: MessageSchema, 403: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Uploader un logo pour une organisation"
)
def upload_logo_endpoint(request: HttpRequest, org_id: UUID4, file: File[UploadedFile]):
    updated_organisation = organisation_service.update_organisation_logo(
        acting_user=request.auth,  # type: ignore
        org_id=org_id,
        logo_file=file
    )
    return updated_organisation

@organizations_router.delete(
    "/{org_id}",
    response={204: None, 401: MessageSchema, 403: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Supprimer une organisation (admin uniquement)"
)
def delete_organisation_endpoint(request: HttpRequest, org_id: UUID4):
    organisation_service.soft_delete_organisation(
        acting_user=request.auth,  # type: ignore
        org_id=org_id
    )
    return 204, None

# ==========================================
# Endpoints Gestion des Membres
# ==========================================

@organizations_router.get(
    "/{org_id}/members",
    response=List[MembreOrganisationOutSchema],
    summary="Lister les membres d'une organisation"
)
def list_members_endpoint(request: HttpRequest, org_id: UUID4):
    return membre_service.list_membres(org_id)

@organizations_router.post(
    "/{org_id}/members",
    response={201: MembreOrganisationOutSchema, 400: MessageSchema, 401: MessageSchema, 403: MessageSchema, 404: MessageSchema, 422: ValidationErrorSchema},
    auth=jwt_auth,
    summary="Ajouter un membre à une organisation"
)
def add_member_endpoint(request: HttpRequest, org_id: UUID4, payload: MembreOrganisationCreateSchema):
    new_member = membre_service.add_membre(
        acting_user=request.auth,  # type: ignore
        org_id=org_id,
        data=payload.dict()
    )
    return 201, new_member

@organizations_router.put(
    "/{org_id}/members/{profil_id}",
    response={200: MembreOrganisationOutSchema, 400: MessageSchema, 401: MessageSchema, 403: MessageSchema, 404: MessageSchema, 422: ValidationErrorSchema},
    auth=jwt_auth,
    summary="Mettre à jour un membre d'une organisation"
)
def update_member_endpoint(request: HttpRequest, org_id: UUID4, profil_id: UUID4, payload: MembreOrganisationUpdateSchema):
    updated_member = membre_service.update_membre(
        acting_user=request.auth,  # type: ignore
        org_id=org_id,
        profil_id=profil_id,
        data=payload.dict(exclude_unset=True)
    )
    return updated_member

@organizations_router.delete(
    "/{org_id}/members/{profil_id}",
    response={204: None, 401: MessageSchema, 403: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Retirer un membre d'une organisation"
)
def remove_member_endpoint(request: HttpRequest, org_id: UUID4, profil_id: UUID4):
    membre_service.remove_membre(
        acting_user=request.auth,  # type: ignore
        org_id=org_id,
        profil_id=profil_id
    )
    return 204, None

# ==========================================
# Endpoints Gestion des Abonnements
# ==========================================

@organizations_router.post(
    "/{org_id}/follow",
    response={201: AbonnementOrganisationOutSchema, 400: MessageSchema, 401: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="S'abonner à une organisation"
)
def follow_organisation_endpoint(request: HttpRequest, org_id: UUID4):
    subscription = abonnement_service.follow_organisation(
        acting_user=request.auth,  # type: ignore
        org_id=org_id
    )
    return 201, subscription

@organizations_router.delete(
    "/{org_id}/follow",
    response={204: None, 401: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Se désabonner d'une organisation"
)
def unfollow_organisation_endpoint(request: HttpRequest, org_id: UUID4):
    abonnement_service.unfollow_organisation(
        acting_user=request.auth,  # type: ignore
        org_id=org_id
    )
    return 204, None

@organizations_router.get(
    "/{org_id}/followers",
    response=List[ProfilOutSchema],
    summary="Lister les abonnés d'une organisation"
)
def list_followers_endpoint(request: HttpRequest, org_id: UUID4):
    return abonnement_service.list_followers(org_id)

@organizations_router.get(
    "/following/me",
    response=List[OrganisationOutSchema],
    auth=jwt_auth,
    summary="Lister les organisations suivies par l'utilisateur connecté"
)
def list_following_endpoint(request: HttpRequest):
    return abonnement_service.list_following(acting_user=request.auth) # type: ignore
