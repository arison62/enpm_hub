erDiagram
    %% --- 1. CŒUR DU SYSTÈME : AUTHENTIFICATION & PROFIL ---
    users ||--|| profil : "possède (1-1)"
    
    users {
        uuid id PK
        varchar email UK
        varchar mot_de_passe_hash
        enum role_systeme "user, admin_site, super_admin"
        timestamp last_login
        boolean est_actif
        timestamp created_at
        timestamp updated_at
    }

    profil {
        uuid id PK
        uuid user_id FK
        varchar nom_complet
        varchar matricule UK
        varchar titre "Ex: Dr., Prof., etc."
        enum statut_global "etudiant, alumni, enseignant, personnel_admin, personnel_technique, partenaire"
        boolean travailleur
        smallint annee_sortie
        varchar telephone
        text photo_profil_url
        varchar domaine
        text bio "Nouveau champ pour description profil"
        timestamp created_at
        timestamp updated_at
    }

    %% --- 2. GESTION RÉSEAUX SOCIAUX (Rel 1-N) ---
    profil ||--o{ lien_reseau_social : "affiche"
    organisation ||--o{ lien_reseau_social : "affiche"

    lien_reseau_social {
        uuid id PK
        uuid profil_id FK "Nullable"
        uuid organisation_id FK "Nullable"
        varchar nom_reseau "LinkedIn, Facebook, SiteWeb, Portfolio"
        varchar url
        boolean est_actif
    }

    %% --- 3. ORGANISATIONS & MEMBRES (Type LinkedIn) ---
    organisation ||--o{ membre_organisation : "emploie"
    profil ||--o{ membre_organisation : "travaille_chez"
    organisation ||--o{ abonnement_organisation : "est_suivie_par"
    profil ||--o{ abonnement_organisation : "suit"

    organisation {
        uuid id PK
        varchar nom_organisation
        enum type_organisation "entreprise, ONG, institution_publique, startup, association"
        varchar secteur_activite
        text adresse
        varchar ville
        varchar pays
        varchar email_general
        varchar telephone_general
        text logo_url
        text description
        date date_creation
        enum statut "active, inactive, en_attente"
        timestamp created_at
        timestamp updated_at
    }

    %% Remplacement de 'contact_organisation' par 'membre_organisation' plus robuste
    membre_organisation {
        uuid id PK
        uuid profil_id FK
        uuid organisation_id FK
        enum role_organisation "employe, administrateur_page"
        varchar poste "Intitulé du poste"
        boolean est_actif
        date date_debut
        date date_fin
        timestamp created_at
    }

    abonnement_organisation {
        uuid profil_id PK, FK
        uuid organisation_id PK, FK
        timestamp date_abonnement
    }

    %% --- 4. FLUX D'ACTUALITÉ (POSTS & ÉVÉNEMENTS) ---
    %% Polymorphisme : Un post est écrit par un Profil OU une Organisation
    profil ||--o{ post : "publie_perso"
    organisation ||--o{ post : "publie_org"
    post ||--o{ commentaire : "reçoit"
    
    post {
        uuid id PK
        text contenu
        text media_url
        uuid auteur_profil_id FK "Rempli si l'auteur est une personne"
        uuid auteur_organisation_id FK "Rempli si publié au nom de l'entreprise"
        integer nombre_likes
        timestamp created_at
        timestamp updated_at
    }

    commentaire {
        uuid id PK
        uuid post_id FK
        text contenu
        uuid auteur_profil_id FK
        uuid auteur_organisation_id FK
        timestamp created_at
    }

    %% Héritage conceptuel pour les événements
    organisation ||--o{ evenement : "organise"
    profil ||--o{ evenement : "organise"

    evenement {
        uuid id PK
        varchar titre
        text description
        varchar lieu
        timestamp date_debut
        timestamp date_fin
        text lien_inscription "Lien externe event"
        uuid organisateur_profil_id FK
        uuid organisateur_organisation_id FK
        timestamp created_at
    }

    %% --- 5. OFFRES (MÉTIER EXISTANT CONSERVÉ + LIENS) ---
    organisation ||--o{ stage : "offre"
    profil ||--o{ stage : "crée"
    organisation ||--o{ emploi : "offre"
    profil ||--o{ emploi : "crée"
    
    stage {
        uuid id PK
        uuid createur_profil_id FK
        uuid organisation_id FK
        varchar titre
        varchar lieu
        varchar nom_structure
        text description
        enum type_stage "ouvrier, academique, professionnel"
        varchar email_contact
        varchar telephone_contact
        text lien_offre_original
        text lien_candidature "Nouveau : Lien pour postuler"
        date date_debut
        date date_fin
        enum statut "active, expiree, pourvue"
        timestamp created_at
        timestamp updated_at
    }

    emploi {
        uuid id PK
        uuid createur_profil_id FK
        uuid organisation_id FK
        varchar titre
        varchar lieu
        varchar nom_structure
        text description
        enum type_emploi "temps_plein_terrain, temps_partiel_terrain, temps_plein_ligne, etc"
        varchar email_contact
        varchar telephone_contact
        text lien_offre_original
        text lien_candidature "Nouveau : Lien pour postuler"
        date date_publication
        date date_expiration
        enum statut "active, expiree, pourvue"
        timestamp created_at
        timestamp updated_at
    }

    %% --- 6. FORMATIONS & VALIDATIONS (EXISTANT CONSERVÉ) ---
    organisation ||--o{ formation : "offre"
    profil ||--o{ formation : "crée"
    formation ||--o{ validation_formation : "fait_objet_de"

    formation {
        uuid id PK
        uuid createur_profil_id FK
        uuid organisation_id FK
        varchar titre
        varchar lieu
        varchar nom_structure
        text description
        enum type_formation "en_ligne, presentiel, hybride"
        boolean est_payante
        varchar email_contact
        varchar telephone_contact
        text lien_formation
        text lien_inscription "Nouveau : Lien pour s'inscrire"
        date date_debut
        date date_fin
        decimal prix
        varchar devise
        boolean est_valide
        timestamp created_at
        timestamp updated_at
    }

    validation_formation {
        uuid id PK
        uuid formation_id FK
        uuid validateur_profil_id FK
        boolean est_approuve
        text commentaire
        timestamp date_validation
    }

    %% --- 7. GROUPES & MESSAGERIE (EXISTANT CONSERVÉ) ---
    profil ||--o{ groupe : "crée"
    groupe ||--o{ membre_groupe : "contient"
    groupe ||--o{ message : "contient"
    groupe ||--o{ validation_groupe : "fait_objet_de"

    groupe {
        uuid id PK
        uuid createur_profil_id FK
        varchar nom_groupe UK
        text photo_groupe_url
        text description
        boolean est_valide
        enum type_groupe "public, prive, administratif"
        integer max_membres
        timestamp created_at
        timestamp updated_at
    }

    membre_groupe {
        uuid id PK
        uuid profil_id FK
        uuid groupe_id FK
        enum role_membre "membre, moderateur, admin"
        timestamp date_adhesion
        timestamp date_sortie
        boolean est_actif
    }

    message {
        uuid id PK
        uuid groupe_id FK
        uuid profil_id FK
        text texte
        text fichier_url
        enum type_fichier "image, pdf, word, excel, powerpoint, video"
        boolean est_supprime
        timestamp created_at
    }

    validation_groupe {
        uuid id PK
        uuid groupe_id FK
        uuid validateur_profil_id FK
        boolean est_approuve
        text commentaire
        timestamp date_validation
    }

    %% --- 8. TABLES SYSTÈME & RÉFÉRENCES (CONSERVÉES) ---
    domaine_reference {
        uuid id PK
        varchar nom_domaine UK
        text description
        boolean est_actif
    }

    annee_reference {
        smallint annee PK
        boolean est_disponible
    }

    audit_log {
        uuid id PK
        uuid user_id FK "Lien vers la table technique user"
        varchar table_name
        varchar action
        jsonb ancien_data
        jsonb nouveau_data
        inet ip_address
        text user_agent
        timestamp created_at
    }