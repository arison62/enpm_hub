# organizations/services/organisation_service.py
from typing import List, Dict, Optional
from uuid import UUID
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.files.uploadedfile import UploadedFile
from core.models import User
from organizations.models import Organisation, MembreOrganisation
from core.api.exceptions import PermissionDeniedAPIException, NotFoundAPIException, BadRequestAPIException

class OrganisationService:
    """
    Service containing the business logic for managing organisations.
    """

    @staticmethod
    def _is_site_admin(user: User) -> bool:
        """Checks if the user is a site administrator."""
        return user.role_systeme in ['admin_site', 'super_admin']

    @staticmethod
    def _is_organisation_admin(user: User, organisation: Organisation) -> bool:
        """Checks if the user is an administrator for the given organisation."""
        if OrganisationService._is_site_admin(user):
            return True
        return MembreOrganisation.objects.filter(
            organisation=organisation,
            profil__user=user,
            role_organisation='administrateur_page',
            est_actif=True
        ).exists()

    @staticmethod
    @transaction.atomic
    def create_organisation(acting_user: User, data: Dict) -> Organisation:
        """
        Creates a new organisation proposed by a user.
        The organisation is created with a 'pending' status by default.
        """
        # Any authenticated user can create an organisation proposal.
        # The first member (the creator) is automatically added as a page admin.
        new_organisation = Organisation.objects.create(statut='en_attente', **data)

        MembreOrganisation.objects.create(
            profil=acting_user.profil,
            organisation=new_organisation,
            role_organisation='administrateur_page',
            poste="Créateur de la page",
            est_actif=True
        )
        return new_organisation

    @staticmethod
    def list_organisations(filters: Dict) -> List[Organisation]:
        """
        Lists all active organisations with optional filters.
        """
        queryset = Organisation.objects.filter(statut='active', deleted=False)

        # Add filtering logic here based on 'filters' dict
        if 'search' in filters:
            queryset = queryset.filter(nom_organisation__icontains=filters['search'])
        if 'pays' in filters:
            queryset = queryset.filter(pays__iexact=filters['pays'])
        if 'secteur_activite' in filters:
            queryset = queryset.filter(secteur_activite__icontains=filters['secteur_activite'])

        return queryset.order_by('nom_organisation')

    @staticmethod
    def list_pending_organisations(acting_user: User) -> List[Organisation]:
        """
        Lists organisations pending approval. Restricted to site admins.
        """
        if not OrganisationService._is_site_admin(acting_user):
            raise PermissionDeniedAPIException("Vous n'avez pas la permission de voir les organisations en attente.")
        return Organisation.objects.filter(statut='en_attente', deleted=False).order_by('created_at')

    @staticmethod
    def get_organisation_by_id(org_id: UUID) -> Organisation:
        """
        Retrieves a single active organisation by its ID.
        """
        try:
            return Organisation.objects.get(id=org_id, statut='active', deleted=False)
        except Organisation.DoesNotExist:
            raise NotFoundAPIException("Organisation non trouvée ou inactive.")

    @staticmethod
    @transaction.atomic
    def update_organisation(acting_user: User, org_id: UUID, data: Dict) -> Organisation:
        """
        Updates an organisation's details.
        Restricted to the organisation's page admins or site admins.
        """
        organisation = get_object_or_404(Organisation, id=org_id, deleted=False)
        if not OrganisationService._is_organisation_admin(acting_user, organisation):
            raise PermissionDeniedAPIException("Vous n'avez pas la permission de modifier cette organisation.")

        for field, value in data.items():
            setattr(organisation, field, value)
        organisation.save()
        return organisation

    @staticmethod
    @transaction.atomic
    def update_organisation_status(acting_user: User, org_id: UUID, new_status: str) -> Organisation:
        """
        Updates an organisation's status (e.g., approve, deactivate).
        Restricted to site admins.
        """
        if not OrganisationService._is_site_admin(acting_user):
            raise PermissionDeniedAPIException("Seuls les administrateurs du site peuvent changer le statut d'une organisation.")

        valid_statuses = [choice[0] for choice in Organisation.STATUT_CHOICES]
        if new_status not in valid_statuses:
            raise BadRequestAPIException(f"Statut invalide. Les statuts valides sont : {', '.join(valid_statuses)}")

        organisation = get_object_or_404(Organisation, id=org_id, deleted=False)
        organisation.statut = new_status
        organisation.save()
        return organisation

    @staticmethod
    @transaction.atomic
    def update_organisation_logo(acting_user: User, org_id: UUID, logo_file: UploadedFile) -> Organisation:
        """
        Updates the logo for an organisation.
        """
        organisation = get_object_or_404(Organisation, id=org_id, deleted=False)
        if not OrganisationService._is_organisation_admin(acting_user, organisation):
            raise PermissionDeniedAPIException("Vous n'avez pas la permission de modifier cette organisation.")

        # Logic to handle file validation and storage can be added here
        organisation.logo = logo_file
        organisation.save()
        return organisation

    @staticmethod
    @transaction.atomic
    def soft_delete_organisation(acting_user: User, org_id: UUID):
        """
        Soft deletes an organisation. Restricted to site admins.
        """
        if not OrganisationService._is_site_admin(acting_user):
            raise PermissionDeniedAPIException("Seuls les administrateurs du site peuvent supprimer une organisation.")

        organisation = get_object_or_404(Organisation, id=org_id)
        organisation.soft_delete()

# Instantiate the service
organisation_service = OrganisationService()
