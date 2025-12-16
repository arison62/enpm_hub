# organizations/services/abonnement_service.py
from typing import List
from uuid import UUID
from django.db import transaction
from django.shortcuts import get_object_or_404
from core.models import User, Profil
from organizations.models import Organisation, AbonnementOrganisation
from core.api.exceptions import BadRequestAPIException

class AbonnementService:
    """
    Service containing the business logic for managing organisation subscriptions (follows).
    """

    @staticmethod
    @transaction.atomic
    def follow_organisation(acting_user: User, org_id: UUID) -> AbonnementOrganisation:
        """
        Allows a user to follow an organisation.
        """
        organisation = get_object_or_404(Organisation, id=org_id, statut='active', deleted=False)

        subscription, created = AbonnementOrganisation.objects.get_or_create(
            profil=acting_user.profil,
            organisation=organisation
        )

        if not created:
            raise BadRequestAPIException("Vous êtes déjà abonné à cette organisation.")

        return subscription

    @staticmethod
    @transaction.atomic
    def unfollow_organisation(acting_user: User, org_id: UUID):
        """
        Allows a user to unfollow an organisation.
        """
        organisation = get_object_or_404(Organisation, id=org_id, deleted=False)

        subscription = get_object_or_404(
            AbonnementOrganisation,
            profil=acting_user.profil,
            organisation=organisation
        )

        subscription.delete()

    @staticmethod
    def list_followers(org_id: UUID) -> List[Profil]:
        """
        Lists all users (profiles) following an organisation.
        """
        organisation = get_object_or_404(Organisation, id=org_id, statut='active', deleted=False)
        return [sub.profil for sub in organisation.abonnés.all().select_related('profil')]

    @staticmethod
    def list_following(acting_user: User) -> List[Organisation]:
        """
        Lists all organisations a user is following.
        """
        return [sub.organisation for sub in acting_user.profil.abonnements.all().select_related('organisation')]

# Instantiate the service
abonnement_service = AbonnementService()
