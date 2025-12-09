import logging
from typing import List
from ninja import Router, Query
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from core.models import User
from core.services.user_service import user_service
from core.api.schemas import UserCreateSchema, UserUpdateSchema, UserListSchema, UserSchema
from core.services.auth_service import jwt_auth
from ninja.pagination import paginate

logger = logging.getLogger(__name__)

# Création du Router
users_router = Router(tags=["Utilisateurs"])

# ==========================================
# Fonctions de Permissions
# ==========================================

# Note sur les permissions :
# Le statut 'personnel_technique' est utilisé pour les permissions administratives
# spécifiques à l'application, car il définit un groupe fonctionnel métier,
# tandis que le champ 'role' est réservé à des permissions plus larges (user, admin).

def is_technical_staff(request: HttpRequest) -> bool:
    """Vérifie si l'utilisateur authentifié est un 'personnel_technique'."""
    return request.auth.statut == 'personnel_technique'

def is_owner_or_technical_staff(request: HttpRequest, obj_user_id: str) -> bool:
    """
    Vérifie si l'utilisateur est le propriétaire de l'objet
    OU un 'personnel_technique'.
    """
    if request.auth.statut == 'personnel_technique':
        return True
    return str(request.auth.id) == obj_user_id

# ==========================================
# Endpoints CRUD
# ==========================================

@users_router.post(
    "/",
    response={201: UserSchema, 403: str},
    auth=jwt_auth,
    summary="Crée un nouvel utilisateur (admin seulement)"
)
def create_user_endpoint(request: HttpRequest, payload: UserCreateSchema):
    """Crée un utilisateur. Réservé au personnel technique."""
    if not is_technical_staff(request):
        return 403, "Action non autorisée."

    new_user = user_service.create_user(
        acting_user=request.auth,
        user_data=payload.dict(),
        request=request
    )
    return 201, new_user

@users_router.get(
    "/",
    response=List[UserListSchema],
    auth=jwt_auth,
    summary="Liste les utilisateurs avec filtres et pagination"
)
@paginate
def list_users_endpoint(request: HttpRequest, email: str = None, nom: str = None, prenom: str = None, role: str = None, est_actif: bool = None):
    """
    Retourne une liste paginée d'utilisateurs.
    Filtres optionnels: email, nom, prenom, role, est_actif.
    """
    users = User.objects.all()
    if email:
        users = users.filter(email__icontains=email)
    if nom:
        users = users.filter(nom__icontains=nom)
    if prenom:
        users = users.filter(prenom__icontains=prenom)
    if role:
        users = users.filter(role=role)
    if est_actif is not None:
        users = users.filter(est_actif=est_actif)

    return users.order_by('nom')

@users_router.get(
    "/{user_id}",
    response={200: UserSchema, 404: str},
    auth=jwt_auth,
    summary="Récupère un utilisateur par son ID"
)
def get_user_endpoint(request: HttpRequest, user_id: str):
    """Retourne les détails d'un utilisateur spécifique."""
    user = get_object_or_404(User, id=user_id)
    return 200, user

@users_router.patch(
    "/{user_id}",
    response={200: UserSchema, 403: str, 404: str},
    auth=jwt_auth,
    summary="Met à jour un utilisateur"
)
def update_user_endpoint(request: HttpRequest, user_id: str, payload: UserUpdateSchema):
    """Met à jour un utilisateur. Autorisé pour le propriétaire ou un admin."""
    if not is_owner_or_technical_staff(request, user_id):
        return 403, "Action non autorisée."

    user_to_update = get_object_or_404(User, id=user_id)

    updated_user = user_service.update_user(
        acting_user=request.auth,
        user_to_update=user_to_update,
        data_update=payload.dict(exclude_unset=True),
        request=request
    )
    return 200, updated_user

@users_router.delete(
    "/{user_id}",
    response={204: None, 403: str, 404: str},
    auth=jwt_auth,
    summary="Supprime (soft delete) un utilisateur"
)
def delete_user_endpoint(request: HttpRequest, user_id: str):
    """Supprime un utilisateur. Autorisé pour le propriétaire ou un admin."""
    if not is_owner_or_technical_staff(request, user_id):
        return 403, "Action non autorisée."

    user_to_delete = get_object_or_404(User, id=user_id)

    user_service.soft_delete_user(
        acting_user=request.auth,
        user_to_delete=user_to_delete,
        request=request
    )
    return 204, None
