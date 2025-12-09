import logging
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from core.models import User
from core.api.schemas import UserCreateSchema # Assurez-vous que ce schéma existe
from core.services.audit_service import audit_log_service, AuditLog

logger = logging.getLogger(__name__)

class UserService:
    """
    Service contenant la logique métier pour la gestion des utilisateurs.
    """

    @staticmethod
    @transaction.atomic
    def create_user(acting_user: User, user_data: dict, request=None) -> User:
        """
        Crée un nouvel utilisateur, génère un mot de passe aléatoire
        et enregistre l'action dans le journal d'audit.
        """
        # Génération d'un mot de passe aléatoire et sécurisé
        random_password = get_random_string(12)
        password_hash = make_password(random_password)

        user_data['password'] = password_hash

        # Assurer que le personnel technique est aussi un membre du staff Django
        if user_data.get('statut') == 'personnel_technique':
            user_data['is_staff'] = True

        # Création de l'utilisateur
        new_user = User.objects.create(**user_data)
        logger.info(f"Nouvel utilisateur créé (ID: {new_user.id}) par {acting_user.email}.")

        # Préparation des données pour l'audit (SANS le mot de passe)
        audit_data = user_data.copy()
        audit_data.pop('password', None)

        # Audit Log
        audit_log_service.log_action(
            user=acting_user,
            action=AuditLog.AuditAction.CREATE,
            entity_type='User',
            entity_id=new_user.id,
            request=request,
            new_values=audit_data
        )

        return new_user

    @staticmethod
    @transaction.atomic
    def update_user(acting_user: User, user_to_update: User, data_update: dict, request=None) -> User:
        """
        Met à jour un utilisateur et enregistre les modifications dans l'audit log.
        """
        old_values = {field: getattr(user_to_update, field) for field in data_update.keys()}

        # Mise à jour des champs
        for field, value in data_update.items():
            setattr(user_to_update, field, value)

        # Cas spécial pour le mot de passe
        if 'password' in data_update and data_update['password']:
            user_to_update.set_password(data_update['password'])

        # Assurer la cohérence du statut et du rôle 'staff'
        if 'statut' in data_update:
            user_to_update.is_staff = (data_update['statut'] == 'personnel_technique')

        user_to_update.save()
        logger.info(f"Utilisateur (ID: {user_to_update.id}) mis à jour par {acting_user.email}.")

        # Audit Log
        audit_log_service.log_action(
            user=acting_user,
            action=AuditLog.AuditAction.UPDATE,
            entity_type='User',
            entity_id=user_to_update.id,
            request=request,
            old_values=old_values,
            new_values=data_update
        )

        return user_to_update

    @staticmethod
    @transaction.atomic
    def soft_delete_user(acting_user: User, user_to_delete: User, request=None):
        """
        Effectue une suppression logique (soft delete) d'un utilisateur.
        """
        user_to_delete.soft_delete()
        logger.info(f"Utilisateur (ID: {user_to_delete.id}) supprimé (soft delete) par {acting_user.email}.")

        # Audit Log
        audit_log_service.log_action(
            user=acting_user,
            action=AuditLog.AuditAction.DELETE,
            entity_type='User',
            entity_id=user_to_delete.id,
            request=request,
            old_values={'id': str(user_to_delete.id), 'deleted': False}
        )

# Instanciation du service pour une utilisation facile
user_service = UserService()
