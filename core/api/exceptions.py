# core/api/exceptions.py

class BaseAPIException(Exception):
    """Classe de base pour les exceptions de l'API."""
    status_code = 500
    default_detail = "Une erreur interne est survenue."

    def __init__(self, detail=None):
        self.detail = detail or self.default_detail

class NotFoundAPIException(BaseAPIException):
    status_code = 404
    default_detail = "La ressource demandée n'a pas été trouvée."

class PermissionDeniedAPIException(BaseAPIException):
    status_code = 403
    default_detail = "Vous n'avez pas la permission d'effectuer cette action."

class BadRequestAPIException(BaseAPIException):
    status_code = 400
    default_detail = "La requête est invalide."
