import { useState } from "react";
import { FormSection } from "@/pages/home/components/opportunities/form-section";
import  RichTextEditor  from "@/components/rich-text-editor/rich-text-editor";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card } from "@/components/ui/card";

import {
  Briefcase,
  GraduationCap,
  MapPin,
  Building2,
  FileText,
  CalendarClock,
  Link as LinkIcon,
  Send,
  Save,
  Info,
} from "lucide-react";

type OpportunityType = "emploi" | "formation";

const OpportunityCreatePage = () => {
  const [activeTab, setActiveTab] = useState<OpportunityType>("emploi");

  return (
    <div className="max-w-4xl mx-auto sm:px-4 py-8 pb-24">
      {/* --- Main Form --- */}
      <Card className="overflow-hidden border-border shadow-sm">
        <Tabs
          defaultValue="emploi"
          value={activeTab}
          onValueChange={(v) => setActiveTab(v as OpportunityType)}
          className="w-full"
        >
          {/* Tabs Header */}
          <div className="bg-muted/30 px-6 pt-6">
            <TabsList className="grid w-full max-w-md grid-cols-2 mx-auto">
              <TabsTrigger value="emploi" className="gap-2">
                <Briefcase className="h-4 w-4" /> Offre d'Emploi
              </TabsTrigger>
              <TabsTrigger value="formation" className="gap-2">
                <GraduationCap className="h-4 w-4" /> Formation
              </TabsTrigger>
            </TabsList>
          </div>

          <form>
            {/* --- 1. Informations Principales (Commun) --- */}
            <FormSection
              title={
                activeTab === "emploi"
                  ? "Informations du poste"
                  : "Détails de la formation"
              }
              icon={<FileText className="h-5 w-5" />}
            >
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="md:col-span-2 space-y-2">
                  <Label htmlFor="titre">
                    {activeTab === "emploi"
                      ? "Intitulé du poste"
                      : "Titre de la formation"}{" "}
                    <span className="text-destructive">*</span>
                  </Label>
                  <Input
                    id="titre"
                    placeholder={
                      activeTab === "emploi"
                        ? "ex: Ingénieur R&D"
                        : "ex: Master Data Science"
                    }
                    className="h-12"
                    required
                  />
                </div>

                <div className="space-y-2 relative">
                  <Label htmlFor="org">
                    Organisation / Entreprise{" "}
                    <span className="text-destructive">*</span>
                  </Label>
                  <div className="relative">
                    <Building2 className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="org"
                      placeholder="Rechercher..."
                      className="pl-10 h-12"
                    />
                  </div>
                </div>

                <div className="space-y-2 relative">
                  <Label htmlFor="lieu">
                    Lieu <span className="text-destructive">*</span>
                  </Label>
                  <div className="relative">
                    <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="lieu"
                      placeholder="ex: Yaoundé, Cameroun"
                      className="pl-10 h-12"
                    />
                  </div>
                </div>
              </div>
            </FormSection>

            {/* --- 2. Détails Spécifiques (Onglets) --- */}
            <TabsContent value="emploi" className="mt-0">
              <FormSection
                title="Conditions de l'offre"
                icon={<Briefcase className="h-5 w-5" />}
                className="bg-muted/30"
              >
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label>
                      Type de contrat{" "}
                      <span className="text-destructive">*</span>
                    </Label>
                    <Select>
                      <SelectTrigger className="h-12 bg-background">
                        <SelectValue placeholder="Sélectionner" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="cdi">CDI</SelectItem>
                        <SelectItem value="cdd">CDD</SelectItem>
                        <SelectItem value="stage">Stage</SelectItem>
                        <SelectItem value="freelance">Freelance</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label>Politique télétravail</Label>
                    <Select defaultValue="hybrid">
                      <SelectTrigger className="h-12 bg-background">
                        <SelectValue placeholder="Sélectionner" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="onsite">Sur site</SelectItem>
                        <SelectItem value="hybrid">Hybride</SelectItem>
                        <SelectItem value="remote">Full Remote</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="md:col-span-2 space-y-2">
                    <Label>Salaire (Mensuel ou Annuel)</Label>
                    <div className="flex items-center gap-4">
                      <Input
                        type="number"
                        placeholder="Min"
                        className="h-12 bg-background"
                      />
                      <span className="text-muted-foreground font-medium">
                        -
                      </span>
                      <Input
                        type="number"
                        placeholder="Max"
                        className="h-12 bg-background"
                      />
                      <Select defaultValue="XAF">
                        <SelectTrigger className="w-[100px] h-12 bg-background">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="XAF">XAF</SelectItem>
                          <SelectItem value="EUR">EUR</SelectItem>
                          <SelectItem value="USD">USD</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                </div>
              </FormSection>
            </TabsContent>

            <TabsContent value="formation" className="mt-0">
              <FormSection
                title="Modalités de la formation"
                icon={<GraduationCap className="h-5 w-5" />}
                className="bg-muted/30"
              >
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label>
                      Format <span className="text-destructive">*</span>
                    </Label>
                    <Select>
                      <SelectTrigger className="h-12 bg-background">
                        <SelectValue placeholder="Sélectionner" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="en_ligne">En ligne</SelectItem>
                        <SelectItem value="presentiel">Présentiel</SelectItem>
                        <SelectItem value="hybride">Hybride</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label>Volume horaire (heures)</Label>
                    <Input
                      type="number"
                      placeholder="Ex: 40"
                      className="h-12 bg-background"
                    />
                  </div>

                  <div className="md:col-span-2 space-y-2">
                    <Label>Coût de la formation</Label>
                    <div className="flex items-center gap-4">
                      <Select defaultValue="payant">
                        <SelectTrigger className="w-[150px] h-12 bg-background">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="payant">Payante</SelectItem>
                          <SelectItem value="gratuit">Gratuite</SelectItem>
                        </SelectContent>
                      </Select>
                      <Input
                        type="number"
                        placeholder="Montant"
                        className="h-12 bg-background flex-1"
                      />
                      <span className="flex items-center justify-center px-4 bg-background border rounded-md h-12 text-sm font-medium">
                        XAF
                      </span>
                    </div>
                  </div>
                </div>
              </FormSection>
            </TabsContent>

            {/* --- 3. Description (WYSIWYG) --- */}
            <FormSection
              title="Description détaillée"
              icon={<FileText className="h-5 w-5" />}
            >
              <div className="space-y-2">
                <Label>
                  À propos <span className="text-destructive">*</span>
                </Label>
                <RichTextEditor
                  onChange={(html)=>console.log(html)}
                  placeholder={
                    activeTab === "emploi"
                      ? "Décrivez les missions, le profil recherché..."
                      : "Décrivez le programme, les objectifs pédagogiques..."
                  }
                />
              </div>
            </FormSection>

            {/* --- 4. Validité & Candidature --- */}
            <FormSection
              title="Candidature & Validité"
              icon={<CalendarClock className="h-5 w-5" />}
              className="bg-muted/30"
            >
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
                <div className="space-y-2">
                  <Label>Date de début (Optionnel)</Label>
                  <Input type="date" className="h-12 bg-background" />
                </div>

                <div className="space-y-2">
                  <Label className="flex items-center gap-2">
                    Date d'expiration{" "}
                    <span className="text-destructive">*</span>
                    <Info className="h-3 w-3 text-amber-500" />
                  </Label>
                  <Input
                    type="date"
                    className="h-12 bg-background border-primary/50 focus-visible:ring-primary"
                    required
                  />
                  <p className="text-[11px] text-muted-foreground">
                    L'offre sera archivée après cette date.
                  </p>
                </div>

                <div className="md:col-span-2 space-y-2">
                  <Label>Lien externe ou Email de contact</Label>
                  <div className="relative">
                    <LinkIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input
                      placeholder="https://..."
                      className="pl-10 h-12 bg-background"
                    />
                  </div>
                </div>
              </div>
            </FormSection>

            {/* --- Action Bar --- */}
            <div className="flex flex-col-reverse sm:flex-row items-center justify-end gap-4 p-6 md:p-8 border-t border-border bg-card">
              <Button
                variant="outline"
                size="lg"
                className="w-full sm:w-auto font-medium gap-2"
              >
                <Save className="h-4 w-4" /> Enregistrer brouillon
              </Button>
              <Button
                size="lg"
                className="w-full sm:w-auto font-bold gap-2 shadow-md"
              >
                <Send className="h-4 w-4" /> Publier l'opportunité
              </Button>
            </div>
          </form>
        </Tabs>
      </Card>

      <div className="mt-8 text-center text-sm text-muted-foreground">
        Besoin d'aide ?{" "}
        <a href="#" className="text-primary hover:underline">
          Consulter le guide de publication
        </a>
      </div>
    </div>
  );
};

export default OpportunityCreatePage;
