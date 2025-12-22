// src/Pages/Profile.tsx
import { useRef } from "react";
import { Link, usePage } from "@inertiajs/react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { ExternalLink, Edit, Briefcase, Calendar, MapPin, Phone } from "lucide-react";

gsap.registerPlugin(useGSAP);


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
        statut_global?: "etudiant" | "alumni" | "enseignant" | "personnel_admin" | "personnel_technique" | "partenaire";
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
        }[]
    }
}

const mockUserData = {
  id: "550e8400-e29b-41d4-a716-446655440000",
  email: "aminatou.seidou@enspm.edu",
  role_systeme: "user",
  est_actif: true,
  last_login: "2025-01-15T10:30:00Z",
  created_at: "2023-09-01T08:00:00Z",
  updated_at: "2025-01-15T10:30:00Z",
  profil: {
    id: "660e8400-e29b-41d4-a716-446655440001",
    nom_complet: "Aminatou Seidou",
    matricule: "ENSPM2015-042",
    titre: "Ing.",
    statut_global: "alumni",
    travailleur: true,
    annee_sortie: 2015,
    telephone: "+237 6 XX XX XX XX",
    domaine: "Energie & Développement Durable",
    bio: "Ingénieure en énergie passionnée par les transitions énergétiques et le développement durable en Afrique. 8 ans d'expérience dans l'optimisation des systèmes énergétiques et la gestion de projets d'énergies renouvelables. Membre active de la communauté ENSPM, je contribue au mentorat des étudiants et au développement de partenariats stratégiques.",
    photo_profil:
      "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=400&fit=crop",
    slug: "aminatou-seidou-x7r2p9",
    created_at: "2023-09-01T08:00:00Z",
    updated_at: "2025-01-15T10:30:00Z",
    liens_reseaux: [
      {
        id: "770e8400-e29b-41d4-a716-446655440002",
        nom_reseau: "LinkedIn",
        url: "https://linkedin.com/in/aminatou-seidou",
        est_actif: true,
        created_at: "2023-09-01T08:00:00Z",
      },
      {
        id: "770e8400-e29b-41d4-a716-446655440003",
        nom_reseau: "GitHub",
        url: "https://github.com/aminatou-seidou",
        est_actif: true,
        created_at: "2023-09-01T08:00:00Z",
      },
      {
        id: "770e8400-e29b-41d4-a716-446655440004",
        nom_reseau: "SiteWeb",
        url: "https://aminatou-seidou.com",
        est_actif: true,
        created_at: "2023-09-01T08:00:00Z",
      },
    ],
  },
};


export default function Profile() {
  const {user} = usePage().props as unknown as {user: UserProps}
  const profil = user.profil;

  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      const tl = gsap.timeline({ defaults: { ease: "power3.out" } });
      tl.from(".animate-fade", {
        opacity: 0,
        y: 20,
        stagger: 0.1,
        duration: 0.8,
      });
    },
    { scope: containerRef }
  );

  return (
    <>
      <div ref={containerRef} className="bg-background pb-12">
        {/* SECTION HEADER : Bannière + Avatar */}
        <div className="relative">
          {/* Bannière (Cover) */}
          <div className="h-40 md:h-64 w-full bg-primary overflow-hidden">
            <div className="absolute inset-0 opacity-30 bg-[url('https://www.transparenttextures.com/patterns/black-thread.png')]" />
          </div>

          {/* Infos de Profil (Chevauchement) */}
          <div className="container mx-auto px-4">
            <div className="relative -mt-16 md:-mt-20 flex flex-col md:flex-row items-center lg:items-end gap-6 animate-fade">
              {/* Avatar avec contour prononcé */}
              <Avatar className="size-32 md:size-44 border-4 border-background shadow-xl">
                <AvatarImage
                  src={profil.photo_profil}
                  alt={profil.nom_complet}
                />
                <AvatarFallback className="text-3xl">
                  {profil.nom_complet?.[0]}
                </AvatarFallback>
              </Avatar>

              {/* Texte du Profil */}
              <div className="flex-1 text-center md:text-left mb-2 md:h-60 md:flex md:flex-col md:justify-end lg:block lg:h-auto">
                <div className="flex flex-col md:flex-row md:items-center gap-2 md:gap-4">
                  <h1 className="text-2xl md:text-4xl font-extrabold text-foreground">
                    {profil.titre && (
                      <span className="text-primary">{profil.titre} </span>
                    )}
                    {profil.nom_complet}
                  </h1>
                  <Badge className="w-fit mx-auto md:mx-0 bg-primary/10 text-primary border-primary/20 hover:bg-primary/20">
                    {profil.statut_global.toUpperCase()}
                  </Badge>
                </div>

                <div className="flex flex-wrap justify-center md:justify-start gap-x-4 gap-y-1 mt-2 text-muted-foreground text-sm md:text-base">
                  <span className="flex items-center gap-1">
                    <Briefcase className="size-4" /> {profil.domaine}
                  </span>
                  <span className="flex items-center gap-1">
                    <MapPin className="size-4" /> Maroua, CM
                  </span>
                </div>
              </div>

              {/* Bouton Action (Desktop: à droite, Mobile: centré) */}
              <div className="flex pb-2">
                <Button
                  variant="outline"
                  size="sm"
                  className="rounded-full shadow-sm"
                  asChild
                >
                  <Link href="/profile/edit">
                    <Edit className="mr-2 size-4" /> Modifier le profil
                  </Link>
                </Button>
              </div>
            </div>
          </div>
        </div>

        {/* SECTION CONTENU : Grid Responsive */}
        <div className="container mx-auto px-4 mt-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            {/* COLONNE GAUCHE : Infos Secondaires (4/12) */}
            <div className="lg:col-span-4 space-y-6 animate-fade">
              <Card className="shadow-sm border-none bg-muted/30">
                <CardHeader>
                  <CardTitle className="text-lg flex items-center gap-2">
                    À propos
                  </CardTitle>
                </CardHeader>
                <CardContent className="text-sm leading-relaxed text-muted-foreground">
                  {profil.bio || "Aucune bio fournie."}
                </CardContent>
              </Card>

              <Card className="shadow-sm border-none">
                <CardHeader>
                  <CardTitle className="text-lg">Informations</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground flex items-center gap-2">
                      <Calendar className="size-4" /> Diplômé en
                    </span>
                    <span className="font-medium">{profil.annee_sortie}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground flex items-center gap-2">
                      <Phone className="size-4" /> Contact
                    </span>
                    <span className="font-medium">{profil.telephone}</span>
                  </div>
                  <hr className="my-2 border-muted" />
                  <div className="space-y-2">
                    <p className="text-xs font-semibold uppercase text-muted-foreground tracking-wider">
                      Réseaux
                    </p>
                    {profil.liens_reseaux?.map((lien: any, i: number) => (
                      <a
                        key={i}
                        href={lien.url}
                        className="flex items-center justify-between p-2 rounded-lg hover:bg-muted transition-colors text-sm text-primary"
                      >
                        {lien.nom_reseau}
                        <ExternalLink className="size-3" />
                      </a>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* COLONNE DROITE : Tabs Principaux (8/12) */}
            <div className="lg:col-span-8 animate-fade">
              <Tabs defaultValue="experiences" className="w-full">
                <div className="overflow-x-auto pb-2 scrollbar-hide">
                  <TabsList className="w-full md:w-fit inline-flex justify-start bg-transparent border-b rounded-none h-auto p-0 gap-6">
                    <TabsTrigger
                      value="experiences"
                      className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent shadow-none py-2 px-1"
                    >
                      Expériences
                    </TabsTrigger>
                    <TabsTrigger
                      value="education"
                      className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent shadow-none py-2 px-1"
                    >
                      Éducation
                    </TabsTrigger>
                    <TabsTrigger
                      value="skills"
                      className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent shadow-none py-2 px-1"
                    >
                      Compétences
                    </TabsTrigger>
                  </TabsList>
                </div>

                <TabsContent value="experiences" className="mt-6 space-y-4">
                  <Card className="border-dashed bg-transparent">
                    <CardContent className="pt-10 pb-10 text-center">
                      <Briefcase className="size-10 mx-auto text-muted-foreground/40 mb-3" />
                      <p className="text-muted-foreground italic">
                        Aucune expérience répertoriée.
                      </p>
                      <Button variant="link" className="text-primary mt-2">
                        Ajouter une expérience
                      </Button>
                    </CardContent>
                  </Card>
                </TabsContent>

                <TabsContent value="education" className="mt-6">
                  <Card className="border-none shadow-sm">
                    <CardHeader>
                      <CardTitle className="text-base">
                        Cursus Académique
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="flex gap-4">
                        <div className="size-10 rounded bg-primary/10 flex items-center justify-center text-primary font-bold">
                          P
                        </div>
                        <div>
                          <p className="font-bold">
                            École Nationale Supérieure Polytechnique de Maroua
                          </p>
                          <p className="text-sm text-muted-foreground">
                            Ingénieur en {profil.domaine}
                          </p>
                          <p className="text-xs text-muted-foreground mt-1">
                            Promotion {profil.annee_sortie}
                          </p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </TabsContent>

                <TabsContent value="skills" className="mt-6">
                  <div className="flex flex-wrap gap-2">
                    {[
                      "Gestion de projet",
                      "Énergies renouvelables",
                      "Audit énergétique",
                      "Python",
                      "Stratégie RSE",
                    ].map((skill) => (
                      <Badge
                        key={skill}
                        variant="secondary"
                        className="px-3 py-1"
                      >
                        {skill}
                      </Badge>
                    ))}
                  </div>
                </TabsContent>
              </Tabs>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}