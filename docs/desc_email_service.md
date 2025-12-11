# 📧 Service d'Email - ENSPM Hub

## 🎯 Vue d'ensemble

Le service d'email est une composante essentielle de l'application ENSPM Hub. Il gère l'envoi d'emails transactionnels et de notifications aux utilisateurs de manière **asynchrone** pour garantir une expérience utilisateur fluide.

### Caractéristiques principales
- ✅ **Envoi asynchrone** : Les emails sont traités en arrière-plan sans bloquer l'application
- ✅ **Templates HTML professionnels** : Design cohérent avec l'identité visuelle de la plateforme
- ✅ **Retry automatique** : 3 tentatives en cas d'échec avec délai de 60 secondes
- ✅ **Logging complet** : Traçabilité de tous les envois d'emails

---

## 🏗️ Architecture technique

```
┌─────────────────┐
│  Requête API    │  Exemple: Création d'un utilisateur
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  user_service   │  Déclenche l'envoi d'email
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ EmailService    │  Met la tâche en file d'attente
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Huey Queue     │  File d'attente (SQLite/Redis)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Huey Workers   │  Traite les emails en arrière-plan
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Serveur SMTP   │  Gmail/MailDev/SendGrid
└─────────────────┘
```

---

## 🛠️ Choix technologiques

### Pourquoi Huey ?

| Critère                    | Huey ✅                          | Celery ❌                         |
| -------------------------- | ------------------------------- | -------------------------------- |
| **Compatibilité Windows**  | Natif                           | Problématique                    |
| **Complexité**             | Simple (1 fichier config)       | Complexe (broker + backend)      |
| **Broker requis**          | SQLite suffit                   | Redis/RabbitMQ obligatoire       |
| **Courbe d'apprentissage** | Faible                          | Élevée                           |
| **Performance**            | Suffisante (< 1000 emails/jour) | Excellente (> 10000 emails/jour) |

**Décision** : Huey est parfaitement adapté pour notre cas d'usage (emails transactionnels à volume modéré) et simplifie le développement et le déploiement.

### Broker : SQLite vs Redis

**Phase de développement** → **SQLite**
- ✅ Aucune dépendance externe
- ✅ Configuration immédiate
- ✅ Suffisant pour < 100 emails/heure

**Phase de production** → **Redis** (migration simple)
- ✅ Meilleures performances
- ✅ Gestion avancée des files d'attente
- ✅ Support de la persistence
- ✅ Scalabilité horizontale

---

## 📁 Structure des fichiers

```
core/
├── services/
│   ├── email_service.py          # Service principal d'envoi d'emails
│   └── user_service.py            # Utilise EmailService
│
templates/
└── emails/
    ├── base.html                  # Template de base (logo, footer)
    ├── welcome.html               # Email de bienvenue
    ├── password_reset.html        # Réinitialisation de mot de passe
    ├── account_activated.html     # Activation de compte
    └── notification.html          # Notification générique
```

---

## 🚀 Utilisation

### 1. Envoi d'email prédéfini

```python
from core.services.email_service import EmailTemplates

# Email de bienvenue (appelé automatiquement lors de la création)
EmailTemplates.send_welcome_email(
    user_email="user@example.com",
    user_name="Jean Dupont",
    temp_password="MotDePasse123"
)

# Email d'activation de compte
EmailTemplates.send_account_activated_email(
    user_email="user@example.com",
    user_name="Jean Dupont"
)
```

### 2. Envoi d'email personnalisé

```python
from core.services.email_service import EmailService

# Asynchrone (recommandé)
EmailService.send_email_async(
    subject="Nouveau message",
    to_emails=["user@example.com"],
    template_name='emails/notification.html',
    context={
        'user_name': 'Jean Dupont',
        'notification_title': 'Titre',
        'notification_message': 'Votre message',
    }
)
```

---

## 🧪 Tests en développement

### Avec MailDev (recommandé)

MailDev est un serveur SMTP de test qui capture tous les emails sans les envoyer réellement.

#### 1. Démarrer MailDev
```bash
npx maildev
```

#### 2. Configuration Django
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
```

#### 3. Consulter les emails
Ouvrir dans le navigateur : **http://localhost:1080**

### Avec le backend Console (alternative)
```python
# settings.py - Affiche les emails dans le terminal
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

---

## 🔧 Configuration

### Développement (MailDev)
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

HUEY = {
    'huey_class': 'huey.SqliteHuey',
    'filename': os.path.join(BASE_DIR, 'huey.db'),
    'immediate': False,  # Mode asynchrone
    'consumer': {'workers': 4}
}
```

### Production (Gmail)
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'votre-email@gmail.com'
EMAIL_HOST_PASSWORD = 'mot-de-passe-application'

HUEY = {
    'huey_class': 'huey.RedisHuey',
    'connection': {'host': 'localhost', 'port': 6379},
    'consumer': {'workers': 8}
}
```

---

## 🏃 Démarrage

### Lancer l'application

**Terminal 1** - Serveur Django
```bash
python manage.py runserver
```

**Terminal 2** - Workers Huey (obligatoire)
```bash
python manage.py run_huey --huey-verbose
```
> **NB** : Sous linux ```python manage.py runserver & python manage.py run_huey --huey-verbose``` pour lancer les deux en même temps

**Terminal 3** - MailDev (pour tests)
```bash
npx maildev
```

> ⚠️ **Important** : Les workers Huey doivent être lancés pour que les emails soient envoyés !

---



## 🎨 Créer un nouveau template

### 1. Créer le fichier HTML
```html
<!-- templates/emails/custom.html -->
{% extends 'emails/base.html' %}

{% block title %}Mon titre{% endblock %}

{% block content %}
<div class="greeting">Bonjour {{ user_name }},</div>

<div class="content">
    <p>{{ custom_message }}</p>
</div>

<div style="text-align: center;">
    <a href="{{ action_url }}" class="button">{{ button_text }}</a>
</div>
{% endblock %}
```

### 2. Ajouter la méthode dans EmailTemplates
```python
# core/services/email_service.py
@staticmethod
def send_custom_email(user_email: str, user_name: str, custom_data: dict):
    EmailService.send_email_async(
        subject="Sujet personnalisé",
        to_emails=[user_email],
        template_name='emails/custom.html',
        context={
            'user_name': user_name,
            **custom_data
        }
    )
```

---

## 🔒 Sécurité et bonnes pratiques

### ✅ À faire
- Utiliser `send_email_async()` en production (non bloquant)
- Valider les adresses email avant l'envoi
- Limiter le nombre d'emails (anti-spam)
- Utiliser des mots de passe d'application (pas le mot de passe principal)
- Surveiller les logs d'envoi

### ❌ À éviter
- Ne jamais utiliser `send_email_sync()` dans une requête HTTP
- Ne jamais stocker les mots de passe SMTP en clair (utiliser variables d'environnement)
- Ne pas envoyer d'emails en boucle sans délai
- Ne pas négliger la gestion des erreurs

---

## 🐛 Résolution des problèmes

### Les emails ne sont pas envoyés
1. Vérifier que les workers Huey sont lancés : `python manage.py run_huey --huey-verbose`

2. Vérifier la configuration SMTP dans `settings.py`

### Les emails sont envoyés plusieurs fois
- Vérifier qu'il n'y a qu'une seule instance de worker Huey active
- Consulter `huey.db` pour voir les tâches en attente

### Erreur de connexion SMTP
- Vérifier les identifiants SMTP
- Pour Gmail : activer "Accès moins sécurisé" ou utiliser un mot de passe d'application
- Vérifier que le port et le protocole TLS/SSL sont corrects

---

## 📚 Ressources

- [Documentation Huey](https://huey.readthedocs.io/)
- [MailDev GitHub](https://github.com/maildev/maildev)
- [Django Email Backend](https://docs.djangoproject.com/en/4.2/topics/email/)
- [Gmail App Passwords](https://support.google.com/accounts/answer/185833)

---

## 🎓 Points clés à retenir

1. **Huey gère l'asynchrone** : Les emails ne bloquent jamais l'application
2. **SQLite pour débuter** : Simple et efficace en développement
3. **Redis pour scaler** : Migration facile si besoin de performances
4. **MailDev pour tester** : Capture tous les emails sans les envoyer
5. **Templates HTML** : Design professionnel et cohérent
6. **Retry automatique** : 3 tentatives en cas d'échec
7. **Logs détaillés** : Traçabilité complète des envois

---

**Version** : 1.0  
**Dernière mise à jour** : Décembre 2024  
**Équipe** : ENSPM Hub Development Team