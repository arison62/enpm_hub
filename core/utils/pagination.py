# core/utils/pagination.py
from math import ceil
from typing import List, Any, Dict


def build_pagination_response(
    items: List[Any],
    total_count: int,
    page: int,
    page_size: int
) -> Dict:
    """
    Construit une réponse paginée standardisée.
    
    Args:
        items: Liste des éléments de la page actuelle
        total_count: Nombre total d'éléments
        page: Numéro de page actuel
        page_size: Taille de la page
    
    Returns:
        Dictionnaire avec structure {"items": [...], "meta": {...}}
    
    Exemple:
        >>> users, total = user_service.list_users(filters, page, page_size)
        >>> return 200, build_pagination_response(users, total, page, page_size)
    """
    total_pages = ceil(total_count / page_size) if total_count > 0 else 1
    
    return {
        "items": items,
        "meta": {
            "page": page,
            "page_size": page_size,
            "total_items": total_count,
            "total_pages": total_pages
        }
    }


def build_enhanced_pagination_response(
    items: List[Any],
    total_count: int,
    page: int,
    page_size: int
) -> Dict:
    """
    Construit une réponse paginée avec informations de navigation supplémentaires.
    
    Returns:
        Dictionnaire avec has_next, has_previous, next_page, previous_page
    
    Exemple:
        >>> return 200, build_enhanced_pagination_response(items, total, page, page_size)
    """
    total_pages = ceil(total_count / page_size) if total_count > 0 else 1
    has_next = page < total_pages
    has_previous = page > 1
    
    return {
        "items": items,
        "meta": {
            "page": page,
            "page_size": page_size,
            "total_items": total_count,
            "total_pages": total_pages,
            "has_next": has_next,
            "has_previous": has_previous,
            "next_page": page + 1 if has_next else None,
            "previous_page": page - 1 if has_previous else None
        }
    }