import {
  Building2,
  Calendar,
  Globe,
  Mail,
  MapPin,
  Phone,
  Users,
} from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import AppLayout from "@/components/layouts/app-layout";
import { Deferred, usePage } from "@inertiajs/react";
import type { OrganisationOut } from "@/types/organisation";

const ProfileSkeleton = () => (
  <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
    {/* Colonne gauche - Skeleton */}
    <div className="lg:col-span-3 space-y-6">
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col items-center text-center">
            <Skeleton className="h-24 w-24 rounded-full mb-4" />
            <Skeleton className="h-7 w-48 mb-2" />
            <Skeleton className="h-5 w-32" />

            <div className="mt-5 flex w-full gap-3">
              <Skeleton className="h-9 flex-1" />
              <Skeleton className="h-9 w-9 rounded-md" />
            </div>
          </div>

          <Separator className="my-6" />

          <div className="space-y-4">
            {Array.from({ length: 3 }).map((_, i) => (
              <div key={i} className="flex items-center gap-3">
                <Skeleton className="h-4 w-4" />
                <Skeleton className="h-4 w-40" />
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="pb-3">
          <Skeleton className="h-6 w-24" />
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center gap-2">
            <Skeleton className="h-4 w-4" />
            <Skeleton className="h-4 w-48" />
          </div>
          <div className="flex items-center gap-2">
            <Skeleton className="h-4 w-4" />
            <Skeleton className="h-4 w-32" />
          </div>
        </CardContent>
      </Card>
    </div>

    {/* Colonne centrale - Skeleton */}
    <div className="lg:col-span-6">
      <Card className="overflow-hidden border-none shadow-sm">
        <Skeleton className="h-32 w-full md:h-40" />

        <CardContent className="p-0">
          {/* Tabs header skeleton */}
          <div className="border-b bg-card px-4 md:px-6">
            <div className="flex h-12 items-center gap-8">
              <Skeleton className="h-6 w-20" />
              <Skeleton className="h-6 w-20" />
              <Skeleton className="h-6 w-28" />
            </div>
          </div>

          <div className="p-5 md:p-6">
            <div className="space-y-6">
              <div className="space-y-4">
                <Skeleton className="h-6 w-32" />
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-3/4" />
              </div>

              <Skeleton className="h-32 rounded-lg" />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    {/* Colonne droite - Skeleton */}
    <div className="lg:col-span-3 space-y-6">
      <Card>
        <CardHeader className="pb-3">
          <Skeleton className="h-6 w-24" />
        </CardHeader>
        <CardContent className="space-y-5">
          <div className="flex items-end justify-between">
            <Skeleton className="h-10 w-24" />
            <Skeleton className="h-6 w-20 rounded-full" />
          </div>
          <Separator />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-3/4" />
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="pb-3">
          <Skeleton className="h-5 w-40" />
        </CardHeader>
        <CardContent className="space-y-4">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="flex items-center gap-3">
              <Skeleton className="h-9 w-9 rounded-full" />
              <div className="min-w-0 flex-1 space-y-2">
                <Skeleton className="h-4 w-32" />
                <Skeleton className="h-3 w-24" />
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  </div>
);

const PageContent = () => {
  const { organisation: org } = usePage().props as unknown as { organisation: OrganisationOut };
  console.log(org);
  return (
    <>
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        {/* ------------------- Colonne gauche ------------------- */}
        <div className="lg:col-span-3 space-y-6">
          <Card className="sticky top-6 lg:top-20">
            <CardContent className="pt-6">
              <div className="flex flex-col items-center text-center">
                <Avatar className="h-24 w-24 border-4 border-background shadow-sm mb-4 ring-1 ring-border/40">
                  <AvatarImage
                    src={org.logo ?? undefined}
                    alt={org.nom_organisation}
                  />
                  <AvatarFallback className="text-3xl font-semibold bg-muted">
                    {org.nom_organisation?.[0]?.toUpperCase() ?? "?"}
                  </AvatarFallback>
                </Avatar>

                <h2 className="text-xl font-bold tracking-tight">
                  {org.nom_organisation}
                </h2>
                <p className="text-sm text-muted-foreground mt-1">
                  {org.type_organisation}
                </p>

                <div className="mt-5 flex w-full gap-3 sm:gap-4">
                  <Button
                    className="flex-1"
                    
                    size="sm"
                    // onClick={() => handleFollow(org.id)} // ← Implémenter l'appel Inertia pour suivre/désabonner
                  >
                    {org.est_suivi ? "Abonné" : "Suivre"}
                  </Button>

                  <Button
                    variant="outline"
                    size="icon"
                    className="h-9 w-9 shrink-0"
                    // onClick={() => window.open("https://example.com", "_blank")} // ← À ajouter quand site web disponible
                  >
                    <Globe className="h-4 w-4" />
                  </Button>
                </div>
              </div>

              <Separator className="my-6" />

              <div className="space-y-4 text-sm">
                {org.secteur_activite?.nom && (
                  <div className="flex items-center gap-3">
                    <Building2 className="h-4 w-4 text-muted-foreground" />
                    <span className="font-medium">
                      {org.secteur_activite.nom}
                    </span>
                  </div>
                )}

                {(org.ville || org.pays) && (
                  <div className="flex items-center gap-3">
                    <MapPin className="h-4 w-4 text-muted-foreground" />
                    <span>
                      {[org.ville, org.pays].filter(Boolean).join(", ")}
                    </span>
                  </div>
                )}

                <div className="flex items-center gap-3">
                  <Users className="h-4 w-4 text-muted-foreground" />
                  <span>
                    {org.nombre_membres ?? 0} membre
                    {org.nombre_membres !== 1 ? "s" : ""}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Contact */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base">Contact</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm">
              {org.email_general && (
                <div className="flex items-center gap-2">
                  <Mail className="h-4 w-4 shrink-0 text-muted-foreground" />
                  <a
                    href={`mailto:${org.email_general}`}
                    className="text-primary hover:underline truncate"
                  >
                    {org.email_general}
                  </a>
                </div>
              )}

              {org.telephone_general && (
                <div className="flex items-center gap-2">
                  <Phone className="h-4 w-4 shrink-0 text-muted-foreground" />
                  <span className="truncate">{org.telephone_general}</span>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* ------------------- Colonne centrale ------------------- */}
        <div className="lg:col-span-6">
          <Card className="overflow-hidden border-none shadow-sm">
            <div className="h-32 bg-gradient-to-r from-primary/80 via-primary to-primary/70 md:h-40" />

            <CardContent className="p-0">
              <Tabs defaultValue="a-propos" className="w-full">
                <div className="border-b bg-card px-4 md:px-6">
                  <TabsList className="h-12 w-full justify-start gap-6 bg-transparent p-0">
                    <TabsTrigger
                      value="a-propos"
                      className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:shadow-none h-12"
                    >
                      À propos
                    </TabsTrigger>
                    <TabsTrigger
                      value="membres"
                      className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:shadow-none h-12"
                    >
                      Membres
                    </TabsTrigger>
                    <TabsTrigger
                      value="offres"
                      className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:shadow-none h-12"
                    >
                      Opportunités
                    </TabsTrigger>
                  </TabsList>
                </div>

                <div className="p-5 md:p-6">
                  <TabsContent value="a-propos" className="mt-0 space-y-6">
                    <div className="prose prose-sm sm:prose max-w-none">
                      <h3 className="text-lg font-semibold mb-3">
                        Présentation
                      </h3>
                      <p className="text-muted-foreground leading-relaxed whitespace-pre-line">
                        {org.description || "Aucune description disponible."}
                      </p>
                    </div>

                    {org.date_creation && (
                      <div className="mt-8 rounded-lg border bg-muted/40 p-4">
                        <p className="mb-1 text-xs font-semibold uppercase text-muted-foreground">
                          Date de création
                        </p>
                        <div className="flex items-center gap-2">
                          <Calendar className="h-4 w-4 text-primary" />
                          <span className="text-sm font-medium">
                            {new Date(org.date_creation).toLocaleDateString(
                              "fr-FR",
                              {
                                year: "numeric",
                                month: "long",
                                day: "numeric",
                              }
                            )}
                          </span>
                        </div>
                      </div>
                    )}
                  </TabsContent>

                  <TabsContent value="membres">
                    <div className="py-12 text-center text-muted-foreground">
                      Liste des membres – en cours de développement
                    </div>
                  </TabsContent>

                  <TabsContent value="offres">
                    <div className="py-12 text-center text-muted-foreground">
                      Opportunités & offres – à venir
                    </div>
                  </TabsContent>
                </div>
              </Tabs>
            </CardContent>
          </Card>
        </div>

        {/* ------------------- Colonne droite ------------------- */}
        <div className="lg:col-span-3 space-y-6">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle>Influence</CardTitle>
            </CardHeader>
            <CardContent className="space-y-5">
              <div className="flex items-end justify-between">
                <div>
                  <p className="text-3xl font-bold tracking-tight">
                    {org.nombre_abonnes?.toLocaleString() ?? 0}
                  </p>
                  <p className="text-xs text-muted-foreground">Abonnés</p>
                </div>
                {/* <Badge
                  variant="secondary"
                  className="bg-green-100/80 text-green-800"
                >
                  +12% ce mois
                </Badge> */}
              </div>

              <Separator />

              {/* <p className="text-xs text-muted-foreground leading-relaxed">
                Cette organisation fait partie du top 10% des plus actives du
                réseau.
              </p> */}
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base">Similaires</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* {Array.from({ length: 3 }).map((_, i) => (
                <div key={i} className="flex items-center gap-3">
                  <Avatar className="h-9 w-9">
                    <AvatarFallback className="text-xs">
                      S{i + 1}
                    </AvatarFallback>
                  </Avatar>
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium">
                      Organisation similaire {i + 1}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {org.secteur_activite?.nom ?? "Secteur"}
                    </p>
                  </div>
                </div>
              ))} */}
            </CardContent>
          </Card>
        </div>
      </div>
    </>
  );
};

const NetworkPageProfile = () => {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto max-w-7xl px-4 py-6 md:px-6 lg:px-8">
        <Deferred data="organisation" fallback={<ProfileSkeleton />}>
         <PageContent />
        </Deferred>
      </div>
    </div>
  );
};

NetworkPageProfile.layout = (page: React.ReactNode) => (
  <AppLayout>{page}</AppLayout>
);

export default NetworkPageProfile;
