# organizations/services/organisation_service.py
import os
import logging
from typing import List, Dict, Optional, Tuple
from uuid import UUID
from django.db import transaction
from django.db.models import Q, Count, Prefetch, Value, OuterRef, Exists, BooleanField
from django.shortcuts import get_object_or_404
from django.core.files.uploadedfile import UploadedFile
from django.core.files.storage import default_storage
from django.utils.text import slugify
from PIL import Image
from io import BytesIO
from nanoid import generate

from core.models import User
from organizations.models import Organisation, MembreOrganisation, AbonnementOrganisation
from core.api.exceptions import (
    PermissionDeniedAPIException, 
    NotFoundAPIException, 
    BadRequestAPIException
)
from users.services.user_service import user_service

logger = logging.getLogger('app')


class OrganisationService:
    """Service contenant la logique métier pour la gestion des organisations."""
    
    ALLOWED_LOGO_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']
    MAX_LOGO_SIZE = 2 * 1024 * 1024  # 2MB
    LOGO_MAX_DIMENSIONS = (400, 400)

    # ==========================================
    # PERMISSIONS
    # ==========================================
    
    @staticmethod
    def _is_site_admin(user: User) -> bool:
        """Vérifie si l'utilisateur est administrateur du site."""
        return user.role_systeme in ['admin_site', 'super_admin']

    @staticmethod
    def _is_organisation_admin(user: User, organisation: Organisation) -> bool:
        """Vérifie si l'utilisateur est administrateur de l'organisation."""
        if OrganisationService._is_site_admin(user):
            return True
        return MembreOrganisation.objects.filter(
            organisation=organisation,
            profil__user=user,
            role_organisation='administrateur_page',
            est_actif=True
        ).exists()

    # ==========================================
    # UTILITAIRES
    # ==========================================
    
    @staticmethod
    def generate_unique_slug(base_name: str) -> str:
        """
        Génère un slug unique format : nom-organisation-nanoId
        Exemple : ensp-maroua-x7r2p9
        """
        return slugify(f"{base_name}-{generate(size=6)}")

    # ==========================================
    # CRUD ORGANISATIONS
    # ==========================================
    
    @staticmethod
    @transaction.atomic
    def create_organisation(acting_user: User, data: Dict, request=None) -> Organisation:
        """
        Crée une nouvelle organisation.
        - Si créée par un admin site : statut 'active', admin non ajouté comme membre
        - Sinon : statut 'en_attente', créateur ajouté comme admin page
        """
        initial_status = 'active' if OrganisationService._is_site_admin(acting_user) else 'en_attente'
        
        # Génération du slug unique
        success = False
        for attempt in range(3):
            try:
                slug = OrganisationService.generate_unique_slug(data.get('nom_organisation')) # type: ignore
                new_organisation = Organisation.objects.create(
                    statut=initial_status,
                    slug=slug,
                    **data
                )
                success = True
                break
            except Exception:
                continue
        
        if not success:
            raise BadRequestAPIException("Impossible de générer un identifiant unique après plusieurs tentatives.")
        
        # Ajouter le créateur comme admin page si ce n'est pas un admin site
        if not OrganisationService._is_site_admin(acting_user):
            MembreOrganisation.objects.create(
                profil=acting_user.profil, # type: ignore
                organisation=new_organisation,
                role_organisation='administrateur_page',
                est_actif=True
            )
        
        logger.info(
            f"Organisation '{new_organisation.nom_organisation}' (ID: {new_organisation.id}) "
            f"créée par {acting_user.email} avec statut '{initial_status}'"
        )
        
        return new_organisation

    @staticmethod
    @transaction.atomic
    def create_organisation_with_members(acting_user: User, data: Dict, request=None) -> Organisation:
        members = data.pop('membres', None)
        new_organisation = OrganisationService.create_organisation(acting_user, data, request)
        if members:
            for member_data in members:
                role_organisation = member_data.pop("role_organisation", "employe")
                user = user_service.create_user(acting_user, member_data, request)
                MembreOrganisation.objects.create(
                    profil=user.profil, # type: ignore
                    organisation=new_organisation,
                    role_organisation = role_organisation,
                    est_actif=True
                )
        return new_organisation
    
    
    @staticmethod
    def list_organisations(
        acting_user: User,
        filters: Optional[Dict] = None,
        page: int = 1,
        page_size: int = 20,
        include_stats: bool = False
    ) -> Tuple[List[Organisation], int]:
        """
        Liste les organisations actives avec filtres et pagination.
        
        Args:
            acting_user: Utilisateur connecté (pour vérifier s'il suit les organisations)
            filters: Dictionnaire de filtres (search, pays, secteur_activite, type_organisation, ville)
            page: Numéro de page
            page_size: Nombre d'éléments par page
            include_stats: Si True, inclut le nombre de membres et d'abonnés
            
        Returns:
            Tuple (liste_organisations, total_count)
        """
        queryset = Organisation.objects.filter(statut='active', deleted=False)
        
        # Annotation pour est_suivi (si l'utilisateur connecté suit l'organisation)
        if acting_user and acting_user.is_authenticated:
            # Vérifier si l'utilisateur a un profil
            try:
                profil = acting_user.profil
                queryset = queryset.annotate(
                    est_suivi=Exists(
                        AbonnementOrganisation.objects.filter(
                            organisation=OuterRef('pk'),
                            profil=profil
                        )
                    )
                )
            except AttributeError:
                # L'utilisateur n'a pas de profil
                queryset = queryset.annotate(
                    est_suivi=Value(False, output_field=BooleanField())
                )
        else:
            # Utilisateur non authentifié
            queryset = queryset.annotate(
                est_suivi=Value(False, output_field=BooleanField())
            )
        
        # Annotations pour les statistiques
        if include_stats:
            queryset = queryset.annotate(
                nombre_membres=Count('membres', filter=Q(membres__est_actif=True)),
                nombre_abonnes=Count('abonnes'),
            )
            queryset = queryset.order_by('-nombre_abonnes', '-nombre_membres')
        # Application des filtres
        if filters:
            if search := filters.get('search'):
                queryset = queryset.filter(
                    Q(nom_organisation__icontains=search) |
                    Q(description__icontains=search) |
                    Q(secteur_activite__nom__icontains=search) |
                    Q(ville__icontains=search)
                )
            
            if pays := filters.get('pays'):
                queryset = queryset.filter(pays__iexact=pays)
            
            if secteur := filters.get('secteur_activite'):
                queryset = queryset.filter(secteur_activite__id=secteur)
            
            if type_org := filters.get('type_organisation'):
                queryset = queryset.filter(type_organisation=type_org)
            
            if ville := filters.get('ville'):
                queryset = queryset.filter(ville__icontains=ville)
        
        # Sélection des relations pour optimiser les requêtes
        queryset = queryset.select_related('secteur_activite')
        
        total_count = queryset.count()
        
        # Pagination
        start = (page - 1) * page_size
        end = start + page_size
        organisations = list(queryset.order_by('nom_organisation')[start:end])
        
        return organisations, total_count

    @staticmethod
    def list_pending_organisations(
        acting_user: User,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Organisation], int]:
        """
        Liste les organisations en attente d'approbation.
        Réservé aux administrateurs du site.
        """
        if not OrganisationService._is_site_admin(acting_user):
            raise PermissionDeniedAPIException(
                "Vous n'avez pas la permission de voir les organisations en attente."
            )
        
        queryset = Organisation.objects.filter(
            statut='en_attente',
            deleted=False
        ).order_by('created_at')
        
        total_count = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        
        organisations = list(queryset[start:end])
        
        return organisations, total_count

    @staticmethod
    def get_organisation_by_id(
        org_id: UUID,
        include_relations: bool = True
    ) -> Optional[Organisation]:
        """
        Récupère une organisation par son ID.
        
        Args:
            org_id: UUID de l'organisation
            include_relations: Si True, inclut membres et abonnés
        
        Returns:
            Organisation ou None
        """
        try:
            queryset = Organisation.objects
            
            if include_relations:
                queryset = queryset.select_related(
                    'secteur_activite',
                    'secteur_activite__categorie_parent',
                    ).prefetch_related(
                    Prefetch(
                        'membres',
                        queryset=MembreOrganisation.objects.filter(est_actif=True)
                    ),
                    'abonnes'
                ).annotate(
                    membres_count=Count('membres', filter=Q(membres__est_actif=True)),
                    abonnes_count=Count('abonnes')
                )
            
            return queryset.get(id=org_id, statut='active', deleted=False)
        except Organisation.DoesNotExist:
            logger.warning(f"Organisation non trouvée avec l'ID: {org_id}")
            return None

    @staticmethod
    def get_organisation_by_slug(slug: str) -> Optional[Organisation]:
        """
        Récupère une organisation par son slug.
        
        Args:
            slug: Slug de l'organisation (ex: ensp-maroua-x7r2p9)
        
        Returns:
            Organisation ou None
        """
        try:
            return Organisation.objects.select_related(
                'secteur_activite',
                'secteur_activite__categorie_parent',
                ).prefetch_related(
                Prefetch(
                    'membres',
                    queryset=MembreOrganisation.objects.filter(est_actif=True)
                ),
                'abonnes'
            ).annotate(
                membres_count=Count('membres', filter=Q(membres__est_actif=True)),
                abonnes_count=Count('abonnes')
            ).get(slug=slug, statut='active', deleted=False)
        except Organisation.DoesNotExist:
            logger.warning(f"Organisation non trouvée avec le slug: {slug}")
            return None

    @staticmethod
    @transaction.atomic
    def update_organisation(
        acting_user: User,
        org_id: UUID,
        data: Dict,
        request=None
    ) -> Organisation:
        """
        Met à jour les détails d'une organisation.
        Réservé aux administrateurs de l'organisation.
        """
        organisation = get_object_or_404(Organisation, id=org_id, deleted=False)
        
        if not OrganisationService._is_organisation_admin(acting_user, organisation):
            raise PermissionDeniedAPIException(
                "Vous n'avez pas la permission de modifier cette organisation."
            )
        
        # Gestion spécifique du slug
        if 'slug' in data:
            new_slug = slugify(data['slug'])
            if Organisation.objects.filter(slug=new_slug).exclude(id=org_id).exists():
                raise BadRequestAPIException(f"Le slug '{new_slug}' est déjà utilisé.")
            data['slug'] = new_slug
        
        for field, value in data.items():
            setattr(organisation, field, value)
        
        organisation.save()
        
        logger.info(
            f"Organisation '{organisation.nom_organisation}' (ID: {org_id}) "
            f"mise à jour par {acting_user.email}"
        )
        
        return organisation

    @staticmethod
    @transaction.atomic
    def update_organisation_status(
        acting_user: User,
        org_id: UUID,
        new_status: str,
        request=None
    ) -> Organisation:
        """
        Met à jour le statut d'une organisation.
        Réservé aux administrateurs du site.
        """
        if not OrganisationService._is_site_admin(acting_user):
            raise PermissionDeniedAPIException(
                "Seuls les administrateurs du site peuvent changer le statut."
            )
        
        valid_statuses = [choice[0] for choice in Organisation.STATUT_CHOICES]
        if new_status not in valid_statuses:
            raise BadRequestAPIException(
                f"Statut invalide. Valides : {', '.join(valid_statuses)}"
            )
        
        organisation = get_object_or_404(Organisation, id=org_id, deleted=False)
        old_status = organisation.statut
        organisation.statut = new_status
        organisation.save()
        
        logger.info(
            f"Statut de '{organisation.nom_organisation}' changé de '{old_status}' "
            f"à '{new_status}' par {acting_user.email}"
        )
        
        return organisation

    @staticmethod
    @transaction.atomic
    def soft_delete_organisation(
        acting_user: User,
        org_id: UUID,
        request=None
    ):
        """
        Suppression logique d'une organisation.
        Réservé aux administrateurs du site.
        """
        if not OrganisationService._is_site_admin(acting_user):
            raise PermissionDeniedAPIException(
                "Seuls les administrateurs du site peuvent supprimer une organisation."
            )
        
        organisation = get_object_or_404(Organisation, id=org_id)
        organisation.soft_delete()
        
        logger.info(
            f"Organisation '{organisation.nom_organisation}' (ID: {org_id}) "
            f"supprimée par {acting_user.email}"
        )

    @staticmethod
    @transaction.atomic
    def restore_organisation(
        acting_user: User,
        org_id: UUID,
        request=None
    ) -> Organisation:
        """
        Restaure une organisation supprimée.
        Réservé aux administrateurs du site.
        """
        if not OrganisationService._is_site_admin(acting_user):
            raise PermissionDeniedAPIException(
                "Seuls les administrateurs du site peuvent restaurer une organisation."
            )
        
        try:
            organisation = Organisation.all_objects.get(id=org_id, deleted=True)
        except Organisation.DoesNotExist:
            raise NotFoundAPIException("Organisation supprimée introuvable.")
        
        organisation.restore()
        
        logger.info(
            f"Organisation '{organisation.nom_organisation}' (ID: {org_id}) "
            f"restaurée par {acting_user.email}"
        )
        
        return organisation

    # ==========================================
    # GESTION DU LOGO
    # ==========================================
    
    @staticmethod
    def _validate_logo(logo_file: UploadedFile):
        """Valide le fichier logo uploadé."""
        if not logo_file:
            raise ValueError("Aucun fichier n'a été fourni.")
        
        file_ext = os.path.splitext(logo_file.name)[1].lower()
        if file_ext not in OrganisationService.ALLOWED_LOGO_EXTENSIONS:
            raise ValueError(
                f"Format non autorisé. Acceptés : {', '.join(OrganisationService.ALLOWED_LOGO_EXTENSIONS)}"
            )
        
        if logo_file.size > OrganisationService.MAX_LOGO_SIZE:
            raise ValueError(
                f"Taille max dépassée : {OrganisationService.MAX_LOGO_SIZE / (1024*1024)} MB."
            )
        
        try:
            Image.open(logo_file).verify()
        except Exception:
            raise ValueError("Le fichier n'est pas une image valide.")

    @staticmethod
    def _optimize_logo(logo_file: UploadedFile) -> BytesIO:
        """Optimise le logo (conversion WebP, redimensionnement)."""
        image = Image.open(logo_file)
        if image.mode in ('RGBA', 'LA'):
            image = image.convert('RGB')
        image.thumbnail(OrganisationService.LOGO_MAX_DIMENSIONS, Image.Resampling.LANCZOS)
        output = BytesIO()
        image.save(output, format='WebP', quality=80)
        output.seek(0)
        return output

    @staticmethod
    @transaction.atomic
    def update_organisation_logo(
        acting_user: User,
        org_id: UUID,
        logo_file: UploadedFile,
        request=None
    ) -> Organisation:
        """
        Met à jour le logo d'une organisation.
        Réservé aux administrateurs de l'organisation.
        """
        organisation = get_object_or_404(Organisation, id=org_id, deleted=False)
        
        if not OrganisationService._is_organisation_admin(acting_user, organisation):
            raise PermissionDeniedAPIException(
                "Vous n'avez pas la permission de modifier le logo."
            )
        
        OrganisationService._validate_logo(logo_file)
        
        # Suppression de l'ancien logo
        if organisation.logo and organisation.logo.path and os.path.exists(organisation.logo.path):
            os.remove(organisation.logo.path)
        
        optimized_logo = OrganisationService._optimize_logo(logo_file)
        file_name = f"logo_{organisation.id}.webp"
        saved_path = default_storage.save(
            os.path.join('logos_organisations', file_name),
            optimized_logo
        )
        
        organisation.logo = saved_path # type: ignore
        organisation.save()
        
        logger.info(
            f"Logo de '{organisation.nom_organisation}' mis à jour par {acting_user.email}"
        )
        
        return organisation

    @staticmethod
    @transaction.atomic
    def delete_organisation_logo(
        acting_user: User,
        org_id: UUID,
        request=None
    ) -> Organisation:
        """
        Supprime le logo d'une organisation.
        Réservé aux administrateurs de l'organisation.
        """
        organisation = get_object_or_404(Organisation, id=org_id, deleted=False)
        
        if not OrganisationService._is_organisation_admin(acting_user, organisation):
            raise PermissionDeniedAPIException(
                "Vous n'avez pas la permission de supprimer le logo."
            )
        
        if organisation.logo and organisation.logo.path and os.path.exists(organisation.logo.path):
            os.remove(organisation.logo.path)
        
        organisation.logo = None # type: ignore
        organisation.save()
        
        logger.info(
            f"Logo de '{organisation.nom_organisation}' supprimé par {acting_user.email}"
        )
        
        return organisation

    # ==========================================
    # STATISTIQUES
    # ==========================================
    
    @staticmethod
    def get_organisation_statistics() -> Dict:
        """
        Retourne les statistiques globales des organisations.
        Réservé aux administrateurs du site.
        """
        total_orgs = Organisation.objects.count()
        active_orgs = Organisation.objects.filter(statut='active').count()
        pending_orgs = Organisation.objects.filter(statut='en_attente').count()
        inactive_orgs = Organisation.objects.filter(statut='inactive').count()
        deleted_orgs = Organisation.all_objects.filter(deleted=True).count()
        
        stats_by_type = {}
        for type_org, _ in Organisation.TYPE_ORGANISATION_CHOICES:
            stats_by_type[type_org] = Organisation.objects.filter(
                type_organisation=type_org,
                statut='active'
            ).count()
        
        # Top 10 organisations par nombre de membres
        top_orgs = Organisation.objects.filter(
            statut='active',
            deleted=False
        ).annotate(
            membres_count=Count('membres', filter=Q(membres__est_actif=True))
        ).order_by('-membres_count')[:10]
        
        top_orgs_data = [
            {
                'id': str(org.id),
                'nom': org.nom_organisation,
                'membres_count': org.membres_count
            }
            for org in top_orgs
        ]
        
        return {
            'total_organisations': total_orgs,
            'active_organisations': active_orgs,
            'pending_organisations': pending_orgs,
            'inactive_organisations': inactive_orgs,
            'deleted_organisations': deleted_orgs,
            'by_type': stats_by_type,
            'top_organisations': top_orgs_data
        }

    @staticmethod
    def get_organisation_stats(org_id: UUID) -> Dict:
        """
        Retourne les statistiques d'une organisation spécifique.
        """
        organisation = get_object_or_404(
            Organisation,
            id=org_id,
            statut='active',
            deleted=False
        )
        
        membres_count = MembreOrganisation.objects.filter(
            organisation=organisation,
            est_actif=True
        ).count()
        
        admins_count = MembreOrganisation.objects.filter(
            organisation=organisation,
            est_actif=True,
            role_organisation='administrateur_page'
        ).count()
        
        followers_count = AbonnementOrganisation.objects.filter(
            organisation=organisation
        ).count()
        
        return {
            'membres_count': membres_count,
            'admins_count': admins_count,
            'followers_count': followers_count
        }


# Instance singleton
organisation_service = OrganisationService()