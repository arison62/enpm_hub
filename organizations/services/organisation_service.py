# organizations/services/organisation_service.py
import os
from typing import List, Dict, Optional
from uuid import UUID
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.files.uploadedfile import UploadedFile
from django.core.files.storage import default_storage
from PIL import Image
from io import BytesIO
from core.models import User
from organizations.models import Organisation, MembreOrganisation
from core.api.exceptions import PermissionDeniedAPIException, NotFoundAPIException, BadRequestAPIException

class OrganisationService:
    """
    Service containing the business logic for managing organisations.
    """
    ALLOWED_LOGO_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']
    MAX_LOGO_SIZE = 2 * 1024 * 1024  # 2MB
    LOGO_MAX_DIMENSIONS = (400, 400)

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
    def _validate_logo(logo_file: UploadedFile):
        if not logo_file:
            raise ValueError("Aucun fichier n'a été fourni.")
        file_ext = os.path.splitext(logo_file.name)[1].lower()
        if file_ext not in OrganisationService.ALLOWED_LOGO_EXTENSIONS:
            raise ValueError(f"Format de fichier non autorisé. Acceptés : {', '.join(OrganisationService.ALLOWED_LOGO_EXTENSIONS)}")
        if logo_file.size > OrganisationService.MAX_LOGO_SIZE:
            raise ValueError(f"La taille du fichier dépasse {OrganisationService.MAX_LOGO_SIZE / (1024*1024)} MB.")
        try:
            Image.open(logo_file).verify()
        except Exception:
            raise ValueError("Le fichier n'est pas une image valide.")

    @staticmethod
    def _optimize_logo(logo_file: UploadedFile) -> BytesIO:
        image = Image.open(logo_file)
        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')
        image.thumbnail(OrganisationService.LOGO_MAX_DIMENSIONS, Image.Resampling.LANCZOS)
        output = BytesIO()
        image.save(output, format='JPEG', quality=85)
        output.seek(0)
        return output

    @staticmethod
    @transaction.atomic
    def update_organisation_logo(acting_user: User, org_id: UUID, logo_file: UploadedFile) -> Organisation:
        """
        Updates the logo for an organisation.
        """
        organisation = get_object_or_404(Organisation, id=org_id, deleted=False)
        if not OrganisationService._is_organisation_admin(acting_user, organisation):
            raise PermissionDeniedAPIException("Vous n'avez pas la permission de modifier le logo de cette organisation.")

        OrganisationService._validate_logo(logo_file)

        # Delete the old logo if it exists
        if organisation.logo and organisation.logo.path and os.path.exists(organisation.logo.path):
            os.remove(organisation.logo.path)

        optimized_logo = OrganisationService._optimize_logo(logo_file)
        file_name = f"logo_{organisation.id}.jpg"
        saved_path = default_storage.save(os.path.join('logos_organisations', file_name), optimized_logo)

        organisation.logo = saved_path
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
