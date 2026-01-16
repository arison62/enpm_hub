import { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { Search, Briefcase } from "lucide-react";

import { OpportuniteList } from "../../components/opportunities/opportunity-list";
import { MentorCTA } from "../../components/opportunities/mentor-cta";
import type {
  OpportuniteAny,
  StageOut,
  EmploiOut,
  FormationOut,
} from "@/types/opportunities";
import OpportunityCreatePage from "./opportunities-create";
import { useInternalNav } from "@/contexts/internal-nav-context";

const OpportunitesHome = () => {
  const { push } = useInternalNav();
  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState<string>("all");
  const [page, setPage] = useState(1);
  const [items, setItems] = useState<OpportuniteAny[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(true);

      const generateData = (): OpportuniteAny[] =>
        Array.from({ length: 12 }, (_, i) => {
          const seed = i % 3;
          const base = {
            id: `uuid-${i}`,
            titre:
              seed === 0
                ? "Stage Développement Web"
                : seed === 1
                ? "Senior Backend Engineer"
                : "Formation DevOps",
            slug: `slug-${i}`,
            nom_structure: `Tech Corp ${i}`,
            description:
              "Une opportunité incroyable pour booster votre carrière...",
            adresse: "Bastos, Yaoundé",
            ville: "Yaoundé",
            pays: "CM",
            pays_nom: "Cameroun",
            date_publication: new Date().toISOString(),
            statut: "active",
            est_valide: true,
            createur_profil: null, // Simplifié pour la démo
            organisation: null,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            email_contact: null,
            telephone_contact: null,
            validateur_profil: null,
            date_validation: null,
            commentaire_validation: null,
          };

          if (seed === 0) {
            return {
              ...base,
              type_stage: "academique",
              date_debut: "2024-06-01",
              date_fin: "2024-09-01",
              lien_offre_original: null,
              lien_candidature: null,
            } as StageOut;
          } else if (seed === 1) {
            return {
              ...base,
              type_emploi: "temps_plein_terrain",
              salaire_min: 500000,
              salaire_max: 800000,
              devise: { code: "XAF", nom: "Franc CFA", symbole: "FCFA" },
              date_expiration: "2024-12-31",
              lien_offre_original: null,
              lien_candidature: null,
            } as EmploiOut;
          } else {
            return {
              ...base,
              type_formation: "en_ligne",
              est_payante: true,
              prix: 25000,
              devise: { code: "XAF", nom: "Franc CFA", symbole: "FCFA" },
              duree_heures: 40,
              date_debut: "2024-05-10",
              date_fin: "2024-05-20",
              lien_formation: null,
              lien_inscription: null,
            } as FormationOut;
          }
        });

      setItems(generateData());
      setLoading(false);
    }, 800);
    return () => clearTimeout(timer);
  }, [search, typeFilter, page]);

  return (
    <div className="min-h-screen bg-slate-50/50 dark:bg-zinc-950">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* --- Header Section --- */}
        <div className="mb-8 space-y-4">
          <div className="flex flex-col items-start md:flex-row md:justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight">
                Opportunités du Réseau
              </h1>
              <p className="text-muted-foreground">
                Trouvez des stages, emplois et formations partagés par la
                communauté.
              </p>
            </div>
            <Button
              onClick={() => {
                push(OpportunityCreatePage, "Publier opportunite");
              }}
              className="mt-4"
            >
              Publier une Opportunité
            </Button>
          </div>

          <div className="flex flex-col gap-4 md:flex-row md:items-center bg-white dark:bg-zinc-900 p-4 rounded-lg shadow-sm border border-slate-100 dark:border-zinc-800">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Rechercher par titre, entreprise..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-10 border-slate-200 max-w-sm"
              />
            </div>
            <Select value={typeFilter} onValueChange={setTypeFilter}>
              <SelectTrigger className="w-full md:w-[200px]">
                <SelectValue placeholder="Catégorie" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Tout voir</SelectItem>
                <SelectItem value="stage">Stages</SelectItem>
                <SelectItem value="emploi">Emplois</SelectItem>
                <SelectItem value="formation">Formations</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="grid grid-cols-1 gap-8 lg:grid-cols-12 items-start">
          {/* --- Sidebar (Filtres & Pubs) --- */}
          <aside className="hidden lg:flex lg:col-span-3 flex-col gap-6 sticky top-24">
            <Card className="border-none shadow-sm bg-white dark:bg-zinc-900">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-bold flex items-center gap-2">
                  <Briefcase className="h-4 w-4 text-primary" /> Filtres avancés
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-5">
                <div className="space-y-2">
                  <Label className="text-xs uppercase text-muted-foreground font-bold">
                    Ville
                  </Label>
                  <Input placeholder="Ex: Douala" className="h-9 text-sm" />
                </div>
                <div className="space-y-3">
                  <Label className="text-xs uppercase text-muted-foreground font-bold">
                    Type de contrat
                  </Label>
                  <div className="space-y-2">
                    {["CDI", "Stage", "Freelance"].map((c) => (
                      <div key={c} className="flex items-center space-x-2">
                        <Checkbox id={c} />
                        <label
                          htmlFor={c}
                          className="text-sm leading-none cursor-pointer"
                        >
                          {c}
                        </label>
                      </div>
                    ))}
                  </div>
                </div>
                <Button className="w-full h-9 text-sm" variant="outline">
                  Appliquer
                </Button>
              </CardContent>
            </Card>
            <MentorCTA />
          </aside>

          {/* --- Main Content --- */}
          <main className="lg:col-span-9 space-y-6">
            {/* Liste isolée avec sa propre logique d'animation */}
            <OpportuniteList items={items} loading={loading} />

            {/* Pagination simple */}
            {!loading && (
              <div className="pt-4">
                <Pagination>
                  <PaginationContent>
                    <PaginationItem>
                      <PaginationPrevious
                        className="cursor-pointer"
                        onClick={() => setPage((p) => Math.max(1, p - 1))}
                      />
                    </PaginationItem>
                    <PaginationItem>
                      <span className="text-sm text-muted-foreground px-4">
                        Page {page}
                      </span>
                    </PaginationItem>
                    <PaginationItem>
                      <PaginationNext
                        className="cursor-pointer"
                        onClick={() => setPage((p) => p + 1)}
                      />
                    </PaginationItem>
                  </PaginationContent>
                </Pagination>
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
};

export default OpportunitesHome;
