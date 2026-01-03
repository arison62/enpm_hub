# organizations/api/views.py
import logging
from ninja import Router, Query, File, UploadedFile
from django.http import HttpRequest
from pydantic import UUID4

from core.utils.pagination import build_pagination_response
from core.services.auth_service import jwt_auth
from organizations.services.organisation_service import organisation_service
from organizations.services.abonnement_service import abonnement_service
from organizations.services.membre_service import membre_service
from organizations.api.schemas import (
    OrganisationCreate,
    OrganisationUpdate,
    OrganisationCompleteOut,
    OrganisationListResponse,
    OrganisationFilter,
    OrganisationStatusUpdate,
    OrganisationStats,
    OrganisationGlobalStats,
    MembreOrganisationCreate,
    MembreOrganisationUpdate,
    MembreListResponse,
    MembreFilter,
    FollowerListResponse,
    FollowingListResponse,
    LogoUploadResponse,
    FollowResponse,
    OrgansisationCreateWithMembers,
    UnfollowResponse
)
from core.api.schemas import MessageResponse
from core.api.exceptions import (
    NotFoundAPIException,
    PermissionDeniedAPIException,
    BadRequestAPIException
)

logger = logging.getLogger('app')

organisations_router = Router(tags=["Organisations"])


# ==========================================
# ENDPOINTS ORGANISATIONS - CRUD
# ==========================================

@organisations_router.post(
    "/",
    response={201: OrganisationCompleteOut, 400: MessageResponse, 401: MessageResponse, 403: MessageResponse},
    auth=jwt_auth,
    summary="Crée une nouvelle organisation"
)
def create_organisation_endpoint(
    request: HttpRequest,
    payload: OrganisationCreate
):
    """
    Crée une nouvelle organisation.
    
    **Comportement :**
    - Admin site : statut 'active', non ajouté comme membre
    - Utilisateur normal : statut 'en_attente', ajouté comme admin page
    """
    try:
        new_org = organisation_service.create_organisation(
            acting_user=request.auth,
            data=payload.dict(),
            request=request
        )
        return 201, new_org
    except BadRequestAPIException as e:
        return 400, {"detail": str(e)}
    except Exception as e:
        logger.exception("Erreur création organisation")
        return 400, {"detail": "Erreur lors de la création"}

@organisations_router.post(
    "/with-members",
    response={201: OrganisationCompleteOut, 400: MessageResponse, 401: MessageResponse, 403: MessageResponse},
    auth=jwt_auth
)
def create_organisation_with_members_endpoint(
    request: HttpRequest,
    payload: OrgansisationCreateWithMembers
):
    """
    Creer une organisation avec les utilisateurs membres complet
    - Creer l'organisation
    - Creer les utilisateur User et Profil
    - Ajouter les membres
    """
    try:
        new_org = organisation_service.create_organisation_with_members(
            acting_user=request.auth,
            data=payload.dict(),
            request=request
        )
        return 201, new_org
    except BadRequestAPIException as e:
        return 400, {"detail": str(e)}
    except Exception as e:
        logger.exception("Erreur création organisation")
        return 400, {"detail": "Erreur lors de la création"}



@organisations_router.get(
    "/",
    response={200: OrganisationListResponse, 401: MessageResponse},
    auth=jwt_auth,
    summary="Liste toutes les organisations actives"
)
def list_organisations_endpoint(
    request: HttpRequest,
    filters: Query[OrganisationFilter],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """
    Liste les organisations actives avec filtres et pagination.
    
    **Filtres disponibles :**
    - search : Recherche dans nom, description, secteur, ville
    - pays : Filtrer par pays
    - secteur_activite : Filtrer par secteur
    - type_organisation : Filtrer par type
    - ville : Filtrer par ville
    """
    orgs_list, total_count = organisation_service.list_organisations(
        acting_user=request.auth,
        filters=filters.dict(exclude_unset=True),
        page=page,
        page_size=page_size,
        include_stats=True
    )
    
    return 200, build_pagination_response(orgs_list, total_count, page, page_size)


@organisations_router.get(
    "/pending",
    response={200: OrganisationListResponse, 401: MessageResponse, 403: MessageResponse},
    auth=jwt_auth,
    summary="Liste les organisations en attente"
)
def list_pending_organisations_endpoint(
    request: HttpRequest,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """
    Liste les organisations en attente d'approbation.
    
    **Permissions requises :** admin_site ou super_admin
    """
    try:
        orgs_list, total_count = organisation_service.list_pending_organisations(
            acting_user=request.auth,
            page=page,
            page_size=page_size
        )
        return 200, build_pagination_response(orgs_list, total_count, page, page_size)
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}


@organisations_router.get(
    "/statistics",
    response={200: OrganisationGlobalStats, 401: MessageResponse, 403: MessageResponse},
    auth=jwt_auth,
    summary="Statistiques globales des organisations"
)
def get_global_statistics_endpoint(request: HttpRequest):
    """
    Retourne les statistiques globales.
    
    **Permissions requises :** admin_site ou super_admin
    """
    if request.auth.role_systeme not in ['admin_site', 'super_admin']:
        return 403, {"detail": "Action non autorisée"}
    
    stats = organisation_service.get_organisation_statistics()
    return 200, stats


@organisations_router.get(
    "/slug/{slug}",
    response={200: OrganisationCompleteOut, 401: MessageResponse, 404: MessageResponse},
    auth=jwt_auth,
    summary="Récupère une organisation par son slug"
)
def get_organisation_by_slug_endpoint(request: HttpRequest, slug: str):
    """
    Récupère une organisation via son slug.
    
    **Exemple :** `/organisations/slug/ensp-maroua-x7r2p9`
    """
    org = organisation_service.get_organisation_by_slug(slug)
    if not org:
        return 404, {"detail": f"Organisation avec le slug '{slug}' introuvable"}
    
    return 200, org


@organisations_router.get(
    "/{org_id}",
    response={200: OrganisationCompleteOut, 401: MessageResponse, 404: MessageResponse},
    auth=jwt_auth,
    summary="Récupère une organisation par son ID"
)
def get_organisation_endpoint(request: HttpRequest, org_id: UUID4):
    """Récupère les informations complètes d'une organisation."""
    org = organisation_service.get_organisation_by_id(org_id, include_relations=True)
    if not org:
        return 404, {"detail": "Organisation introuvable"}
    
    return 200, org


@organisations_router.get(
    "/{org_id}/stats",
    response={200: OrganisationStats, 401: MessageResponse, 404: MessageResponse},
    auth=jwt_auth,
    summary="Statistiques d'une organisation"
)
def get_organisation_stats_endpoint(request: HttpRequest, org_id: UUID4):
    """Retourne les statistiques d'une organisation spécifique."""
    try:
        stats = organisation_service.get_organisation_stats(org_id)
        return 200, stats
    except Exception:
        return 404, {"detail": "Organisation introuvable"}


@organisations_router.put(
    "/{org_id}",
    response={200: OrganisationCompleteOut, 400: MessageResponse, 401: MessageResponse, 403: MessageResponse, 404: MessageResponse},
    auth=jwt_auth,
    summary="Met à jour une organisation"
)
def update_organisation_endpoint(
    request: HttpRequest,
    org_id: UUID4,
    payload: OrganisationUpdate
):
    """
    Met à jour les informations d'une organisation.
    
    **Permissions :** Administrateur de l'organisation ou admin site
    """
    try:
        updated_org = organisation_service.update_organisation(
            acting_user=request.auth,
            org_id=org_id,
            data=payload.dict(exclude_unset=True),
            request=request
        )
        return 200, updated_org
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except BadRequestAPIException as e:
        return 400, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Organisation introuvable"}


@organisations_router.patch(
    "/{org_id}/status",
    response={200: OrganisationCompleteOut, 400: MessageResponse, 401: MessageResponse, 403: MessageResponse, 404: MessageResponse},
    auth=jwt_auth,
    summary="Change le statut d'une organisation"
)
def update_organisation_status_endpoint(
    request: HttpRequest,
    org_id: UUID4,
    payload: OrganisationStatusUpdate
):
    """
    Change le statut d'une organisation.
    
    **Permissions requises :** admin_site ou super_admin
    """
    try:
        updated_org = organisation_service.update_organisation_status(
            acting_user=request.auth,
            org_id=org_id,
            new_status=payload.statut,
            request=request
        )
        return 200, updated_org
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except BadRequestAPIException as e:
        return 400, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Organisation introuvable"}


@organisations_router.delete(
    "/{org_id}",
    response={204: None, 401: MessageResponse, 403: MessageResponse, 404: MessageResponse},
    auth=jwt_auth,
    summary="Supprime une organisation"
)
def delete_organisation_endpoint(request: HttpRequest, org_id: UUID4):
    """
    Suppression logique d'une organisation.
    
    **Permissions requises :** admin_site ou super_admin
    """
    try:
        organisation_service.soft_delete_organisation(
            acting_user=request.auth,
            org_id=org_id,
            request=request
        )
        return 204, None
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Organisation introuvable"}


@organisations_router.post(
    "/{org_id}/restore",
    response={200: OrganisationCompleteOut, 401: MessageResponse, 403: MessageResponse, 404: MessageResponse},
    auth=jwt_auth,
    summary="Restaure une organisation supprimée"
)
def restore_organisation_endpoint(request: HttpRequest, org_id: UUID4):
    """
    Restaure une organisation précédemment supprimée.
    
    **Permissions requises :** admin_site ou super_admin
    """
    try:
        restored_org = organisation_service.restore_organisation(
            acting_user=request.auth,
            org_id=org_id,
            request=request
        )
        return 200, restored_org
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except NotFoundAPIException as e:
        return 404, {"detail": str(e)}


# ==========================================
# ENDPOINTS LOGO
# ==========================================

@organisations_router.post(
    "/{org_id}/logo",
    response={200: LogoUploadResponse, 400: MessageResponse, 401: MessageResponse, 403: MessageResponse, 404: MessageResponse},
    auth=jwt_auth,
    summary="Upload le logo de l'organisation"
)
def upload_logo_endpoint(
    request: HttpRequest,
    org_id: UUID4,
    file: File[UploadedFile]
):
    """
    Upload ou remplace le logo d'une organisation.
    
    **Formats acceptés :** JPG, JPEG, PNG, WEBP  
    **Taille max :** 2 MB  
    **Optimisation :** Conversion WebP, redimensionnement à 400x400px
    """
    try:
        updated_org = organisation_service.update_organisation_logo(
            acting_user=request.auth,
            org_id=org_id,
            logo_file=file,
            request=request
        )
        return 200, {
            "message": "Logo mis à jour avec succès",
            "logo_url": updated_org.logo.url if updated_org.logo else None
        }
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except ValueError as e:
        return 400, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Organisation introuvable"}


@organisations_router.delete(
    "/{org_id}/logo",
    response={204: None, 401: MessageResponse, 403: MessageResponse, 404: MessageResponse},
    auth=jwt_auth,
    summary="Supprime le logo de l'organisation"
)
def delete_logo_endpoint(request: HttpRequest, org_id: UUID4):
    """Supprime le logo d'une organisation."""
    try:
        organisation_service.delete_organisation_logo(
            acting_user=request.auth,
            org_id=org_id,
            request=request
        )
        return 204, None
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Organisation introuvable"}


# ==========================================
# ENDPOINTS MEMBRES
# ==========================================

@organisations_router.get(
    "/{org_id}/membres",
    response={200: MembreListResponse, 401: MessageResponse, 404: MessageResponse},
    auth=jwt_auth,
    summary="Liste les membres d'une organisation"
)
def list_membres_endpoint(
    request: HttpRequest,
    org_id: UUID4,
    filters: Query[MembreFilter],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Liste tous les membres actifs d'une organisation."""
    try:
        membres_list, total_count = membre_service.list_membres(
            org_id=org_id,
            filters=filters.dict(exclude_unset=True),
            page=page,
            page_size=page_size
        )
        return 200, build_pagination_response(membres_list, total_count, page, page_size)
    except Exception:
        return 404, {"detail": "Organisation introuvable"}


@organisations_router.post(
    "/{org_id}/membres",
    response={201: MessageResponse, 400: MessageResponse, 401: MessageResponse, 403: MessageResponse, 404: MessageResponse},
    auth=jwt_auth,
    summary="Ajoute un membre à l'organisation"
)
def add_membre_endpoint(
    request: HttpRequest,
    org_id: UUID4,
    payload: MembreOrganisationCreate
):
    """
    Ajoute un nouveau membre à l'organisation.
    
    **Permissions :** Administrateur de l'organisation
    """
    try:
        membre_service.add_membre(
            acting_user=request.auth,
            org_id=org_id,
            data=payload.dict(),
            request=request
        )
        return 201, {"detail": "Membre ajouté avec succès"}
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except BadRequestAPIException as e:
        return 400, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Organisation ou profil introuvable"}


@organisations_router.put(
    "/{org_id}/membres/{profil_id}",
    response={200: MessageResponse, 400: MessageResponse, 401: MessageResponse, 403: MessageResponse, 404: MessageResponse},
    auth=jwt_auth,
    summary="Met à jour un membre"
)
def update_membre_endpoint(
    request: HttpRequest,
    org_id: UUID4,
    profil_id: UUID4,
    payload: MembreOrganisationUpdate
):
    """
    Met à jour les informations d'un membre.
    
    **Permissions :** Administrateur de l'organisation
    """
    try:
        membre_service.update_membre(
            acting_user=request.auth,
            org_id=org_id,
            profil_id=profil_id,
            data=payload.dict(exclude_unset=True),
            request=request
        )
        return 200, {"detail": "Membre mis à jour avec succès"}
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Membre introuvable"}


@organisations_router.delete(
    "/{org_id}/membres/{profil_id}",
    response={204: None, 401: MessageResponse, 403: MessageResponse, 404: MessageResponse},
    auth=jwt_auth,
    summary="Retire un membre de l'organisation"
)
def remove_membre_endpoint(
    request: HttpRequest,
    org_id: UUID4,
    profil_id: UUID4
):
    """
    Retire un membre de l'organisation.
    
    **Permissions :** Administrateur de l'organisation
    """
    try:
        membre_service.remove_membre(
            acting_user=request.auth,
            org_id=org_id,
            profil_id=profil_id,
            request=request
        )
        return 204, None
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Membre introuvable"}


# ==========================================
# ENDPOINTS ABONNEMENTS
# ==========================================

@organisations_router.post(
    "/{org_id}/follow",
    response={201: FollowResponse, 400: MessageResponse, 401: MessageResponse, 404: MessageResponse},
    auth=jwt_auth,
    summary="Suivre une organisation"
)
def follow_organisation_endpoint(request: HttpRequest, org_id: UUID4):
    """Permet à l'utilisateur connecté de suivre une organisation."""
    try:
        subscription = abonnement_service.follow_organisation(
            acting_user=request.auth,
            org_id=org_id,
            request=request
        )
        return 201, {
            "message": "Vous suivez maintenant cette organisation",
            "organisation": subscription.organisation
        }
    except BadRequestAPIException as e:
        return 400, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Organisation introuvable"}


@organisations_router.delete(
    "/{org_id}/follow",
    response={200: UnfollowResponse, 401: MessageResponse, 404: MessageResponse},
    auth=jwt_auth,
    summary="Ne plus suivre une organisation"
)
def unfollow_organisation_endpoint(request: HttpRequest, org_id: UUID4):
    """Permet à l'utilisateur connecté de ne plus suivre une organisation."""
    try:
        abonnement_service.unfollow_organisation(
            acting_user=request.auth,
            org_id=org_id,
            request=request
        )
        return 200, {"message": "Vous ne suivez plus cette organisation"}
    except NotFoundAPIException as e:
        return 404, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Organisation introuvable"}


@organisations_router.get(
    "/{org_id}/followers",
    response={200: FollowerListResponse, 401: MessageResponse, 404: MessageResponse},
    auth=jwt_auth,
    summary="Liste les abonnés d'une organisation"
)
def list_followers_endpoint(
    request: HttpRequest,
    org_id: UUID4,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Liste tous les utilisateurs qui suivent l'organisation."""
    try:
        followers_list, total_count = abonnement_service.list_followers(
            org_id=org_id,
            page=page,
            page_size=page_size
        )
        return 200, build_pagination_response(followers_list, total_count, page, page_size)
    except Exception:
        return 404, {"detail": "Organisation introuvable"}


@organisations_router.get(
    "/me/following",
    response={200: FollowingListResponse, 401: MessageResponse},
    auth=jwt_auth,
    summary="Liste les organisations suivies"
)
def list_following_endpoint(
    request: HttpRequest,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Liste toutes les organisations que l'utilisateur suit."""
    following_list, total_count = abonnement_service.list_following(
        acting_user=request.auth,
        page=page,
        page_size=page_size
    )
    return 200, build_pagination_response(following_list, total_count, page, page_size)