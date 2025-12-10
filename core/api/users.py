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
    UserCreateSchema, 
    UserUpdateSchema, 
    UserListSchema, 
    UserSchema,
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
    page_size = 20  # Nombre d'éléments par page par défaut
    page_size_query_param = "page_size"  # Paramètre pour changer la taille
    max_page_size = 100  # Taille maximale autorisée

# ==========================================
# Fonctions de Permissions 
# ==========================================

def is_admin(request: HttpRequest) -> bool:
    """Vérifie si l'utilisateur a le role 'admin' ou 'super_admin'."""
    return request.auth.role in ['admin', 'super_admin'] # type: ignore

def is_owner_or_admin(request: HttpRequest, user_id: str) -> bool:
    """
    Vérifie si l'utilisateur est le propriétaire de la ressource
    OU s'il a le rôle admin/super_admin.
    """
    return str(request.auth.id) == user_id or is_admin(request) # type: ignore

# ==========================================
# Endpoints CRUD
# ==========================================

@users_router.post(
    "/",
    response={201: UserSchema, 403: dict, 400: dict},
    auth=jwt_auth,
    summary="Crée un nouvel utilisateur (admin uniquement)"
)
def create_user_endpoint(request: HttpRequest, payload: UserCreateSchema):
    """
    Crée un utilisateur. Réservé aux administrateurs (admin et super_admin).
    """
    # Vérification des permissions : seuls les admins peuvent créer
    if not is_admin(request):
        return 403, {"detail": "Action non autorisée. Seuls les administrateurs peuvent créer des utilisateurs."}

    try:
        new_user = user_service.create_user(
            acting_user=request.auth, # type: ignore
            user_data=payload.dict(),
            request=request
        )
        return 201, new_user
    except ValueError as e:
        return 400, {"detail": str(e)}

@users_router.get(
    "/",
    response=List[UserListSchema],
    auth=jwt_auth,
    summary="Liste les utilisateurs avec filtres et pagination"
)
@paginate(CustomPagination)
def list_users_endpoint(
    request: HttpRequest, 
    filters: Query[UserFilterSchema]
):
    """
    Retourne une liste paginée d'utilisateurs avec recherche optimisée.
    
    La recherche globale (param 'search') cherche dans : nom, prenom, email, matricule.
    Vous pouvez également filtrer par role, statut, est_actif, travailleur.
    """
    # Requête de base : seulement les utilisateurs actifs et non supprimés
    users = User.objects.filter(est_actif=True, deleted=False)
    search = filters.search
    role = filters.role
    statut = filters.statut
    est_actif = filters.est_actif
    travailleur = filters.travailleur
    # Recherche globale optimisée avec Q objects
    if search:
        search_query = Q(nom__icontains=search) | \
                      Q(prenom__icontains=search) | \
                      Q(email__icontains=search) | \
                      Q(matricule__icontains=search)
        users = users.filter(search_query)
    
    # Filtres spécifiques
    if role:
        users = users.filter(role=role)
    if statut:
        users = users.filter(statut=statut)
    if est_actif is not None:
        users = users.filter(est_actif=est_actif)
    if travailleur is not None:
        users = users.filter(travailleur=travailleur)

    # Optimisation : sélection uniquement des champs nécessaires
    users = users.only('id', 'nom', 'prenom', 'email', 'statut', 'travailleur', 'photo_profile', 'role', 'est_actif')
    
    return users.order_by('nom', 'prenom')

@users_router.get(
    "/{user_id}",
    response={200: UserSchema, 404: dict},
    auth=jwt_auth,
    summary="Récupère un utilisateur par son ID"
)
def get_user_endpoint(request: HttpRequest, user_id: str):
    """Retourne les détails d'un utilisateur spécifique."""
    user = get_object_or_404(User, id=user_id, deleted=False)
    return 200, user

@users_router.put(
    "/{user_id}",
    response={200: UserSchema, 403: dict, 404: dict, 400: dict},
    auth=jwt_auth,
    summary="Met à jour un utilisateur"
)
def update_user_endpoint(request: HttpRequest, user_id: str, payload: UserUpdateSchema):
    """
    Met à jour un utilisateur. 
    Autorisé pour : le propriétaire du compte OU un administrateur.
    """
    # Vérification des permissions
    if not is_owner_or_admin(request, user_id):
        return 403, {"detail": "Action non autorisée. Vous ne pouvez modifier que votre propre profil."}

    user_to_update = get_object_or_404(User, id=user_id, deleted=False)

    # Sécurité : seuls les admins peuvent modifier le rôle
    if 'role' in payload.dict(exclude_unset=True) and not is_admin(request):
        return 403, {"detail": "Seuls les administrateurs peuvent modifier le rôle d'un utilisateur."}

    try:
        updated_user = user_service.update_user(
            acting_user=request.auth, # type: ignore
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
    """
    Supprime un utilisateur (soft delete). 
    Autorisé pour : le propriétaire du compte OU un administrateur.
    """
    # Vérification des permissions
    if not is_owner_or_admin(request, user_id):
        return 403, {"detail": "Action non autorisée."}

    user_to_delete = get_object_or_404(User, id=user_id, deleted=False)

    user_service.soft_delete_user(
        acting_user=request.auth, # type: ignore
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
    file: File[UploadedFile]
):
    """
    Upload ou remplace la photo de profil d'un utilisateur.
    Autorisé pour : le propriétaire du compte OU un administrateur.
    
    Formats acceptés : JPG, JPEG, PNG, WEBP
    Taille maximale : 5 MB
    """
    # Vérification des permissions
    if not is_owner_or_admin(request, user_id):
        return 403, {"detail": "Action non autorisée. Vous ne pouvez modifier que votre propre photo."}

    user = get_object_or_404(User, id=user_id, deleted=False)

    try:
        updated_user = user_service.upload_profile_photo(
            acting_user=request.auth, # type: ignore
            user=user,
            photo_file=file,
            request=request
        )
        
        return 200, {
            "message": "Photo de profil mise à jour avec succès",
            "photo_url": updated_user.photo_profile.url if updated_user.photo_profile else None
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
    # Vérification des permissions
    if not is_owner_or_admin(request, user_id):
        return 403, {"detail": "Action non autorisée."}

    user = get_object_or_404(User, id=user_id, deleted=False)

    user_service.delete_profile_photo(
        acting_user=request.auth, # type: ignore
        user=user,
        request=request
    )
    
    return 204, None