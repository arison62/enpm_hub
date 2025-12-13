# organizations/services/membre_service.py
from typing import List, Dict, Optional
from uuid import UUID
from django.db import transaction
from django.shortcuts import get_object_or_404
from core.models import User, Profil
from organizations.models import Organisation, MembreOrganisation
from core.api.exceptions import PermissionDeniedAPIException, NotFoundAPIException, BadRequestAPIException
from organizations.services.organisation_service import OrganisationService

class MembreService:
    """
    Service containing the business logic for managing organisation members.
    """

    @staticmethod
    def list_membres(org_id: UUID) -> List[MembreOrganisation]:
        """
        Lists all active members of an organisation.
        """
        organisation = get_object_or_404(Organisation, id=org_id, deleted=False)
        return MembreOrganisation.objects.filter(organisation=organisation, est_actif=True).select_related('profil')

    @staticmethod
    @transaction.atomic
    def add_membre(acting_user: User, org_id: UUID, data: Dict) -> MembreOrganisation:
        """
        Adds a new member to an organisation.
        Restricted to the organisation's page admins or site admins.
        """
        organisation = get_object_or_404(Organisation, id=org_id, deleted=False)
        if not OrganisationService._is_organisation_admin(acting_user, organisation):
            raise PermissionDeniedAPIException("Vous n'avez pas la permission d'ajouter des membres à cette organisation.")

        profil_id = data.pop('profil_id')
        profil = get_object_or_404(Profil, id=profil_id)

        # Deactivate any existing membership for this profile
        MembreOrganisation.objects.filter(profil=profil, organisation=organisation).update(est_actif=False)

        # Create the new active membership
        new_membre = MembreOrganisation.objects.create(
            profil=profil,
            organisation=organisation,
            est_actif=True,
            **data
        )
        return new_membre

    @staticmethod
    @transaction.atomic
    def update_membre(acting_user: User, org_id: UUID, profil_id: UUID, data: Dict) -> MembreOrganisation:
        """
        Updates a member's details within an organisation.
        Restricted to the organisation's page admins or site admins.
        """
        organisation = get_object_or_404(Organisation, id=org_id, deleted=False)
        if not OrganisationService._is_organisation_admin(acting_user, organisation):
            raise PermissionDeniedAPIException("Vous n'avez pas la permission de modifier les membres de cette organisation.")

        membre = get_object_or_404(MembreOrganisation, organisation=organisation, profil_id=profil_id, est_actif=True)

        for field, value in data.items():
            setattr(membre, field, value)
        membre.save()
        return membre

    @staticmethod
    @transaction.atomic
    def remove_membre(acting_user: User, org_id: UUID, profil_id: UUID):
        """
        Removes a member from an organisation by deactivating their membership.
        Restricted to the organisation's page admins or site admins.
        """
        organisation = get_object_or_404(Organisation, id=org_id, deleted=False)
        if not OrganisationService._is_organisation_admin(acting_user, organisation):
            raise PermissionDeniedAPIException("Vous n'avez pas la permission de retirer des membres de cette organisation.")

        membre = get_object_or_404(MembreOrganisation, organisation=organisation, profil_id=profil_id, est_actif=True)
        membre.est_actif = False
        membre.save()

# Instantiate the service
membre_service = MembreService()
