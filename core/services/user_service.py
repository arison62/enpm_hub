import logging
import os
from typing import Optional
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.core.files.uploadedfile import UploadedFile
from django.core.files.storage import default_storage
from django.conf import settings
from core.models import User, Profil
from core.services.audit_service import audit_log_service, AuditLog
from core.services.email_service import EmailTemplates
from PIL import Image
from io import BytesIO

logger = logging.getLogger('app')

class UserService:
    """
    Service contenant la logique métier pour la gestion des utilisateurs.
    """
    
    ALLOWED_PHOTO_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']
    MAX_PHOTO_SIZE = 5 * 1024 * 1024
    PHOTO_MAX_DIMENSIONS = (800, 800)

    @staticmethod
    @transaction.atomic
    def create_user(acting_user: User, user_data: dict, request=None) -> User:
        if User.objects.filter(email=user_data.get('email')).exists():
            raise ValueError(f"Un utilisateur avec l'email {user_data.get('email')} existe déjà.")

        profil_data = user_data.pop('profil', {})
        if not profil_data.get('nom_complet'):
            raise ValueError("Le nom complet est requis pour la création du profil.")

        random_password = get_random_string(12)
        user_data['password'] = make_password(random_password)

        if user_data.get('role_systeme') in ['admin_site', 'super_admin']:
            user_data['is_staff'] = True

        new_user = User.objects.create(**user_data)
        Profil.objects.create(user=new_user, **profil_data)

        logger.info(f"Nouvel utilisateur créé (ID: {new_user.id}) par {acting_user.email}.")

        audit_data = {**user_data, 'profil': profil_data}
        audit_data.pop('password', None)

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
        profil_data = data_update.pop('profil', None)
        old_values = {}

        if data_update:
            for field, value in data_update.items():
                old_values[field] = getattr(user_to_update, field)
                setattr(user_to_update, field, value)
            user_to_update.save()

        if profil_data:
            profil, _ = Profil.objects.get_or_create(user=user_to_update)
            for field, value in profil_data.items():
                old_values[f'profil__{field}'] = getattr(profil, field)
                setattr(profil, field, value)
            profil.save()

        logger.info(f"Utilisateur (ID: {user_to_update.id}) mis à jour par {acting_user.email}.")
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
        user_to_delete.soft_delete()
        logger.info(f"Utilisateur (ID: {user_to_delete.id}) supprimé (soft delete) par {acting_user.email}.")
        audit_log_service.log_action(
            user=acting_user,
            action=AuditLog.AuditAction.DELETE,
            entity_type='User',
            entity_id=user_to_delete.id,
            request=request
        )

    @staticmethod
    def _validate_photo(photo_file: UploadedFile):
        if not photo_file:
            raise ValueError("Aucun fichier n'a été fourni.")
        file_ext = os.path.splitext(photo_file.name)[1].lower()
        if file_ext not in UserService.ALLOWED_PHOTO_EXTENSIONS:
            raise ValueError(f"Format de fichier non autorisé. Acceptés : {', '.join(UserService.ALLOWED_PHOTO_EXTENSIONS)}")
        if photo_file.size > UserService.MAX_PHOTO_SIZE:
            raise ValueError(f"La taille du fichier dépasse {UserService.MAX_PHOTO_SIZE / (1024*1024)} MB.")
        try:
            Image.open(photo_file).verify()
        except Exception:
            raise ValueError("Le fichier n'est pas une image valide.")

    @staticmethod
    def _optimize_photo(photo_file: UploadedFile) -> BytesIO:
        image = Image.open(photo_file)
        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')
        image.thumbnail(UserService.PHOTO_MAX_DIMENSIONS, Image.Resampling.LANCZOS)
        output = BytesIO()
        image.save(output, format='JPEG', quality=85)
        output.seek(0)
        return output

    @staticmethod
    @transaction.atomic
    def upload_profile_photo(acting_user: User, user: User, photo_file: UploadedFile, request=None) -> User:
        UserService._validate_photo(photo_file)
        profil, _ = Profil.objects.get_or_create(user=user)

        if profil.photo_profil and profil.photo_profil.path and os.path.exists(profil.photo_profil.path):
            os.remove(profil.photo_profil.path)

        optimized_photo = UserService._optimize_photo(photo_file)
        file_name = f"profile_{user.id}.jpg"
        saved_path = default_storage.save(os.path.join('photos_profils', file_name), optimized_photo)

        profil.photo_profil = saved_path # type: ignore
        profil.save()

        logger.info(f"Photo de profil mise à jour pour {user.id} par {acting_user.email}.")
        audit_log_service.log_action(
            user=acting_user,
            action=AuditLog.AuditAction.UPDATE,
            entity_type='Profil',
            entity_id=profil.id,
            request=request,
            new_values={'photo_profil': saved_path}
        )
        return user

    @staticmethod
    @transaction.atomic
    def delete_profile_photo(acting_user: User, user: User, request=None):
        profil = getattr(user, 'profil', None)
        if not profil or not profil.photo_profil:
            return user

        if profil.photo_profil.path and os.path.exists(profil.photo_profil.path):
            os.remove(profil.photo_profil.path)

        profil.photo_profil = None
        profil.save()

        logger.info(f"Photo de profil de {user.id} supprimée par {acting_user.email}.")
        audit_log_service.log_action(
            user=acting_user,
            action=AuditLog.AuditAction.UPDATE,
            entity_type='Profil',
            entity_id=profil.id,
            request=request,
            new_values={'photo_profil': None}
        )
        return user

user_service = UserService()
