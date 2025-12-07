import logging
from core.models import AuditLog, User
from django.http import HttpRequest
from typing import Optional, Any, Dict

logger = logging.getLogger('app')

class AuditLogService:
    """
    Service dédié à l'enregistrement des actions auditables du système.
    """

    @staticmethod
    def _extract_request_info(request: Optional[HttpRequest]) -> Dict[str, Any]:
        """
        Extrait l'adresse IP et l'User-Agent de l'objet HttpRequest pour l'audit.
        """
        info = {
            'ip_address': '0.0.0.0',
            'user_agent': '',
        }

        if request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')

            info['ip_address'] = ip or '0.0.0.0'
            info['user_agent'] = request.META.get('HTTP_USER_AGENT', '')

        return info

    @staticmethod
    def log_action(
        user: User,
        action: AuditLog.AuditAction,
        entity_type: str,
        entity_id: Optional[Any],
        request: Optional[HttpRequest] = None,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """
        Enregistre une action auditable.

        :param user: L'utilisateur qui a effectué l'action.
        :param action: Le type d'action (ex: AuditLog.AuditAction.CREATE).
        :param entity_type: Le type de l'entité affectée.
        :param entity_id: L'ID de l'entité affectée.
        :param request: L'objet HttpRequest pour les infos d'accès.
        :param old_values: Données originales de l'entité.
        :param new_values: Nouvelles données de l'entité.
        :return: L'objet AuditLog créé.
        """

        request_info = AuditLogService._extract_request_info(request)

        audit_log = AuditLog.objects.create(
            user=user,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=request_info['ip_address'],
            user_agent=request_info['user_agent']
        )

        logger.info(
            f"Audit log created: User {user.id} performed {action} on {entity_type} {entity_id}"
        )
        return audit_log
