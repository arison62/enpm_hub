# opportunities/api/views.py
import logging
from ninja import Router, Query
from django.http import HttpRequest
from pydantic import UUID4

from core.utils.pagination import build_pagination_response
from core.services.auth_service import jwt_auth
from opportunities.services.stage_service import stage_service
from opportunities.services.emploi_service import emploi_service
from opportunities.services.formation_service import formation_service
from opportunities.api.schemas import (
    # Stages
    StageCreateSchema,
    StageUpdateSchema,
    StageOutSchema,
    StageListResponseSchema,
    StageFilterSchema,
    StageValidationSchema,
    StageStatusUpdateSchema,
    StageStatsSchema,
    # Emplois
    EmploiCreateSchema,
    EmploiUpdateSchema,
    EmploiOutSchema,
    EmploiListResponseSchema,
    EmploiFilterSchema,
    EmploiValidationSchema,
    EmploiStatusUpdateSchema,
    EmploiStatsSchema,
    # Formations
    FormationCreateSchema,
    FormationUpdateSchema,
    FormationOutSchema,
    FormationListResponseSchema,
    FormationFilterSchema,
    FormationValidationSchema,
    FormationStatusUpdateSchema,
    FormationStatsSchema,
    # Communs
    MessageSchema
)
from core.api.exceptions import (
    PermissionDeniedAPIException,
    BadRequestAPIException
)

logger = logging.getLogger('app')

# Création des routers
stages_router = Router(tags=["Stages"])
emplois_router = Router(tags=["Emplois"])
formations_router = Router(tags=["Formations"])


# ==========================================
# ENDPOINTS STAGES
# ==========================================

@stages_router.post(
    "/",
    response={201: StageOutSchema, 400: MessageSchema, 401: MessageSchema},
    auth=jwt_auth,
    summary="Créer un stage"
)
def create_stage_endpoint(request: HttpRequest, payload: StageCreateSchema):
    """
    Crée une nouvelle offre de stage.
    
    **Validation automatique pour :**
    - Partenaires (membres d'organisation avec statut_global='partenaire')
    - Administrateurs du site
    
    **Validation requise pour :**
    - Utilisateurs normaux
    """
    try:
        new_stage = stage_service.create_stage(
            acting_user=request.auth,
            data=payload.dict(),
            request=request
        )
        return 201, new_stage
    except BadRequestAPIException as e:
        return 400, {"detail": str(e)}
    except Exception as e:
        logger.exception("Erreur création stage")
        return 400, {"detail": "Erreur lors de la création"}


@stages_router.get(
    "/",
    response={200: StageListResponseSchema, 401: MessageSchema},
    auth=jwt_auth,
    summary="Liste des stages"
)
def list_stages_endpoint(
    request: HttpRequest,
    filters: Query[StageFilterSchema],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """
    Liste les stages actifs et validés.
    
    **Filtres disponibles :**
    - search : Recherche dans titre, description, structure, lieu
    - type_stage : ouvrier, academique, professionnel
    - lieu, ville, pays : Filtrer par localisation
    - statut : active, expiree, pourvue
    """
    stages_list, total_count = stage_service.list_stages(
        filters=filters.dict(exclude_unset=True),
        page=page,
        page_size=page_size
    )
    
    return 200, build_pagination_response(stages_list, total_count, page, page_size)


@stages_router.get(
    "/pending",
    response={200: StageListResponseSchema, 401: MessageSchema, 403: MessageSchema},
    auth=jwt_auth,
    summary="Stages en attente de validation"
)
def list_pending_stages_endpoint(
    request: HttpRequest,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """
    Liste les stages en attente de validation.
    
    **Permissions requises :** admin_site ou super_admin
    """
    try:
        stages_list, total_count = stage_service.list_pending_stages(
            acting_user=request.auth,
            page=page,
            page_size=page_size
        )
        return 200, build_pagination_response(stages_list, total_count, page, page_size)
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}


@stages_router.get(
    "/statistics",
    response={200: StageStatsSchema, 401: MessageSchema, 403: MessageSchema},
    auth=jwt_auth,
    summary="Statistiques des stages"
)
def get_stage_statistics_endpoint(request: HttpRequest):
    """
    Statistiques globales des stages.
    
    **Permissions requises :** admin_site ou super_admin
    """
    if request.auth.role_systeme not in ['admin_site', 'super_admin']:
        return 403, {"detail": "Action non autorisée"}
    
    stats = stage_service.get_stage_statistics()
    return 200, stats


@stages_router.get(
    "/me",
    response={200: StageListResponseSchema, 401: MessageSchema},
    auth=jwt_auth,
    summary="Mes stages créés"
)
def get_my_stages_endpoint(
    request: HttpRequest,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Liste tous les stages créés par l'utilisateur connecté."""
    stages_list, total_count = stage_service.get_user_stages(
        user=request.auth,
        page=page,
        page_size=page_size
    )
    return 200, build_pagination_response(stages_list, total_count, page, page_size)


@stages_router.get(
    "/slug/{slug}",
    response={200: StageOutSchema, 401: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Récupérer un stage par son slug"
)
def get_stage_by_slug_endpoint(request: HttpRequest, slug: str):
    """Récupère un stage via son slug unique."""
    stage = stage_service.get_stage_by_slug(slug)
    if not stage:
        return 404, {"detail": f"Stage avec le slug '{slug}' introuvable"}
    return 200, stage


@stages_router.get(
    "/{stage_id}",
    response={200: StageOutSchema, 401: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Récupérer un stage par son ID"
)
def get_stage_endpoint(request: HttpRequest, stage_id: UUID4):
    """Récupère les détails complets d'un stage."""
    stage = stage_service.get_stage_by_id(stage_id)
    if not stage:
        return 404, {"detail": "Stage introuvable"}
    return 200, stage


@stages_router.put(
    "/{stage_id}",
    response={200: StageOutSchema, 400: MessageSchema, 401: MessageSchema, 403: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Mettre à jour un stage"
)
def update_stage_endpoint(
    request: HttpRequest,
    stage_id: UUID4,
    payload: StageUpdateSchema
):
    """
    Met à jour un stage.
    
    **Permissions :** Créateur, admin de l'organisation ou admin du site
    """
    try:
        updated_stage = stage_service.update_stage(
            acting_user=request.auth,
            stage_id=stage_id,
            data=payload.dict(exclude_unset=True),
            request=request
        )
        return 200, updated_stage
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except BadRequestAPIException as e:
        return 400, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Stage introuvable"}


@stages_router.post(
    "/{stage_id}/validate",
    response={200: StageOutSchema, 400: MessageSchema, 401: MessageSchema, 403: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Valider ou rejeter un stage"
)
def validate_stage_endpoint(
    request: HttpRequest,
    stage_id: UUID4,
    payload: StageValidationSchema
):
    """
    Valide ou rejette un stage en attente.
    
    **Permissions requises :** admin_site ou super_admin
    """
    try:
        validated_stage = stage_service.validate_stage(
            acting_user=request.auth,
            stage_id=stage_id,
            approved=payload.approved,
            commentaire=payload.commentaire,
            request=request
        )
        return 200, validated_stage
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except BadRequestAPIException as e:
        return 400, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Stage introuvable"}


@stages_router.patch(
    "/{stage_id}/status",
    response={200: StageOutSchema, 400: MessageSchema, 401: MessageSchema, 403: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Changer le statut d'un stage"
)
def update_stage_status_endpoint(
    request: HttpRequest,
    stage_id: UUID4,
    payload: StageStatusUpdateSchema
):
    """
    Change le statut d'un stage (active, expiree, pourvue).
    
    **Permissions :** Gestionnaire du stage
    """
    try:
        updated_stage = stage_service.update_stage_status(
            acting_user=request.auth,
            stage_id=stage_id,
            new_status=payload.statut,
            request=request
        )
        return 200, updated_stage
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except BadRequestAPIException as e:
        return 400, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Stage introuvable"}


@stages_router.delete(
    "/{stage_id}",
    response={204: None, 401: MessageSchema, 403: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Supprimer un stage"
)
def delete_stage_endpoint(request: HttpRequest, stage_id: UUID4):
    """
    Suppression logique d'un stage.
    
    **Permissions :** Gestionnaire du stage
    """
    try:
        stage_service.soft_delete_stage(
            acting_user=request.auth,
            stage_id=stage_id,
            request=request
        )
        return 204, None
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Stage introuvable"}


# ==========================================
# ENDPOINTS EMPLOIS
# ==========================================

@emplois_router.post(
    "/",
    response={201: EmploiOutSchema, 400: MessageSchema, 401: MessageSchema},
    auth=jwt_auth,
    summary="Créer une offre d'emploi"
)
def create_emploi_endpoint(request: HttpRequest, payload: EmploiCreateSchema):
    """Crée une nouvelle offre d'emploi."""
    try:
        new_emploi = emploi_service.create_emploi(
            acting_user=request.auth,
            data=payload.dict(),
            request=request
        )
        return 201, new_emploi
    except BadRequestAPIException as e:
        return 400, {"detail": str(e)}


@emplois_router.get(
    "/",
    response={200: EmploiListResponseSchema, 401: MessageSchema},
    auth=jwt_auth,
    summary="Liste des emplois"
)
def list_emplois_endpoint(
    request: HttpRequest,
    filters: Query[EmploiFilterSchema],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Liste les offres d'emploi actives et validées."""
    emplois_list, total_count = emploi_service.list_emplois(
        filters=filters.dict(exclude_unset=True),
        page=page,
        page_size=page_size
    )
    return 200, build_pagination_response(emplois_list, total_count, page, page_size)


@emplois_router.get(
    "/pending",
    response={200: EmploiListResponseSchema, 401: MessageSchema, 403: MessageSchema},
    auth=jwt_auth,
    summary="Emplois en attente"
)
def list_pending_emplois_endpoint(
    request: HttpRequest,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Liste les emplois en attente de validation."""
    try:
        emplois_list, total_count = emploi_service.list_pending_emplois(
            acting_user=request.auth,
            page=page,
            page_size=page_size
        )
        return 200, build_pagination_response(emplois_list, total_count, page, page_size)
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}


@emplois_router.get(
    "/statistics",
    response={200: EmploiStatsSchema, 401: MessageSchema, 403: MessageSchema},
    auth=jwt_auth,
    summary="Statistiques des emplois"
)
def get_emploi_statistics_endpoint(request: HttpRequest):
    """Statistiques globales des emplois."""
    if request.auth.role_systeme not in ['admin_site', 'super_admin']:
        return 403, {"detail": "Action non autorisée"}
    
    stats = emploi_service.get_emploi_statistics()
    return 200, stats


@emplois_router.get(
    "/slug/{slug}",
    response={200: EmploiOutSchema, 401: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Récupérer un emploi par slug"
)
def get_emploi_by_slug_endpoint(request: HttpRequest, slug: str):
    """Récupère un emploi via son slug unique."""
    emploi = emploi_service.get_emploi_by_slug(slug)
    if not emploi:
        return 404, {"detail": f"Emploi avec le slug '{slug}' introuvable"}
    return 200, emploi


@emplois_router.get(
    "/{emploi_id}",
    response={200: EmploiOutSchema, 401: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Récupérer un emploi par ID"
)
def get_emploi_endpoint(request: HttpRequest, emploi_id: UUID4):
    """Récupère les détails d'un emploi."""
    emploi = emploi_service.get_emploi_by_id(emploi_id)
    if not emploi:
        return 404, {"detail": "Emploi introuvable"}
    return 200, emploi


@emplois_router.put(
    "/{emploi_id}",
    response={200: EmploiOutSchema, 400: MessageSchema, 401: MessageSchema, 403: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Mettre à jour un emploi"
)
def update_emploi_endpoint(
    request: HttpRequest,
    emploi_id: UUID4,
    payload: EmploiUpdateSchema
):
    """Met à jour une offre d'emploi."""
    try:
        updated_emploi = emploi_service.update_emploi(
            acting_user=request.auth,
            emploi_id=emploi_id,
            data=payload.dict(exclude_unset=True),
            request=request
        )
        return 200, updated_emploi
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except BadRequestAPIException as e:
        return 400, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Emploi introuvable"}


@emplois_router.post(
    "/{emploi_id}/validate",
    response={200: EmploiOutSchema, 400: MessageSchema, 401: MessageSchema, 403: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Valider un emploi"
)
def validate_emploi_endpoint(
    request: HttpRequest,
    emploi_id: UUID4,
    payload: EmploiValidationSchema
):
    """Valide ou rejette une offre d'emploi."""
    try:
        validated_emploi = emploi_service.validate_emploi(
            acting_user=request.auth,
            emploi_id=emploi_id,
            approved=payload.approved,
            commentaire=payload.commentaire,
            request=request
        )
        return 200, validated_emploi
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except BadRequestAPIException as e:
        return 400, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Emploi introuvable"}


@emplois_router.patch(
    "/{emploi_id}/status",
    response={200: EmploiOutSchema, 400: MessageSchema, 401: MessageSchema, 403: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Changer le statut d'un emploi"
)
def update_emploi_status_endpoint(
    request: HttpRequest,
    emploi_id: UUID4,
    payload: EmploiStatusUpdateSchema
):
    """Change le statut d'une offre d'emploi."""
    try:
        updated_emploi = emploi_service.update_emploi_status(
            acting_user=request.auth,
            emploi_id=emploi_id,
            new_status=payload.statut,
            request=request
        )
        return 200, updated_emploi
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except BadRequestAPIException as e:
        return 400, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Emploi introuvable"}


@emplois_router.delete(
    "/{emploi_id}",
    response={204: None, 401: MessageSchema, 403: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Supprimer un emploi"
)
def delete_emploi_endpoint(request: HttpRequest, emploi_id: UUID4):
    """Suppression logique d'un emploi."""
    try:
        emploi_service.soft_delete_emploi(
            acting_user=request.auth,
            emploi_id=emploi_id,
            request=request
        )
        return 204, None
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Emploi introuvable"}


# ==========================================
# ENDPOINTS FORMATIONS
# ==========================================

@formations_router.post(
    "/",
    response={201: FormationOutSchema, 400: MessageSchema, 401: MessageSchema},
    auth=jwt_auth,
    summary="Créer une formation"
)
def create_formation_endpoint(request: HttpRequest, payload: FormationCreateSchema):
    """Crée une nouvelle formation."""
    try:
        new_formation = formation_service.create_formation(
            acting_user=request.auth,
            data=payload.dict(),
            request=request
        )
        return 201, new_formation
    except BadRequestAPIException as e:
        return 400, {"detail": str(e)}


@formations_router.get(
    "/",
    response={200: FormationListResponseSchema, 401: MessageSchema},
    auth=jwt_auth,
    summary="Liste des formations"
)
def list_formations_endpoint(
    request: HttpRequest,
    filters: Query[FormationFilterSchema],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Liste les formations actives et validées."""
    formations_list, total_count = formation_service.list_formations(
        filters=filters.dict(exclude_unset=True),
        page=page,
        page_size=page_size
    )
    return 200, build_pagination_response(formations_list, total_count, page, page_size)


@formations_router.get(
    "/pending",
    response={200: FormationListResponseSchema, 401: MessageSchema, 403: MessageSchema},
    auth=jwt_auth,
    summary="Formations en attente"
)
def list_pending_formations_endpoint(
    request: HttpRequest,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Liste les formations en attente de validation."""
    try:
        formations_list, total_count = formation_service.list_pending_formations(
            acting_user=request.auth,
            page=page,
            page_size=page_size
        )
        return 200, build_pagination_response(formations_list, total_count, page, page_size)
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}


@formations_router.get(
    "/statistics",
    response={200: FormationStatsSchema, 401: MessageSchema, 403: MessageSchema},
    auth=jwt_auth,
    summary="Statistiques des formations"
)
def get_formation_statistics_endpoint(request: HttpRequest):
    """Statistiques globales des formations."""
    if request.auth.role_systeme not in ['admin_site', 'super_admin']:
        return 403, {"detail": "Action non autorisée"}
    
    stats = formation_service.get_formation_statistics()
    return 200, stats


@formations_router.get(
    "/slug/{slug}",
    response={200: FormationOutSchema, 401: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Récupérer une formation par slug"
)
def get_formation_by_slug_endpoint(request: HttpRequest, slug: str):
    """Récupère une formation via son slug unique."""
    formation = formation_service.get_formation_by_slug(slug)
    if not formation:
        return 404, {"detail": f"Formation avec le slug '{slug}' introuvable"}
    return 200, formation


@formations_router.get(
    "/{formation_id}",
    response={200: FormationOutSchema, 401: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Récupérer une formation par ID"
)
def get_formation_endpoint(request: HttpRequest, formation_id: UUID4):
    """Récupère les détails d'une formation."""
    formation = formation_service.get_formation_by_id(formation_id)
    if not formation:
        return 404, {"detail": "Formation introuvable"}
    return 200, formation


@formations_router.put(
    "/{formation_id}",
    response={200: FormationOutSchema, 400: MessageSchema, 401: MessageSchema, 403: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Mettre à jour une formation"
)
def update_formation_endpoint(
    request: HttpRequest,
    formation_id: UUID4,
    payload: FormationUpdateSchema
):
    """Met à jour une formation."""
    try:
        updated_formation = formation_service.update_formation(
            acting_user=request.auth,
            formation_id=formation_id,
            data=payload.dict(exclude_unset=True),
            request=request
        )
        return 200, updated_formation
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except BadRequestAPIException as e:
        return 400, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Formation introuvable"}


@formations_router.post(
    "/{formation_id}/validate",
    response={200: FormationOutSchema, 400: MessageSchema, 401: MessageSchema, 403: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Valider une formation"
)
def validate_formation_endpoint(
    request: HttpRequest,
    formation_id: UUID4,
    payload: FormationValidationSchema
):
    """Valide ou rejette une formation."""
    try:
        validated_formation = formation_service.validate_formation(
            acting_user=request.auth,
            formation_id=formation_id,
            approved=payload.approved,
            commentaire=payload.commentaire,
            request=request
        )
        return 200, validated_formation
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except BadRequestAPIException as e:
        return 400, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Formation introuvable"}


@formations_router.patch(
    "/{formation_id}/status",
    response={200: FormationOutSchema, 400: MessageSchema, 401: MessageSchema, 403: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Changer le statut d'une formation"
)
def update_formation_status_endpoint(
    request: HttpRequest,
    formation_id: UUID4,
    payload: FormationStatusUpdateSchema
):
    """Change le statut d'une formation."""
    try:
        updated_formation = formation_service.update_formation_status(
            acting_user=request.auth,
            formation_id=formation_id,
            new_status=payload.statut,
            request=request
        )
        return 200, updated_formation
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except BadRequestAPIException as e:
        return 400, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Formation introuvable"}


@formations_router.delete(
    "/{formation_id}",
    response={204: None, 401: MessageSchema, 403: MessageSchema, 404: MessageSchema},
    auth=jwt_auth,
    summary="Supprimer une formation"
)
def delete_formation_endpoint(request: HttpRequest, formation_id: UUID4):
    """Suppression logique d'une formation."""
    try:
        formation_service.soft_delete_formation(
            acting_user=request.auth,
            formation_id=formation_id,
            request=request
        )
        return 204, None
    except PermissionDeniedAPIException as e:
        return 403, {"detail": str(e)}
    except Exception:
        return 404, {"detail": "Formation introuvable"}