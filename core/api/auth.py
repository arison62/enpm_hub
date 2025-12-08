from ninja import Router
from django.http import HttpRequest
from core.services.auth_service import AuthService, jwt_auth
from django.views.decorators.csrf import csrf_exempt
from core.api.schemas import LoginSchema, TokenSchema, UserSchema
from ninja.security import django_auth

# Création du Router
auth_router = Router(tags=["Authentification"])

@auth_router.post(
    "/login", 
    response={200: TokenSchema, 401: dict}, 
    summary="Authentification par Matricule ou Email"
)
def login_endpoint(request: HttpRequest, payload: LoginSchema):
    """
    Connecte l'utilisateur en créant une session (pour Inertia) et des tokens JWT (pour React).
    """
    # 1. Appel du Service Layer (logique métier dans AuthService)
    auth_data = AuthService.login_user(request, payload.login_id, payload.password)
    
    # 2. Gestion des erreurs et de la réponse
    if auth_data is None:
        return 401, {"detail": "Identifiant ou mot de passe invalide."}

    return 200, auth_data

@auth_router.post(
    "/logout", 
    response={204: None}, 
    auth=[django_auth, jwt_auth], # Permet la déconnexion via Session ou JWT
    summary="Déconnexion de l'utilisateur"
)
@csrf_exempt
def logout_endpoint(request: HttpRequest):
    """
    Déconnecte l'utilisateur, supprime la session et enregistre l'AuditLog.
    """
    # Utilisation de request.user pour l'AuditLog
    AuthService.logout_user(request)
    
    return 204, None # 204 No Content

@auth_router.get(
    "/me", 
    response={200: UserSchema, 401: dict}, 
    auth=[jwt_auth, django_auth], # Accès par JWT (API) ou Session (Template/Inertia)
    summary="Récupère les informations de l'utilisateur connecté"
)
def get_current_user(request: HttpRequest):
    """
    Retourne les informations de l'utilisateur après authentification par JWT ou Session.
    """
    # request.auth contient l'utilisateur authentifié (grâce à jwt_auth ou django_auth)
    # Le type est garanti d'être User car l'authentification a réussi
    return 200, request.auth # type: ignore