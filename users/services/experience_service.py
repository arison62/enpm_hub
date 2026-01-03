import logging
from typing import List, Dict, Optional, Tuple
from uuid import UUID
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError

from core.models import User, AuditLog
from core.services.audit_service import audit_log_service
from users.models import Profil, ExperienceProfessionnelle
from users.api.schemas import ExperienceProfessionnelleCreate, ExperienceProfessionnelleUpdate
from core.api.exceptions import (
    PermissionDeniedAPIException,
    NotFoundAPIException,
    BadRequestAPIException
)

logger = logging.getLogger('app')

class ExperienceService:
    """
    Service contenant la logique métier pour la gestion des expériences professionnelles.
    Gère le CRUD, la validation des dates, l'audit et la sécurité (RLS).
    """

    # ==========================================
    # UTILITAIRES & VERIFICATIONS
    # ==========================================

    @staticmethod
    def _validate_dates(date_debut, date_fin, est_poste_actuel):
        """Valide la logique temporelle de l'expérience."""
        if est_poste_actuel and date_fin:
             # Règle métier : Si c'est actuel, on ignore la date de fin envoyée
            return None 
            
        if date_fin and date_debut > date_fin:
            raise BadRequestAPIException(
                "La date de fin ne peut pas être antérieure à la date de début."
            )
        return date_fin

    @staticmethod
    def _serialize_for_audit(instance) -> Dict:
        """Helper pour nettoyer les données avant l'audit (exclusion des objets non sérialisables)."""
        data = model_to_dict(instance, exclude=['profil', 'organisation', 'created_at', 'updated_at'])
        # Conversion manuelle des dates en string pour le JSONField
        if data.get('date_debut'): data['date_debut'] = str(data['date_debut'])
        if data.get('date_fin'): data['date_fin'] = str(data['date_fin'])
        return data

    # ==========================================
    # CRUD EXPERIENCES
    # ==========================================

    @staticmethod
    def list_experiences(
        user: Optional[User] = None,
        profil_id: Optional[UUID] = None,
        request = None
    ) -> List[ExperienceProfessionnelle]:
        """
        Liste les expériences.
        - Si profil_id est fourni : Vue publique (CV d'un autre membre).
        - Si user est fourni sans profil_id : Vue privée (Mes expériences).
        """
        qs = ExperienceProfessionnelle.objects.select_related('organisation')

        if profil_id:
            qs = qs.filter(profil_id=profil_id)
        elif user:
            try:
                qs = qs.filter(profil=user.profil) # type: ignore
            except Profil.DoesNotExist:
                return []
        else:
            return []

        # Tri : Postes actuels en premier, puis du plus récent au plus ancien
        return list(qs.order_by('-est_poste_actuel', '-date_debut'))

    @staticmethod
    @transaction.atomic
    def create_experience(acting_user: User, profil_id: UUID, data: ExperienceProfessionnelleCreate, request=None) -> ExperienceProfessionnelle:
        """
        Ajoute une nouvelle expérience au profil de l'utilisateur.
        """

        # 1. Validation et Nettoyage
        cleaned_date_fin = ExperienceService._validate_dates(
            data.date_debut, 
            data.date_fin, 
            data.est_poste_actuel
        )

        # 2. Création
        # Note : exclude_unset=True est important pour ne pas écraser les défauts avec des None
        experience_data = data.dict(exclude_unset=True)
        experience_data['date_fin'] = cleaned_date_fin # Applique la date nettoyée

        try:
            experience = ExperienceProfessionnelle.objects.create(
                profil_id=profil_id,
                **experience_data
            )
        except Exception as e:
            logger.error(f"Erreur DB création expérience user {acting_user.id}: {str(e)}")
            raise BadRequestAPIException("Impossible de créer l'expérience. Vérifiez les données.")

        # 3. Audit Log
        audit_log_service.log_action(
            user=acting_user,
            action=AuditLog.AuditAction.CREATE,
            entity_type= "ExperienceProfessionnelle",
            entity_id= experience.id,
            new_values=ExperienceService._serialize_for_audit(experience),
            request=request
        )


        logger.info(f"Expérience créée pour {acting_user.email}: {experience.titre_poste}")
        
        return experience

    @staticmethod
    @transaction.atomic
    def update_experience(
        acting_user: User, 
        experience_id: UUID, 
        data: ExperienceProfessionnelleUpdate,
        request = None
    ) -> ExperienceProfessionnelle:
        """
        Met à jour une expérience existante.
        Sécurité : Vérifie que l'expérience appartient bien à l'utilisateur (RLS).
        """
        # 1. Récupération sécurisée (RLS)
        try:
            experience = ExperienceProfessionnelle.objects.select_for_update().get(
                id=experience_id, 
                profil__user=acting_user
            )
        except ExperienceProfessionnelle.DoesNotExist:
            raise NotFoundAPIException("Expérience introuvable ou accès refusé.")

        # Capture pour Audit
        ancien_data = ExperienceService._serialize_for_audit(experience)

        # 2. Application des modifications
        incoming_data = data.dict(exclude_unset=True)
        
        # Logique spéciale pour les dates lors de l'update
        # On doit prendre les nouvelles dates ou garder les anciennes pour la validation
        new_date_debut = incoming_data.get('date_debut', experience.date_debut)
        new_date_fin = incoming_data.get('date_fin', experience.date_fin)
        new_est_poste = incoming_data.get('est_poste_actuel', experience.est_poste_actuel)

        cleaned_date_fin = ExperienceService._validate_dates(new_date_debut, new_date_fin, new_est_poste)
        
        # Mise à jour des champs
        for field, value in incoming_data.items():
            setattr(experience, field, value)
        
        experience.date_fin = cleaned_date_fin # Force la cohérence
        experience.save()

        # 3. Audit Log
        audit_log_service.log_action(
            user=acting_user,
            action=AuditLog.AuditAction.UPDATE,
            entity_type= "ExperienceProfessionnelle",
            entity_id= experience.id,
            new_values=ExperienceService._serialize_for_audit(experience),
            old_values=ancien_data,
            request=request
        )        

        logger.info(f"Expérience {experience_id} mise à jour par {acting_user.email}")
        return experience

    @staticmethod
    @transaction.atomic
    def delete_experience(acting_user: User, experience_id: UUID, request=None):
        """
        Supprime une expérience.
        Sécurité : Vérifie que l'expérience appartient bien à l'utilisateur (RLS).
        """
        # 1. Récupération sécurisée (RLS)
        try:
            experience = ExperienceProfessionnelle.objects.get(
                id=experience_id, 
                profil__user=acting_user
            )
        except ExperienceProfessionnelle.DoesNotExist:
            raise NotFoundAPIException("Expérience introuvable ou accès refusé.")

        description_log = f"{experience.titre_poste} chez {experience.nom_entreprise}"
        ancien_data = ExperienceService._serialize_for_audit(experience)

        # 2. Suppression
        experience.delete()
        # 3. Audit Log
        audit_log_service.log_action(
            user=acting_user,
            action=AuditLog.AuditAction.DELETE,
            entity_type= "ExperienceProfessionnelle",
            entity_id= experience_id,
            old_values=ExperienceService._serialize_for_audit(experience),
            request=request
        )

        logger.info(f"Expérience supprimée par {acting_user.email}: {description_log}")

# Singleton pour usage direct dans les controllers
experience_service = ExperienceService()