from abc import ABC, abstractmethod
from core.services.email_service import EmailTemplates
import logging

logger = logging.getLogger("app")

class BaseNotificationSender(ABC):
    """
    Classe abstraite pour l'envoi de notifications.
    """

    @abstractmethod
    def send_otp(self, recipient: str, otp: str) -> None:
        """
        Envoie un OTP (One-Time Password) au destinataire spécifié.

        :param recipient: Le destinataire de l'OTP (ex: adresse e-mail ou numéro de téléphone).
        :param otp: Le code OTP à envoyer.
        """
        pass
    

class EmailNotificationSender(BaseNotificationSender):
    """
    Implémentation concrète de l'envoi de notifications par e-mail.
    """

    def send_otp(self, recipient: str, otp: str) -> None:
        """
        Envoie un OTP par e-mail.

        :param recipient: L'adresse e-mail du destinataire.
        :param otp: Le code OTP à envoyer.
        """
        EmailTemplates.send_password_reset_email(
            user_email=recipient,
            user_name= recipient,
            otp_code=otp
        )
        logger.info(f"Envoi de l'OTP à l'adresse e-mail {recipient}")

class SMSNotificationSender(BaseNotificationSender):
    """
    Implémentation concrète de l'envoi de notifications par SMS.
    """

    def send_otp(self, recipient: str, otp: str) -> None:
        """
        Envoie un OTP par SMS.

        :param recipient: Le numéro de téléphone du destinataire.
        :param otp: Le code OTP à envoyer.
        """
        # Logique d'envoi de SMS (à implémenter)
        logger.info(f"Envoi de l'OTP {otp} au numéro de téléphone {recipient}")
        # Ici, vous pouvez intégrer avec un service d'envoi de SMS réel
        pass

class NotificationFactory:
    """
    Factory pour créer des instances de senders de notifications.
    """

    @staticmethod
    def get_sender(method: str) -> BaseNotificationSender:
        """
        Retourne une instance de sender de notification en fonction de la méthode spécifiée.

        :param method: La méthode d'envoi ('email' ou 'sms').
        :return: Une instance de BaseNotificationSender.
        :raises ValueError: Si la méthode n'est pas supportée.
        """
        if method == 'email':
            return EmailNotificationSender()
        elif method == 'sms':
            return SMSNotificationSender()
        else:
            raise ValueError(f"Méthode d'envoi non supportée: {method}")