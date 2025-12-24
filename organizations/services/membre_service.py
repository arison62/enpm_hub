
# organizations/services/membre_service.py
import logging
from typing import List, Dict, Optional, Tuple
from uuid import UUID
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from core.models import User
from users.models import Profil
from organizations.models import Organisation, MembreOrganisation
from core.api.exceptions import (
    PermissionDeniedAPIException,
    BadRequestAPIException
)
from organizations.services.organisation_service import OrganisationService

logger = logging.getLogger('app')


class MembreService:
    """
    Service contenant la logique métier pour la gestion des membres d'organisations.
    """

    @staticmethod
    def list_membres(
        org_id: UUID,
        filters: Dict = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[MembreOrganisation], int]:
        """
        Liste les membres actifs d'une organisation avec filtres et pagination.
        
        Args:
            org_id: UUID de l'organisation
            filters: Filtres (search, role_organisation)
            page: Numéro de page
            page_size: Taille de page
        
        Returns:
            Tuple (liste_membres, total_count)
        """
        organisation = get_object_or_404(Organisation, id=org_id, deleted=False)
        
        queryset = MembreOrganisation.objects.filter(
            organisation=organisation,
            est_actif=True
        ).select_related('profil', 'profil__user')
        
        # Application des filtres
        if filters:
            if search := filters.get('search'):
                queryset = queryset.filter(
                    Q(profil__nom_complet__icontains=search) |
                    Q(poste__icontains=search) |
                    Q(profil__user__email__icontains=search)
                )
            
            if role := filters.get('role_organisation'):
                queryset = queryset.filter(role_organisation=role)
        
        total_count = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        
        membres = list(queryset.order_by('profil__nom_complet')[start:end])
        
        return membres, total_count

    @staticmethod
    def get_membre_by_id(
        org_id: UUID,
        profil_id: UUID
    ) -> Optional[MembreOrganisation]:
        """
        Récupère un membre spécifique d'une organisation.
        """
        try:
            return MembreOrganisation.objects.select_related(
                'profil',
                'profil__user'
            ).get(
                organisation_id=org_id,
                profil_id=profil_id,
                est_actif=True
            )
        except MembreOrganisation.DoesNotExist:
            logger.warning(
                f"Membre non trouvé - Org: {org_id}, Profil: {profil_id}"
            )
            return None

    @staticmethod
    def is_membre(user: User, org_id: UUID) -> bool:
        """Vérifie si un utilisateur est membre d'une organisation."""
        return MembreOrganisation.objects.filter(
            organisation_id=org_id,
            profil__user=user,
            est_actif=True
        ).exists()

    @staticmethod
    def is_admin(user: User, org_id: UUID) -> bool:
        """Vérifie si un utilisateur est admin d'une organisation."""
        if user.role_systeme in ['admin_site', 'super_admin']:
            return True
        
        return MembreOrganisation.objects.filter(
            organisation_id=org_id,
            profil__user=user,
            role_organisation='administrateur_page',
            est_actif=True
        ).exists()

    @staticmethod
    @transaction.atomic
    def add_membre(
        acting_user: User,
        org_id: UUID,
        data: Dict,
        request=None
    ) -> MembreOrganisation:
        """
        Ajoute un nouveau membre à une organisation.
        Réservé aux administrateurs de l'organisation.
        """
        organisation = get_object_or_404(Organisation, id=org_id, deleted=False)
        
        if not OrganisationService._is_organisation_admin(acting_user, organisation):
            raise PermissionDeniedAPIException(
                "Vous n'avez pas la permission d'ajouter des membres."
            )
        
        profil_id = data.pop('profil_id')
        profil = get_object_or_404(Profil, id=profil_id)
        
        # Vérifier si le profil est déjà membre actif
        if MembreOrganisation.objects.filter(
            profil=profil,
            organisation=organisation,
            est_actif=True
        ).exists():
            raise BadRequestAPIException(
                "Ce profil est déjà membre actif de l'organisation."
            )
        
        # Désactiver toute ancienne adhésion
        MembreOrganisation.objects.filter(
            profil=profil,
            organisation=organisation
        ).update(est_actif=False)
        
        # Créer la nouvelle adhésion active
        new_membre = MembreOrganisation.objects.create(
            profil=profil,
            organisation=organisation,
            est_actif=True,
            **data
        )
        
        logger.info(
            f"Membre {profil.nom_complet} ajouté à '{organisation.nom_organisation}' "
            f"par {acting_user.email}"
        )
        
        return new_membre

    @staticmethod
    @transaction.atomic
    def update_membre(
        acting_user: User,
        org_id: UUID,
        profil_id: UUID,
        data: Dict,
        request=None
    ) -> MembreOrganisation:
        """
        Met à jour les informations d'un membre.
        Réservé aux administrateurs de l'organisation.
        """
        organisation = get_object_or_404(Organisation, id=org_id, deleted=False)
        
        if not OrganisationService._is_organisation_admin(acting_user, organisation):
            raise PermissionDeniedAPIException(
                "Vous n'avez pas la permission de modifier les membres."
            )
        
        membre = get_object_or_404(
            MembreOrganisation,
            organisation=organisation,
            profil_id=profil_id,
            est_actif=True
        )
        
        for field, value in data.items():
            setattr(membre, field, value)
        
        membre.save()
        
        logger.info(
            f"Membre {membre.profil.nom_complet} de '{organisation.nom_organisation}' "
            f"mis à jour par {acting_user.email}"
        )
        
        return membre

    @staticmethod
    @transaction.atomic
    def remove_membre(
        acting_user: User,
        org_id: UUID,
        profil_id: UUID,
        request=None
    ):
        """
        Retire un membre d'une organisation (désactivation).
        Réservé aux administrateurs de l'organisation.
        """
        organisation = get_object_or_404(Organisation, id=org_id, deleted=False)
        
        if not OrganisationService._is_organisation_admin(acting_user, organisation):
            raise PermissionDeniedAPIException(
                "Vous n'avez pas la permission de retirer des membres."
            )
        
        membre = get_object_or_404(
            MembreOrganisation,
            organisation=organisation,
            profil_id=profil_id,
            est_actif=True
        )
        
        membre.est_actif = False
        membre.save()
        
        logger.info(
            f"Membre {membre.profil.nom_complet} retiré de '{organisation.nom_organisation}' "
            f"par {acting_user.email}"
        )

    @staticmethod
    def get_membres_count(org_id: UUID) -> int:
        """Retourne le nombre de membres actifs d'une organisation."""
        return MembreOrganisation.objects.filter(
            organisation_id=org_id,
            est_actif=True
        ).count()

    @staticmethod
    def get_admins_count(org_id: UUID) -> int:
        """Retourne le nombre d'administrateurs d'une organisation."""
        return MembreOrganisation.objects.filter(
            organisation_id=org_id,
            est_actif=True,
            role_organisation='administrateur_page'
        ).count()

    @staticmethod
    def get_user_organisations(
        user: User,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Organisation], int]:
        """
        Liste les organisations dont l'utilisateur est membre.
        
        Returns:
            Tuple (liste_organisations, total_count)
        """
        queryset = MembreOrganisation.objects.filter(
            profil__user=user,
            est_actif=True
        ).select_related('organisation').order_by('-date_joindre')
        
        total_count = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        
        organisations = [membre.organisation for membre in queryset[start:end]]
        
        return organisations, total_count


# Instance singleton
membre_service = MembreService()