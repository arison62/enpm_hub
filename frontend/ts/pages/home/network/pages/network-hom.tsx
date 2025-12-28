import { useState, useEffect, useRef} from "react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
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
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { cn } from "@/lib/utils";
import { Separator } from "@/components/ui/separator";
import { useInternalNav } from "@/contexts/internal-nav-context";
import NetworkFormPage from "./network-form-page";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";

gsap.registerPlugin(useGSAP);
// Types (basés sur vos schémas)
interface Organisation {
  id: string;
  nom_organisation: string;
  slug: string;
  type_organisation: string;
  secteur_activite?: { nom: string } | null;
  ville?: string | null;
  pays?: string | null;
  logo?: string | null;
  nombre_abonnes: number;
  est_suivi: boolean;
}

export default function NetworkHome() {
 const [search, setSearch] = useState("");
 const [typeFilter, setTypeFilter] = useState<string>("all");
 const [page, setPage] = useState(1);
 const pageSize = 12;
 const [organisations, setOrganisations] = useState<Organisation[]>([]);
 const [totalPages, setTotalPages] = useState(1);
 const [loading, setLoading] = useState(true);
 const {push} = useInternalNav();
 const containerRef = useRef<HTMLDivElement>(null);



   useGSAP(() => {
     gsap.from(containerRef.current?.children || [], {
       opacity: 0,
       y: 20,
       stagger: 0.1,
       duration: 0.6,
       ease: "power2.out",
     });
   }, []);

 useEffect(() => {
   
   setTimeout(() => {
    setLoading(true);
     const data: Organisation[] = Array.from({ length: 40 }, (_, i) => ({
       id: `org-${i}`,
       nom_organisation: `Organisation ${i + 1}`,
       slug: `org-${i + 1}`,
       type_organisation: [
         "entreprise",
         "ong",
         "institution_publique",
         "startup",
         "association",
       ][i % 5],
       secteur_activite: {
         nom: ["Technologie", "Éducation", "Santé", "Énergie", "Agriculture"][
           i % 5
         ],
       },
       ville: ["Maroua", "Yaoundé", "Douala", "Garoua", "Bamenda"][i % 5],
       pays: "CM",
       logo: null,
       nombre_abonnes: Math.floor(Math.random() * 8000),
       est_suivi: Math.random() > 0.6,
     }));

     const filtered = data.filter((org) => {
       const matchesSearch =
         org.nom_organisation.toLowerCase().includes(search.toLowerCase()) ||
         org.secteur_activite?.nom
           .toLowerCase()
           .includes(search.toLowerCase()) ||
         org.ville?.toLowerCase().includes(search.toLowerCase());
       const matchesType =
         typeFilter === "all" || org.type_organisation === typeFilter;
       return matchesSearch && matchesType;
     });

     setOrganisations(filtered.slice((page - 1) * pageSize, page * pageSize));
     setTotalPages(Math.ceil(filtered.length / pageSize));
     setLoading(false);
   }, 800);
 }, [search, typeFilter, page]);

 return (
   <div className="" ref={containerRef}>
     <div className="container mx-auto px-4 py-6 lg:px-6">
       {/* Barre de recherche + filtres */}
       <div className="flex flex-col gap-4 mb-6 md:flex-row md:items-center md:justify-between">
         <Input
           placeholder="Rechercher une organisation..."
           value={search}
           onChange={(e) => {
             setSearch(e.target.value);
             setPage(1);
           }}
           className="flex-1"
         />

         <div className="flex flex-col gap-3 sm:flex-row">
           <Select
             value={typeFilter}
             onValueChange={(v) => {
               setTypeFilter(v);
               setPage(1);
             }}
           >
             <SelectTrigger className="w-full sm:w-[180px]">
               <SelectValue placeholder="Tous les types" />
             </SelectTrigger>
             <SelectContent>
               <SelectItem value="all">Tous les types</SelectItem>
               <SelectItem value="entreprise">Entreprise</SelectItem>
               <SelectItem value="ong">ONG</SelectItem>
               <SelectItem value="institution_publique">
                 Institution publique
               </SelectItem>
               <SelectItem value="startup">Startup</SelectItem>
               <SelectItem value="association">Association</SelectItem>
             </SelectContent>
           </Select>

           <Button onClick={()=>{
            push(NetworkFormPage, "Profile", {isEdit : false})
           }}>
             + Nouvelle organisation
           </Button>
         </div>
       </div>

       {/* Layout principal avec sidebars sur grand écran */}
       <div className="grid  grid-cols-1 lg:grid-cols-12 gap-6">
         {/* Sidebar gauche (visible uniquement sur lg+) */}
         <div className="hidden lg:block lg:col-span-2 space-y-6">
           {/* Card : Suggestions d'organisations */}
           <Card>
             <CardHeader className="pb-3">
               <CardTitle className="text-base">
                 Organisations populaires
               </CardTitle>
             </CardHeader>
             <CardContent className="space-y-4">
               {Array.from({ length: 3 }).map((_, i) => (
                 <div key={i} className="flex items-center gap-3">
                   <Avatar className="h-10 w-10">
                     <AvatarFallback>O{i + 1}</AvatarFallback>
                   </Avatar>
                   <div className="flex-1 min-w-0">
                     <p className="font-medium text-sm truncate">
                       Organisation populaire {i + 1}
                     </p>
                     <p className="text-xs text-muted-foreground">
                       12k abonnés
                     </p>
                   </div>
                 </div>
               ))}
             </CardContent>
           </Card>

           {/* Card : Annonce ou promotion */}
           <Card className="bg-gradient-to-br from-primary/10 to-primary/5">
             <CardContent className="p-5 text-center">
               <h3 className="font-semibold mb-2">
                 Recrutez les talents ENSPM
               </h3>
               <p className="text-sm text-muted-foreground mb-4">
                 Publiez une offre d'emploi ou de stage gratuitement
               </p>
               <Button variant="default" size="sm" className="w-full">
                 Publier une offre
               </Button>
             </CardContent>
           </Card>
         </div>

         {/* Contenu principal */}
         <div className="lg:col-span-6 space-y-6">
           {loading ? (
             <div className="text-center py-10 text-muted-foreground">
               Chargement...
             </div>
           ) : organisations.length === 0 ? (
             <div className="text-center py-10 text-muted-foreground">
               Aucune organisation trouvée
             </div>
           ) : (
             <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
               {organisations.map((org) => (
                 <Card
                   key={org.id}
                   className="cursor-pointer hover:shadow-md transition-all duration-200"
                  
                 >
                   <CardHeader className="pb-3">
                     <div className="flex items-center gap-3">
                       <Avatar className="h-10 w-10">
                         <AvatarImage
                           src={org.logo || ""}
                           alt={org.nom_organisation}
                         />
                         <AvatarFallback>
                           {org.nom_organisation[0]}
                         </AvatarFallback>
                       </Avatar>
                       <div className="flex-1 min-w-0">
                         <CardTitle className="text-base font-semibold truncate">
                           {org.nom_organisation}
                         </CardTitle>
                         <CardDescription className="text-xs mt-0.5">
                           {org.type_organisation}
                         </CardDescription>
                       </div>
                     </div>
                   </CardHeader>
                   <CardContent className="pt-0 space-y-3">
                     <div className="flex flex-wrap gap-1">
                       <Badge variant="secondary" className="text-xs">
                         {org.secteur_activite?.nom || "Non spécifié"}
                       </Badge>
                       <Badge variant="outline" className="text-xs">
                         {org.ville}, {org.pays}
                       </Badge>
                     </div>

                     <div className="flex justify-between items-center text-xs text-muted-foreground">
                       <span>
                         {org.nombre_abonnes.toLocaleString()} abonnés
                       </span>
                       <Button
                         variant={org.est_suivi ? "default" : "outline"}
                         size="sm"
                         className="h-7 px-3 text-xs"
                         onClick={(e) => {
                           e.stopPropagation();
                           // Logique follow/unfollow
                         }}
                       >
                         {org.est_suivi ? "Suivi" : "Suivre"}
                       </Button>
                     </div>
                   </CardContent>
                 </Card>
               ))}
             </div>
           )}

           {/* Pagination */}
           {!loading && totalPages > 1 && (
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
           )}
         </div>

         {/* Sidebar droite (visible uniquement sur lg+) */}
         <div className="hidden lg:block lg:col-span-3 space-y-6">
           {/* Card : Vos abonnements récents */}
           <Card>
             <CardHeader className="pb-3">
               <CardTitle className="text-base">
                 Organisations que vous suivez
               </CardTitle>
             </CardHeader>
             <CardContent className="space-y-4">
               {Array.from({ length: 3 }).map((_, i) => (
                 <div key={i} className="flex items-center gap-3">
                   <Avatar className="h-10 w-10">
                     <AvatarFallback>F{i + 1}</AvatarFallback>
                   </Avatar>
                   <div className="flex-1 min-w-0">
                     <p className="font-medium text-sm truncate">
                       Organisation suivie {i + 1}
                     </p>
                     <p className="text-xs text-muted-foreground">
                       Dernière activité : il y a 2j
                     </p>
                   </div>
                 </div>
               ))}
             </CardContent>
           </Card>

           {/* Card : Statistiques rapides */}
           <Card>
             <CardHeader className="pb-3">
               <CardTitle className="text-base">Statistiques</CardTitle>
             </CardHeader>
             <CardContent className="space-y-2 text-sm">
               <div className="flex justify-between">
                 <span className="text-muted-foreground">
                   Organisations totales
                 </span>
                 <span className="font-medium">1 248</span>
               </div>
               <Separator />
               <div className="flex justify-between">
                 <span className="text-muted-foreground">
                   Nouvelles cette semaine
                 </span>
                 <span className="font-medium text-primary">+47</span>
               </div>
             </CardContent>
           </Card>
         </div>
       </div>
     </div>
   </div>
 );
}
