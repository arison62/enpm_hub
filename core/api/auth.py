# core/api/auth.py
from ninja import Router
from django.http import HttpRequest
from core.services.auth_service import AuthService, jwt_auth
from django.views.decorators.csrf import csrf_exempt
from core.api.schemas import LoginSchema, TokenSchema, UserSchema, RefreshTokenSchema
from ninja.security import django_auth
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from ninja.errors import HttpError

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

@auth_router.post(
    "/refresh",
    response={200: TokenSchema, 401: dict},
    summary="Rafraîchit un token JWT"
)
def refresh_token(request: HttpRequest, payload: RefreshTokenSchema):
    """
    Accepte un refresh token valide et retourne une nouvelle paire
    de tokens (access et refresh), implémentant ainsi la rotation.
    """
    try:
        refresh = RefreshToken(payload.refresh) # type: ignore

        # La rotation est gérée automatiquement si `ROTATE_REFRESH_TOKENS` est à True.
        # Le simple fait d'accéder à `refresh.access_token` peut suffire si
        # la rotation est la seule chose que l'on souhaite.
        # Pour être explicite et clair, nous allons créer les nouveaux tokens.

        new_access_token = str(refresh.access_token)
        new_refresh_token = str(refresh)

        # Note : Le `user_id` et le `role` sont extraits du token.
        # simple-jwt ajoute automatiquement ces infos si le User model est standard.
        # Pour notre modèle custom, vérifions que les claims sont bien là.
        user_id = refresh.get('user_id')

        # On doit récupérer le rôle depuis la BDD pour être sûr qu'il est à jour.
        from core.models import User
        try:
            user = User.objects.get(id=user_id)
            role = user.role
        except User.DoesNotExist:
            return 401, {"detail": "L'utilisateur associé à ce token n'existe plus."}

        return 200, {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "user_id": str(user_id),
            "role": role
        }

    except TokenError as e:
        # Le refresh token est invalide, expiré ou a déjà été utilisé
        return 401, {"detail": f"Token de rafraîchissement invalide ou expiré. {str(e)}"}

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