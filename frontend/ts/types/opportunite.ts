import type { UUID, DateString, DateTimeString } from "./base";

export type TypeStage = "ouvrier" | "academique" | "professionnel";

export type StatutOpportunite =
  | "en_attente"
  | "active"
  | "expiree"
  | "pourvue"
  | "rejetee";

export type TypeEmploi =
  | "temps_plein_terrain"
  | "temps_partiel_terrain"
  | "temps_plein_ligne"
  | "temps_partiel_ligne"
  | "freelance"
  | "contrat";

export type TypeFormation = "en_ligne" | "presentiel" | "hybride";

export type TypeReseau =
  | "professionnel"
  | "social"
  | "academique"
  | "personnel";


  export interface StageOut {
    id: UUID;
    createur_profil: UUID | null;
    organisation: UUID | null;
    titre: string;
    slug: string;
    nom_structure: string;
    description: string;
    type_stage: TypeStage;
    adresse: string;
    ville: string | null;
    pays: string | null;
    email_contact: string | null;
    telephone_contact: string | null;
    lien_offre_original: string | null;
    lien_candidature: string | null;
    date_debut: DateString | null;
    date_fin: DateString | null;
    date_publication: DateTimeString;
    statut: StatutOpportunite;
    est_valide: boolean;
    validateur_profil: UUID | null;
    date_validation: DateTimeString | null;
    commentaire_validation: string | null;
  }

  export interface EmploiOut {
    id: UUID;
    createur_profil: UUID | null;
    organisation: UUID | null;
    titre: string;
    slug: string;
    nom_structure: string;
    description: string;
    type_emploi: TypeEmploi | null;
    adresse: string;
    ville: string | null;
    pays: string | null;
    email_contact: string | null;
    telephone_contact: string | null;
    lien_offre_original: string | null;
    lien_candidature: string | null;
    date_publication: DateTimeString;
    date_expiration: DateString | null;
    salaire_min: number | null;
    salaire_max: number | null;
    devise: UUID | null;
    statut: StatutOpportunite;
    est_valide: boolean;
    validateur_profil: UUID | null;
    date_validation: DateTimeString | null;
    commentaire_validation: string | null;
  }

  export interface FormationOut {
    id: UUID;
    createur_profil: UUID | null;
    organisation: UUID | null;
    titre: string;
    slug: string;
    nom_structure: string;
    description: string;
    type_formation: TypeFormation;
    adresse: string | null;
    ville: string | null;
    pays: string | null;
    email_contact: string | null;
    telephone_contact: string | null;
    lien_formation: string | null;
    lien_inscription: string | null;
    date_debut: DateString | null;
    date_fin: DateString | null;
    date_publication: DateTimeString;
    est_payante: boolean;
    prix: number | null;
    devise: UUID | null;
    duree_heures: number | null;
    statut: StatutOpportunite;
    est_valide: boolean;
    validateur_profil: UUID | null;
    date_validation: DateTimeString | null;
    commentaire_validation: string | null;
  }

  export interface StageCreate {
    titre: string;
    nom_structure: string;
    description: string;
    type_stage: TypeStage;
    adresse: string;
    ville: string | null;
    pays: string | null;
    email_contact: string | null;
    telephone_contact: string | null;
    lien_offre_original: string | null;
    lien_candidature: string | null;
    date_debut: DateString | null;
    date_fin: DateString | null;
    organisation?: UUID | null;
  }

  export interface EmploiCreate {
    titre: string;
    nom_structure: string;
    description: string;
    type_emploi: TypeEmploi | null;
    adresse: string;
    ville: string | null;
    pays: string | null;
    email_contact: string | null;
    telephone_contact: string | null;
    lien_offre_original: string | null;
    lien_candidature: string | null;
    date_expiration: DateString | null;
    salaire_min: number | null;
    salaire_max: number | null;
    devise: UUID | null;
    organisation?: UUID | null;
  }

  export interface FormationCreate {
    titre: string;
    nom_structure: string;
    description: string;
    type_formation: TypeFormation;
    adresse: string | null;
    ville: string | null;
    pays: string | null;
    email_contact: string | null;
    telephone_contact: string | null;
    lien_formation: string | null;
    lien_inscription: string | null;
    date_debut: DateString | null;
    date_fin: DateString | null;
    est_payante: boolean;
    prix: number | null;
    devise: UUID | null;
    duree_heures: number | null;
    organisation?: UUID | null;
  }

  export interface OpportuniteUpdate {
    titre?: string | null;
    nom_structure?: string | null;
    description?: string | null;
    type?: string | null; // TypeStage | TypeEmploi | TypeFormation
    adresse?: string | null;
    ville?: string | null;
    pays?: string | null;
    email_contact?: string | null;
    telephone_contact?: string | null;
    lien_offre_original?: string | null;
    lien_candidature?: string | null;
    date_debut?: DateString | null;
    date_fin?: DateString | null;
    est_payante?: boolean | null;
    prix?: number | null;
    devise?: UUID | null;
    duree_heures?: number | null;
    salaire_min?: number | null;
    salaire_max?: number | null;
    date_expiration?: DateString | null;
    slug?: string | null;
  }

  export interface OpportuniteValidation {
    approved: boolean;
    commentaire: string | null;
  }

  export interface OpportuniteStatusUpdate {
    statut: string;
  }