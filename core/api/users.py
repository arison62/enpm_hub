import logging
from typing import List
from ninja import Router, Query, File, UploadedFile
from ninja.pagination import paginate, PageNumberPagination
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.db.models import Q
from core.models import User
from core.services.user_service import user_service
from core.api.schemas import (
    UserCreateAdminSchema,
    UserUpdateAdminSchema,
    UserDetailSchema,
    UserFilterSchema,
    PhotoUploadResponseSchema
)
from core.services.auth_service import jwt_auth

logger = logging.getLogger("app")

# Création du Router
users_router = Router(tags=["Utilisateurs"])

# ==========================================
# Configuration de la pagination
# ==========================================
class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

# ==========================================
# Fonctions de Permissions 
# ==========================================
def is_admin(request: HttpRequest) -> bool:
    """Vérifie si l'utilisateur a le rôle 'admin_site' ou 'super_admin'."""
    user = request.auth
    return user.role_systeme in ['admin_site', 'super_admin']

def is_owner_or_admin(request: HttpRequest, user_id: str) -> bool:
    """Vérifie si l'utilisateur est le propriétaire ou un admin."""
    return str(request.auth.id) == user_id or is_admin(request)

# ==========================================
# Endpoints CRUD
# ==========================================
@users_router.post(
    "/",
    response={201: UserDetailSchema, 403: dict, 400: dict},
    auth=jwt_auth,
    summary="Crée un nouvel utilisateur (admin uniquement)"
)
def create_user_endpoint(request: HttpRequest, payload: UserCreateAdminSchema):
    if not is_admin(request):
        return 403, {"detail": "Action non autorisée."}
    try:
        new_user = user_service.create_user(
            acting_user=request.auth,
            user_data=payload.dict(),
            request=request
        )
        return 201, new_user
    except ValueError as e:
        return 400, {"detail": str(e)}

@users_router.get(
    "/",
    response=List[UserDetailSchema],
    auth=jwt_auth,
    summary="Liste les utilisateurs avec filtres et pagination"
)
@paginate(CustomPagination)
def list_users_endpoint(request: HttpRequest, filters: UserFilterSchema = Query(...)):
    users = User.objects.select_related('profil').filter(deleted=False)
    
    if filters.search:
        users = users.filter(
            Q(profil__nom_complet__icontains=filters.search) |
            Q(email__icontains=filters.search) |
            Q(profil__matricule__icontains=filters.search)
        )
    if filters.role_systeme:
        users = users.filter(role_systeme=filters.role_systeme)
    if filters.statut_global:
        users = users.filter(profil__statut_global=filters.statut_global)
    if filters.est_actif is not None:
        users = users.filter(est_actif=filters.est_actif)
    if filters.travailleur is not None:
        users = users.filter(profil__travailleur=filters.travailleur)

    return users.order_by('profil__nom_complet')

@users_router.get(
    "/{user_id}",
    response={200: UserDetailSchema, 404: dict},
    auth=jwt_auth,
    summary="Récupère un utilisateur par son ID"
)
def get_user_endpoint(request: HttpRequest, user_id: str):
    user = get_object_or_404(User.objects.select_related('profil'), id=user_id, deleted=False)
    return 200, user

@users_router.put(
    "/{user_id}",
    response={200: UserDetailSchema, 403: dict, 404: dict, 400: dict},
    auth=jwt_auth,
    summary="Met à jour un utilisateur"
)
def update_user_endpoint(request: HttpRequest, user_id: str, payload: UserUpdateAdminSchema):
    if not is_owner_or_admin(request, user_id):
        return 403, {"detail": "Action non autorisée."}

    user_to_update = get_object_or_404(User, id=user_id, deleted=False)

    if 'role_systeme' in payload.dict(exclude_unset=True) and not is_admin(request):
        return 403, {"detail": "Seuls les administrateurs peuvent modifier le rôle."}

    try:
        updated_user = user_service.update_user(
            acting_user=request.auth,
            user_to_update=user_to_update,
            data_update=payload.dict(exclude_unset=True),
            request=request
        )
        return 200, updated_user
    except ValueError as e:
        return 400, {"detail": str(e)}

@users_router.delete(
    "/{user_id}",
    response={204: None, 403: dict, 404: dict},
    auth=jwt_auth,
    summary="Supprime (soft delete) un utilisateur"
)
def delete_user_endpoint(request: HttpRequest, user_id: str):
    if not is_owner_or_admin(request, user_id):
        return 403, {"detail": "Action non autorisée."}

    user_to_delete = get_object_or_404(User, id=user_id, deleted=False)
    user_service.soft_delete_user(
        acting_user=request.auth,
        user_to_delete=user_to_delete,
        request=request
    )
    return 204, None

# ==========================================
# Upload de photo de profil
# ==========================================

@users_router.post(
    "/{user_id}/photo",
    response={200: PhotoUploadResponseSchema, 403: dict, 404: dict, 400: dict},
    auth=jwt_auth,
    summary="Upload ou met à jour la photo de profil"
)
def upload_profile_photo(
    request: HttpRequest, 
    user_id: str, 
    file: UploadedFile = File(...)
):
    """
    Upload ou remplace la photo de profil d'un utilisateur.
    Autorisé pour : le propriétaire du compte OU un administrateur.
    
    Formats acceptés : JPG, JPEG, PNG, WEBP
    Taille maximale : 5 MB
    """
    if not is_owner_or_admin(request, user_id):
        return 403, {"detail": "Action non autorisée."}

    user = get_object_or_404(User, id=user_id, deleted=False)

    try:
        updated_user = user_service.upload_profile_photo(
            acting_user=request.auth,
            user=user,
            photo_file=file,
            request=request
        )
        
        return 200, {
            "message": "Photo de profil mise à jour avec succès",
            "photo_profil_url": updated_user.profil.photo_profil.url if updated_user.profil.photo_profil else None
        }
    except ValueError as e:
        return 400, {"detail": str(e)}

@users_router.delete(
    "/{user_id}/photo",
    response={204: None, 403: dict, 404: dict},
    auth=jwt_auth,
    summary="Supprime la photo de profil"
)
def delete_profile_photo(request: HttpRequest, user_id: str):
    """
    Supprime la photo de profil d'un utilisateur.
    Autorisé pour : le propriétaire du compte OU un administrateur.
    """
    if not is_owner_or_admin(request, user_id):
        return 403, {"detail": "Action non autorisée."}

    user = get_object_or_404(User, id=user_id, deleted=False)

    user_service.delete_profile_photo(
        acting_user=request.auth,
        user=user,
        request=request
    )
    
    return 204, None
