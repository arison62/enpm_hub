# core/api/auth.py
from ninja import Router
from ninja.throttling import AnonRateThrottle
from django.http import HttpRequest
from core.api.schemas import LoginSchema, PasswordResetConfirm, PasswordResetRequest, RefreshTokenSchema, TokenSchema
from core.services.auth_service import AuthService, jwt_auth
from django.views.decorators.csrf import csrf_exempt
from users.api.schemas import UserDetailOut,  MessageResponse, ValidationErrorResponse
from ninja.security import django_auth
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from core.models import User
from users.services.user_service import user_service
from core.services.email_service import EmailTemplates

# Création du Router
auth_router = Router(tags=["Authentification"])

@auth_router.post(
    "/login", 
    response={200: TokenSchema, 401: MessageResponse, 422: ValidationErrorResponse  },
    summary="Authentification par Email"
)
def login_endpoint(request: HttpRequest, payload: LoginSchema):
    """
    Connecte l'utilisateur en créant une session (pour Inertia) et des tokens JWT (pour React).
    """
    # 1. Appel du Service Layer (logique métier dans AuthService)
    auth_data = AuthService.login_user(request, payload.email, payload.password)
    # 2. Gestion des erreurs et de la réponse
    if auth_data is None:
        return 401, {"detail": "Identifiant ou mot de passe invalide."}

    return 200, auth_data

@auth_router.post(
    "/logout", 
    response={204: None, 401: MessageResponse},
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
    response={200: TokenSchema, 401: MessageResponse, 422: ValidationErrorResponse},
    summary="Rafraîchit un token JWT"
)
def refresh_token(request: HttpRequest, payload: RefreshTokenSchema):
    """
    Accepte un refresh token valide et retourne une nouvelle paire
    de tokens (access et refresh), implémentant ainsi la rotation.
    """
    try:
        refresh = RefreshToken(payload.refresh) # type: ignore

        new_access_token = str(refresh.access_token)
        new_refresh_token = str(refresh)

        user_id = refresh.get('user_id')
        try:
            user = User.objects.select_related('profil').get(id=user_id)
        except User.DoesNotExist:
            return 401, {"detail": "L'utilisateur associé à ce token n'existe plus."}

        return 200, {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "user": user
        }

    except TokenError as e:
        return 401, {"detail": f"Token de rafraîchissement invalide ou expiré. {str(e)}"}


@auth_router.get(
    "/me", 
    response={200: UserDetailOut, 401: MessageResponse},
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


@auth_router.post("/password-reset-request"
    , response={204: None, 422: ValidationErrorResponse}
    ,summary="Lance la procédure de réinitialisation du mot de passe")
def password_reset_request_endpoint(request: HttpRequest, payload: PasswordResetRequest):
    """
    Lance la procédure de réinitialisation de mot de passe en générant un token OTP
    et en l'envoyant par la méthode spécifiée (email ou SMS).
    Retourne toujours 204 pour des raisons de sécurité.
    """
    AuthService.request_password_reset(user_id=payload.user_id, method=payload.method)
    return 204, None

@auth_router.post("/password-reset-confirm", 
    response={204: None, 400: MessageResponse, 422: ValidationErrorResponse},
    throttle=[
        AnonRateThrottle(rate='5/m'),  # 5 requêtes par minute pour les utilisateurs anonymes
    ]
    ,summary="Confirme la réinitialisation du mot de passe")
def password_reset_confirm_endpoint(request: HttpRequest, payload: PasswordResetConfirm):
    """
    Confirme la réinitialisation du mot de passe en validant le token OTP
    et en mettant à jour le mot de passe de l'utilisateur.
    Retourne 204 si réussi, 400 si le token est invalide ou expiré.
    """
    success = AuthService.confirm_password_reset(
        user_id=payload.user_id,
        token=payload.token,
        new_password=payload.new_password
    )
    if success:
        return 204, None
    else:
        return 400, {"detail": "Token invalide ou expiré."}
