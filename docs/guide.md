# Guide du Projet : Architecture et Organisation des Fichiers

## 📋 Table des matières

1. [Vue d'ensemble du projet](#vue-densemble-du-projet)
2. [Architecture technique](#architecture-technique)
3. [Organisation des modules Django](#organisation-des-modules-django)
4. [Structure détaillée des dossiers](#structure-détaillée-des-dossiers)
5. [Couche API (Django Ninja)](#couche-api-django-ninja)
6. [Couche Service (Logique Métier)](#couche-service-logique-métier)
7. [Couche Frontend (Inertia + React)](#couche-frontend-inertia--react)
8. [Flux de données](#flux-de-données)
9. [Conventions de nommage](#conventions-de-nommage)
10. [Guide de démarrage rapide](#guide-de-démarrage-rapide)

---

## 🎯 Vue d'ensemble du projet

**ENSPM Hub** est une plateforme de réseau professionnel destinée aux alumni, étudiants et partenaires de l'École Nationale Supérieure Polytechnique de Maroua. 

### Stack Technique

- **Backend**: Django 5.0+ avec Django Ninja (API REST)
- **Frontend**: React 18 + TypeScript via Inertia.js
- **Base de données**: PostgreSQL 15+
- **Architecture**: Architecture en couches (Service Layer Pattern)

### Principe d'architecture

Le projet suit une **architecture en 3 couches** :

```
┌─────────────────────────────────────────┐
│         Frontend (React + TS)           │  ← Présentation
│         via Inertia.js                  │
└─────────────────────────────────────────┘
                   ↕ JSON
┌─────────────────────────────────────────┐
│      API Layer (Django Ninja)           │  ← Endpoints REST
│      - Routes (views.py)                │
│      - Validation (schemas.py)          │
│      - Auth (auth.py)                   │
└─────────────────────────────────────────┘
                   ↕
┌─────────────────────────────────────────┐
│    Service Layer (Logique Métier)       │  ← Business Logic
│    - Services métier                    │
│    - Règles de gestion                  │
└─────────────────────────────────────────┘
                   ↕
┌─────────────────────────────────────────┐
│      Data Layer (Models Django)         │  ← Persistance
│      - ORM Django                       │
│      - Base de données PostgreSQL       │
└─────────────────────────────────────────┘
```

**🚨 IMPORTANT** : On ne fait **JAMAIS** de CRUD direct sur les models depuis les views. Toute la logique métier passe par la **couche Service**.

---

## 🏗️ Architecture technique

### Modules Django (Applications)

Le projet est divisé en **6 modules fonctionnels** :

| Module            | Responsabilité                           | Priorité         |
| ----------------- | ---------------------------------------- | ---------------- |
| **CORE**          | Auth, permissions, audit, config globale | P0 (Obligatoire) |
| **USERS**         | Gestion profils utilisateurs             | P0               |
| **ORGANIZATIONS** | Gestion organisations partenaires        | P1               |
| **OPPORTUNITIES** | Stages, formations, emplois              | P0               |
| **CHAT**          | Groupes de discussion, messages          | P1               |
| **STATISTICS**    | Statistiques d'emploi, dashboards        | P1               |

### Flux de communication entre couches

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                     │
│  Pages/Components → Appels Inertia → JSON              │
└─────────────────────────────────────────────────────────┘
                           ↓ HTTP Request
┌─────────────────────────────────────────────────────────┐
│                  API LAYER (views.py)                   │
│  1. Authentification (auth.py)                          │
│  2. Validation données (schemas.py - Pydantic)          │
│  3. Appel Service Layer                                 │
│  4. Sérialisation réponse (schemas.py)                  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│               SERVICE LAYER (services/)                 │
│  1. Validation métier                                   │
│  2. Logique complexe                                    │
│  3. Transactions                                        │
│  4. Interactions entre models                           │
│  5. Appel repositories/models                           │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│               DATA LAYER (models.py)                    │
│  ORM Django → PostgreSQL                                │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Structure détaillée des dossiers

```
enspm_hub/
├── enspm_hub/                      # Configuration projet Django
│   ├── __init__.py
│   ├── settings.py                 # Configuration globale
│   ├── urls.py                     # Routes principales (Inertia + API)
│   ├── wsgi.py                     # WSGI config
│   ├── asgi.py                     # ASGI config (WebSocket)
│   └── api.py                      # ⭐ API principale Django Ninja
│
├── core/                           # 🔐 Module CORE (Auth, Config)
│   ├── __init__.py
│   ├── models.py                   # Modèle User personnalisé
│   ├── admin.py                    # Interface admin Django
│   ├── apps.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_api.py
│   ├── api/                        # 🌐 Couche API
│   │   ├── __init__.py
│   │   ├── auth.py                 # Classes d'authentification Django Ninja
│   │   ├── schemas.py              # Schémas Pydantic (DTO)
│   │   └── views.py                # Endpoints API (routers)
│   ├── services/                   # 💼 Couche Service (Logique métier)
│   │   ├── __init__.py
│   │   ├── user_service.py         # Service gestion utilisateurs
│   │   ├── auth_service.py         # Service authentification
│   │   ├── email_service.py        # Service envoi emails
│   │   └── password_service.py     # Service génération mots de passe
│   ├── middleware/                 # Middleware personnalisés
│   │   ├── __init__.py
│   │   ├── audit_middleware.py     # Logging automatique
│   │   └── rls_middleware.py       # Row Level Security
│   ├── management/                 # Commandes Django
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── populate_references.py
│   └── migrations/
│       └── ...
│
├── users/                          # 👤 Module USERS
│   ├── __init__.py
│   ├── models.py                   # DomaineReference, AnneeReference
│   ├── admin.py
│   ├── apps.py
│   ├── tests/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── schemas.py              # UserListSchema, UserFilterSchema, etc.
│   │   └── views.py                # Endpoints liste/recherche users
│   └── services/
│       ├── __init__.py
│       └── user_profile_service.py # Service profil utilisateur
│
├── organizations/                  # 🏢 Module ORGANIZATIONS
│   ├── __init__.py
│   ├── models.py                   # Organisation, ContactOrganisation
│   ├── admin.py
│   ├── apps.py
│   ├── tests/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── schemas.py              # OrganisationOutSchema, ContactSchema, etc.
│   │   └── views.py                # Endpoints CRUD organisations
│   └── services/
│       ├── __init__.py
│       ├── organisation_service.py # Logique métier organisations
│       └── contact_service.py      # Gestion contacts organisations
│
├── opportunities/                  # 💼 Module OPPORTUNITIES
│   ├── __init__.py
│   ├── models.py                   # Stage, Formation, Emploi, ValidationFormation
│   ├── admin.py
│   ├── apps.py
│   ├── tests/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── schemas.py              # StageOutSchema, FormationCreateSchema, etc.
│   │   └── views.py                # Endpoints stages/formations/emplois
│   ├── services/
│   │   ├── __init__.py
│   │   ├── stage_service.py        # Logique métier stages
│   │   ├── formation_service.py    # Logique métier formations
│   │   ├── emploi_service.py       # Logique métier emplois
│   │   └── validation_service.py   # Validation formations
│   └── cron/                       # Jobs planifiés
│       ├── __init__.py
│       └── expire_old_offers.py    # Expiration automatique offres
│
├── chat/                           # 💬 Module CHAT
│   ├── __init__.py
│   ├── models.py                   # Groupe, MembreGroupe, Message
│   ├── admin.py
│   ├── apps.py
│   ├── tests/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── schemas.py              # GroupeOutSchema, MessageSchema, etc.
│   │   └── views.py                # Endpoints groupes/messages
│   ├── services/
│   │   ├── __init__.py
│   │   ├── groupe_service.py       # Logique métier groupes
│   │   ├── message_service.py      # Logique métier messages
│   │   ├── membre_service.py       # Gestion membres groupes
│   │   └── file_upload_service.py  # Upload fichiers messages
│   ├── consumers/                  # WebSocket (Django Channels)
│   │   ├── __init__.py
│   │   └── chat_consumer.py        # Consumer temps réel
│   ├── routing.py                  # Routes WebSocket
│   └── cron/
│       ├── __init__.py
│       └── delete_old_messages.py  # Suppression auto messages
│
├── statistics/                     # 📊 Module STATISTICS
│   ├── __init__.py
│   ├── models.py                   # StatsEmploiParAnnee (vue matérialisée)
│   ├── admin.py
│   ├── apps.py
│   ├── tests/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── schemas.py              # StatsEmploiSchema, DashboardSchema, etc.
│   │   └── views.py                # Endpoints statistiques
│   └── services/
│       ├── __init__.py
│       ├── emploi_stats_service.py # Calcul statistiques emploi
│       └── dashboard_service.py    # Données dashboard
│
├── frontend/                       # ⚛️ Frontend React + TypeScript
│   ├── ts/
│   │   ├── main.tsx                # Point d'entrée Inertia
│   │   ├── types/                  # Types TypeScript
│   │   │   ├── index.ts
│   │   │   ├── models.ts           # Types des modèles
│   │   │   └── api.ts              # Types des réponses API
│   │   ├── components/             # Composants réutilisables
│   │   │   ├── layout/
│   │   │   │   ├── Layout.tsx
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Footer.tsx
│   │   │   ├── ui/                 # Shadcn UI components
│   │   │   │   ├── button.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   ├── form.tsx
│   │   │   │   └── ...
│   │   │   ├── StageCard.tsx
│   │   │   ├── FormationCard.tsx
│   │   │   ├── GroupeCard.tsx
│   │   │   └── ...
│   │   ├── pages/                  # Pages Inertia
│   │   │   ├── Auth/
│   │   │   │   ├── Login.tsx
│   │   │   │   └── ForgotPassword.tsx
│   │   │   ├── Profile/
│   │   │   │   ├── Show.tsx
│   │   │   │   └── Edit.tsx
│   │   │   ├── Stages/
│   │   │   │   ├── Index.tsx       # Liste stages
│   │   │   │   ├── Show.tsx        # Détail stage
│   │   │   │   ├── Create.tsx      # Création stage
│   │   │   │   └── Edit.tsx        # Édition stage
│   │   │   ├── Formations/
│   │   │   │   └── ...
│   │   │   ├── Emplois/
│   │   │   │   └── ...
│   │   │   ├── Organisations/
│   │   │   │   └── ...
│   │   │   ├── Groupes/
│   │   │   │   ├── Index.tsx
│   │   │   │   ├── Chat.tsx
│   │   │   │   └── Create.tsx
│   │   │   ├── Admin/
│   │   │   │   ├── Users/
│   │   │   │   │   ├── Index.tsx
│   │   │   │   │   └── Edit.tsx
│   │   │   │   ├── FormationsEnAttente.tsx
│   │   │   │   ├── GroupesEnAttente.tsx
│   │   │   │   └── AuditLogs.tsx
│   │   │   ├── Statistiques/
│   │   │   │   └── Emploi.tsx
│   │   │   └── Dashboard.tsx
│   │   ├── services/               # Services frontend
│   │   │   ├── api.ts              # Client API
│   │   │   └── websocket.ts        # WebSocket client
│   │   └── utils/                  # Utilitaires
│   │       ├── validation.ts       # Schémas Zod
│   │       ├── formatters.ts
│   │       └── helpers.ts
│   └── css/
│       └── app.css                 # Styles Tailwind
│
├── templates/                      # Templates Django
│   ├── inertia_base.html          # Template de base Inertia
│   └── emails/                     # Templates emails
│       ├── welcome_email.html
│       ├── formation_validated.html
│       └── ...
│
├── static/                         # Fichiers statiques
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                          # Fichiers uploadés
│   ├── profile_photos/
│   ├── groupe_photos/
│   └── chat_files/
│
├── requirements.txt                # Dépendances Python
├── package.json                    # Dépendances Node.js
├── vite.config.ts                  # Configuration Vite
├── tailwind.config.js              # Configuration Tailwind
├── tsconfig.json                   # Configuration TypeScript
├── .env.example                    # Variables d'environnement exemple
├── .gitignore
├── manage.py
└── README.md
```

---

## 🌐 Couche API (Django Ninja)

### Structure d'un module API

Chaque module Django possède un dossier `api/` avec 3 fichiers principaux :

```
module_name/
├── api/
│   ├── __init__.py
│   ├── auth.py       # ⚠️ Uniquement dans core/
│   ├── schemas.py    # Schémas Pydantic (DTO)
│   └── views.py      # Endpoints (routers)
```

### 1. `schemas.py` - Schémas Pydantic (DTO - Data Transfer Objects)

Les schémas Pydantic définissent les **contrats d'API** (entrées/sorties) avec validation automatique.

**Types de schémas** :

- **`*OutSchema`** : Sortie API (ce qui est renvoyé au client)
- **`*CreateSchema`** : Entrée pour création
- **`*UpdateSchema`** : Entrée pour mise à jour (champs optionnels)
- **`*FilterSchema`** : Paramètres de filtrage/recherche

**Exemple** : `opportunities/api/schemas.py`

```python
from ninja import Schema, Field, validator
from typing import Optional
from datetime import date, datetime
from uuid import UUID
from decimal import Decimal
from ninja import Schema

# ========== SCHÉMAS DE SORTIE (OUT) ==========

class StageOutSchema(Schema):
    """Schéma de sortie pour un stage (ce qui est renvoyé au client)"""
    id: UUID
    titre: str
    lieu: str
    nom_structure: str
    description: Optional[str]
    type_stage: Optional[str]
    email_contact: str
    telephone_contact: Optional[str]
    lien_offre: Optional[str]
    date_debut: Optional[date]
    date_fin: Optional[date]
    statut: str
    created_at: datetime
    updated_at: datetime
    
    # Champs calculés (relations)
    createur_id: UUID
    createur_nom: str
    organisation_id: Optional[UUID]
    organisation_nom: Optional[str]

...
```

### 2. `views.py` - Endpoints API (Routers)

Les routers Django Ninja définissent les **endpoints REST**. Ils appellent les **services** pour la logique métier.

**🚨 RÈGLE IMPORTANTE** : Les views **NE FONT PAS** de CRUD direct sur les models. Elles appellent la couche Service.

**Exemple** : `opportunities/api/views.py`

```python
from ninja import Router, Query
from ninja.pagination import paginate, PageNumberPagination
from django.shortcuts import get_object_or_404
from typing import List
from uuid import UUID

from core.api.auth import django_auth, get_current_user, require_role
from core.api.schemas import MessageSchema
from .schemas import (
    StageOutSchema, 
    StageCreateSchema, 
    StageUpdateSchema,
    StageFilterSchema
)
# 
from opportunities.services.stage_service import StageService

# Créer le router
stages_router = Router(tags=["Stages"])

# ========== LISTE & RECHERCHE ==========

@stages_router.get("/", auth=django_auth, response=List[StageOutSchema])
@paginate(PageNumberPagination, page_size=20)
def list_stages(
    request,
    filters: Query[StageFilterSchema]  # Validation automatique des filtres
):
    """
    Liste paginée des stages avec filtres
    
    Filtres disponibles:
    - statut: active, expiree, pourvue
    - lieu: ville
    - type_stage: ouvrier, academique, professionnel
    - q: recherche textuelle
    """
    # Appel du SERVICE (pas de logique ici)
    stages = StageService.list_stages(
        user=request.user,
        filters=filters.dict(exclude_none=True)
    )
    
    return stages


```

### 3. `auth.py` - Authentification (uniquement dans `core/`)

**Emplacement** : `core/api/auth.py`

```python
from typing import Optional
from ninja.security import SessionAuth
from django.contrib.auth import get_user_model
from django.http import HttpRequest

User = get_user_model()

# ========== CLASSES D'AUTHENTIFICATION ==========

class DjangoSessionAuth(SessionAuth):
    """Authentification basée sur la session Django"""
    def authenticate(self, request: HttpRequest, key: Optional[str]) -> Optional[User]:
        if request.user.is_authenticated:
            return request.user
        return None

# Instance réutilisable
django_auth = DjangoSessionAuth()


# ========== HELPERS ==========

def get_current_user(request: HttpRequest) -> User:
    """
    Récupérer l'utilisateur connecté
    Lève PermissionError si non authentifié
    """
    if not request.user.is_authenticated:
        raise PermissionError("Authentification requise")
    return request.user


def require_role(allowed_roles: list):
    """
    Décorateur pour vérifier le rôle utilisateur
    
    Usage:
        @require_role(['admin', 'super_admin'])
        def my_view(request):
            ...
    """
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            user = get_current_user(request)
            if user.role not in allowed_roles:
                raise PermissionError(f"Rôle requis: {', '.join(allowed_roles)}")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
```

### 4. Configuration API principale

**Emplacement** : `enspm_hub/api_v1.py`

```python
from ninja import NinjaAPI
from django.conf import settings

# Créer l'API principale
api_v1 = NinjaAPI(
    title="ENSPM Hub API",
    version="1.0.0",
    description="API REST pour la plateforme ENSPM Hub",
    docs_url="/api/docs",  # Documentation Swagger
    csrf=True,
)

# ========== ENREGISTREMENT DES ROUTERS ==========

# Core (Auth)
from core.api.views import auth_router, users_router
api_v1.add_router("/auth/", auth_router)
api_v1.add_router("/users/", users_router)

# Opportunities
from opportunities.api.views import stages_router, formations_router, emplois_router
api_v1.add_router("/stages/", stages_router)
...

# Organizations
from organizations.api.views import organisations_router, contacts_router
api_v1.add_router("/organisations/", organisations_router)
...


**Enregistrement dans les URLs** : `enspm_hub/urls.py`

```python
from django.contrib import admin
from django.urls import path
from .api import api  # Import de l'API

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API REST (Django Ninja)
    path('api/v1/', api.urls),
    
    # Routes Inertia (SPA)
    # ...
]
```

### 5. Gestion Globale des Erreurs

Pour garantir une expérience cohérente et prévisible, l'API ENSPM Hub utilise un système de gestion globale des exceptions. Toutes les erreurs retournent une réponse JSON standardisée, ce qui simplifie la gestion des erreurs côté client.

La configuration se trouve dans `enspm_hub/api_v1.py` et utilise les décorateurs `@api_v1.exception_handler`.

#### Structure des Réponses d'Erreur

La structure générale pour une erreur est la suivante :

```json
{
    "detail": "Message principal de l'erreur."
}
```

Pour les erreurs plus complexes comme la validation, des détails supplémentaires peuvent être fournis.

#### Types d'Erreurs Gérées

1.  **Erreur de Validation (`422 Unprocessable Content`)**
    -   **Déclencheur** : Échec de la validation d'un schéma Pydantic (`*Schema`).
    -   **Exemple de Réponse** :
        ```json
        {
            "detail": "Erreur de validation.",
            "errors": [
                {
                    "field": "email",
                    "message": "value is not a valid email address"
                },
                {
                    "field": "password",
                    "message": "ensure this value has at least 8 characters"
                }
            ]
        }
        ```

2.  **Ressource Non Trouvée (`404 Not Found`)**
    -   **Déclencheur** : Levée d'une exception `Http404` (ex: `get_object_or_404`).
    -   **Exemple de Réponse** :
        ```json
        {
            "detail": "La ressource demandée n'a pas été trouvée."
        }
        ```

3.  **Erreur de Serveur (`500 Internal Server Error`)**
    -   **Déclencheur** : Toute exception non interceptée par les autres gestionnaires.
    -   **Comportement** :
        -   En mode `DEBUG=True`, la réponse contient des détails techniques pour faciliter le débogage.
        -   En mode `DEBUG=False` (production), un message générique est retourné pour ne pas exposer de détails d'implémentation. L'erreur complète est enregistrée dans les logs.
    -   **Exemple de Réponse (Production)** :
        ```json
        {
            "detail": "Une erreur inattendue est survenue. L'équipe technique a été notifiée."
        }
        ```

4.  **Exceptions Métier Personnalisées**
    -   **Objectif** : Permettre de lever des erreurs spécifiques depuis la couche Service avec des codes de statut HTTP appropriés.
    -   **Implémentation** : Des classes d'exception personnalisées sont définies dans `core/api/exceptions.py`.
    -   **Exemple d'utilisation dans un service** :
        ```python
        # core/services/some_service.py
        from core.api.exceptions import PermissionDeniedAPIException

        class SomeService:
            @staticmethod
            def some_action(user, resource):
                if not user.has_permission_for(resource):
                    # Lève une exception qui sera interceptée par le gestionnaire global
                    raise PermissionDeniedAPIException("Vous n'êtes pas autorisé à modifier cette ressource.")
        ```
    -   **Réponse API (`403 Forbidden`)** :
        ```json
        {
            "detail": "Vous n'êtes pas autorisé à modifier cette ressource."
        }
        ```

---

## 💼 Couche Service (Logique Métier)

### Principe

La couche Service contient **toute la logique métier**. Elle est appelée par les views API et **ne doit jamais être bypassée**.

```
Views API → Services → Models/DB
```

### Structure d'un service

```python
# opportunities/services/stage_service.py

from typing import List, Dict, Optional
from uuid import UUID
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Q

from opportunities.models import Stage
from core.models import User
from organizations.models import Organisation

class StageService:
    """
    Service de gestion des stages
    Contient toute la logique métier
    """
    
    @staticmethod
    def list_stages(user: User, filters: Dict) -> List[Stage]:
        """
        Liste les stages avec filtres et permissions
        
        Args:
            user: Utilisateur connecté
            filters: Dictionnaire de filtres
            
        Returns:
            Liste de stages
        """
        queryset = Stage.objects.select_related('createur', 'organisation').all()
        
        # ========== ROW LEVEL SECURITY (RLS) ==========
        # Seul le créateur ou admin peut voir ses stages inactifs
        if user.role not in ['admin', 'super_admin']:
            queryset = queryset.filter(
                Q(statut='active') | Q(createur=user)
            )
        
        # ========== FILTRES ==========
        statut = filters.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)
        else:
            queryset = queryset.filter(statut='active')  # Par défaut
        
        lieu = filters.get('lieu')
        if lieu:
            queryset = queryset.filter(lieu__icontains=lieu)
        
        type_stage = filters.get('type_stage')
        if type_stage:
            queryset = queryset.filter(type_stage=type_stage)
        
        # Recherche textuelle
        q = filters.get('q')
        if q:
            queryset = queryset.filter(
                Q(titre__icontains=q) | 
                Q(description__icontains=q) |
                Q(nom_structure__icontains=q)
            )
        
        # Tri
        queryset = queryset.order_by('-created_at')
        
        return queryset
    
    
    @staticmethod
    def get_stage_by_id(stage_id: UUID, user: User) -> Stage:
        """
        Récupère un stage par son ID avec vérifications de permissions
        
        Args:
            stage_id: UUID du stage
            user: Utilisateur connecté
            
        Returns:
            Stage
            
        Raises:
            Http404: Si stage non trouvé
            PermissionError: Si pas de permission
        """
        stage = get_object_or_404(
            Stage.objects.select_related('createur', 'organisation'),
            id=stage_id
        )
        
        # ========== VÉRIFICATION PERMISSIONS ==========
        # Seul le créateur ou admin peut voir un stage inactif
        if stage.statut != 'active':
            if user.id != stage.createur.id and user.role not in ['admin', 'super_admin']:
                raise PermissionError("Vous n'avez pas accès à ce stage")
        
        # Ajouter champs calculés pour sérialisation
        stage.createur_nom = stage.createur.nom_complet
        stage.organisation_nom = stage.organisation.nom_organisation if stage.organisation else None
        
        return stage
    
    
    @staticmethod
    @transaction.atomic
    def create_stage(user: User, data: Dict) -> Stage:
        """
        Crée un nouveau stage avec validations métier
        
        Args:
            user: Utilisateur créateur
            data: Données du stage
            
        Returns:
            Stage créé
            
        Raises:
            ValueError: Si validation métier échoue
        """
        # ========== PRÉ-REMPLISSAGE AUTOMATIQUE ==========
        if not data.get('email_contact'):
            data['email_contact'] = user.email
        
        if not data.get('telephone_contact') and user.telephone:
            data['telephone_contact'] = user.telephone
        
        # ========== VALIDATION MÉTIER ==========
        # Vérifier que l'organisation existe si fournie
        organisation_id = data.pop('organisation_id', None)
        organisation = None
        
        if organisation_id:
            organisation = get_object_or_404(Organisation, id=organisation_id, statut='active')
        
        # ========== CRÉATION ==========
        stage = Stage.objects.create(
            **data,
            createur=user,
            organisation=organisation,
            statut='active'
        )
        
        # ========== POST-TRAITEMENT ==========
        # Envoyer notification (optionnel)
        # EmailService.send_new_stage_notification(stage)
        
        # Ajouter champs calculés
        stage.createur_nom = user.nom_complet
        stage.organisation_nom = organisation.nom_organisation if organisation else None
        
        return stage
    
    
    @staticmethod
    @transaction.atomic
    def update_stage(stage_id: UUID, user: User, data: Dict) -> Stage:
        """
        Met à jour un stage avec vérifications de permissions
        
        Args:
            stage_id: UUID du stage
            user: Utilisateur effectuant la modification
            data: Données à mettre à jour
            
        Returns:
            Stage mis à jour
            
        Raises:
            PermissionError: Si pas de permission
        """
        stage = get_object_or_404(Stage, id=stage_id)
        
        # ========== VÉRIFICATION PERMISSIONS ==========
        if stage.createur.id != user.id and user.role not in ['admin', 'super_admin']:
            raise PermissionError("Vous ne pouvez modifier que vos propres offres")
        
        # ========== MISE À JOUR ==========
        for field, value in data.items():
            setattr(stage, field, value)
        
        stage.save()
        
        # Ajouter champs calculés
        stage.createur_nom = stage.createur.nom_complet
        stage.organisation_nom = stage.organisation.nom_organisation if stage.organisation else None
        
        return stage
    
    
    @staticmethod
    @transaction.atomic
    def delete_stage(stage_id: UUID, user: User) -> str:
        """
        Supprime un stage avec vérifications de permissions
        
        Args:
            stage_id: UUID du stage
            user: Utilisateur effectuant la suppression
            
        Returns:
            Titre du stage supprimé
            
        Raises:
            PermissionError: Si pas de permission
        """
        stage = get_object_or_404(Stage, id=stage_id)
        
        # ========== VÉRIFICATION PERMISSIONS ==========
        if stage.createur.id != user.id and user.role not in ['admin', 'super_admin']:
            raise PermissionError("Vous ne pouvez supprimer que vos propres offres")
        
        titre = stage.titre
        stage.delete()
        
        return titre
    
    
    @staticmethod
    def search_stages(user: User, filters: Dict) -> List[Stage]:
        """
        Recherche avancée avec full-text search
        
        Args:
            user: Utilisateur connecté
            filters: Dictionnaire de filtres
            
        Returns:
            Liste de stages
        """
        # Réutiliser list_stages avec filtres
        return StageService.list_stages(user, filters)
```

### Autres exemples de services

**Service Email** : `core/services/email_service.py`

```python
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """Service d'envoi d'emails transactionnels"""
    
    @staticmethod
    def send_welcome_email(user, password: str):
        """
        Envoie l'email de bienvenue avec identifiants
        
        Args:
            user: Instance User
            password: Mot de passe en clair
        """
        try:
            subject = "Bienvenue sur ENSPM Hub"
            html_message = render_to_string('emails/welcome_email.html', {
                'user': user,
                'password': password,
                'login_url': f"{settings.SITE_URL}/login"
            })
            
            send_mail(
                subject=subject,
                message="",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False
            )
            
            logger.info(f"Email de bienvenue envoyé à {user.email}")
            
        except Exception as e:
            logger.error(f"Erreur envoi email à {user.email}: {str(e)}")
            # Ne pas bloquer le processus si l'email échoue
```

**Service Génération Mot de Passe** : `core/services/password_service.py`

```python
import secrets
import string

class PasswordService:
    """Service de génération de mots de passe sécurisés"""
    
    @staticmethod
    def generate_secure_password(length: int = 12) -> str:
        """
        Génère un mot de passe aléatoire sécurisé
        
        Args:
            length: Longueur du mot de passe
            
        Returns:
            Mot de passe généré
        """
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password
```

---

## ⚛️ Couche Frontend (Inertia + React)

### Architecture Frontend

```
frontend/ts/
├── main.tsx              # Point d'entrée Inertia
├── types/                # Types TypeScript
├── components/           # Composants réutilisables
├── pages/                # Pages Inertia (routes)
├── services/             # Services API
└── utils/                # Utilitaires
```


## 🔄 Flux de données

### Exemple complet : Création d'un stage

```
1. Frontend (React)
   └─> Formulaire Create.tsx
       └─> Validation Zod
           └─> Inertia.post('/api/stages/', data)

2. API Layer (Django Ninja)
   └─> stages_router.post() dans views.py
       └─> Validation Pydantic (StageCreateSchema)
           └─> Authentification (django_auth)
               └─> StageService.create_stage(user, data)

3. Service Layer
   └─> StageService.create_stage()
       └─> Validation métier
           └─> Pré-remplissage email/téléphone
               └─> Stage.objects.create()
                   └─> EmailService.send_notification()

4. Data Layer
   └─> Django ORM
       └─> INSERT INTO opportunities_stage
           └─> Commit transaction

5. Réponse
   └─> Service retourne Stage
       └─> View sérialise en StageOutSchema
           └─> JSON retourné au Frontend
               └─> Inertia redirige vers /stages/{id}
```

---

## 📝 Conventions de nommage

### Backend (Python)

- **Modules** : `snake_case` (ex: `stage_service.py`)
- **Classes** : `PascalCase` (ex: `StageService`)
- **Fonctions/méthodes** : `snake_case` (ex: `create_stage()`)
- **Variables** : `snake_case` (ex: `current_user`)
- **Constantes** : `UPPER_CASE` (ex: `MAX_FILE_SIZE`)

### Schémas Pydantic

- **Out** : `ModelNameOutSchema` (ex: `StageOutSchema`)
- **Create** : `ModelNameCreateSchema` (ex: `StageCreateSchema`)
- **Update** : `ModelNameUpdateSchema` (ex: `StageUpdateSchema`)
- **Filter** : `ModelNameFilterSchema` (ex: `StageFilterSchema`)

### Frontend (TypeScript)

- **Composants** : `PascalCase` (ex: `StageCard.tsx`)
- **Pages** : `PascalCase` (ex: `Index.tsx`, `Create.tsx`)
- **Fonctions** : `camelCase` (ex: `handleSubmit()`)
- **Variables** : `camelCase` (ex: `currentUser`)
- **Types/Interfaces** : `PascalCase` (ex: `interface Stage {}`)

### Endpoints API

```
GET    /api/{resource}/              # Liste
GET    /api/{resource}/{id}/         # Détail
POST   /api/{resource}/              # Création
PATCH  /api/{resource}/{id}/         # Mise à jour partielle
DELETE /api/{resource}/{id}/         # Suppression
GET    /api/{resource}/search/       # Recherche avancée
POST   /api/{resource}/{id}/action/  # Action spécifique
```

---

## 🚀 Guide de démarrage rapide

### 1. Prérequis

```bash
# Python 3.10+
python --version

# Node.js 18+
node --version

# PostgreSQL 15+
psql --version
```

### 2. Installation

```bash
# Cloner le projet
git clone https://github.com/your-org/enspm-hub.git
cd enspm-hub

# Créer environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate  # Windows

# Installer dépendances Python
pip install -r requirements.txt

# Installer dépendances Node.js
npm install

# Copier .env.example vers .env
cp .env.example .env

# Éditer .env avec vos configurations
nano .env
```

### 3. Configuration Base de Données

```bash
# Créer la base de données PostgreSQL
createdb enspm_hub

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Peupler les données de référence
python manage.py populate_references
```

### 4. Lancement

```bash
# Terminal 1 : Django
python manage.py runserver

# Terminal 2 : Vite (hot-reload frontend)
npm run dev

# Accéder à l'application
# Frontend : http://localhost:8000
# API Docs : http://localhost:8000/api/docs
# Admin : http://localhost:8000/admin
```

### 5. Créer un nouveau module

```bash
# 1. Créer l'app Django
python manage.py startapp mon_module

# 2. Créer la structure
mkdir -p mon_module/api
mkdir -p mon_module/services
mkdir -p mon_module/tests

touch mon_module/api/__init__.py
touch mon_module/api/schemas.py
touch mon_module/api/views.py
touch mon_module/services/__init__.py
touch mon_module/services/mon_service.py

# 3. Ajouter dans INSTALLED_APPS (settings.py)
INSTALLED_APPS = [
    ...
    'mon_module',
]

# 4. Créer les modèles dans mon_module/models.py

# 5. Créer les migrations
python manage.py makemigrations mon_module
python manage.py migrate

# 6. Créer les schémas dans api/schemas.py

# 7. Créer le service dans services/mon_service.py

# 8. Créer les endpoints dans api/views.py

# 9. Enregistrer le router dans enspm_hub/api.py
from mon_module.api.views import mon_router
api.add_router("/mon-resource/", mon_router)

# 10. Créer les pages frontend
mkdir -p frontend/ts/pages/MonModule
touch frontend/ts/pages/MonModule/Index.tsx
```

---

## 📚 Ressources

### Documentation officielle

- [Django](https://docs.djangoproject.com/)
- [Django Ninja](https://django-ninja.rest-framework.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [Inertia.js](https://inertiajs.com/)
- [React](https://react.dev/)
- [TypeScript](https://www.typescriptlang.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Shadcn UI](https://ui.shadcn.com/)

### Commandes utiles

```bash
# Créer migrations
python manage.py makemigrations

# Appliquer migrations
python manage.py migrate

# Créer superuser
python manage.py createsuperuser

# Shell Django
python manage.py shell

# Tests
python manage.py test

# Collecter fichiers statiques
python manage.py collectstatic

# Build frontend production
npm run build
```

---

## 🎓 Bonnes pratiques

### Backend

1. ✅ **Toujours utiliser la couche Service** (pas de CRUD direct dans views)
2. ✅ **Valider avec Pydantic** (schémas dans `api/schemas.py`)
3. ✅ **Gérer les permissions** dans les services
4. ✅ **Utiliser `@transaction.atomic`** pour les opérations critiques
5. ✅ **Logger les erreurs** avec `logging`
6. ✅ **Optimiser les requêtes** (`select_related`, `prefetch_related`)
7. ✅ **Écrire des tests** pour chaque service

### Frontend

1. ✅ **Typer avec TypeScript** (pas de `any`)
2. ✅ **Valider les formulaires** avec Zod
3. ✅ **Utiliser Shadcn UI** pour les composants
4. ✅ **Gérer les états** avec React Hooks
5. ✅ **Optimiser les rendus** (`useMemo`, `useCallback`)
6. ✅ **Gérer les erreurs** avec try/catch
7. ✅ **Responsive design** (mobile-first)

---

## 🪵 Stratégie de Logging

Un bon logging est crucial pour la maintenance, le débogage et la supervision de l'application.

### Configuration

Le logging est configuré dans `enspm_hub/settings.py` et est conçu pour être flexible :

- **En Développement (`DEBUG=True`)** : Les logs sont affichés dans la console dans un format simple et lisible pour faciliter le débogage.
- **En Production (`DEBUG=False`)** : Les logs sont formatés en **JSON**. Ce format structuré est idéal pour être ingéré par des outils de supervision comme Graylog, Splunk, ou la stack ELK (Elasticsearch, Logstash, Kibana).

### Comment Logger

Pour ajouter des logs dans le code, utilisez le logger `app` configuré spécifiquement pour notre application.

**1. Importez le logger**

Dans n'importe quel fichier de service, vue, ou autre module :

```python
import logging

logger = logging.getLogger('app')
```

**2. Utilisez les niveaux de log appropriés**

Chaque niveau a une signification précise :

| Niveau       | Quand l'utiliser                                                                                                     | Exemple                                                              |
|--------------|----------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|
| `DEBUG`      | Pour des informations de diagnostic très détaillées, utiles uniquement lors du débogage d'un problème spécifique.       | `logger.debug(f"User {user.id} raw data: {raw_data}")`               |
| `INFO`       | Pour des événements normaux qui tracent le déroulement de l'application. C'est le niveau par défaut.                   | `logger.info(f"User {user.email} logged in successfully.")`           |
| `WARNING`    | Pour des événements inattendus qui ne sont pas des erreurs, mais qui pourraient indiquer un futur problème.          | `logger.warning(f"API key for service X is expiring in 3 days.")`    |
| `ERROR`      | Pour des erreurs qui ont empêché une opération de se terminer, mais qui ne mettent pas en péril l'application.        | `logger.error(f"Failed to send email to {user.email}: {e}")`         |
| `CRITICAL`   | Pour des erreurs très graves qui peuvent entraîner l'arrêt de l'application ou une corruption de données.           | `logger.critical("Database connection lost!")`                       |

**3. Ajouter un contexte structuré**

Pour enrichir les logs JSON, vous pouvez passer un dictionnaire `extra` avec des informations contextuelles. C'est extrêmement utile pour la recherche et l'analyse dans les outils de supervision.

```python
# Exemple dans un service
def process_payment(user, amount, request_id):
    logger.info(
        "Processing payment.",
        extra={
            'user_id': user.id,
            'amount': amount,
            'request_id': request_id,
        }
    )

    try:
        # ... logique métier ...
        logger.info("Payment successful.", extra={'user_id': user.id})
    except Exception as e:
        logger.error(
            "Payment failed.",
            exc_info=True,  # Ajoute automatiquement le traceback de l'exception
            extra={
                'user_id': user.id,
                'amount': amount,
                'request_id': request_id,
            }
        )
```

En suivant ces conventions, nous nous assurons que les logs de l'application sont cohérents, utiles, et prêts pour une supervision efficace en production.

---

**🎉 Vous êtes prêt à contribuer au projet ENSPM Hub !**
