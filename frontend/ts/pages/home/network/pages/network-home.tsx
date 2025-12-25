import { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";

import { OrganisationCard } from "../components/organisation-card";
import {
  OrganisationCardSkeleton,
  SidebarSkeleton,
} from "../components/organisation-skeleton";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import axios from "@/lib/axios";
import type { OrganisationOut } from "@/types/organisation";
import { cn } from "@/lib/utils";
import { useInternalNav } from "@/contexts/internal-nav-context";
import NetworkFormPage from "./network-form-page";

export default function NetworkHome() {
  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState<string>("all");
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [organisations, setOrganisations] = useState<OrganisationOut[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const {push} = useInternalNav();

  // Animation GSAP pour l'entrée des cartes
  useGSAP(() => {
    if (!loading) {
      gsap.from(".organisation-card", {
        opacity: 0,
        y: 20,
        stagger: 0.05,
        duration: 0.4,
        ease: "power2.out",
      });
    }
  }, [loading, organisations]);

  useEffect(() => {
    async function fetchOrganisations() {
      setLoading(true);
      try {
        const response = await axios.get(
          `/organisations/?page=${page}&page_size=12&search=${search}&type_organisation=${
            typeFilter === "all" ? "" : typeFilter
          }`
        );

        if (response.status === 200) {
          const data = response.data.items as OrganisationOut[];

          const metaData = response.data.meta as {
            page: number;
            total_pages: number;
            total_items: number;
          };
          if (page > metaData.total_pages) {
            setTotalPages(metaData.total_pages);
          }
          if (data.length === 0) {
            setPage(1);
          }

          setOrganisations((prev) => {
            // delete duplication
            data.filter((org) => {
              return !data.find((o) => o.id === org.id);
            });
            return data.map((org) => {
              const existingOrg = prev.find((o) => o.id === org.id);
              if (existingOrg) {
                return existingOrg;
              } else {
                return org;
              }
            });
          });
        }
        setLoading(false);
      } catch (error) {
        console.error(error);
      }
    }

    fetchOrganisations();
  }, [search, typeFilter, page]);

  return (
    <div className="w-full bg-slate-50/30 min-h-screen">
      <div className="container mx-auto px-4 py-6 lg:px-6 2xl:max-w-[1600px]">
        {/* HEADER : Recherche & Filtres */}
        <div className="flex flex-col gap-4 mb-8 md:flex-row md:items-center">
          <div className="relative flex-1">
            <Input
              placeholder="Rechercher une organisation (nom, ville, secteur)..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="bg-white shadow-sm"
            />
          </div>

          <div className="flex gap-3">
            <Select value={typeFilter} onValueChange={setTypeFilter}>
              <SelectTrigger className="w-[180px] bg-white shadow-sm">
                <SelectValue placeholder="Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Tous</SelectItem>
                <SelectItem value="entreprise">Entreprise</SelectItem>
                <SelectItem value="ong">ONG</SelectItem>
                <SelectItem value="institution_publique">
                  Institution publique
                </SelectItem>
                <SelectItem value="startup">Startup</SelectItem>
                <SelectItem value="universite">Université</SelectItem>
                <SelectItem value="gouvernement">Gouvernement</SelectItem>
              </SelectContent>
            </Select>

            <Button 
              className="shadow-sm"
              onClick={()=>{
                push(NetworkFormPage, "Creer une Organisation")
              }}
            >+ Nouvelle organisation</Button>
          </div>
        </div>

        {/* GRID PRINCIPALE */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* SIDEBAR GAUCHE */}
          <aside className="hidden lg:block lg:col-span-2">
            {loading ? (
              <SidebarSkeleton />
            ) : (
              <div className="space-y-6">
                {/* Votre composant Suggestions ici */}
                <Card>
                  <CardHeader className="pb-3 px-4 text-sm font-bold uppercase tracking-wider text-muted-foreground">
                    Populaires
                  </CardHeader>
                  <CardContent className="px-4 pb-4">
                    {/* ... items ... */}
                  </CardContent>
                </Card>
              </div>
            )}
          </aside>

          {/* CONTENU CENTRAL */}
          <main className="lg:col-span-8 space-y-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-4">
              {loading ? (
                // Affichage de 12 skeletons pendant le chargement
                Array.from({ length: 12 }).map((_, i) => (
                  <OrganisationCardSkeleton key={i} />
                ))
              ) : organisations.length > 0 ? (
                organisations.map((org) => (
                  <OrganisationCard
                    key={org.id}
                    org={org}
                    onClick={(slug) => console.log(slug)}
                    follow={() => console.log("follow")}
                  />
                ))
              ) : (
                <div className="col-span-full py-20 text-center text-muted-foreground">
                  Aucun résultat trouvé.
                </div>
              )}
            </div>

            {/* PAGINATION */}
            <div className="flex justify-center mt-8">
              <Pagination>
                <PaginationContent>
                  <PaginationItem>
                    <PaginationPrevious
                      onClick={() => setPage((p) => Math.max(1, p - 1))}
                      className={cn(
                        page === 1 && "pointer-events-none opacity-50"
                      )}
                    />
                  </PaginationItem>

                  {Array.from({ length: Math.min(7, totalPages) }, (_, i) => {
                    const pageNum = page + i - Math.min(3, page - 1);
                    if (pageNum < 1 || pageNum > totalPages) return null;
                    return (
                      <PaginationItem key={pageNum}>
                        <PaginationLink
                          isActive={page === pageNum}
                          onClick={() => setPage(pageNum)}
                        >
                          {pageNum}
                        </PaginationLink>
                      </PaginationItem>
                    );
                  })}

                  <PaginationItem>
                    <PaginationNext
                      onClick={() =>
                        setPage((p) => Math.min(totalPages, p + 1))
                      }
                      className={cn(
                        page === totalPages && "pointer-events-none opacity-50"
                      )}
                    />
                  </PaginationItem>
                </PaginationContent>
              </Pagination>
            </div>
          </main>

          {/* SIDEBAR DROITE */}
          <aside className="hidden lg:block lg:col-span-2">
            {loading ? (
              <SidebarSkeleton />
            ) : (
              <div className="space-y-6">
                {/* Vos Statistiques / Flux récents */}
              </div>
            )}
          </aside>
        </div>
      </div>
    </div>
  );
}
