from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.conf import settings
from phonenumber_field.phonenumber import PhoneNumber
import logging

# Initialisation du logger
logger = logging.getLogger("app")

User = get_user_model()

class EmailOrPhoneAuthBackend(BaseBackend):
    """
    Backend d'authentification personnalisé.
    Permet la connexion via email OU téléphone, avec le mot de passe.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        La variable 'username' ici est en réalité l'identifiant (email ou téléphone)
        fourni par l'utilisateur lors de la tentative de connexion.
        """
        if not username or not password:
            return None

        # Tentative de recherche de l'utilisateur par email OU téléphone
        try:
            if '@' in username:
                # Recherche par email, insensible à la casse
                user = User.objects.get(email__iexact=username)
            else:
                # Recherche par téléphone : normaliser le numéro
                phone = PhoneNumber.from_string(username, region='CM')  # 'CM' pour Cameroun
                if not phone.is_valid():
                    raise ValueError("Numéro de téléphone invalide")
                
                user = User.objects.get(telephone=phone)
        except (User.DoesNotExist, ValueError):
            logger.info(f"Échec authentification: Identifiant non trouvé: {username}")
            return None

        # Vérification du mot de passe et du statut actif
        if user.check_password(password) and user.est_actif:  # type: ignore
            # Logging : L'AuditLog sera géré dans le Service d'Auth pour ne pas polluer le backend
            logger.info(
                f"Authentification réussie pour User ID: {user.id} ({user.email or user.telephone})",  # type: ignore
                extra={'user_id': str(user.id), 'auth_method': 'email_or_phone'}  # type: ignore
            )
            return user

        # Journalisation des échecs (mot de passe ou inactif)
        if not user.est_actif:  # type: ignore
            logger.warning(f"Tentative de connexion échouée (Compte inactif) pour: {username}")
        else:
            logger.warning(f"Tentative de connexion échouée (Mot de passe invalide) pour: {username}")
        return None

    def get_user(self, user_id):
        """Requis par Django pour récupérer l'utilisateur à partir de l'ID de session."""
        try:
            # Utiliser all_objects pour supporter les sessions des comptes qui ont été soft-deleted
            # (Bien qu'une session active doive être invalidée si soft_delete est appelé).
            return User.all_objects.get(pk=user_id)  # type: ignore
        except User.DoesNotExist:
            return None