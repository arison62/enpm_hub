import {
  ArrowLeft,
  Building2,
  MapPin,
  Users,
  Globe,
  Edit,
  Calendar,
  Mail,
  Phone,
  ExternalLink,
} from "lucide-react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";

const mockOrganisations = [
    {
        id: "1",
        nom_organisation: "Organisation 1",
        logo: "https://via.placeholder.com/150",
        secteur_activite: { id: "1", nom: "Secteur 1", code: "S1" },
        ville: "Ville 1",
        pays: "Pays 1",
        pays_nom: "Nom du pays 1",
        description: "Description 1",
        email_general: "contact@org1.com",
        telephone_general: "+33 1 23 45 67 89",
        date_creation: "1924-03-01",
        membres_count: 10,
        abonnes_count: 100,
        statut: "active",
        type_organisation: "entreprise",
    }
]

const NetworkProfile = ({ orgId }: { orgId: string }) => {
  // Simulation de la récupération (à remplacer par votre logique de données)
  const org = mockOrganisations.find((o) => o.id === orgId);

  if (!org) {
    return <div className="p-10 text-center">Organisation non trouvée</div>;
  }

  return (
    <div className="w-full bg-slate-50/50 min-h-screen">
      {/* 1. Conteneur large cohérent */}
      <div className="container mx-auto px-4 py-6 lg:px-6 2xl:max-w-[1600px]">

        {/* 2. Layout en grille 12 colonnes */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* COLONNE GAUCHE : Infos rapides (lg:col-span-3) */}
          <div className="lg:col-span-3 space-y-6">
            <Card>
              <CardContent className="pt-6">
                <div className="flex flex-col items-center text-center">
                  <Avatar className="h-24 w-24 border-4 border-background shadow-sm mb-4">
                    <AvatarImage src={org.logo || ""} />
                    <AvatarFallback className="text-2xl">
                      {org.nom_organisation[0]}
                    </AvatarFallback>
                  </Avatar>
                  <h2 className="font-bold text-xl">{org.nom_organisation}</h2>
                  <p className="text-sm text-muted-foreground mt-1">
                    {org.type_organisation}
                  </p>

                  <div className="flex gap-2 mt-4 w-full">
                    <Button className="flex-1" variant="default" size="sm">
                      Suivre
                    </Button>
                    <Button variant="outline" size="icon" className="h-9 w-9">
                      <Globe className="h-4 w-4" />
                    </Button>
                  </div>
                </div>

                <Separator className="my-6" />

                <div className="space-y-4">
                  <div className="flex items-center gap-3 text-sm">
                    <Building2 className="h-4 w-4 text-muted-foreground" />
                    <span className="font-medium">
                      {org.secteur_activite?.nom}
                    </span>
                  </div>
                  <div className="flex items-center gap-3 text-sm">
                    <MapPin className="h-4 w-4 text-muted-foreground" />
                    <span>
                      {org.ville}, {org.pays_nom}
                    </span>
                  </div>
                  <div className="flex items-center gap-3 text-sm">
                    <Users className="h-4 w-4 text-muted-foreground" />
                    <span>{org.membres_count} membres</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-semibold">Contact</CardTitle>
              </CardHeader>
              <CardContent className="text-sm space-y-3">
                <div className="flex items-center gap-2 overflow-hidden">
                  <Mail className="h-4 w-4 shrink-0 text-muted-foreground" />
                  <a
                    href={`mailto:${org.email_general}`}
                    className="text-primary truncate hover:underline"
                  >
                    {org.email_general}
                  </a>
                </div>
                <div className="flex items-center gap-2">
                  <Phone className="h-4 w-4 shrink-0 text-muted-foreground" />
                  <span>{org.telephone_general}</span>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* COLONNE CENTRALE : Contenu Principal (lg:col-span-6) */}
          <div className="lg:col-span-6 space-y-6">
            {/* Banner / Hero */}
            <Card className="overflow-hidden border-none shadow-sm">
              <div className="h-40 w-full bg-gradient-to-r from-blue-600 via-indigo-500 to-purple-500" />
              <CardContent className="p-0">
                <Tabs defaultValue="a-propos" className="w-full">
                  <div className="px-6 border-b bg-card">
                    <TabsList className="bg-transparent h-14 w-full justify-start gap-6 p-0">
                      <TabsTrigger
                        value="a-propos"
                        className="data-[state=active]:bg-transparent data-[state=active]:border-b-2 data-[state=active]:border-primary data-[state=active]:shadow-none rounded-none h-14"
                      >
                        À propos
                      </TabsTrigger>
                      <TabsTrigger
                        value="membres"
                        className="data-[state=active]:bg-transparent data-[state=active]:border-b-2 data-[state=active]:border-primary data-[state=active]:shadow-none rounded-none h-14"
                      >
                        Membres
                      </TabsTrigger>
                      <TabsTrigger
                        value="offres"
                        className="data-[state=active]:bg-transparent data-[state=active]:border-b-2 data-[state=active]:border-primary data-[state=active]:shadow-none rounded-none h-14"
                      >
                        Opportunités
                      </TabsTrigger>
                    </TabsList>
                  </div>

                  <div className="p-6">
                    <TabsContent value="a-propos" className="mt-0 space-y-6">
                      <div className="prose prose-slate max-w-none">
                        <h3 className="text-lg font-semibold mb-2">
                          Présentation
                        </h3>
                        <p className="text-muted-foreground leading-relaxed">
                          {org.description ||
                            "Aucune description disponible pour cette organisation."}
                        </p>
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-6">
                        <div className="p-4 border rounded-lg bg-slate-50/50">
                          <p className="text-xs text-muted-foreground uppercase font-bold mb-1">
                            Date de création
                          </p>
                          <div className="flex items-center gap-2">
                            <Calendar className="h-4 w-4 text-primary" />
                            <span className="text-sm font-medium">
                              {org.date_creation
                                ? new Date(
                                    org.date_creation
                                  ).toLocaleDateString()
                                : "Non spécifiée"}
                            </span>
                          </div>
                        </div>
                        <div className="p-4 border rounded-lg bg-slate-50/50">
                          <p className="text-xs text-muted-foreground uppercase font-bold mb-1">
                            Site Web
                          </p>
                          <div className="flex items-center gap-2">
                            <ExternalLink className="h-4 w-4 text-primary" />
                            <a
                              href="#"
                              className="text-sm font-medium text-primary hover:underline truncate"
                            >
                              www.
                              {org.nom_organisation
                                .toLowerCase()
                                .replace(/\s/g, "")}
                              .com
                            </a>
                          </div>
                        </div>
                      </div>
                    </TabsContent>

                    <TabsContent value="membres">
                      <div className="text-center py-10 text-muted-foreground">
                        Liste des membres (En développement)
                      </div>
                    </TabsContent>
                  </div>
                </Tabs>
              </CardContent>
            </Card>
          </div>

          {/* COLONNE DROITE : Widgets (lg:col-span-3) */}
          <div className="lg:col-span-3 space-y-6">
            {/* Statistique de visibilité */}
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-base">Influence</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex justify-between items-end">
                  <div>
                    <p className="text-3xl font-bold">
                      {org.abonnes_count || 0}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      Abonnés totaux
                    </p>
                  </div>
                  <Badge className="bg-green-100 text-green-700 hover:bg-green-100 border-none">
                    +12% ce mois
                  </Badge>
                </div>
                <Separator />
                <div className="text-xs text-muted-foreground">
                  Cette organisation fait partie du top 10% des organisations
                  les plus actives du réseau.
                </div>
              </CardContent>
            </Card>

            {/* Suggestions Similaires (Comme sur la Home) */}
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm">
                  Organisations similaires
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {Array.from({ length: 3 }).map((_, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <Avatar className="h-8 w-8">
                      <AvatarFallback>S{i}</AvatarFallback>
                    </Avatar>
                    <div className="min-w-0">
                      <p className="text-xs font-medium truncate">
                        Concurrent ou Partenaire {i + 1}
                      </p>
                      <p className="text-[10px] text-muted-foreground">
                        {org.secteur_activite?.nom}
                      </p>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NetworkProfile;