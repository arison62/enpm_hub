import logging
import os
from typing import Optional
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.core.files.uploadedfile import UploadedFile
from django.core.files.storage import default_storage
from django.conf import settings
from core.models import User
from core.services.audit_service import audit_log_service, AuditLog
from PIL import Image
from io import BytesIO

logger = logging.getLogger('app')

class UserService:
    """
    Service contenant la logique métier pour la gestion des utilisateurs.
    """
    
    # Configuration pour les photos de profil
    ALLOWED_PHOTO_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']
    MAX_PHOTO_SIZE = 5 * 1024 * 1024  # 5 MB
    PHOTO_MAX_DIMENSIONS = (800, 800)  # Redimensionner les images trop grandes

    @staticmethod
    @transaction.atomic
    def create_user(acting_user: User, user_data: dict, request=None) -> User:
        """
        Crée un nouvel utilisateur, génère un mot de passe aléatoire
        et enregistre l'action dans le journal d'audit.
        """
        # Validation : vérifier que l'email n'existe pas déjà
        if User.objects.filter(email=user_data.get('email')).exists():
            raise ValueError(f"Un utilisateur avec l'email {user_data.get('email')} existe déjà.")
        
        # Validation : vérifier que le matricule n'existe pas (si fourni)
        if user_data.get('matricule') and User.objects.filter(matricule=user_data.get('matricule')).exists():
            raise ValueError(f"Un utilisateur avec le matricule {user_data.get('matricule')} existe déjà.")

        # Génération d'un mot de passe aléatoire et sécurisé
        random_password = get_random_string(12)
        password_hash = make_password(random_password)
        user_data['password'] = password_hash

        # Logique métier : le personnel technique doit avoir accès à l'admin Django
        if user_data.get('statut') == 'personnel_technique':
            user_data['is_staff'] = True

        # Création de l'utilisateur
        new_user = User.objects.create(**user_data)
        logger.info(f"Nouvel utilisateur créé (ID: {new_user.id}) par {acting_user.email}.")

        # Préparation des données pour l'audit (SANS le mot de passe)
        audit_data = user_data.copy()
        audit_data.pop('password', None)
        audit_data['generated_password'] = random_password  # Pour envoi par email

        # Audit Log
        audit_log_service.log_action(
            user=acting_user,
            action=AuditLog.AuditAction.CREATE,
            entity_type='User',
            entity_id=new_user.id,
            request=request,
            new_values=audit_data
        )

        # TODO: Envoyer le mot de passe par email à l'utilisateur
        logger.warning(f"Mot de passe généré pour {new_user.email}: {random_password} (À envoyer par email)")

        return new_user

    @staticmethod
    @transaction.atomic
    def update_user(acting_user: User, user_to_update: User, data_update: dict, request=None) -> User:
        """
        Met à jour un utilisateur et enregistre les modifications dans l'audit log.
        """
        # Validation : vérifier l'unicité de l'email si modifié
        if 'email' in data_update:
            existing_user = User.objects.filter(email=data_update['email']).exclude(id=user_to_update.id).first()
            if existing_user:
                raise ValueError(f"L'email {data_update['email']} est déjà utilisé par un autre utilisateur.")
        
        # Validation : vérifier l'unicité du matricule si modifié
        if 'matricule' in data_update and data_update['matricule']:
            existing_user = User.objects.filter(matricule=data_update['matricule']).exclude(id=user_to_update.id).first()
            if existing_user:
                raise ValueError(f"Le matricule {data_update['matricule']} est déjà utilisé par un autre utilisateur.")

        # Sauvegarde des anciennes valeurs pour l'audit
        old_values = {field: getattr(user_to_update, field) for field in data_update.keys()}

        # Mise à jour des champs
        for field, value in data_update.items():
            if field == 'password':
                # Cas spécial pour le mot de passe
                if value:
                    user_to_update.set_password(value)
            else:
                setattr(user_to_update, field, value)

        # Logique métier : synchroniser is_staff avec le statut
        if 'statut' in data_update:
            user_to_update.is_staff = (data_update['statut'] == 'personnel_technique')

        user_to_update.save()
        logger.info(f"Utilisateur (ID: {user_to_update.id}) mis à jour par {acting_user.email}.")

        # Audit Log (sans le mot de passe)
        audit_data = data_update.copy()
        if 'password' in audit_data:
            audit_data['password'] = '***HIDDEN***'

        audit_log_service.log_action(
            user=acting_user,
            action=AuditLog.AuditAction.UPDATE,
            entity_type='User',
            entity_id=user_to_update.id,
            request=request,
            old_values=old_values,
            new_values=audit_data
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

    @staticmethod
    def _validate_photo(photo_file: UploadedFile) -> None:
        """
        Valide le fichier photo uploadé.
        Vérifie : extension, taille, format image valide.
        """
        # Vérifier l'extension
        file_ext = os.path.splitext(photo_file.name)[1].lower()
        if file_ext not in UserService.ALLOWED_PHOTO_EXTENSIONS:
            raise ValueError(
                f"Format de fichier non autorisé. Formats acceptés : {', '.join(UserService.ALLOWED_PHOTO_EXTENSIONS)}"
            )

        # Vérifier la taille
        if photo_file.size > UserService.MAX_PHOTO_SIZE:
            max_size_mb = UserService.MAX_PHOTO_SIZE / (1024 * 1024)
            raise ValueError(f"La taille du fichier dépasse {max_size_mb} MB.")

        # Vérifier que c'est une image valide
        try:
            image = Image.open(photo_file)
            image.verify()
        except Exception:
            raise ValueError("Le fichier n'est pas une image valide.")

    @staticmethod
    def _optimize_photo(photo_file: UploadedFile) -> BytesIO:
        """
        Optimise la photo : redimensionne si nécessaire et compresse.
        Retourne un objet BytesIO contenant l'image optimisée.
        """
        image = Image.open(photo_file)
        
        # Convertir en RGB si nécessaire (pour PNG avec transparence)
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background

        # Redimensionner si l'image est trop grande
        image.thumbnail(UserService.PHOTO_MAX_DIMENSIONS, Image.Resampling.LANCZOS)

        # Sauvegarder dans un buffer
        output = BytesIO()
        image.save(output, format='JPEG', quality=85, optimize=True)
        output.seek(0)
        
        return output

    @staticmethod
    @transaction.atomic
    def upload_profile_photo(acting_user: User, user: User, photo_file: UploadedFile, request=None) -> User:
        """
        Upload ou met à jour la photo de profil d'un utilisateur.
        Supprime l'ancienne photo si elle existe.
        """
        # Validation du fichier
        UserService._validate_photo(photo_file)

        # Supprimer l'ancienne photo si elle existe
        if user.photo_profile:
            old_photo_path = user.photo_profile.path
            if os.path.exists(old_photo_path):
                os.remove(old_photo_path)
                logger.info(f"Ancienne photo supprimée : {old_photo_path}")

        # Optimiser l'image
        optimized_photo = UserService._optimize_photo(photo_file)

        # Générer un nom de fichier unique basé sur l'ID utilisateur
        file_ext = '.jpg'  # Toujours JPEG après optimisation
        file_name = f"profile_{user.id}{file_ext}"
        file_path = os.path.join('profils', file_name)

        # Sauvegarder le fichier
        saved_path = default_storage.save(file_path, optimized_photo)
        user.photo_profile = saved_path # type: ignore
        user.save()

        logger.info(f"Photo de profil mise à jour pour l'utilisateur {user.id} par {acting_user.email}.")

        # Audit Log
        audit_log_service.log_action(
            user=acting_user,
            action=AuditLog.AuditAction.UPDATE,
            entity_type='User',
            entity_id=user.id,
            request=request,
            new_values={'photo_profile': saved_path}
        )

        return user

    @staticmethod
    @transaction.atomic
    def delete_profile_photo(acting_user: User, user: User, request=None) -> User:
        """
        Supprime la photo de profil d'un utilisateur.
        """
        if not user.photo_profile:
            logger.warning(f"Tentative de suppression de photo inexistante pour l'utilisateur {user.id}.")
            return user

        # Supprimer le fichier physique
        photo_path = user.photo_profile.path
        if os.path.exists(photo_path):
            os.remove(photo_path)
            logger.info(f"Photo supprimée : {photo_path}")

        old_photo = user.photo_profile.name
        user.photo_profile = None # type: ignore
        user.save()

        logger.info(f"Photo de profil supprimée pour l'utilisateur {user.id} par {acting_user.email}.")

        # Audit Log
        audit_log_service.log_action(
            user=acting_user,
            action=AuditLog.AuditAction.UPDATE,
            entity_type='User',
            entity_id=user.id,
            request=request,
            old_values={'photo_profile': old_photo},
            new_values={'photo_profile': None}
        )

        return user

# Instanciation du service pour une utilisation facile
user_service = UserService()