# Rapport d'État d'Avancement du Projet ENSPM Hub

**Date du rapport :** 17 décembre 2025

## 1. Introduction

Ce rapport présente un état des lieux complet du projet ENSPM Hub. Il détaille les fonctionnalités déjà développées, identifie les modules et tâches à venir, et organise les interfaces applicatives par ordre de priorité. L'objectif est de fournir une vision claire de l'avancement actuel et de la feuille de route pour les prochaines phases de développement.

---

## 2. Fonctionnalités Développées

Cette section analyse en détail les modules dont le développement est terminé ou bien avancé.

### Module `core` (P0 - Terminé)

Le module `core` constitue le socle de l'application. Il est fonctionnel et robuste.

*   **Modèles de Données :**
    *   `User` : Modèle d'authentification basé sur l'email, avec gestion des rôles (`user`, `admin_site`, `super_admin`) et statut (`est_actif`).
    *   `Profil` : Modèle riche contenant les informations personnelles des utilisateurs (nom, statut, bio, photo, etc.), lié en 1-à-1 avec `User`.
    *   `AuditLog` : Modèle complet pour la traçabilité des actions (création, mise à jour, suppression) avec enregistrement des anciennes/nouvelles valeurs, IP et User-Agent.
    *   `ENSPMHubBaseModel` : Modèle de base abstrait intégrant un `UUID` comme clé primaire, les timestamps (`created_at`, `updated_at`) et le mécanisme de *soft delete*.

*   **Services (Logique Métier) :**
    *   `AuthService` : Gère l'authentification (login/logout) via JWT avec rotation des *refresh tokens*. La sécurité des endpoints est assurée par une classe `JWTAuthBearer`.
    *   `UserService` : Implémente la logique de création, mise à jour et suppression (soft delete) des utilisateurs et de leurs profils. Inclut un système complet d'upload et d'optimisation des photos de profil.
    *   `AuditLogService` : Service centralisé pour enregistrer toutes les actions sensibles dans le journal d'audit.
    *   `EmailService` : Service d'envoi d'emails transactionnels (bienvenue, reset mot de passe) de manière asynchrone via des tâches de fond (Huey).

*   **API Endpoints (`/api/v1/`) :**
    *   `/auth/login`, `/auth/logout`, `/auth/refresh` : Endpoints pour la gestion complète du cycle de vie de l'authentification.
    *   `/auth/me` : Endpoint sécurisé pour récupérer les informations de l'utilisateur connecté.
    *   `/users/` : Endpoints CRUD complets pour la gestion des utilisateurs (création, liste paginée avec filtres, détail, mise à jour, suppression), avec des permissions granulaires basées sur les rôles (admin vs utilisateur).
    *   `/users/{user_id}/photo` : Endpoints pour l'upload et la suppression de la photo de profil.

### Module `organizations` (P1 - Partiellement Implémenté)

Le travail sur ce module a commencé, mais seule la couche de données est en place.

*   **Modèles de Données :**
    *   `Organisation` : Modèle pour décrire les entreprises et institutions partenaires (nom, secteur, logo, statut de validation, etc.).
    *   `MembreOrganisation` : Modèle de liaison pour définir la relation entre un `Profil` et une `Organisation` (poste, rôle, statut actif).
    *   `AbonnementOrganisation` : Modèle pour permettre aux utilisateurs de suivre des organisations.

*   **État Actuel :**
    *   **À faire :** L'implémentation de la logique métier (`services`), des contrats d'API (`schemas`) et des endpoints (`views`) est entièrement à réaliser.

---

## 3. Fonctionnalités à Développer

Cette section définit la feuille de route pour les prochains modules, basée sur le `guide.md` et `database.md`.

### Module `opportunities` (P0 - Critique)

Ce module est prioritaire et doit être développé après le `core`.

*   **Modèles à implémenter :**
    *   `Stage` : Offres de stage avec détails (type, lieu, statut, etc.).
    *   `Emploi` : Offres d'emploi.
    *   `Formation` : Formations continues, séminaires, etc.
    *   `ValidationFormation` : Système de validation des formations par les administrateurs.

*   **Services à créer :**
    *   `StageService`, `EmploiService`, `FormationService` : Services implémentant la logique CRUD complète, la gestion des statuts (active, expirée), et les règles de permission (qui peut créer/modifier/voir les offres).
    *   `ValidationService` : Service pour la logique d'approbation des formations.

*   **API Endpoints à créer (`/api/v1/`) :**
    *   `/stages/`, `/emplois/`, `/formations/` : Endpoints CRUD pour chaque type d'opportunité, avec des filtres de recherche avancés.

### Module `feeds` (P1 - Élevé)

Ce module permettra de créer un fil d'actualité social.

*   **Modèles à implémenter :**
    *   `Post` : Publication pouvant contenir du texte et un média, avec un auteur polymorphe (un `Profil` ou une `Organisation`).
    *   `Commentaire` : Commentaires sur les posts.
    *   `Evenement` : Publications spécifiques pour les événements.

*   **Services à créer :**
    *   `FeedService` : Service pour créer, lister et interagir avec les posts, commentaires et événements. Gérera la logique du fil d'actualité.

*   **API Endpoints à créer (`/api/v1/`) :**
    *   `/feed/posts/`, `/feed/events/` : Pour lister et créer des publications.
    *   `/posts/{post_id}/comments/` : Pour ajouter et lister les commentaires d'un post.

### Module `chat` (P1 - Élevé)

Ce module ajoutera une messagerie instantanée à la plateforme.

*   **Modèles à implémenter :**
    *   `Groupe` : Groupes de discussion (publics, privés) avec un système de validation.
    *   `MembreGroupe` : Gestion des membres et de leurs rôles (admin, modérateur).
    *   `Message` : Messages texte ou avec fichiers.
    *   `ValidationGroupe` : Système de validation des groupes par les administrateurs.

*   **Services à créer :**
    *   `GroupeService` : Logique de création, validation, et gestion des membres d'un groupe.
    *   `MessageService` : Logique d'envoi, réception et suppression des messages.
    *   **Intégration WebSocket** : Nécessite la configuration de `Django Channels` pour la communication en temps réel.

*   **API Endpoints à créer (`/api/v1/`) :**
    *   `/chat/groupes/` : CRUD pour les groupes de discussion.
    *   `/chat/groupes/{groupe_id}/messages/` : Pour charger l'historique et envoyer de nouveaux messages.

---

## 4. Interfaces Applicatives par Priorité et Dépendances

### Priorité P0 (Critique)

*   **Backend (Interface d'administration Django) :**
    *   Panneaux pour gérer `User`, `Profil`, `AuditLog`.
    *   Panneaux pour gérer et valider `Stage`, `Emploi`, `Formation`.
*   **Frontend (React/Inertia) :**
    *   **Pages d'authentification** : Connexion, Déconnexion, Mot de passe oublié.
    *   **Pages de profil utilisateur** : Consultation et édition de son propre profil. Consultation des profils publics.
    *   **Pages des opportunités** : Liste, détail, création et modification des stages, emplois et formations.
    *   **Interface d'administration (React)** : Tableau de bord pour la gestion des utilisateurs et la validation des opportunités.
*   **Dépendances :** Le module `core` doit être stable.

### Priorité P1 (Élevée)

*   **Backend (Interface d'administration Django) :**
    *   Panneaux pour gérer et valider `Organisation` et `Groupe`.
    *   Panneaux pour modérer `Post` et `Commentaire`.
*   **Frontend (React/Inertia) :**
    *   **Pages des organisations** : Liste, détail, création et gestion des organisations et de leurs membres.
    *   **Page du fil d'actualité** : Affichage des posts et événements, création de publications.
    *   **Interface de chat** : Liste des groupes et fenêtre de discussion en temps réel.
    *   **Tableaux de bord statistiques** : Visualisation des données (module `stats`).
*   **Dépendances :** Modules `core` et `organizations` (pour les auteurs de posts).

---

## 5. Conclusion

Le projet ENSPM Hub dispose d'une base technique solide et bien architecturée avec le module `core`. La priorité immédiate est le développement complet du module `opportunities` (P0) pour apporter une valeur ajoutée essentielle aux utilisateurs. Par la suite, le développement des modules `organizations`, `feeds`, et `chat` (P1) enrichira la plateforme avec des fonctionnalités sociales et collaboratives, conformément à la vision du projet.
