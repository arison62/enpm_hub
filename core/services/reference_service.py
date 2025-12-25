"""
core/services/references_service.py
Service pour gérer les données de référence
"""

import logging
from typing import List, Optional
from uuid import UUID
from django.core.cache import cache
from core.models import (
    AnneePromotion, Domaine, Filiere, SecteurActivite,
    Poste, Devise, TitreHonorifique, ReseauSocial
)

logger = logging.getLogger(__name__)


class ReferenceService:
    """Service centralisé pour gérer les données de référence"""
    
    # Durées de cache (en secondes)
    CACHE_TIMEOUT = 60 * 60 * 24  # 24 heures
    
    # =========================================
    # Pays
    # =========================================
    @staticmethod
    def get_all_pays():
        """Récupère tous les pays"""
        from django_countries import countries
        
        cached_data = cache.get("countries")
        if cached_data:
            return cached_data
        list_countries = [{"code": code, "name": name} for code, name in countries]
        cache.set("countries", list_countries, ReferenceService.CACHE_TIMEOUT)
        return list_countries
    
    # ==========================================
    # ANNÉES DE PROMOTION
    # ==========================================
    
    @staticmethod
    def get_all_annees_promotion(actives_only: bool = True) -> List[AnneePromotion]:
        """Récupère toutes les années de promotion"""
        cache_key = f"annees_promotion_{'actives' if actives_only else 'all'}"
        
        # Essayer de récupérer depuis le cache
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        # Récupérer depuis la DB
        queryset = AnneePromotion.objects.all()
        if actives_only:
            queryset = queryset.filter(est_active=True)
        
        result = list(queryset.order_by('-annee'))
        
        # Mettre en cache
        cache.set(cache_key, result, ReferenceService.CACHE_TIMEOUT)
        
        return result
    
    @staticmethod
    def get_annee_by_id(annee_id: UUID) -> Optional[AnneePromotion]:
        """Récupère une année spécifique"""
        try:
            return AnneePromotion.objects.get(id=annee_id)
        except AnneePromotion.DoesNotExist:
            logger.warning(f"Année promotion non trouvée: {annee_id}")
            return None
    
    # ==========================================
    # DOMAINES
    # ==========================================
    
    @staticmethod
    def get_all_domaines(actifs_only: bool = True) -> List[Domaine]:
        """Récupère tous les domaines"""
        cache_key = f"domaines_{'actifs' if actifs_only else 'all'}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        queryset = Domaine.objects.all()
        if actifs_only:
            queryset = queryset.filter(est_actif=True)
        
        result = list(queryset.order_by('ordre_affichage', 'nom'))
        cache.set(cache_key, result, ReferenceService.CACHE_TIMEOUT)
        
        return result
    
    @staticmethod
    def get_domaine_by_id(domaine_id: UUID, include_filieres: bool = False) -> Optional[Domaine]:
        """Récupère un domaine spécifique"""
        try:
            queryset = Domaine.objects
            if include_filieres:
                queryset = queryset.prefetch_related('filieres')
            return queryset.get(id=domaine_id)
        except Domaine.DoesNotExist:
            logger.warning(f"Domaine non trouvé: {domaine_id}")
            return None
    
    # ==========================================
    # FILIÈRES
    # ==========================================
    
    @staticmethod
    def get_filieres_by_domaine(domaine_id: UUID, actives_only: bool = True) -> List[Filiere]:
        """Récupère les filières d'un domaine"""
        cache_key = f"filieres_domaine_{domaine_id}_{'actives' if actives_only else 'all'}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        queryset = Filiere.objects.filter(domaine_id=domaine_id).select_related('domaine')
        if actives_only:
            queryset = queryset.filter(est_actif=True)
        
        result = list(queryset.order_by('ordre_affichage', 'nom'))
        cache.set(cache_key, result, ReferenceService.CACHE_TIMEOUT)
        
        return result
    
    @staticmethod
    def get_all_filieres(actives_only: bool = True) -> List[Filiere]:
        """Récupère toutes les filières"""
        cache_key = f"filieres_{'actives' if actives_only else 'all'}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        queryset = Filiere.objects.select_related('domaine')
        if actives_only:
            queryset = queryset.filter(est_actif=True)
        
        result = list(queryset.order_by('domaine__ordre_affichage', 'ordre_affichage'))
        cache.set(cache_key, result, ReferenceService.CACHE_TIMEOUT)
        
        return result
    
    # ==========================================
    # SECTEURS D'ACTIVITÉ
    # ==========================================
    
    @staticmethod
    def get_all_secteurs(actifs_only: bool = True, parents_only: bool = False) -> List[SecteurActivite]:
        """Récupère tous les secteurs d'activité"""
        cache_key = f"secteurs_{'actifs' if actifs_only else 'all'}_{'parents' if parents_only else 'all'}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        queryset = SecteurActivite.objects.select_related('categorie_parent')
        if actifs_only:
            queryset = queryset.filter(est_actif=True)
        if parents_only:
            queryset = queryset.filter(categorie_parent__isnull=True)
        
        result = list(queryset.order_by('ordre_affichage', 'nom'))
        cache.set(cache_key, result, ReferenceService.CACHE_TIMEOUT)
        
        return result
    
    @staticmethod
    def get_secteur_by_id(secteur_id: UUID, include_children: bool = False) -> Optional[SecteurActivite]:
        """Récupère un secteur spécifique"""
        try:
            queryset = SecteurActivite.objects
            if include_children:
                queryset = queryset.prefetch_related('sous_secteurs')
            return queryset.get(id=secteur_id)
        except SecteurActivite.DoesNotExist:
            logger.warning(f"Secteur non trouvé: {secteur_id}")
            return None
    
    # ==========================================
    # POSTES
    # ==========================================
    
    @staticmethod
    def get_all_postes(actifs_only: bool = True) -> List[Poste]:
        """Récupère tous les postes"""
        cache_key = f"postes_{'actifs' if actifs_only else 'all'}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        queryset = Poste.objects.select_related('secteur')
        if actifs_only:
            queryset = queryset.filter(est_actif=True)
        
        result = list(queryset.order_by('categorie', 'ordre_affichage', 'titre'))
        cache.set(cache_key, result, ReferenceService.CACHE_TIMEOUT)
        
        return result
    
    @staticmethod
    def get_postes_by_categorie(categorie: str, actifs_only: bool = True) -> List[Poste]:
        """Récupère les postes par catégorie"""
        queryset = Poste.objects.filter(categorie=categorie)
        if actifs_only:
            queryset = queryset.filter(est_actif=True)
        return list(queryset.order_by('ordre_affichage', 'titre'))
    
    # ==========================================
    # DEVISES
    # ==========================================
    
    @staticmethod
    def get_all_devises(actives_only: bool = True) -> List[Devise]:
        """Récupère toutes les devises"""
        cache_key = f"devises_{'actives' if actives_only else 'all'}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        queryset = Devise.objects.all()
        if actives_only:
            queryset = queryset.filter(est_active=True)
        
        result = list(queryset.order_by('ordre_affichage', 'code'))
        cache.set(cache_key, result, ReferenceService.CACHE_TIMEOUT)
        
        return result
    
    @staticmethod
    def get_devise_by_code(code: str) -> Optional[Devise]:
        """Récupère une devise par son code"""
        try:
            return Devise.objects.get(code=code)
        except Devise.DoesNotExist:
            logger.warning(f"Devise non trouvée: {code}")
            return None
    
    # ==========================================
    # TITRES HONORIFIQUES
    # ==========================================
    
    @staticmethod
    def get_all_titres(actifs_only: bool = True) -> List[TitreHonorifique]:
        """Récupère tous les titres honorifiques"""
        cache_key = f"titres_{'actifs' if actifs_only else 'all'}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        queryset = TitreHonorifique.objects.all()
        if actifs_only:
            queryset = queryset.filter(est_actif=True)
        
        result = list(queryset.order_by('ordre_affichage', 'titre'))
        cache.set(cache_key, result, ReferenceService.CACHE_TIMEOUT)
        
        return result
    
    @staticmethod
    def get_titres_by_type(type_titre: str, actifs_only: bool = True) -> List[TitreHonorifique]:
        """Récupère les titres par type"""
        queryset = TitreHonorifique.objects.filter(type_titre=type_titre)
        if actifs_only:
            queryset = queryset.filter(est_actif=True)
        return list(queryset.order_by('ordre_affichage', 'titre'))
    
    # ==========================================
    # RÉSEAUX SOCIAUX
    # ==========================================
    
    @staticmethod
    def get_all_reseaux(actifs_only: bool = True) -> List[ReseauSocial]:
        """Récupère tous les réseaux sociaux"""
        cache_key = f"reseaux_{'actifs' if actifs_only else 'all'}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        queryset = ReseauSocial.objects.all()
        if actifs_only:
            queryset = queryset.filter(est_actif=True)
        
        result = list(queryset.order_by('ordre_affichage', 'nom'))
        cache.set(cache_key, result, ReferenceService.CACHE_TIMEOUT)
        
        return result
    
    @staticmethod
    def get_reseaux_by_type(type_reseau: str, actifs_only: bool = True) -> List[ReseauSocial]:
        """Récupère les réseaux par type"""
        queryset = ReseauSocial.objects.filter(type_reseau=type_reseau)
        if actifs_only:
            queryset = queryset.filter(est_actif=True)
        return list(queryset.order_by('ordre_affichage', 'nom'))
    
    # ==========================================
    # INVALIDATION DU CACHE
    # ==========================================
    
    @staticmethod
    def clear_all_caches():
        """Invalide tous les caches de référence"""
        cache_keys = [
            'annees_promotion_actives', 'annees_promotion_all',
            'domaines_actifs', 'domaines_all',
            'filieres_actives', 'filieres_all',
            'secteurs_actifs_all', 'secteurs_all_all', 'secteurs_actifs_parents',
            'postes_actifs', 'postes_all',
            'devises_actives', 'devises_all',
            'titres_actifs', 'titres_all',
            'reseaux_actifs', 'reseaux_all',
            
        ]
        
        for key in cache_keys:
            cache.delete(key)
        
        logger.info("Tous les caches de référence ont été invalidés")


# Instance globale du service
reference_service = ReferenceService()