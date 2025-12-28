import AppLayout from "@/components/layouts/app-layout";
import type { ReactNode } from "react";
import { useEffect, useState, useRef } from "react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
  CardFooter,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { cn } from "@/lib/utils";
import {
  MapPin,
  DollarSign,
  Clock,
  Users,
  Briefcase,
  GraduationCap,
  Search,
} from "lucide-react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";

// --- Types ---
type OpportuniteType = "stage" | "emploi" | "formation";

interface Opportunite {
  id: string;
  type: OpportuniteType;
  titre: string;
  organisation: string;
  lieu: string;
  duree: string | null;
  salaire_min: number | null;
  salaire_max: number | null;
  devise: string | null;
  date_publication: string;
  description: string;
}

const OpportunitesPage = () => {
  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState<OpportuniteType | "all">("all");
  const [page, setPage] = useState(1);
  const pageSize = 9;
  const [opportunites, setOpportunites] = useState<Opportunite[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);

  const containerRef = useRef<HTMLDivElement>(null);

  // --- Animation GSAP ---
  useGSAP(() => {
    if (!loading) {
      gsap.from(".opp-card", {
        y: 30,
        opacity: 0,
        stagger: 0.05,
        duration: 0.5,
        ease: "power2.out",
      });
    }
  }, [loading, opportunites]);

  // Simulation API
  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(true);
      const data: Opportunite[] = Array.from({ length: 45 }, (_, i) => {
        const type = ["stage", "emploi", "formation"][i % 3] as OpportuniteType;
        return {
          id: `opp-${i}`,
          type,
          titre:
            type === "stage"
              ? `Stage Ingénieur ${i + 1}`
              : type === "emploi"
              ? `Développeur Fullstack ${i + 1}`
              : `Formation Expert ${i + 1}`,
          organisation: `Organisation Alpha ${(i % 7) + 1}`,
          lieu: ["Yaoundé", "Douala", "Maroua", "Garoua", "Dschang"][i % 5],
          duree: type !== "emploi" ? "6 mois" : null,
          salaire_min: type === "emploi" ? 250000 : null,
          salaire_max: type === "emploi" ? 450000 : null,
          devise: "XAF",
          date_publication: "24/12/2025",
          description:
            "Rejoignez une équipe dynamique pour travailler sur des projets innovants.",
        };
      });

      const filtered = data.filter((opp) => {
        const matchesSearch =
          opp.titre.toLowerCase().includes(search.toLowerCase()) ||
          opp.organisation.toLowerCase().includes(search.toLowerCase());
        const matchesType = typeFilter === "all" || opp.type === typeFilter;
        return matchesSearch && matchesType;
      });

      setOpportunites(filtered.slice((page - 1) * pageSize, page * pageSize));
      setTotalPages(Math.ceil(filtered.length / pageSize));
      setLoading(false);
    }, 600);
    return () => clearTimeout(timer);
  }, [search, typeFilter, page]);

  return (
    <div
      className="min-h-screen bg-slate-50/50 dark:bg-zinc-950"
      ref={containerRef}
    >
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header Section */}
        <div className="mb-8 space-y-4">
          <h1 className="text-3xl font-bold tracking-tight">
            Opportunités du Réseau
          </h1>
          <p className="text-muted-foreground">
            Trouvez des stages, emplois et formations partagés par la
            communauté.
          </p>

          <div className="flex flex-col gap-4 md:flex-row md:items-center">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Titre, entreprise, mots-clés..."
                value={search}
                onChange={(e) => {
                  setSearch(e.target.value);
                  setPage(1);
                }}
                className="pl-10 bg-white dark:bg-zinc-900 border-none shadow-sm"
              />
            </div>
            <Select
              value={typeFilter}
              onValueChange={(v) => {
                // eslint-disable-next-line @typescript-eslint/no-explicit-any
                setTypeFilter(v as any);
                setPage(1);
              }}
            >
              <SelectTrigger className="w-full md:w-[200px] bg-white dark:bg-zinc-900 border-none shadow-sm">
                <SelectValue placeholder="Catégorie" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Toutes les catégories</SelectItem>
                <SelectItem value="stage">Stages</SelectItem>
                <SelectItem value="emploi">Emplois</SelectItem>
                <SelectItem value="formation">Formations</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="grid grid-cols-1 gap-8 lg:grid-cols-12 items-start">
          {/* SIDEBAR */}
          <aside className="hidden lg:flex lg:col-span-3 flex-col gap-6 sticky top-24">
            {/* Filtres Avancés */}
            <Card className="border-none shadow-sm">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-bold flex items-center gap-2">
                  <Briefcase className="h-4 w-4 text-primary" /> Filtres avancés
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-5">
                <div className="space-y-2">
                  <Label className="text-xs uppercase text-muted-foreground font-bold">
                    Lieu
                  </Label>
                  <Input placeholder="Ex: Douala" className="h-9 text-sm" />
                </div>
                <div className="space-y-3">
                  <Label className="text-xs uppercase text-muted-foreground font-bold">
                    Contrat
                  </Label>
                  <div className="space-y-2">
                    {["CDI", "CDD", "Freelance"].map((c) => (
                      <div key={c} className="flex items-center space-x-2">
                        <Checkbox id={c} />
                        <label
                          htmlFor={c}
                          className="text-sm leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                        >
                          {c}
                        </label>
                      </div>
                    ))}
                  </div>
                </div>
                <Button className="w-full h-9 text-sm">Filtrer</Button>
              </CardContent>
            </Card>

            {/* SECTION TROUVER UN MENTOR */}
            <Card className="border-none shadow-md bg-gradient-to-br from-primary to-indigo-700 text-primary-foreground overflow-hidden relative">
              <CardHeader className="pb-2 relative z-10">
                <CardTitle className="text-lg flex items-center gap-2">
                  <Users className="h-5 w-5" /> Trouver un mentor
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4 relative z-10">
                <p className="text-sm text-indigo-100">
                  Besoin de conseils pour votre carrière ? Échangez avec des
                  diplômés expérimentés du réseau.
                </p>
                <Button variant="secondary" className="w-full font-bold">
                  Explorer le programme
                </Button>
              </CardContent>
              <GraduationCap className="absolute -bottom-4 -right-4 h-24 w-24 opacity-20 rotate-12" />
            </Card>
          </aside>

          {/* MAIN CONTENT */}
          <main className="lg:col-span-9 space-y-6">
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {loading ? (
                Array.from({ length: 6 }).map((_, i) => (
                  <Card
                    key={i}
                    className="h-[220px] flex flex-col border-none shadow-sm"
                  >
                    <CardHeader>
                      <Skeleton className="h-5 w-3/4" />
                      <Skeleton className="h-4 w-1/2 mt-2" />
                    </CardHeader>
                    <CardContent className="flex-1">
                      <Skeleton className="h-20 w-full" />
                    </CardContent>
                    <CardFooter>
                      <Skeleton className="h-8 w-full" />
                    </CardFooter>
                  </Card>
                ))
              ) : opportunites.length === 0 ? (
                <div className="col-span-full py-20 text-center">
                  <p className="text-muted-foreground">
                    Aucune opportunité ne correspond à votre recherche.
                  </p>
                </div>
              ) : (
                opportunites.map((opp) => (
                  <Card
                    key={opp.id}
                    className="opp-card flex flex-col h-full border-none shadow-sm hover:shadow-md transition-shadow bg-white dark:bg-zinc-900 group"
                  >
                    <CardHeader className="pb-3">
                      <div className="flex items-start justify-between">
                        <div className="space-y-1">
                          <CardTitle className="text-sm font-bold group-hover:text-primary transition-colors">
                            {opp.titre}
                          </CardTitle>
                          <CardDescription className="text-xs font-medium">
                            {opp.organisation}
                          </CardDescription>
                        </div>
                        <Badge
                          variant="outline"
                          className="text-[10px] capitalize"
                        >
                          {opp.type}
                        </Badge>
                      </div>
                    </CardHeader>

                    <CardContent className="flex-1 space-y-4">
                      <div className="flex flex-wrap gap-3">
                        <div className="flex items-center text-[11px] text-muted-foreground">
                          <MapPin className="h-3 w-3 mr-1 text-primary" />{" "}
                          {opp.lieu}
                        </div>
                        {opp.duree && (
                          <div className="flex items-center text-[11px] text-muted-foreground">
                            <Clock className="h-3 w-3 mr-1 text-primary" />{" "}
                            {opp.duree}
                          </div>
                        )}
                        {opp.salaire_min && (
                          <div className="flex items-center text-[11px] text-muted-foreground">
                            <DollarSign className="h-3 w-3 mr-1 text-primary" />
                            {opp.salaire_min / 1000}k –{" "}
                            {opp.salaire_max! / 1000}k {opp.devise}
                          </div>
                        )}
                      </div>
                      <p className="text-xs text-muted-foreground line-clamp-3 leading-relaxed">
                        {opp.description}
                      </p>
                    </CardContent>

                    <CardFooter className="pt-4 border-t border-slate-100 dark:border-zinc-800 flex justify-between items-center">
                      <span className="text-[10px] text-muted-foreground">
                        Posté le {opp.date_publication}
                      </span>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="h-8 text-xs font-bold text-primary hover:text-primary hover:bg-primary/5"
                      >
                        Détails
                      </Button>
                    </CardFooter>
                  </Card>
                ))
              )}
            </div>

            {/* Pagination */}
            {!loading && totalPages > 1 && (
              <div className="pt-6">
                <Pagination>
                  <PaginationContent>
                    <PaginationItem>
                      <PaginationPrevious
                        onClick={() => setPage((p) => Math.max(1, p - 1))}
                        className={cn(
                          "cursor-pointer",
                          page === 1 && "pointer-events-none opacity-50"
                        )}
                      />
                    </PaginationItem>
                    {/* Logique simplifiée de pagination */}
                    <PaginationItem>
                      <span className="text-sm text-muted-foreground px-4">
                        Page {page} sur {totalPages}
                      </span>
                    </PaginationItem>
                    <PaginationItem>
                      <PaginationNext
                        onClick={() =>
                          setPage((p) => Math.min(totalPages, p + 1))
                        }
                        className={cn(
                          "cursor-pointer",
                          page === totalPages &&
                            "pointer-events-none opacity-50"
                        )}
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

OpportunitesPage.layout = (page: ReactNode) => <AppLayout>{page}</AppLayout>;
export default OpportunitesPage;
