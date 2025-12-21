# organizations/services/abonnement_service.py
import logging
from typing import List, Tuple, Dict
from uuid import UUID
from django.db import transaction
from django.shortcuts import get_object_or_404
from core.models import User, Profil
from organizations.models import Organisation, AbonnementOrganisation
from core.api.exceptions import BadRequestAPIException, NotFoundAPIException

logger = logging.getLogger('app')


class AbonnementService:
    """
    Service contenant la logique métier pour la gestion des abonnements aux organisations.
    """

    @staticmethod
    @transaction.atomic
    def follow_organisation(
        acting_user: User,
        org_id: UUID,
        request=None
    ) -> AbonnementOrganisation:
        """
        Permet à un utilisateur de suivre une organisation.
        """
        organisation = get_object_or_404(
            Organisation,
            id=org_id,
            statut='active',
            deleted=False
        )
        
        subscription, created = AbonnementOrganisation.objects.get_or_create(
            profil=acting_user.profil,
            organisation=organisation
        )
        
        if not created:
            raise BadRequestAPIException("Vous êtes déjà abonné à cette organisation.")
        
        logger.info(
            f"Utilisateur {acting_user.email} suit maintenant "
            f"'{organisation.nom_organisation}'"
        )
        
        return subscription

    @staticmethod
    @transaction.atomic
    def unfollow_organisation(
        acting_user: User,
        org_id: UUID,
        request=None
    ):
        """
        Permet à un utilisateur de ne plus suivre une organisation.
        """
        organisation = get_object_or_404(Organisation, id=org_id, deleted=False)
        
        try:
            subscription = AbonnementOrganisation.objects.get(
                profil=acting_user.profil,
                organisation=organisation
            )
            subscription.delete()
            
            logger.info(
                f"Utilisateur {acting_user.email} ne suit plus "
                f"'{organisation.nom_organisation}'"
            )
        except AbonnementOrganisation.DoesNotExist:
            raise NotFoundAPIException("Vous n'êtes pas abonné à cette organisation.")

    @staticmethod
    def is_following(user: User, org_id: UUID) -> bool:
        """
        Vérifie si un utilisateur suit une organisation.
        """
        return AbonnementOrganisation.objects.filter(
            profil=user.profil,
            organisation_id=org_id
        ).exists()

    @staticmethod
    def list_followers(
        org_id: UUID,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Profil], int]:
        """
        Liste les utilisateurs qui suivent une organisation.
        
        Returns:
            Tuple (liste_profils, total_count)
        """
        organisation = get_object_or_404(
            Organisation,
            id=org_id,
            statut='active',
            deleted=False
        )
        
        queryset = AbonnementOrganisation.objects.filter(
            organisation=organisation
        ).select_related('profil').order_by('-date_abonnement')
        
        total_count = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        
        profils = [sub.profil for sub in queryset[start:end]]
        
        return profils, total_count

    @staticmethod
    def list_following(
        acting_user: User,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Organisation], int]:
        """
        Liste les organisations qu'un utilisateur suit.
        
        Returns:
            Tuple (liste_organisations, total_count)
        """
        queryset = AbonnementOrganisation.objects.filter(
            profil=acting_user.profil
        ).select_related('organisation').order_by('-date_abonnement')
        
        total_count = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        
        organisations = [sub.organisation for sub in queryset[start:end]]
        
        return organisations, total_count

    @staticmethod
    def get_followers_count(org_id: UUID) -> int:
        """Retourne le nombre d'abonnés d'une organisation."""
        return AbonnementOrganisation.objects.filter(
            organisation_id=org_id
        ).count()

    @staticmethod
    def get_following_count(user: User) -> int:
        """Retourne le nombre d'organisations suivies par un utilisateur."""
        return AbonnementOrganisation.objects.filter(
            profil=user.profil
        ).count()


# Instance singleton
abonnement_service = AbonnementService()
