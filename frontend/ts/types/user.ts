export type Profil = {
  id: string;
  nom_complet: string;
  matricule: string | null;
  titre: string | null;
  statut_global: string | null;
  travailleur: boolean | null;
  annee_sortie: number | null;
  telephone: string | null;
  domaine: string | null;
  bio: string | null;
  created_at: string;
  updated_at: string;
};

export type User = {
  id: string;
  email: string;
  role_systeme: string;
  est_actif: boolean;
  last_login: string | null;
  created_at: string;
  updated_at: string;
  profil: Profil;
};
