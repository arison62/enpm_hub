# 🎯 ISSUES GITHUB - ENSPM HUB PROJECT

## 📋 TEMPLATE D'ISSUE GITHUB

```markdown
## Description
[Description claire de la fonctionnalité]

## Objectif
[Objectif métier de cette issue]

## Dépendances
- [ ] #[numéro_issue]

## Critères d'acceptation
- [ ] Critère 1
- [ ] Critère 2

## Tâches techniques
- [ ] Tâche 1
- [ ] Tâche 2

## Estimation
[X jours]

## Labels
`epic:[nom]` `priority:[P0/P1/P2]` `type:[backend/frontend/devops]`
```

---

## 🏗️ EPIC 1 - CORE & AUTHENTIFICATION

### Issue #1 - Configuration initiale du projet Django
```markdown
## Description
Mise en place de la structure Django avec configuration PostgreSQL

## Objectif
Avoir un projet Django fonctionnel avec base de données configurée

## Dépendances
Aucune

## Critères d'acceptation
- [ ] Projet Django créé et exécutable
- [ ] PostgreSQL connecté avec succès
- [ ] Variables d'environnement configurées
- [ ] Migrations de base appliquées
- [ ] Structure de dossiers en place

## Tâches techniques
- [ ] Créer le projet Django `enspm_hub`
- [ ] Configurer `settings.py` (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
- [ ] Configurer PostgreSQL via `DATABASE_URL`
- [ ] Installer et configurer `python-decouple` pour `.env`
- [ ] Créer la structure de dossiers (`frontend/`, `templates/`, `static/`, `media/`)
- [ ] Appliquer les migrations initiales
- [ ] Tester la connexion à la base de données
- [ ] Créer `requirements.txt` avec dépendances de base

## Estimation
1 jour

## Labels
`epic:core` `priority:P0` `type:backend` `sprint:1`
```

### Issue #2 - Modèle Utilisateur personnalisé
```markdown
## Description
Créer un modèle `User` personnalisé avec tous les attributs métier

## Objectif
Remplacer le modèle User par défaut de Django avec un modèle adapté aux besoins ENSPM Hub

## Dépendances
- [ ] #1

## Critères d'acceptation
- [ ] Modèle User créé avec tous les champs requis
- [ ] UserManager personnalisé implémenté
- [ ] Contraintes CHECK en place (annee_sortie pour étudiants uniquement)
- [ ] Signal empêchant modification de `travailleur`
- [ ] Migrations créées et appliquées
- [ ] Tests de création d'utilisateurs passent

## Tâches techniques
- [ ] Créer l'app `core`
- [ ] Définir les ENUM pour `statut` et `role`
```python
STATUT_CHOICES = [
    ('etudiant', 'Étudiant'),
    ('enseignant', 'Enseignant'),
    ('directeur', 'Directeur'),
    ('personnel_admin', 'Personnel Administratif'),
    ('personnel_technique', 'Personnel Technique'),
]

ROLE_CHOICES = [
    ('user', 'Utilisateur'),
    ('admin', 'Administrateur'),
    ('super_admin', 'Super Administrateur'),
]
```
- [ ] Créer le modèle `User` héritant de `AbstractBaseUser`
```python
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    nom_complet = models.CharField(max_length=255)
    matricule = models.CharField(max_length=50, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES)
    travailleur = models.BooleanField(default=False)
    annee_sortie = models.SmallIntegerField(null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    photo_profil_url = models.TextField(null=True, blank=True)
    domaine = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    est_actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom_complet', 'statut']
```
- [ ] Implémenter le `UserManager` personnalisé
- [ ] Ajouter les contraintes CHECK
- [ ] Créer un signal pour empêcher la modification de `travailleur`
- [ ] Configurer `AUTH_USER_MODEL` dans `settings.py`
- [ ] Créer des tests unitaires

## Estimation
2 jours

## Labels
`epic:core` `priority:P0` `type:backend` `sprint:1`
```

### Issue #3 - API Django Ninja - Configuration de base
```markdown
## Description
Configurer Django Ninja pour l'API REST selon le guide d'intégration

## Objectif
Avoir une API REST fonctionnelle avec documentation automatique

## Dépendances
- [ ] #1

## Critères d'acceptation
- [ ] Django Ninja installé et configuré
- [ ] API principale créée dans `enspm_hub/api.py`
- [ ] Documentation Swagger accessible sur `/api/docs`
- [ ] Endpoint health check fonctionnel
- [ ] Gestion d'erreurs globale implémentée

## Tâches techniques
- [ ] Installer Django Ninja : `pip install django-ninja`
- [ ] Installer dépendances recommandées :
```bash
pip install pydantic[email]
pip install python-multipart
```
- [ ] Créer `enspm_hub/api.py` avec configuration de base
```python
from ninja import NinjaAPI
from django.conf import settings

api = NinjaAPI(
    title="ENSPM Hub API",
    version="1.0.0",
    description="API REST pour la plateforme ENSPM Hub",
    docs_url="/api/docs",
    csrf=True,
)

@api.get("/health", auth=None, tags=["System"])
def health_check(request):
    return {
        "status": "ok",
        "version": "1.0.0",
        "environment": "development" if settings.DEBUG else "production"
    }
```
- [ ] Enregistrer l'API dans `enspm_hub/urls.py`
```python
from .api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    # ... autres routes
]
```
- [ ] Créer le gestionnaire d'erreurs global
- [ ] Tester l'accès à `/api/docs` et `/api/health`
- [ ] Mettre à jour `requirements.txt`

## Estimation
1 jour

## Labels
`epic:core` `priority:P0` `type:backend` `sprint:1`
```

### Issue #4 - Schémas Pydantic pour l'authentification
```markdown
## Description
Créer les schémas Pydantic pour l'authentification et les utilisateurs

## Objectif
Définir les contrats d'API avec validation automatique

## Dépendances
- [ ] #2
- [ ] #3

## Critères d'acceptation
- [ ] Tous les schémas créés dans `core/api/schemas.py`
- [ ] Validation Pydantic fonctionnelle
- [ ] Conversion ORM vers schéma testée

## Tâches techniques
- [ ] Créer `core/api/__init__.py`
- [ ] Créer `core/api/schemas.py` avec tous les schémas :
```python
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from uuid import UUID

class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserOutSchema(BaseModel):
    id: UUID
    nom_complet: str
    email: EmailStr
    matricule: Optional[str]
    statut: str
    travailleur: bool
    annee_sortie: Optional[int]
    telephone: Optional[str]
    photo_profil_url: Optional[str]
    domaine: Optional[str]
    role: str
    est_actif: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

class UserCreateSchema(BaseModel):
    nom_complet: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    matricule: Optional[str]
    statut: str
    travailleur: bool
    annee_sortie: Optional[int] = Field(None, ge=2000, le=2030)
    telephone: Optional[str]
    domaine: Optional[str]
    
    @validator('annee_sortie')
    def validate_annee_sortie(cls, v, values):
        if values.get('statut') == 'etudiant' and v is None:
            raise ValueError("L'année de sortie est obligatoire pour les étudiants")
        return v

class UserUpdateSchema(BaseModel):
    nom_complet: Optional[str]
    telephone: Optional[str]
    photo_profil_url: Optional[str]
    domaine: Optional[str]
    
    class Config:
        extra = "forbid"

class MessageSchema(BaseModel):
    message: str
    success: bool = True
```
- [ ] Tester la validation des schémas
- [ ] Documenter les schémas

## Estimation
1 jour

## Labels
`epic:core` `priority:P0` `type:backend` `sprint:1`
```

### Issue #5 - Système d'authentification Django Ninja
```markdown
## Description
Implémenter l'authentification par session Django avec Django Ninja

## Objectif
Permettre la connexion des utilisateurs via API

## Dépendances
- [ ] #2
- [ ] #3
- [ ] #4

## Critères d'acceptation
- [ ] Classes d'authentification créées dans `core/api/auth.py`
- [ ] Authentification par session fonctionnelle
- [ ] Décorateurs de vérification de rôle implémentés
- [ ] Tests d'authentification passent

## Tâches techniques
- [ ] Créer `core/api/auth.py` :
```python
from typing import Optional
from ninja.security import SessionAuth
from django.contrib.auth import get_user_model
from django.http import HttpRequest

User = get_user_model()

class DjangoSessionAuth(SessionAuth):
    def authenticate(self, request: HttpRequest, key: Optional[str]) -> Optional[User]:
        if request.user.is_authenticated:
            return request.user
        return None

django_auth = DjangoSessionAuth()

def get_current_user(request: HttpRequest) -> User:
    if not request.user.is_authenticated:
        raise PermissionError("Authentification requise")
    return request.user

def require_role(allowed_roles: list):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            user = get_current_user(request)
            if user.role not in allowed_roles:
                raise PermissionError(f"Rôle requis: {', '.join(allowed_roles)}")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
```
- [ ] Tester l'authentification
- [ ] Documenter l'utilisation

## Estimation
1.5 jour

## Labels
`epic:core` `priority:P0` `type:backend` `sprint:1`
```

### Issue #6 - API Endpoints d'authentification
```markdown
## Description
Créer les endpoints login, logout et profil utilisateur avec Django Ninja

## Objectif
Permettre aux utilisateurs de se connecter via API

## Dépendances
- [ ] #4
- [ ] #5

## Critères d'acceptation
- [ ] Endpoint `/api/auth/login` fonctionnel
- [ ] Endpoint `/api/auth/logout` fonctionnel
- [ ] Endpoint `/api/auth/me` fonctionnel
- [ ] Gestion des erreurs 401
- [ ] Tests d'intégration passent

## Tâches techniques
- [ ] Créer `core/api/views.py` avec router d'authentification :
```python
from ninja import Router
from django.contrib.auth import authenticate, login, logout
from .schemas import LoginSchema, UserOutSchema, MessageSchema
from .auth import django_auth, get_current_user

auth_router = Router(tags=["Authentification"])

@auth_router.post("/login", auth=None, response={200: UserOutSchema, 401: MessageSchema})
def login_user(request, payload: LoginSchema):
    user = authenticate(
        request,
        username=payload.email,
        password=payload.password
    )
    
    if user is not None:
        if not user.est_actif:
            return 401, {"message": "Ce compte est désactivé", "success": False}
        
        login(request, user)
        return user
    
    return 401, {"message": "Email ou mot de passe incorrect", "success": False}

@auth_router.post("/logout", auth=django_auth, response=MessageSchema)
def logout_user(request):
    logout(request)
    return {"message": "Déconnexion réussie"}

@auth_router.get("/me", auth=django_auth, response=UserOutSchema)
def get_current_user_info(request):
    return request.user
```
- [ ] Enregistrer le router dans `enspm_hub/api.py` :
```python
from core.api.views import auth_router
api.add_router("/auth/", auth_router)
```
- [ ] Tester avec curl/Postman
- [ ] Documenter les endpoints

## Estimation
1.5 jour

## Labels
`epic:core` `priority:P0` `type:backend` `sprint:1`
```

### Issue #7 - API Gestion des utilisateurs (Admin)
```markdown
## Description
Créer les endpoints CRUD pour la gestion des utilisateurs (admin uniquement)

## Objectif
Permettre aux admins de gérer les comptes utilisateurs via API

## Dépendances
- [ ] #5
- [ ] #6

## Critères d'acceptation
- [ ] Endpoint GET `/api/users/` avec filtres et pagination
- [ ] Endpoint GET `/api/users/{id}` fonctionnel
- [ ] Endpoint POST `/api/users/` avec génération de mot de passe
- [ ] Endpoint PATCH `/api/users/{id}` fonctionnel
- [ ] Endpoint DELETE `/api/users/{id}` (soft delete)
- [ ] Vérification des permissions admin
- [ ] Tests d'intégration passent

## Tâches techniques
- [ ] Créer le router utilisateurs dans `core/api/views.py` :
```python
from typing import List
from django.shortcuts import get_object_or_404
from .auth import require_role

users_router = Router(tags=["Utilisateurs"])

@users_router.get("/", auth=django_auth, response=List[UserOutSchema])
@require_role(['admin', 'super_admin'])
def list_users(
    request,
    statut: str = None,
    travailleur: bool = None,
    annee_sortie: int = None,
    limit: int = 50,
    offset: int = 0
):
    queryset = User.objects.filter(est_actif=True)
    
    if statut:
        queryset = queryset.filter(statut=statut)
    if travailleur is not None:
        queryset = queryset.filter(travailleur=travailleur)
    if annee_sortie:
        queryset = queryset.filter(annee_sortie=annee_sortie)
    
    return list(queryset[offset:offset + limit])

@users_router.get("/{user_id}", auth=django_auth, response=UserOutSchema)
def get_user(request, user_id: str):
    user = get_object_or_404(User, id=user_id, est_actif=True)
    return user

@users_router.post("/", auth=django_auth, response={201: UserOutSchema, 400: MessageSchema})
@require_role(['admin', 'super_admin'])
def create_user(request, payload: UserCreateSchema):
    if User.objects.filter(email=payload.email).exists():
        return 400, {"message": "Cet email est déjà utilisé", "success": False}
    
    # Génération mot de passe
    import secrets, string
    password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
    
    user = User.objects.create(
        **payload.dict(),
        password=make_password(password),
        role='user'
    )
    
    # TODO: Envoyer email avec identifiants
    return 201, user

@users_router.patch("/{user_id}", auth=django_auth, response=UserOutSchema)
def update_user(request, user_id: str, payload: UserUpdateSchema):
    user = get_object_or_404(User, id=user_id)
    current_user = get_current_user(request)
    
    if current_user.id != user.id and current_user.role not in ['admin', 'super_admin']:
        raise PermissionError("Vous ne pouvez modifier que votre propre profil")
    
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(user, attr, value)
    
    user.save()
    return user

@users_router.delete("/{user_id}", auth=django_auth, response=MessageSchema)
@require_role(['admin', 'super_admin'])
def deactivate_user(request, user_id: str):
    user = get_object_or_404(User, id=user_id)
    user.est_actif = False
    user.save()
    return {"message": f"L'utilisateur {user.email} a été désactivé"}
```
- [ ] Enregistrer le router : `api.add_router("/users/", users_router)`
- [ ] Créer service de génération de mot de passe
- [ ] Tester tous les endpoints
- [ ] Documenter l'API

## Estimation
2 jours

## Labels
`epic:core` `priority:P0` `type:backend` `sprint:1`
```

### Issue #8 - Service d'envoi d'emails
```markdown
## Description
Configurer Django pour envoyer des emails transactionnels

## Objectif
Pouvoir envoyer des emails de bienvenue et notifications

## Dépendances
- [ ] #1

## Critères d'acceptation
- [ ] Configuration SMTP fonctionnelle
- [ ] Service d'email créé
- [ ] Template email de bienvenue
- [ ] Test d'envoi réussi

## Tâches techniques
- [ ] Configurer `EMAIL_BACKEND` dans `settings.py`
- [ ] Ajouter variables SMTP dans `.env`
- [ ] Créer `core/services/email_service.py`
- [ ] Implémenter `send_welcome_email(user, password)`
- [ ] Créer template `templates/emails/welcome_email.html`
- [ ] Gérer les erreurs d'envoi
- [ ] Tester l'envoi

## Estimation
1 jour

## Labels
`epic:core` `priority:P1` `type:backend` `sprint:1`
```

### Issue #9 - Audit Log automatique
```markdown
## Description
Créer un système de logging automatique des actions utilisateur

## Objectif
Traçabilité complète des modifications

## Dépendances
- [ ] #2

## Critères d'acceptation
- [ ] Modèle AuditLog créé
- [ ] Signals Django configurés
- [ ] Logs créés automatiquement sur INSERT/UPDATE/DELETE
- [ ] Vue admin pour consulter les logs

## Tâches techniques
- [ ] Créer le modèle `AuditLog` :
```python
class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    table_name = models.CharField(max_length=50)
    action = models.CharField(max_length=10, choices=[('INSERT', 'Insert'), ('UPDATE', 'Update'), ('DELETE', 'Delete')])
    ancien_data = models.JSONField(null=True, blank=True)
    nouveau_data = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```
- [ ] Créer signals `post_save` et `post_delete`
- [ ] Capturer IP et User-Agent via middleware
- [ ] Attacher aux modèles sensibles
- [ ] Implémenter rétention (2 ans)
- [ ] Tester

## Estimation
2 jours

## Labels
`epic:core` `priority:P2` `type:backend` `sprint:1`
```

### Issue #10 - Configuration Inertia.js + React + TypeScript
```markdown
## Description
Configurer le frontend avec Inertia, React, Vite et Tailwind

## Objectif
Environnement de développement frontend prêt

## Dépendances
- [ ] #1

## Critères d'acceptation
- [ ] Inertia.js configuré avec Django
- [ ] React + TypeScript fonctionnel
- [ ] Vite configuré avec hot-reload
- [ ] Tailwind CSS intégré
- [ ] Shadcn UI installé
- [ ] Page de test fonctionnelle

## Tâches techniques
- [ ] Installer `inertia-django`
- [ ] Créer `vite.config.ts`
- [ ] Créer `frontend/ts/main.tsx` avec `createInertiaApp`
- [ ] Configurer Tailwind CSS
- [ ] Installer Shadcn UI
- [ ] Créer `templates/inertia_base.html`
- [ ] Tester le rendu d'une page simple
- [ ] Configurer hot-reload

## Estimation
1 jour

## Labels
`epic:core` `priority:P0` `type:frontend` `sprint:1`
```

### Issue #11 - Composant Layout principal
```markdown
## Description
Créer le layout de base de l'application (Header, Sidebar, Footer)

## Objectif
Structure réutilisable pour toutes les pages

## Dépendances
- [ ] #10

## Critères d'acceptation
- [ ] Composant Layout.tsx fonctionnel
- [ ] Header avec navigation
- [ ] Sidebar responsive
- [ ] Footer
- [ ] Design mobile-first
- [ ] Intégration Shadcn UI

## Tâches techniques
- [ ] Créer `frontend/ts/components/layout/Layout.tsx`
- [ ] Créer `Header.tsx` (logo, menu, profil utilisateur)
- [ ] Créer `Sidebar.tsx` avec liens vers modules
- [ ] Créer `Footer.tsx`
- [ ] Implémenter responsive design
- [ ] Intégrer Shadcn UI (Button, Avatar, DropdownMenu)
- [ ] Gérer l'état de connexion
- [ ] Tester sur différentes tailles d'écran

## Estimation
2 jours

## Labels
`epic:core` `priority:P0` `type:frontend` `sprint:1`
```

### Issue #12 - Page de connexion (Login)
```markdown
## Description
Interface de connexion utilisateur avec Inertia.js

## Objectif
Permettre aux utilisateurs de se connecter

## Dépendances
- [ ] #6
- [ ] #10

## Critères d'acceptation
- [ ] Page Login.tsx fonctionnelle
- [ ] Formulaire avec validation
- [ ] Appel API `/api/auth/login`
- [ ] Gestion des erreurs
- [ ] Redirection après succès

## Tâches techniques
- [ ] Créer `frontend/ts/pages/Auth/Login.tsx`
- [ ] Créer formulaire avec Shadcn UI
- [ ] Implémenter validation (React Hook Form + Zod)
- [ ] Gérer soumission avec `Inertia.post('/api/auth/login')`
- [ ] Afficher erreurs de validation
- [ ] Ajouter lien "Mot de passe oublié"
- [ ] Tester le flux complet

## Estimation
1.5 jour

## Labels
`epic:core` `priority:P0` `type:frontend` `sprint:1`
```

### Issue #13 - Page de profil utilisateur
```markdown
## Description
Page d'affichage et édition du profil

## Objectif
Permettre aux utilisateurs de voir et modifier leur profil

## Dépendances
- [ ] #7
- [ ] #11

## Critères d'acceptation
- [ ] Page Profile/Show.tsx affiche toutes les infos
- [ ] Formulaire d'édition modal
- [ ] Upload de photo de profil
- [ ] Validation côté client et serveur
- [ ] Mise à jour réussie

## Tâches techniques
- [ ] Créer `frontend/ts/pages/Profile/Show.tsx`
- [ ] Afficher toutes les informations du profil
- [ ] Créer modal d'édition
- [ ] Gérer l'upload de photo (API)
- [ ] Implémenter validation
- [ ] Tester la mise à jour

## Estimation
2 jours

## Labels
`epic:core` `priority:P1` `type:frontend` `sprint:1`
```

---

## 🏗️ EPIC 2 - MODÈLES MÉTIER

### Issue #14 - Modèles de référence (Domaine, Année)
```markdown
## Description
Créer les tables de référence dynamiques pour domaines et années

## Objectif
Fournir des listes pour les dropdowns

## Dépendances
- [ ] #1

## Critères d'acceptation
- [ ] Modèles DomaineReference et AnneeReference créés
- [ ] Migrations appliquées
- [ ] Commande `populate_references` fonctionnelle
- [ ] Job cron pour nouvelles années

## Tâches techniques
- [ ] Créer modèles DomaineReference et AnneeReference
- [ ] Créer migrations
- [ ] Créer commande Django `populate_references`
- [ ] Ajouter domaines initiaux
- [ ] Générer années 2000 à aujourd'hui + 5 ans
- [ ] Créer job Django Cron
- [ ] Tester

## Estimation
1 jour

## Labels
`epic:models` `priority:P1` `type:backend` `sprint:2`
```

### Issue #15 - Modèle Organisation
```markdown
## Description
Créer le modèle pour les entreprises et partenaires

## Objectif
Gérer les organisations externes

## Dépendances
- [ ] #1

## Critères d'acceptation
- [ ] Modèle Organisation créé avec tous les champs
- [ ] ENUM définis
- [ ] Index créés
- [ ] Full-text search configuré
- [ ] Tests de création passent

## Tâches techniques
- [ ] Créer app `organizations`
- [ ] Créer modèle Organisation
- [ ] Définir ENUM (type_organisation, statut)
- [ ] Créer migrations
- [ ] Ajouter index (statut, secteur, ville)
- [ ] Créer index full-text
- [ ] Tester

## Estimation
1 jour

## Labels
`epic:models` `priority:P1` `type:backend` `sprint:2`
```

### Issue #16 - Modèle ContactOrganisation
```markdown
## Description
Table de liaison entre Utilisateur et Organisation

## Objectif
Gérer les contacts d'une organisation

## Dépendances
- [ ] #2
- [ ] #15

## Critères d'acceptation
- [ ] Modèle ContactOrganisation créé
- [ ] Contrainte "un seul contact principal par org" implémentée
- [ ] Tests de création/modification passent

## Tâches techniques
- [ ] Créer modèle ContactOrganisation
- [ ] Définir ENUM role_contact
- [ ] Implémenter contrainte unicitécontact principal
- [ ] Créer migrations
- [ ] Ajouter index
- [ ] Tester

## Estimation
1 jour

## Labels
`epic:models` `priority:P1` `type:backend` `sprint:2`
```

### Issue #17 - Modèle Stage
```markdown
## Description
Créer le modèle pour les offres de stage

## Objectif
Gérer les offres de stage

## Dépendances
- [ ] #2
- [ ] #15

## Critères d'acceptation
- [ ] Modèle Stage créé
- [ ] Contrainte CHECK (date_fin > date_debut)
- [ ] Signal pré-remplissage contacts
- [ ] Full-text search configuré
- [ ] Tests passent

## Tâches techniques
- [ ] Créer app `opportunities`
- [ ] Créer modèle Stage
- [ ] Définir ENUM
- [ ] Ajouter contrainte dates
- [ ] Créer signal `pre_save`
- [ ] Créer migrations
- [ ] Ajouter index + full-text
- [ ] Tester

## Estimation
1.5 jour

## Labels
`epic:models` `priority:P0` `type:backend` `sprint:2`
```

### Issue #18 - Modèle Formation
```markdown
## Description
Créer le modèle pour les offres de formation

## Objectif
Gérer les offres de formation

## Dépendances
- [ ] #2
- [ ] #15

## Critères d'acceptation
- [ ] Modèle Formation créé
- [ ] Contrainte (si payante, prix requis)
- [ ] Signal pré-remplissage
- [ ] Tests passent

## Tâches techniques
- [ ] Créer modèle Formation
- [ ] Définir ENUM type_formation
- [ ] Ajouter contrainte CHECK prix
- [ ] Créer signal `pre_save`
- [ ] Créer migrations
- [ ] Ajouter index + full-text
- [ ] Tester

## Estimation
1.5 jour

## Labels
`epic:models` `priority:P0` `type:backend` `sprint:2`
```

### Issue #19 - Modèle Emploi
```markdown
## Description
Créer le modèle pour les offres d'emploi

## Objectif
Gérer les offres d'emploi

## Dépendances
- [ ] #2
- [ ] #15

## Critères d'acceptation
- [ ] Modèle Emploi créé
- [ ] Tous les champs requis
- [ ] Tests passent

## Tâches techniques
- [ ] Créer modèle Emploi (similaire à Stage)
- [ ] Définir ENUM type_emploi
- [ ] Gérer date_expiration
- [ ] Créer migrations
- [ ] Ajouter index
- [ ] Tester

## Estimation
1.5 jour

## Labels
`epic:models` `priority:P0` `type:backend` `sprint:2`
```

### Issue #20 - Modèle ValidationFormation
```markdown
## Description
Système de validation des formations par admin

## Objectif
Traçabilité des validations

## Dépendances
- [ ] #18

## Critères d'acceptation
- [ ] Modèle ValidationFormation créé
- [ ] Signal mise à jour `est_valide`
- [ ] Tests workflow validation

## Tâches techniques
- [ ] Créer modèle ValidationFormation
- [ ] Ajouter contrainte UNIQUE
- [ ] Créer signal `post_save`
- [ ] Créer migrations
- [ ] Tester workflow

## Estimation
1 jour

## Labels
`epic:models` `priority:P1` `type:backend` `sprint:2`
```

---

## 🏗️ EPIC 3 - API CRUD STAGES

### Issue #25 - API CRUD Stage - Liste & Détail
```markdown
## Description
Créer les endpoints Django Ninja de lecture des stages

## Objectif
Permettre de lister et voir le détail d'un stage

## Dépendances
- [ ] #17
- [ ] #3

## Critères d'acceptation
- [ ] GET `/api/stages/` avec pagination fonctionnel
- [ ] GET `/api/stages/{uuid}/` fonctionnel
- [ ] Filtres (statut, lieu, type, dates) implémentés
- [ ] RLS appliqué
- [ ] Documentation Swagger à jour

## Tâches techniques
- [ ] Créer `opportunities/api/__init__.py`
- [ ] Créer `opportunities/api/schemas.py` avec schémas Pydantic :
```python
class StageOutSchema(BaseModel):
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
    createur_id: UUID
    createur_nom: str
    organisation_id: Optional[UUID]
    organisation_nom: Optional[str]
    
    class Config:
        from_attributes = True
```
- [ ] Créer `opportunities/api/views.py` avec router :
```python
from ninja import Router, Query
from ninja.pagination import paginate, PageNumberPagination
from typing import List

stages_router = Router(tags=["Stages"])

@stages_router.get("/", auth=django_auth, response=List[StageOutSchema])
@paginate(PageNumberPagination, page_size=20)
def list_stages(
    request,
    statut: str = Query(None),
    lieu: str = Query(None),
    type_stage: str = Query(None),
    q: str = Query(None)
):
    queryset = Stage.objects.select_related('createur', 'organisation').all()
    
    if statut:
        queryset = queryset.filter(statut=statut)
    else:
        queryset = queryset.filter(statut='active')
    
    if lieu:
        queryset = queryset.filter(lieu__icontains=lieu)
    if type_stage:
        queryset = queryset.filter(type_stage=type_stage)
    if q:
        queryset = queryset.filter(Q(titre__icontains=q) | Q(description__icontains=q))
    
    # Ajouter champs calculés
    stages = []
    for stage in queryset:
        stage_dict = stage.__dict__.copy()
        stage_dict['createur_nom'] = stage.createur.nom_complet
        stage_dict['organisation_nom'] = stage.organisation.nom_organisation if stage.organisation else None
        stages.append(Stage(**stage_dict))
    
    return stages

@stages_router.get("/{stage_id}", auth=django_auth, response=StageOutSchema)
def get_stage(request, stage_id: UUID):
    stage = get_object_or_404(Stage.objects.select_related('createur', 'organisation'), id=stage_id)
    stage.createur_nom = stage.createur.nom_complet
    stage.organisation_nom = stage.organisation.nom_organisation if stage.organisation else None
    return stage
```
- [ ] Enregistrer router dans `enspm_hub/api.py` : `api.add_router("/stages/", stages_router)`
- [ ] Tester avec Postman/curl
- [ ] Vérifier documentation Swagger

## Estimation
1 jour

## Labels
`epic:stages` `priority:P0` `type:backend` `sprint:3`
```

### Issue #26 - API CRUD Stage - Création
```markdown
## Description
Endpoint pour créer une offre de stage avec Django Ninja

## Objectif
Permettre aux utilisateurs d'ajouter des stages

## Dépendances
- [ ] #17
- [ ] #25

## Critères d'acceptation
- [ ] POST `/api/stages/` fonctionnel
- [ ] Validation Pydantic active
- [ ] Pré-remplissage contacts
- [ ] Statut 201 retourné
- [ ] Tests d'intégration passent

## Tâches techniques
- [ ] Créer schéma `StageCreateSchema` dans `schemas.py` :
```python
class StageCreateSchema(BaseModel):
    titre: str = Field(..., min_length=5, max_length=255)
    lieu: str = Field(..., max_length=255)
    nom_structure: str = Field(..., max_length=255)
    description: Optional[str] = None
    type_stage: Optional[str] = Field(None, pattern="^(ouvrier|academique|professionnel)$")
    email_contact: Optional[str] = None
    telephone_contact: Optional[str] = None
    lien_offre: Optional[str] = None
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    organisation_id: Optional[UUID] = None
    
    @validator('date_fin')
    def validate_dates(cls, v, values):
        if v and values.get('date_debut') and v <= values['date_debut']:
            raise ValueError("La date de fin doit être postérieure à la date de début")
        return v
```
- [ ] Ajouter endpoint dans `views.py` :
```python
@stages_router.post("/", auth=django_auth, response={201: StageOutSchema, 400: MessageSchema})
def create_stage(request, payload: StageCreateSchema):
    current_user = get_current_user(request)
    
    # Pré-remplir contacts
    if not payload.email_contact:
        payload.email_contact = current_user.email
    if not payload.telephone_contact and current_user.telephone:
        payload.telephone_contact = current_user.telephone
    
    stage = Stage.objects.create(
        **payload.dict(),
        createur=current_user,
        statut='active'
    )
    
    stage.createur_nom = current_user.nom_complet
    stage.organisation_nom = stage.organisation.nom_organisation if stage.organisation else None
    
    return 201, stage
```
- [ ] Tester création
- [ ] Tester validation erreurs
- [ ] Documenter

## Estimation
1 jour

## Labels
`epic:stages` `priority:P0` `type:backend` `sprint:3`
```

### Issue #27 - API CRUD Stage - Mise à jour & Suppression
```markdown
## Description
Endpoints pour modifier et supprimer un stage

## Objectif
Permettre au créateur de gérer ses stages

## Dépendances
- [ ] #17
- [ ] #25

## Critères d'acceptation
- [ ] PATCH `/api/stages/{uuid}/` fonctionnel
- [ ] DELETE `/api/stages/{uuid}/` fonctionnel
- [ ] Vérification permissions (créateur ou admin)
- [ ] Tests passent

## Tâches techniques
- [ ] Créer schéma `StageUpdateSchema`
- [ ] Ajouter endpoint PATCH
- [ ] Ajouter endpoint DELETE
- [ ] Vérifier permissions
- [ ] Tester

## Estimation
1 jour

## Labels
`epic:stages` `priority:P0` `type:backend` `sprint:3`
```
## 🏗️ EPIC 3 - API CRUD STAGES (suite)

### Issue #28 - Recherche multi-critères Stages
```markdown
## Description
Endpoint de recherche avancée avec full-text search

## Objectif
Permettre de rechercher par titre, lieu, type, dates

## Dépendances
- [ ] #25

## Critères d'acceptation
- [ ] GET `/api/stages/search/` fonctionnel
- [ ] Full-text search PostgreSQL implémenté
- [ ] Filtres combinables
- [ ] Tri par pertinence
- [ ] Pagination fonctionnelle

## Tâches techniques
- [ ] Ajouter endpoint search dans `views.py` :
```python
@stages_router.get("/search/", auth=django_auth, response=List[StageOutSchema])
@paginate(PageNumberPagination, page_size=20)
def search_stages(
    request,
    q: str = Query(None, description="Recherche textuelle"),
    lieu: str = Query(None),
    type_stage: str = Query(None),
    date_debut_min: date = Query(None),
    date_debut_max: date = Query(None)
):
    queryset = Stage.objects.select_related('createur', 'organisation').filter(statut='active')
    
    if q:
        # Full-text search PostgreSQL
        queryset = queryset.filter(
            Q(titre__icontains=q) | Q(description__icontains=q) | Q(nom_structure__icontains=q)
        )
    
    if lieu:
        queryset = queryset.filter(lieu__icontains=lieu)
    if type_stage:
        queryset = queryset.filter(type_stage=type_stage)
    if date_debut_min:
        queryset = queryset.filter(date_debut__gte=date_debut_min)
    if date_debut_max:
        queryset = queryset.filter(date_debut__lte=date_debut_max)
    
    queryset = queryset.order_by('-created_at')
    
    return queryset
```
- [ ] Optimiser avec index full-text
- [ ] Tester différentes combinaisons
- [ ] Documenter

## Estimation
1 jour

## Labels
`epic:stages` `priority:P1` `type:backend` `sprint:3`
```

### Issue #29 - Page Liste des Stages (Frontend)
```markdown
## Description
Interface pour afficher toutes les offres de stage

## Objectif
Permettre aux utilisateurs de parcourir les stages

## Dépendances
- [ ] #25
- [ ] #11

## Critères d'acceptation
- [ ] Page Index.tsx affiche la liste des stages
- [ ] Composant StageCard fonctionnel
- [ ] Pagination côté serveur
- [ ] Champ de recherche
- [ ] Filtres (lieu, type)
- [ ] Design responsive

## Tâches techniques
- [ ] Créer `frontend/ts/pages/Stages/Index.tsx` :
```typescript
import { router } from '@inertiajs/react'
import { useState } from 'react'
import Layout from '@/components/layout/Layout'
import StageCard from '@/components/StageCard'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'

interface Stage {
  id: string
  titre: string
  lieu: string
  nom_structure: string
  type_stage: string
  created_at: string
  createur_nom: string
}

interface Props {
  stages: {
    items: Stage[]
    page: number
    total: number
  }
}

export default function StagesIndex({ stages }: Props) {
  const [search, setSearch] = useState('')
  const [filters, setFilters] = useState({ lieu: '', type_stage: '' })
  
  const handleSearch = () => {
    router.get('/stages', { q: search, ...filters }, { preserveState: true })
  }
  
  return (
    <Layout>
      <div className="container mx-auto py-8">
        <h1 className="text-3xl font-bold mb-6">Offres de Stage</h1>
        
        {/* Barre de recherche et filtres */}
        <div className="flex gap-4 mb-6">
          <Input
            placeholder="Rechercher..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
          <Select
            value={filters.lieu}
            onValueChange={(value) => setFilters({ ...filters, lieu: value })}
          >
            <option value="">Tous les lieux</option>
            <option value="Douala">Douala</option>
            <option value="Yaoundé">Yaoundé</option>
          </Select>
          <Select
            value={filters.type_stage}
            onValueChange={(value) => setFilters({ ...filters, type_stage: value })}
          >
            <option value="">Tous les types</option>
            <option value="ouvrier">Ouvrier</option>
            <option value="academique">Académique</option>
            <option value="professionnel">Professionnel</option>
          </Select>
        </div>
        
        {/* Liste des stages */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {stages.items.map(stage => (
            <StageCard key={stage.id} stage={stage} />
          ))}
        </div>
        
        {/* Pagination */}
        {/* TODO: Implémenter pagination */}
      </div>
    </Layout>
  )
}
```
- [ ] Créer `frontend/ts/components/StageCard.tsx` avec Shadcn Card
- [ ] Implémenter pagination
- [ ] Ajouter animations
- [ ] Tester responsive

## Estimation
2 jours

## Labels
`epic:stages` `priority:P0` `type:frontend` `sprint:3`
```

### Issue #30 - Page Détail d'un Stage (Frontend)
```markdown
## Description
Vue détaillée d'une offre de stage

## Objectif
Afficher toutes les informations d'un stage

## Dépendances
- [ ] #25
- [ ] #11

## Critères d'acceptation
- [ ] Page Show.tsx affiche tous les détails
- [ ] Boutons "Postuler" et "Contacter"
- [ ] Boutons "Modifier" et "Supprimer" si créateur/admin
- [ ] Infos organisation affichées
- [ ] Design professionnel

## Tâches techniques
- [ ] Créer `frontend/ts/pages/Stages/Show.tsx`
- [ ] Afficher tous les champs
- [ ] Gérer les permissions (boutons conditionnels)
- [ ] Ajouter modal de confirmation suppression
- [ ] Tester

## Estimation
1.5 jour

## Labels
`epic:stages` `priority:P0` `type:frontend` `sprint:3`
```

### Issue #31 - Formulaire Création de Stage (Frontend)
```markdown
## Description
Interface pour ajouter une offre de stage

## Objectif
Permettre aux utilisateurs de publier des stages

## Dépendances
- [ ] #26
- [ ] #11

## Critères d'acceptation
- [ ] Page Create.tsx avec formulaire complet
- [ ] Validation React Hook Form + Zod
- [ ] Pré-remplissage email/téléphone
- [ ] Gestion erreurs API
- [ ] Redirection après succès

## Tâches techniques
- [ ] Créer `frontend/ts/pages/Stages/Create.tsx`
- [ ] Utiliser Shadcn Form + React Hook Form
- [ ] Créer schéma Zod :
```typescript
import { z } from 'zod'

const stageSchema = z.object({
  titre: z.string().min(5, 'Minimum 5 caractères').max(255),
  lieu: z.string().min(1, 'Requis'),
  nom_structure: z.string().min(1, 'Requis'),
  description: z.string().optional(),
  type_stage: z.enum(['ouvrier', 'academique', 'professionnel']).optional(),
  email_contact: z.string().email().optional(),
  telephone_contact: z.string().optional(),
  lien_offre: z.string().url().optional(),
  date_debut: z.date().optional(),
  date_fin: z.date().optional(),
}).refine(data => {
  if (data.date_debut && data.date_fin) {
    return data.date_fin > data.date_debut
  }
  return true
}, {
  message: "La date de fin doit être postérieure à la date de début",
  path: ["date_fin"]
})
```
- [ ] Implémenter soumission avec Inertia
- [ ] Gérer erreurs validation
- [ ] Tester création complète

## Estimation
2 jours

## Labels
`epic:stages` `priority:P0` `type:frontend` `sprint:3`
```

### Issue #32 - Formulaire Modification de Stage (Frontend)
```markdown
## Description
Interface pour modifier une offre existante

## Objectif
Permettre au créateur de mettre à jour son stage

## Dépendances
- [ ] #27
- [ ] #30

## Critères d'acceptation
- [ ] Page Edit.tsx fonctionnelle
- [ ] Formulaire pré-rempli
- [ ] Validation identique à création
- [ ] Mise à jour réussie

## Tâches techniques
- [ ] Créer `frontend/ts/pages/Stages/Edit.tsx`
- [ ] Réutiliser composant formulaire de Create
- [ ] Pré-remplir champs
- [ ] Gérer soumission PATCH
- [ ] Tester

## Estimation
1.5 jour

## Labels
`epic:stages` `priority:P1` `type:frontend` `sprint:3`
```

---

## 🏗️ EPIC 4 - API CRUD FORMATIONS

### Issue #33 - API CRUD Formation - Liste & Détail
```markdown
## Description
Créer les endpoints Django Ninja de lecture des formations

## Objectif
Permettre de lister et voir le détail d'une formation

## Dépendances
- [ ] #18
- [ ] #3

## Critères d'acceptation
- [ ] GET `/api/formations/` fonctionnel
- [ ] GET `/api/formations/{uuid}/` fonctionnel
- [ ] Filtres implémentés
- [ ] RLS appliqué (ne montrer que validées sauf pour créateur/admin)

## Tâches techniques
- [ ] Créer `opportunities/api/schemas.py` avec `FormationOutSchema`
- [ ] Créer router formations dans `opportunities/api/views.py`
- [ ] Implémenter list_formations avec pagination
- [ ] Implémenter get_formation
- [ ] Enregistrer router dans api.py
- [ ] Tester

## Estimation
1 jour

## Labels
`epic:formations` `priority:P0` `type:backend` `sprint:4`
```

### Issue #34 - API CRUD Formation - Création
```markdown
## Description
Endpoint pour créer une offre de formation

## Objectif
Permettre d'ajouter des formations (validation admin requise)

## Dépendances
- [ ] #18
- [ ] #33

## Critères d'acceptation
- [ ] POST `/api/formations/` fonctionnel
- [ ] Formation créée avec `est_valide=False` par défaut
- [ ] Validation prix si `est_payante=True`
- [ ] Notification admin envoyée

## Tâches techniques
- [ ] Créer `FormationCreateSchema` :
```python
class FormationCreateSchema(BaseModel):
    titre: str = Field(..., min_length=5, max_length=255)
    lieu: Optional[str] = Field(None, max_length=255)
    nom_structure: Optional[str] = Field(None, max_length=255)
    description: str
    type_formation: str = Field(..., pattern="^(presentiel|en_ligne|hybride)$")
    est_payante: bool = False
    prix: Optional[Decimal] = Field(None, ge=0)
    devise: str = "FCFA"
    email_contact: Optional[str] = None
    telephone_contact: Optional[str] = None
    lien_formation: str
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    organisation_id: Optional[UUID] = None
    
    @validator('prix')
    def validate_prix(cls, v, values):
        if values.get('est_payante') and v is None:
            raise ValueError("Le prix est requis pour une formation payante")
        return v
```
- [ ] Implémenter endpoint create_formation
- [ ] Mettre `est_valide=False` par défaut
- [ ] Envoyer notification aux admins
- [ ] Tester

## Estimation
1 jour

## Labels
`epic:formations` `priority:P0` `type:backend` `sprint:4`
```

### Issue #35 - API CRUD Formation - Mise à jour & Suppression
```markdown
## Description
Endpoints pour modifier et supprimer une formation

## Objectif
Permettre au créateur de gérer ses formations

## Dépendances
- [ ] #18
- [ ] #33

## Critères d'acceptation
- [ ] PATCH `/api/formations/{uuid}/` fonctionnel
- [ ] DELETE `/api/formations/{uuid}/` fonctionnel
- [ ] Permissions vérifiées

## Tâches techniques
- [ ] Créer `FormationUpdateSchema`
- [ ] Implémenter update_formation
- [ ] Implémenter delete_formation
- [ ] Tester

## Estimation
1 jour

## Labels
`epic:formations` `priority:P0` `type:backend` `sprint:4`
```

### Issue #36 - Recherche multi-critères Formations
```markdown
## Description
Endpoint de recherche avancée formations

## Objectif
Recherche par titre, type, prix, dates

## Dépendances
- [ ] #33

## Critères d'acceptation
- [ ] GET `/api/formations/search/` fonctionnel
- [ ] Filtres combinables
- [ ] Tri par pertinence

## Tâches techniques
- [ ] Implémenter endpoint search
- [ ] Ajouter filtres (type, est_payante, prix_max, dates)
- [ ] Tester

## Estimation
1 jour

## Labels
`epic:formations` `priority:P1` `type:backend` `sprint:4`
```

### Issue #37 - Page Liste des Formations (Frontend)
```markdown
## Description
Interface pour afficher toutes les offres de formation

## Objectif
Permettre de parcourir les formations

## Dépendances
- [ ] #33
- [ ] #11

## Critères d'acceptation
- [ ] Page Formations/Index.tsx fonctionnelle
- [ ] Composant FormationCard
- [ ] Filtres (type, payante/gratuite)
- [ ] Badge "En attente de validation" si non validée

## Tâches techniques
- [ ] Créer Formations/Index.tsx
- [ ] Créer FormationCard.tsx
- [ ] Implémenter filtres
- [ ] Ajouter badges validation
- [ ] Tester

## Estimation
2 jours

## Labels
`epic:formations` `priority:P0` `type:frontend` `sprint:4`
```

### Issue #38 - Page Détail Formation (Frontend)
```markdown
## Description
Vue détaillée d'une formation

## Objectif
Afficher toutes les informations

## Dépendances
- [ ] #33
- [ ] #11

## Critères d'acceptation
- [ ] Page Show.tsx affiche détails
- [ ] Affichage prix si payante
- [ ] Statut validation visible

## Tâches techniques
- [ ] Créer Formations/Show.tsx
- [ ] Afficher tous les champs
- [ ] Gérer affichage conditionnel prix
- [ ] Tester

## Estimation
1.5 jour

## Labels
`epic:formations` `priority:P0` `type:frontend` `sprint:4`
```

### Issue #39 - Formulaire Création Formation (Frontend)
```markdown
## Description
Interface pour ajouter une formation

## Objectif
Permettre de publier des formations

## Dépendances
- [ ] #34
- [ ] #11

## Critères d'acceptation
- [ ] Page Create.tsx fonctionnelle
- [ ] Checkbox "Formation payante"
- [ ] Champs prix/devise apparaissent si payante
- [ ] Message "En attente de validation" après création

## Tâches techniques
- [ ] Créer Formations/Create.tsx
- [ ] Créer schéma Zod avec validation prix
- [ ] Gérer affichage conditionnel prix
- [ ] Implémenter soumission
- [ ] Tester

## Estimation
2 jours

## Labels
`epic:formations` `priority:P0` `type:frontend` `sprint:4`
```

### Issue #40 - Formulaire Modification Formation (Frontend)
```markdown
## Description
Interface pour modifier une formation

## Objectif
Permettre mise à jour

## Dépendances
- [ ] #35
- [ ] #38

## Critères d'acceptation
- [ ] Page Edit.tsx fonctionnelle
- [ ] Formulaire pré-rempli
- [ ] Mise à jour réussie

## Tâches techniques
- [ ] Créer Formations/Edit.tsx
- [ ] Réutiliser formulaire Create
- [ ] Pré-remplir
- [ ] Tester

## Estimation
1.5 jour

## Labels
`epic:formations` `priority:P1` `type:frontend` `sprint:4`
```

### Issue #41 - API Validation des Formations
```markdown
## Description
Endpoint pour valider/invalider une formation (admin uniquement)

## Objectif
Contrôler les formations publiées

## Dépendances
- [ ] #20
- [ ] #34

## Critères d'acceptation
- [ ] POST `/api/formations/{uuid}/validate/` fonctionnel
- [ ] Entrée ValidationFormation créée
- [ ] Email envoyé au créateur
- [ ] Permission admin vérifiée

## Tâches techniques
- [ ] Créer endpoint validate_formation :
```python
@formations_router.post("/{formation_id}/validate/", auth=django_auth, response=MessageSchema)
@require_role(['admin', 'super_admin'])
def validate_formation(request, formation_id: UUID, est_approuve: bool, commentaire: str = None):
    formation = get_object_or_404(Formation, id=formation_id)
    
    ValidationFormation.objects.create(
        formation=formation,
        validateur=request.user,
        est_approuve=est_approuve,
        commentaire=commentaire
    )
    
    formation.est_valide = est_approuve
    formation.save()
    
    # Envoyer email au créateur
    if est_approuve:
        send_formation_approved_email(formation.createur, formation)
    else:
        send_formation_rejected_email(formation.createur, formation, commentaire)
    
    return {"message": f"Formation {'approuvée' if est_approuve else 'rejetée'}"}
```
- [ ] Implémenter services email
- [ ] Tester workflow complet

## Estimation
1 jour

## Labels
`epic:formations` `priority:P1` `type:backend` `sprint:4`
```

### Issue #42 - Interface Admin Validation Formations (Frontend)
```markdown
## Description
Page admin pour valider les formations en attente

## Objectif
Permettre aux admins de gérer les validations

## Dépendances
- [ ] #41

## Critères d'acceptation
- [ ] Page Admin/FormationsEnAttente.tsx fonctionnelle
- [ ] Liste des formations `est_valide=False`
- [ ] Modal validation avec commentaire
- [ ] Boutons Approuver/Rejeter

## Tâches techniques
- [ ] Créer Admin/FormationsEnAttente.tsx
- [ ] Créer ValidationModal.tsx
- [ ] Implémenter appels API validation
- [ ] Retirer de liste après validation
- [ ] Tester workflow

## Estimation
2 jours

## Labels
`epic:formations` `priority:P1` `type:frontend` `sprint:4`
```

---

## 🏗️ EPIC 5 - API CRUD EMPLOIS

### Issue #43-50 - CRUD Emplois (Backend & Frontend)
```markdown
## Description
Reproduire exactement les issues #25 à #32 pour les Emplois

## Objectif
Fonctionnalités complètes de gestion des offres d'emploi

## Dépendances
- [ ] #19 (Modèle Emploi)

## Issues à créer
- [ ] #43: API Liste & Détail Emplois
- [ ] #44: API Création Emploi
- [ ] #45: API Mise à jour & Suppression Emplois
- [ ] #46: Recherche multi-critères Emplois
- [ ] #47: Page Liste Emplois (Frontend)
- [ ] #48: Page Détail Emploi (Frontend)
- [ ] #49: Formulaire Création Emploi (Frontend)
- [ ] #50: Formulaire Modification Emploi (Frontend)

## Particularités
- Champ `type_emploi` au lieu de `type_stage`
- Gestion `date_expiration` au lieu de `date_fin`
- Pas de validation admin (publication directe)

## Estimation totale
8 jours

## Labels
`epic:emplois` `priority:P0` `type:backend+frontend` `sprint:5`
```

### Issue #51 - Job d'expiration automatique des offres
```markdown
## Description
Créer un job pour marquer les offres expirées

## Objectif
Mettre à jour automatiquement le statut

## Dépendances
- [ ] #17 (Stage)
- [ ] #19 (Emploi)

## Critères d'acceptation
- [ ] Job Django Cron créé
- [ ] Stages expirés marqués `statut='expiree'`
- [ ] Emplois expirés marqués `statut='expiree'`
- [ ] Job exécuté quotidiennement
- [ ] Logging implémenté

## Tâches techniques
- [ ] Installer `django-crontab` ou `django-q`
- [ ] Créer `opportunities/cron/expire_old_offers.py` :
```python
from django.utils import timezone
from opportunities.models import Stage, Emploi

def expire_old_offers():
    today = timezone.now().date()
    
    # Expirer les stages
    stages_expired = Stage.objects.filter(
        date_fin__lt=today,
        statut='active'
    ).update(statut='expiree')
    
    # Expirer les emplois
    emplois_expired = Emploi.objects.filter(
        date_expiration__lt=today,
        statut='active'
    ).update(statut='expiree')
    
    print(f"Expiré: {stages_expired} stages, {emplois_expired} emplois")
```
- [ ] Configurer dans settings.py :
```python
CRONJOBS = [
    ('0 2 * * *', 'opportunities.cron.expire_old_offers.expire_old_offers'),  # 2h du matin
]
```
- [ ] Tester manuellement
- [ ] Ajouter logging

## Estimation
1 jour

## Labels
`epic:emplois` `priority:P2` `type:backend` `sprint:5`
```

---

## 🏗️ EPIC 6 - ORGANISATIONS

### Issue #52 - API CRUD Organisation - Liste & Détail
```markdown
## Description
Endpoints de lecture des organisations

## Objectif
Lister et afficher les organisations partenaires

## Dépendances
- [ ] #15

## Critères d'acceptation
- [ ] GET `/api/organisations/` fonctionnel
- [ ] GET `/api/organisations/{uuid}/` fonctionnel
- [ ] Filtres (statut, secteur, ville, type)
- [ ] RLS appliqué

## Tâches techniques
- [ ] Créer `organizations/api/schemas.py`
- [ ] Créer `organizations/api/views.py` avec router
- [ ] Implémenter list_organisations
- [ ] Implémenter get_organisation
- [ ] Enregistrer router
- [ ] Tester

## Estimation
1 jour

## Labels
`epic:organisations` `priority:P1` `type:backend` `sprint:6`
```

### Issue #53 - API CRUD Organisation - Création
```markdown
## Description
Endpoint pour créer une organisation

## Objectif
Permettre d'ajouter des partenaires

## Dépendances
- [ ] #15

## Critères d'acceptation
- [ ] POST `/api/organisations/` fonctionnel
- [ ] Organisation créée avec `statut='en_attente'`
- [ ] Notification admins envoyée

## Tâches techniques
- [ ] Créer OrganisationCreateSchema
- [ ] Implémenter endpoint
- [ ] Notifier admins
- [ ] Tester

## Estimation
1 jour

## Labels
`epic:organisations` `priority:P1` `type:backend` `sprint:6`
```

### Issue #54 - API CRUD Organisation - Mise à jour & Suppression
```markdown
## Description
Endpoints pour gérer les organisations

## Objectif
Modifier ou supprimer une organisation

## Dépendances
- [ ] #15

## Critères d'acceptation
- [ ] PATCH `/api/organisations/{uuid}/` fonctionnel
- [ ] DELETE `/api/organisations/{uuid}/` fonctionnel

## Tâches techniques
- [ ] Créer OrganisationUpdateSchema
- [ ] Implémenter update
- [ ] Implémenter delete (soft delete)
- [ ] Tester

## Estimation
1 jour

## Labels
`epic:organisations` `priority:P1` `type:backend` `sprint:6`
```

### Issue #55 - API Validation Organisation (Admin)
```markdown
## Description
Endpoint pour activer/désactiver une organisation

## Objectif
Contrôler les partenariats

## Dépendances
- [ ] #15

## Critères d'acceptation
- [ ] POST `/api/organisations/{uuid}/change-statut/` fonctionnel
- [ ] Statuts (active/inactive/en_attente) gérés
- [ ] Notification contacts envoyée

## Tâches techniques
- [ ] Créer endpoint change_statut
- [ ] Implémenter notification email
- [ ] Tester

## Estimation
0.5 jour

## Labels
`epic:organisations` `priority:P1` `type:backend` `sprint:6`
```

### Issue #56 - API Gestion des Contacts Organisation
```markdown
## Description
Endpoints pour lier des utilisateurs à des organisations

## Objectif
Gérer les contacts d'une organisation

## Dépendances
- [ ] #16

## Critères d'acceptation
- [ ] GET `/api/organisations/{uuid}/contacts/` fonctionnel
- [ ] POST `/api/organisations/{uuid}/contacts/` fonctionnel
- [ ] PATCH `/api/contacts-organisation/{uuid}/` fonctionnel
- [ ] DELETE `/api/contacts-organisation/{uuid}/` fonctionnel
- [ ] Contrainte contact principal respectée

## Tâches techniques
- [ ] Créer ContactOrganisationSchema
- [ ] Implémenter CRUD contacts
- [ ] Vérifier contrainte unique contact principal
- [ ] Tester

## Estimation
1.5 jour

## Labels
`epic:organisations` `priority:P1` `type:backend` `sprint:6`
```

### Issue #57 - Pages CRUD Organisations (Frontend)
```markdown
## Description
Interfaces complètes pour gérer les organisations

## Objectif
Permettre la gestion des partenaires

## Dépendances
- [ ] #52-#56

## Critères d'acceptation
- [ ] Page Organisations/Index.tsx fonctionnelle
- [ ] Page Show.tsx fonctionnelle
- [ ] Page Create.tsx fonctionnelle
- [ ] Page Edit.tsx fonctionnelle
- [ ] Composant OrganisationCard créé

## Tâches techniques
- [ ] Créer toutes les pages
- [ ] Créer OrganisationCard.tsx
- [ ] Implémenter formulaires
- [ ] Tester workflow complet

## Estimation
4 jours

## Labels
`epic:organisations` `priority:P1` `type:frontend` `sprint:6`
```

### Issue #58 - Interface Admin Gestion des Contacts (Frontend)
```markdown
## Description
Page pour gérer les contacts d'une organisation

## Objectif
Lier des utilisateurs aux organisations

## Dépendances
- [ ] #56
- [ ] #57

## Critères d'acceptation
- [ ] Page ManageContacts.tsx fonctionnelle
- [ ] Liste contacts existants
- [ ] Formulaire ajout contact
- [ ] Marquer contact principal
- [ ] Gérer dates début/fin

## Tâches techniques
- [ ] Créer Organisations/ManageContacts.tsx
- [ ] Formulaire recherche utilisateur
- [ ] Implémenter ajout/modification/suppression
- [ ] Tester

## Estimation
2 jours

## Labels
`epic:organisations` `priority:P2` `type:frontend` `sprint:6`
```
## 🏗️ EPIC 7 - SYSTÈME DE CHAT

### Issue #21 - Modèle Groupe (Backend)
```markdown
## Description
Créer le modèle pour les groupes de chat

## Objectif
Gérer les espaces de discussion

## Dépendances
- [ ] #2

## Critères d'acceptation
- [ ] Modèle Groupe créé avec tous les champs
- [ ] ENUM type_groupe définis
- [ ] Migrations appliquées
- [ ] Tests passent

## Tâches techniques
- [ ] Créer app `chat`
- [ ] Créer modèle Groupe :
```python
class Groupe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    createur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='groupes_crees')
    nom_groupe = models.CharField(max_length=100, unique=True)
    photo_groupe_url = models.TextField(null=True, blank=True)
    description = models.TextField()
    est_valide = models.BooleanField(default=False)
    type_groupe = models.CharField(max_length=20, choices=TYPE_GROUPE_CHOICES)
    max_membres = models.IntegerField(default=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```
- [ ] Définir ENUM (type_groupe: public, prive, administratif)
- [ ] Créer migrations
- [ ] Ajouter index
- [ ] Tester

## Estimation
1 jour

## Labels
`epic:chat` `priority:P1` `type:backend` `sprint:7`
```

### Issue #22 - Modèle MembreGroupe (Backend)
```markdown
## Description
Table de liaison Utilisateur-Groupe avec rôles

## Objectif
Gérer les membres des groupes

## Dépendances
- [ ] #2
- [ ] #21

## Critères d'acceptation
- [ ] Modèle MembreGroupe créé
- [ ] Contrainte unicité membre actif implémentée
- [ ] Signal ajout créateur comme admin
- [ ] Tests passent

## Tâches techniques
- [ ] Créer modèle MembreGroupe :
```python
class MembreGroupe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    role_membre = models.CharField(max_length=20, choices=ROLE_MEMBRE_CHOICES, default='membre')
    date_adhesion = models.DateTimeField(auto_now_add=True)
    date_sortie = models.DateTimeField(null=True, blank=True)
    est_actif = models.BooleanField(default=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['utilisateur', 'groupe'],
                condition=models.Q(est_actif=True),
                name='unique_membre_actif_par_groupe'
            )
        ]
```
- [ ] Définir ENUM (role_membre: membre, moderateur, admin)
- [ ] Créer signal post_save pour ajouter créateur comme admin
- [ ] Créer migrations
- [ ] Tester

## Estimation
1 jour

## Labels
`epic:chat` `priority:P1` `type:backend` `sprint:7`
```

### Issue #23 - Modèle Message (Backend)
```markdown
## Description
Créer le modèle pour les messages de chat

## Objectif
Stocker les messages des groupes

## Dépendances
- [ ] #2
- [ ] #21

## Critères d'acceptation
- [ ] Modèle Message créé
- [ ] Contrainte CHECK (texte OU fichier)
- [ ] Signal calcul date_suppression_auto
- [ ] Index créés
- [ ] Tests passent

## Tâches techniques
- [ ] Créer modèle Message :
```python
class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='messages')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    texte = models.TextField(null=True, blank=True)
    fichier_url = models.TextField(null=True, blank=True)
    type_fichier = models.CharField(max_length=20, choices=TYPE_FICHIER_CHOICES, null=True)
    est_supprime = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_suppression_auto = models.DateTimeField()
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(texte__isnull=False) | models.Q(fichier_url__isnull=False),
                name='message_contenu_requis'
            )
        ]
```
- [ ] Définir ENUM type_fichier
- [ ] Créer signal pre_save pour calculer date_suppression_auto (6 mois)
- [ ] Créer migrations
- [ ] Ajouter index (groupe, created_at DESC)
- [ ] Tester

## Estimation
1.5 jour

## Labels
`epic:chat` `priority:P1` `type:backend` `sprint:7`
```

### Issue #24 - Job de suppression automatique des messages
```markdown
## Description
Créer un job Django Cron pour supprimer les vieux messages

## Objectif
Libérer de l'espace disque automatiquement

## Dépendances
- [ ] #23

## Critères d'acceptation
- [ ] Job créé et configuré
- [ ] Messages expirés supprimés quotidiennement
- [ ] Logging implémenté
- [ ] Test manuel réussi

## Tâches techniques
- [ ] Installer `django-crontab`
- [ ] Créer `chat/cron/delete_old_messages.py` :
```python
from django.utils import timezone
from chat.models import Message

def delete_old_messages():
    now = timezone.now()
    deleted_count = Message.objects.filter(
        date_suppression_auto__lt=now
    ).delete()[0]
    
    print(f"Supprimé {deleted_count} messages expirés")
```
- [ ] Configurer dans settings.py :
```python
CRONJOBS = [
    ('0 3 * * *', 'chat.cron.delete_old_messages.delete_old_messages'),  # 3h du matin
]
```
- [ ] Ajouter logging
- [ ] Tester manuellement

## Estimation
1 jour

## Labels
`epic:chat` `priority:P2` `type:backend` `sprint:7`
```

### Issue #59 - API CRUD Groupe - Liste & Détail
```markdown
## Description
Endpoints pour lister et voir les groupes

## Objectif
Permettre de découvrir les groupes disponibles

## Dépendances
- [ ] #21

## Critères d'acceptation
- [ ] GET `/api/groupes/` (groupes de l'utilisateur)
- [ ] GET `/api/groupes/publics/` (groupes publics)
- [ ] GET `/api/groupes/{uuid}/` fonctionnel
- [ ] RLS appliqué

## Tâches techniques
- [ ] Créer `chat/api/schemas.py` avec GroupeOutSchema
- [ ] Créer `chat/api/views.py` avec router :
```python
groupes_router = Router(tags=["Groupes"])

@groupes_router.get("/", auth=django_auth, response=List[GroupeOutSchema])
def list_groupes(request):
    # Groupes dont l'utilisateur est membre actif
    return Groupe.objects.filter(
        membregroupe__utilisateur=request.user,
        membregroupe__est_actif=True
    ).distinct()

@groupes_router.get("/publics/", auth=django_auth, response=List[GroupeOutSchema])
def list_groupes_publics(request):
    return Groupe.objects.filter(type_groupe='public', est_valide=True)

@groupes_router.get("/{groupe_id}", auth=django_auth, response=GroupeOutSchema)
def get_groupe(request, groupe_id: UUID):
    groupe = get_object_or_404(Groupe, id=groupe_id)
    # Vérifier que user est membre ou que groupe est public
    return groupe
```
- [ ] Enregistrer router
- [ ] Tester

## Estimation
1 jour

## Labels
`epic:chat` `priority:P1` `type:backend` `sprint:7`
```

### Issue #60 - API Création de Groupe
```markdown
## Description
Endpoint pour créer un nouveau groupe

## Objectif
Permettre aux utilisateurs de créer des espaces de discussion

## Dépendances
- [ ] #21

## Critères d'acceptation
- [ ] POST `/api/groupes/` fonctionnel
- [ ] Validation unicité nom
- [ ] Si privé, `est_valide=False`
- [ ] Créateur ajouté comme admin automatiquement

## Tâches techniques
- [ ] Créer GroupeCreateSchema :
```python
class GroupeCreateSchema(BaseModel):
    nom_groupe: str = Field(..., min_length=3, max_length=100)
    photo_groupe_url: Optional[str] = None
    description: str
    type_groupe: str = Field(..., pattern="^(public|prive|administratif)$")
    max_membres: int = Field(default=500, ge=2, le=1000)
```
- [ ] Implémenter endpoint :
```python
@groupes_router.post("/", auth=django_auth, response={201: GroupeOutSchema, 400: MessageSchema})
def create_groupe(request, payload: GroupeCreateSchema):
    if Groupe.objects.filter(nom_groupe=payload.nom_groupe).exists():
        return 400, {"message": "Ce nom de groupe existe déjà", "success": False}
    
    current_user = get_current_user(request)
    
    # Vérifier permissions pour type administratif
    if payload.type_groupe == 'administratif' and current_user.role not in ['admin', 'super_admin']:
        return 400, {"message": "Seuls les admins peuvent créer des groupes administratifs", "success": False}
    
    # Déterminer si validation requise
    est_valide = payload.type_groupe == 'public'
    
    groupe = Groupe.objects.create(
        **payload.dict(),
        createur=current_user,
        est_valide=est_valide
    )
    
    # Ajouter créateur comme admin (fait par signal)
    
    if not est_valide:
        # Notifier admins pour validation
        pass
    
    return 201, groupe
```
- [ ] Tester

## Estimation
1 jour

## Labels
`epic:chat` `priority:P1` `type:backend` `sprint:7`
```

### Issue #61 - API Validation des Groupes Privés
```markdown
## Description
Endpoint pour valider/invalider un groupe privé

## Objectif
Contrôler les groupes créés par les utilisateurs

## Dépendances
- [ ] #60

## Critères d'acceptation
- [ ] POST `/api/groupes/{uuid}/validate/` fonctionnel
- [ ] Modèle ValidationGroupe créé
- [ ] Email envoyé au créateur
- [ ] Permission admin vérifiée

## Tâches techniques
- [ ] Créer modèle ValidationGroupe (similaire à ValidationFormation)
- [ ] Créer endpoint validate_groupe
- [ ] Implémenter service email
- [ ] Tester

## Estimation
1 jour

## Labels
`epic:chat` `priority:P1` `type:backend` `sprint:7`
```

### Issue #62 - API Gestion des Membres de Groupe
```markdown
## Description
Endpoints pour ajouter/retirer des membres

## Objectif
Gérer l'appartenance aux groupes

## Dépendances
- [ ] #22

## Critères d'acceptation
- [ ] GET `/api/groupes/{uuid}/membres/` fonctionnel
- [ ] POST `/api/groupes/{uuid}/join/` fonctionnel
- [ ] POST `/api/groupes/{uuid}/leave/` fonctionnel
- [ ] POST `/api/groupes/{uuid}/add-membre/` (admin groupe)
- [ ] DELETE `/api/groupes/{uuid}/remove-membre/{user_id}/` (admin)
- [ ] Vérification max_membres

## Tâches techniques
- [ ] Créer MembreGroupeSchema
- [ ] Implémenter tous les endpoints :
```python
@groupes_router.get("/{groupe_id}/membres/", auth=django_auth, response=List[MembreGroupeOutSchema])
def list_membres(request, groupe_id: UUID):
    groupe = get_object_or_404(Groupe, id=groupe_id)
    return MembreGroupe.objects.filter(groupe=groupe, est_actif=True).select_related('utilisateur')

@groupes_router.post("/{groupe_id}/join/", auth=django_auth, response={200: MessageSchema, 400: MessageSchema})
def join_groupe(request, groupe_id: UUID):
    groupe = get_object_or_404(Groupe, id=groupe_id)
    user = get_current_user(request)
    
    # Vérifier type groupe
    if groupe.type_groupe == 'prive' and not groupe.est_valide:
        return 400, {"message": "Ce groupe n'est pas encore validé", "success": False}
    
    # Vérifier max_membres
    if MembreGroupe.objects.filter(groupe=groupe, est_actif=True).count() >= groupe.max_membres:
        return 400, {"message": "Le groupe est complet", "success": False}
    
    # Créer membre
    MembreGroupe.objects.get_or_create(
        utilisateur=user,
        groupe=groupe,
        defaults={'role_membre': 'membre', 'est_actif': True}
    )
    
    return {"message": f"Vous avez rejoint le groupe {groupe.nom_groupe}"}

@groupes_router.post("/{groupe_id}/leave/", auth=django_auth, response=MessageSchema)
def leave_groupe(request, groupe_id: UUID):
    groupe = get_object_or_404(Groupe, id=groupe_id)
    user = get_current_user(request)
    
    membre = get_object_or_404(MembreGroupe, utilisateur=user, groupe=groupe, est_actif=True)
    
    # Ne pas permettre au créateur de quitter
    if groupe.createur == user:
        raise PermissionError("Le créateur ne peut pas quitter le groupe")
    
    membre.est_actif = False
    membre.date_sortie = timezone.now()
    membre.save()
    
    return {"message": "Vous avez quitté le groupe"}
```
- [ ] Tester tous les cas

## Estimation
1.5 jour

## Labels
`epic:chat` `priority:P0` `type:backend` `sprint:7`
```

### Issue #63 - API Messages - Liste & Création
```markdown
## Description
Endpoints pour les messages d'un groupe

## Objectif
Permettre de lire et poster des messages

## Dépendances
- [ ] #23
- [ ] #22

## Critères d'acceptation
- [ ] GET `/api/groupes/{uuid}/messages/` fonctionnel
- [ ] POST `/api/groupes/{uuid}/messages/` fonctionnel
- [ ] DELETE `/api/messages/{uuid}/` fonctionnel
- [ ] Pagination inversée (50 derniers)
- [ ] Vérification appartenance au groupe

## Tâches techniques
- [ ] Créer MessageSchema
- [ ] Implémenter endpoints :
```python
messages_router = Router(tags=["Messages"])

@messages_router.get("/{groupe_id}/messages/", auth=django_auth, response=List[MessageOutSchema])
@paginate(PageNumberPagination, page_size=50)
def list_messages(request, groupe_id: UUID):
    groupe = get_object_or_404(Groupe, id=groupe_id)
    user = get_current_user(request)
    
    # Vérifier que user est membre
    if not MembreGroupe.objects.filter(groupe=groupe, utilisateur=user, est_actif=True).exists():
        raise PermissionError("Vous n'êtes pas membre de ce groupe")
    
    return Message.objects.filter(
        groupe=groupe,
        est_supprime=False
    ).select_related('utilisateur').order_by('-created_at')

@messages_router.post("/{groupe_id}/messages/", auth=django_auth, response={201: MessageOutSchema, 400: MessageSchema})
def create_message(request, groupe_id: UUID, texte: str = None, fichier_url: str = None):
    groupe = get_object_or_404(Groupe, id=groupe_id)
    user = get_current_user(request)
    
    # Vérifier membre actif
    if not MembreGroupe.objects.filter(groupe=groupe, utilisateur=user, est_actif=True).exists():
        return 400, {"message": "Vous n'êtes pas membre de ce groupe", "success": False}
    
    if not texte and not fichier_url:
        return 400, {"message": "Le message doit contenir du texte ou un fichier", "success": False}
    
    # Calculer date_suppression_auto (6 mois)
    from datetime import timedelta
    date_suppression = timezone.now() + timedelta(days=180)
    
    message = Message.objects.create(
        groupe=groupe,
        utilisateur=user,
        texte=texte,
        fichier_url=fichier_url,
        date_suppression_auto=date_suppression
    )
    
    return 201, message

@messages_router.delete("/{message_id}/", auth=django_auth, response=MessageSchema)
def delete_message(request, message_id: UUID):
    message = get_object_or_404(Message, id=message_id)
    user = get_current_user(request)
    
    # Vérifier permissions (créateur ou modérateur/admin du groupe)
    membre = MembreGroupe.objects.filter(
        groupe=message.groupe,
        utilisateur=user,
        est_actif=True
    ).first()
    
    if message.utilisateur != user and membre.role_membre not in ['moderateur', 'admin']:
        raise PermissionError("Vous ne pouvez supprimer que vos propres messages")
    
    message.est_supprime = True
    message.save()
    
    return {"message": "Message supprimé"}
```
- [ ] Enregistrer router
- [ ] Tester

## Estimation
2 jours

## Labels
`epic:chat` `priority:P0` `type:backend` `sprint:7`
```

### Issue #64 - Upload de fichiers pour messages
```markdown
## Description
Service d'upload de fichiers (images, PDF, vidéos)

## Objectif
Permettre le partage de fichiers dans les messages

## Dépendances
- [ ] #63

## Critères d'acceptation
- [ ] Service upload créé
- [ ] Validation type fichier (whitelist)
- [ ] Validation taille (max 50 MB)
- [ ] Stockage configuré (local ou S3)
- [ ] URL retournée

## Tâches techniques
- [ ] Configurer stockage dans settings.py
- [ ] Créer `chat/services/file_upload.py` :
```python
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
import uuid
import os

ALLOWED_TYPES = [
    'image/jpeg', 'image/png', 'image/gif', 'image/webp',
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'video/mp4', 'video/webm'
]

MAX_SIZE = 50 * 1024 * 1024  # 50 MB

def upload_message_file(file, groupe_id):
    # Valider type
    if file.content_type not in ALLOWED_TYPES:
        raise ValidationError(f"Type de fichier non autorisé: {file.content_type}")
    
    # Valider taille
    if file.size > MAX_SIZE:
        raise ValidationError(f"Fichier trop volumineux (max 50 MB)")
    
    # Générer nom unique
    ext = os.path.splitext(file.name)[1]
    filename = f"chat/{groupe_id}/{uuid.uuid4()}{ext}"
    
    # Stocker
    path = default_storage.save(filename, file)
    
    # Retourner URL
    return default_storage.url(path)
```
- [ ] Créer endpoint upload :
```python
@messages_router.post("/{groupe_id}/upload/", auth=django_auth)
def upload_file(request, groupe_id: UUID, file: UploadedFile):
    try:
        url = upload_message_file(file, groupe_id)
        return {"url": url, "filename": file.name}
    except ValidationError as e:
        return 400, {"message": str(e), "success": False}
```
- [ ] Tester upload différents types

## Estimation
1.5 jour

## Labels
`epic:chat` `priority:P1` `type:backend` `sprint:7`
```

### Issue #65 - Page Liste des Groupes (Frontend)
```markdown
## Description
Interface pour découvrir et rejoindre des groupes

## Objectif
Afficher les groupes accessibles

## Dépendances
- [ ] #59
- [ ] #11

## Critères d'acceptation
- [ ] Page Groupes/Index.tsx fonctionnelle
- [ ] Deux onglets: "Mes groupes" et "Groupes publics"
- [ ] Composant GroupeCard créé
- [ ] Bouton "Rejoindre" fonctionnel

## Tâches techniques
- [ ] Créer `frontend/ts/pages/Groupes/Index.tsx`
- [ ] Créer `GroupeCard.tsx`
- [ ] Implémenter onglets avec Shadcn Tabs
- [ ] Appel API rejoindre groupe
- [ ] Tester

## Estimation
2 jours

## Labels
`epic:chat` `priority:P1` `type:frontend` `sprint:7`
```

### Issue #66 - Page Chat d'un Groupe (Frontend)
```markdown
## Description
Interface de chat en temps réel

## Objectif
Permettre d'envoyer et recevoir des messages

## Dépendances
- [ ] #63
- [ ] #11

## Critères d'acceptation
- [ ] Page Groupes/Chat.tsx fonctionnelle
- [ ] Liste messages (scroll inversé)
- [ ] Composant MessageBubble
- [ ] Composant ChatInput
- [ ] Envoi message fonctionnel
- [ ] Upload fichier fonctionnel
- [ ] Polling 3s pour nouveaux messages
- [ ] Auto-scroll vers le bas

## Tâches techniques
- [ ] Créer `frontend/ts/pages/Groupes/Chat.tsx` :
```typescript
import { useState, useEffect, useRef } from 'react'
import { router } from '@inertiajs/react'
import Layout from '@/components/layout/Layout'
import MessageBubble from '@/components/chat/MessageBubble'
import ChatInput from '@/components/chat/ChatInput'

interface Message {
  id: string
  texte: string
  fichier_url?: string
  created_at: string
  utilisateur: {
    id: string
    nom_complet: string
    photo_profil_url?: string
  }
}

interface Props {
  groupe: {
    id: string
    nom_groupe: string
  }
  messages: Message[]
  currentUserId: string
}

export default function GroupeChat({ groupe, messages: initialMessages, currentUserId }: Props) {
  const [messages, setMessages] = useState(initialMessages)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  
  // Polling pour nouveaux messages
  useEffect(() => {
    const interval = setInterval(() => {
      fetch(`/api/groupes/${groupe.id}/messages/`)
        .then(res => res.json())
        .then(data => {
          setMessages(data.items)
          scrollToBottom()
        })
    }, 3000)
    
    return () => clearInterval(interval)
  }, [groupe.id])
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }
  
  const handleSendMessage = (texte: string, fichier?: File) => {
    // Upload fichier si présent
    let fichier_url = null
    if (fichier) {
      const formData = new FormData()
      formData.append('file', fichier)
      
      fetch(`/api/groupes/${groupe.id}/upload/`, {
        method: 'POST',
        body: formData
      })
        .then(res => res.json())
        .then(data => {
          fichier_url = data.url
          sendMessage(texte, fichier_url)
        })
    } else {
      sendMessage(texte, null)
    }
  }
  
  const sendMessage = (texte: string, fichier_url: string | null) => {
    fetch(`/api/groupes/${groupe.id}/messages/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ texte, fichier_url })
    })
      .then(res => res.json())
      .then(newMessage => {
        setMessages([...messages, newMessage])
        scrollToBottom()
      })
  }
  
  return (
    <Layout>
      <div className="flex flex-col h-screen">
        <div className="bg-white shadow p-4">
          <h1 className="text-2xl font-bold">{groupe.nom_groupe}</h1>
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map(message => (
            <MessageBubble
              key={message.id}
              message={message}
              isOwn={message.utilisateur.id === currentUserId}
            />
          ))}
          <div ref={messagesEndRef} />
        </div>
        
        <ChatInput onSend={handleSendMessage} />
      </div>
    </Layout>
  )
}
```
- [ ] Créer `MessageBubble.tsx`
- [ ] Créer `ChatInput.tsx`
- [ ] Tester

## Estimation
3 jours

## Labels
`epic:chat` `priority:P0` `type:frontend` `sprint:7`
```

### Issue #67 - Formulaire Création de Groupe (Frontend)
```markdown
## Description
Interface pour créer un nouveau groupe

## Objectif
Permettre aux utilisateurs de créer des espaces

## Dépendances
- [ ] #60
- [ ] #11

## Critères d'acceptation
- [ ] Page Create.tsx fonctionnelle
- [ ] Formulaire avec validation
- [ ] Avertissement si privé
- [ ] Redirection après création

## Tâches techniques
- [ ] Créer `frontend/ts/pages/Groupes/Create.tsx`
- [ ] Créer schéma Zod
- [ ] Implémenter formulaire
- [ ] Gérer type_groupe (select)
- [ ] Avertissement validation pour privé
- [ ] Tester

## Estimation
1.5 jour

## Labels
`epic:chat` `priority:P1` `type:frontend` `sprint:7`
```

### Issue #68 - Interface Admin Validation des Groupes (Frontend)
```markdown
## Description
Page admin pour valider les groupes privés

## Objectif
Contrôler les groupes créés par les utilisateurs

## Dépendances
- [ ] #61

## Critères d'acceptation
- [ ] Page Admin/GroupesEnAttente.tsx fonctionnelle
- [ ] Liste groupes `est_valide=False`
- [ ] Modal validation
- [ ] Boutons Approuver/Rejeter

## Tâches techniques
- [ ] Créer Admin/GroupesEnAttente.tsx
- [ ] Réutiliser ValidationModal
- [ ] Appeler API validation
- [ ] Tester

## Estimation
1.5 jour

## Labels
`epic:chat` `priority:P2` `type:frontend` `sprint:7`
```

---

## 🏗️ EPIC 8 - STATISTIQUES & TABLEAUX DE BORD

### Issue #72 - Vue matérialisée PostgreSQL pour statistiques
```markdown
## Description
Créer une vue matérialisée pour les stats d'emploi

## Objectif
Performance optimale pour les statistiques

## Dépendances
- [ ] #2

## Critères d'acceptation
- [ ] Vue `stats_emploi_par_annee` créée
- [ ] Index unique créé
- [ ] Job rafraîchissement quotidien configuré
- [ ] Tests de requête réussis

## Tâches techniques
- [ ] Créer migration avec RunSQL :
```python
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_user_model'),
    ]
    
    operations = [
        migrations.RunSQL(
            sql="""
            CREATE MATERIALIZED VIEW stats_emploi_par_annee AS
            SELECT
                annee_sortie,
                COUNT(*) as total_diplomes,
                COUNT(*) FILTER (WHERE travailleur = TRUE) as nb_travaillent,
                COUNT(*) FILTER (WHERE travailleur = FALSE) as nb_recherche,
                ROUND(100.0 * COUNT(*) FILTER (WHERE travailleur = TRUE) / COUNT(*), 2) as taux_emploi
            FROM core_user
            WHERE statut = 'etudiant' AND annee_sortie IS NOT NULL AND est_actif = TRUE
            GROUP BY annee_sortie
            ORDER BY annee_sortie DESC;
            
            CREATE UNIQUE INDEX ON stats_emploi_par_annee (annee_sortie);
            """,
            reverse_sql="DROP MATERIALIZED VIEW IF EXISTS stats_emploi_par_annee;"
        )
    ]
```
- [ ] Créer modèle Django (managed=False)
- [ ] Créer job cron rafraîchissement
- [ ]Tester

## Estimation
1 jour

## Labels
`epic:statistiques` `priority:P1` `type:backend` `sprint:9`
```

### Issue #73 - API Statistiques d'Emploi
```markdown
## Description
Endpoints pour consulter les statistiques

## Objectif
Fournir les données au frontend

## Dépendances
- [ ] #72

## Critères d'acceptation
- [ ] GET `/api/statistiques/emploi/` fonctionnel
- [ ] Filtres (année, plage, liste) implémentés
- [ ] Cache 5 minutes actif
- [ ] Permission admin/personnel vérifiée

## Tâches techniques
- [ ] Créer app `statistics`
- [ ] Créer `statistics/api/views.py` :
```python
from django.core.cache import cache

stats_router = Router(tags=["Statistiques"])

@stats_router.get("/emploi/", auth=django_auth, response=List[StatsEmploiSchema])
@require_role(['admin', 'super_admin', 'personnel_admin'])
def get_emploi_stats(
    request,
    annee: int = None,
    annee_min: int = None,
    annee_max: int = None,
    annees: str = None  # "2017,2021,2025"
):
    cache_key = f"stats_emploi_{annee}_{annee_min}_{annee_max}_{annees}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    # Requête sur vue matérialisée
    from statistics.models import StatsEmploiParAnnee
    
    queryset = StatsEmploiParAnnee.objects.all()
    
    if annee:
        queryset = queryset.filter(annee_sortie=annee)
    elif annee_min and annee_max:
        queryset = queryset.filter(annee_sortie__gte=annee_min, annee_sortie__lte=annee_max)
    elif annees:
        annee_list = [int(a) for a in annees.split(',')]
        queryset = queryset.filter(annee_sortie__in=annee_list)
    
    result = list(queryset)
    cache.set(cache_key, result, 300)  # 5 minutes
    
    return result
```
- [ ] Enregistrer router
- [ ] Tester

## Estimation
1 jour

## Labels
`epic:statistiques` `priority:P1` `type:backend` `sprint:9`
```

### Issue #74 - Page Statistiques d'Emploi (Frontend)
```markdown
## Description
Interface pour visualiser les statistiques

## Objectif
Afficher les taux d'emploi de manière claire

## Dépendances
- [ ] #73
- [ ] #11

## Critères d'acceptation
- [ ] Page Statistiques/Emploi.tsx fonctionnelle
- [ ] Graphique en barres (recharts)
- [ ] Tableau détaillé
- [ ] Filtres (années, plages)
- [ ] Export CSV/PDF

## Tâches techniques
- [ ] Installer `recharts` : `npm install recharts`
- [ ] Créer `frontend/ts/pages/Statistiques/Emploi.tsx`
- [ ] Implémenter graphique BarChart
- [ ] Implémenter tableau avec Shadcn Table
- [ ] Créer formulaire filtres
- [ ] Implémenter export CSV
- [ ] Tester

## Estimation
2 jours

## Labels
`epic:statistiques` `priority:P1` `type:frontend` `sprint:9`
```

### Issue #75 - Dashboard Principal (Frontend)
```markdown
## Description
Page d'accueil avec KPIs et statistiques générales

## Objectif
Vue d'ensemble de la plateforme

## Dépendances
- [ ] #73
- [ ] #11

## Critères d'acceptation
- [ ] Page Dashboard.tsx fonctionnelle
- [ ] KPIs affichés (utilisateurs, offres, groupes, taux emploi)
- [ ] Graphiques (évolution inscriptions)
- [ ] Dernières offres affichées

## Tâches techniques
- [ ] Créer `frontend/ts/pages/Dashboard.tsx`
- [ ] Créer composant `StatCard.tsx`
- [ ] Fetch données depuis multiples endpoints
- [ ] Afficher KPIs
- [ ] Ajouter graphiques recharts
- [ ] Tester

## Estimation
3 jours

## Labels
`epic:statistiques` `priority:P2` `type:frontend` `sprint:9`
```

---

## 🏗️ EPIC 9 - ADMINISTRATION

### Issue #76 - API Liste & Recherche Utilisateurs (Admin)
```markdown
## Description
Endpoint pour lister tous les utilisateurs (admin uniquement)

## Objectif
Permettre la gestion des comptes

## Dépendances
- [ ] #2
- [ ] #7

## Critères d'acceptation
- [ ] GET `/api/users/` fonctionnel (déjà fait en #7 mais à améliorer)
- [ ] Filtres avancés
- [ ] Recherche full-text
- [ ] Pagination 50 par page

## Tâches techniques
- [ ] Améliorer endpoint existant si nécessaire
- [ ] Ajouter recherche full-text (nom, email, matricule)
- [ ] Optimiser avec select_related
- [ ] Tester

## Estimation
1 jour

## Labels
`epic:admin` `priority:P1` `type:backend` `sprint:10`
```

### Issue #77 - API Modification Utilisateur (Admin)
```markdown
## Description
Endpoint pour modifier un utilisateur (déjà fait en #7)

## Objectif
Permettre aux admins de gérer les comptes

## Dépendances
- [ ] #7

## Critères d'acceptation
- [ ] Endpoint fonctionnel
- [ ] Changement de rôle possible
- [ ] Activation/désactivation possible

## Tâches techniques
- [ ] Vérifier endpoint existant
- [ ] Compléter si nécessaire
- [ ] Tester

## Estimation
0.5 jour

## Labels
`epic:admin` `priority:P1` `type:backend` `sprint:10`
```

### Issue #78 - API Suppression Utilisateur (Soft Delete)
```markdown
## Description
Désactiver un compte utilisateur (déjà fait en #7)

## Objectif
Soft delete pour préserver l'intégrité

## Dépendances
- [ ] #7

## Critères d'acceptation
- [ ] Endpoint fonctionnel
- [ ] Sessions invalidées

## Tâches techniques
- [ ] Vérifier endpoint existant
- [ ] Invalider sessions Django
- [ ] Tester

## Estimation
0.5 jour

## Labels
`epic:admin` `priority:P2` `type:backend` `sprint:10`
```

### Issue #79 - Page Admin - Liste Utilisateurs (Frontend)
```markdown
## Description
Interface de gestion des utilisateurs

## Objectif
Permettre aux admins de voir et gérer les comptes

## Dépendances
- [ ] #76
- [ ] #11

## Critères d'acceptation
- [ ] Page Admin/Users/Index.tsx fonctionnelle
- [ ] Tableau avec colonnes complètes
- [ ] Filtres et recherche
- [ ] Actions CRUD
- [ ] Pagination

## Tâches techniques
- [ ] Créer `frontend/ts/pages/Admin/Users/Index.tsx`
- [ ] Implémenter tableau Shadcn DataTable
- [ ] Ajouter filtres (statut, travailleur, année)
- [ ] Barre de recherche
- [ ] Boutons actions
- [ ] Pagination
- [ ] Tester

## Estimation
2 jours

## Labels
`epic:admin` `priority:P1` `type:frontend` `sprint:10`
```

### Issue #80 - Page Admin - Modifier Utilisateur (Frontend)
```markdown
## Description
Formulaire de modification utilisateur

## Objectif
Permettre l'édition des comptes

## Dépendances
- [ ] #77
- [ ] #79

## Critères d'acceptation
- [ ] Page Edit.tsx fonctionnelle
- [ ] Champ travailleur grisé
- [ ] Changement rôle possible
- [ ] Toggle est_actif

## Tâches techniques
- [ ] Créer Admin/Users/Edit.tsx
- [ ] Formulaire avec tous les champs
- [ ] Désactiver champ travailleur
- [ ] Dropdown rôle
- [ ] Switch est_actif
- [ ] Tester

## Estimation
1.5 jour

## Labels
`epic:admin` `priority:P1` `type:frontend` `sprint:10`
```

### Issue #81 - Page Admin - Logs d'Audit (Frontend)
```markdown
## Description
Interface pour consulter les logs

## Objectif
Traçabilité des actions

## Dépendances
- [ ] #9

## Critères d'acceptation
- [ ] Page Admin/AuditLogs.tsx fonctionnelle
- [ ] Table logs
- [ ] Filtres (utilisateur, table, action, date)
- [ ] Modal voir détails JSON

## Tâches techniques
- [ ] Créer endpoint API GET `/api/audit-logs/`
- [ ] Créer Admin/AuditLogs.tsx
- [ ] Tableau avec colonnes
- [ ] Filtres
- [ ] Modal JSON viewer
- [ ] Pagination
- [ ] Tester

## Estimation
2 jours

## Labels
`epic:admin` `priority:P2` `type:frontend` `sprint:10`
```

---

## 🏗️ EPIC 10 - SÉCURITÉ & OPTIMISATIONS

### Issue #82 - Configuration HTTPS & SSL
```markdown
## Description
Configurer le certificat SSL pour l'application

## Objectif
Sécuriser les communications

## Dépendances
- [ ] Configuration serveur

## Critères d'acceptation
- [ ] Certificat SSL obtenu (Let's Encrypt)
- [ ] Nginx configuré avec SSL
- [ ] Redirection HTTPS forcée
- [ ] HSTS configuré
- [ ] Test SSL Labs A+

## Tâches techniques
- [ ] Obtenir certificat SSL avec Certbot
- [ ] Configurer Nginx avec SSL
- [ ] Configurer Django settings :
```python
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```
- [ ] Tester accès HTTPS
- [ ] Vérifier sur SSL Labs

## Estimation
0.5 jour

## Labels
`epic:securite` `priority:P0` `type:devops` `sprint:11`
```

### Issue #83 - Protection CSRF & XSS
```markdown
## Description
Configurer les protections Django

## Objectif
Protéger contre les attaques courantes

## Dépendances
- [ ] #1

## Critères d'acceptation
- [ ] CSRF activé
- [ ] Cookies sécurisés
- [ ] Headers sécurité configurés
- [ ] Tests de sécurité passent

## Tâches techniques
- [ ] Vérifier `CSRF_COOKIE_SECURE=True`
- [ ] Vérifier `SESSION_COOKIE_SECURE=True`
- [ ] Configurer `X-Frame-Options = 'DENY'`
- [ ] Configurer `SECURE_CONTENT_TYPE_NOSNIFF = True`
- [ ] Configurer `X_CONTENT_SECURITY_POLICY`
- [ ] Tester protections

## Estimation
0.5 jour

## Labels
`epic:securite` `priority:P0` `type:backend` `sprint:11`
```

### Issue #84 - Rate Limiting
```markdown
## Description
Implémenter un rate limiting sur les APIs

## Objectif
Protéger contre les abus

## Dépendances
- [ ] API endpoints

## Critères d'acceptation
- [ ] Rate limiting configuré
- [ ] Login limité à 5 tentatives/minute
- [ ] API limitée à 100 req/minute/user
- [ ] Erreur 429 avec Retry-After

## Tâches techniques
- [ ] Installer `django-ratelimit`
- [ ] Configurer throttling :
```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', method='POST')
def login_view(request):
    ...

# Pour Django Ninja
from ninja import NinjaAPI
from django.core.cache import cache

def rate_limit_middleware(get_response):
    def middleware(request):
        # Implémenter rate limiting
        pass
    return middleware
```
- [ ] Tester rate limiting
- [ ] Vérifier erreur 429

## Estimation
1 jour

## Labels
`epic:securite` `priority:P1` `type:backend` `sprint:11`
```

### Issue #85 - Configuration Cache Redis
```markdown
## Description
Configurer Redis pour le caching

## Objectif
Améliorer les performances

## Dépendances
- [ ] Infrastructure

## Critères d'acceptation
- [ ] Redis installé et configuré
- [ ] Cache Django fonctionnel
- [ ] Vues statiques cachées
- [ ] Statistiques cachées (5 min)
- [ ] Listes offres cachées (1 min)

## Tâches techniques
- [ ] Installer Redis
- [ ] Configurer dans settings.py :
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```
- [ ] Utiliser `@cache_page` sur vues statiques
- [ ] Cacher API statistiques
- [ ] Cacher listes offres
- [ ] Tester cache

## Estimation
1 jour

## Labels
`epic:performance` `priority:P2` `type:backend` `sprint:11`
```

### Issue #86 - Optimisation des Requêtes DB
```markdown
## Description
Ajouter `select_related` et `prefetch_related`

## Objectif
Réduire les N+1 queries

## Dépendances
- [ ] Tous les endpoints

## Critères d'acceptation
- [ ] Audit Django Debug Toolbar réalisé
- [ ] N+1 queries identifiées et corrigées
- [ ] Gains de performance mesurés
- [ ] Documentation des optimisations

## Tâches techniques
- [ ] Installer Django Debug Toolbar
- [ ] Auditer toutes les vues
- [ ] Identifier N+1 queries
- [ ] Ajouter `select_related` pour ForeignKey
- [ ] Ajouter `prefetch_related` pour M2M
- [ ] Exemples :
```python
# Avant
stages = Stage.objects.all()
for stage in stages:
    print(stage.createur.nom_complet)  # N+1 query

# Après
stages = Stage.objects.select_related('createur', 'organisation').all()
for stage in stages:
    print(stage.createur.nom_complet)  # 1 query
```
- [ ] Mesurer gains
- [ ] Documenter

## Estimation
2 jours

## Labels
`epic:performance` `priority:P1` `type:backend` `sprint:11`
```

### Issue #87 - Compression & Minification Assets
```markdown
## Description
Optimiser les fichiers statiques

## Objectif
Réduire le temps de chargement

## Dépendances
- [ ] #10

## Critères d'acceptation
- [ ] Minification Vite en production
- [ ] Compression Gzip/Brotli active
- [ ] Images optimisées (WebP)
- [ ] Lazy load composants React
- [ ] Score Lighthouse > 90

## Tâches techniques
- [ ] Configurer Vite pour production
- [ ] Activer compression Nginx :
```nginx
gzip on;
gzip_types text/css application/javascript application/json;
brotli on;
brotli_types text/css application/javascript application/json;
```
- [ ] Optimiser images
- [ ] Lazy load React :
```typescript
const LazyComponent = lazy(() => import('./Component'))
```
- [ ] Tester Lighthouse

## Estimation
1 jour

## Labels
`epic:performance` `priority:P2` `type:frontend+devops` `sprint:11`
```
