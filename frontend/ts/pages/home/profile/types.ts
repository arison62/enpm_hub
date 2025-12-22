export interface UserProps {
  id: string;
  email: string;
  role_systeme: "user" | "admin_site" | "super_admin";
  est_actif: boolean;
  last_login: string;
  created_at: string;
  updated_at: string;
  profil: {
    id: string;
    nom_complet: string;
    matricule?: string;
    titre?: string;
    statut_global?:
      | "etudiant"
      | "alumni"
      | "enseignant"
      | "personnel_admin"
      | "personnel_technique"
      | "partenaire";
    travailleur?: boolean;
    annee_sortie?: number;
    telephone?: string;
    domaine?: string;
    bio?: string;
    adresse?: string;
    photo_profil?: string;
    slug?: string;
    liens_reseaux?: {
      id: string;
      nom_reseau: string;
      url: string;
      est_actif: boolean;
    }[];
  };
}
