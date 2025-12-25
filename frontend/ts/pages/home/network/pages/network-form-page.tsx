import { useState, useEffect } from "react";
import { Users, UserPlus, X } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "sonner";
import axios from "@/lib/axios";
import type { SecteurActiviteOut } from "@/types/base";

const typeOrganisationOptions = [
  { value: "entreprise", label: "Entreprise" },
  { value: "ong", label: "ONG" },
  { value: "institution_publique", label: "Institution publique" },
  { value: "startup", label: "Startup" },
  { value: "universite", label: "Université" },
  { value: "gouvernement", label: "Gouvernement" },
  { value: "association", label: "Association" },
  { value: "autre", label: "Autre" },
];

const roleOptions = [
  { value: "employe", label: "Employé" },
  { value: "administrateur_page", label: "Administrateur page" },
];

const NetworkFormPage: React.FC<{
  isEdit?: boolean;
}> = ({ isEdit = false }) => {
  const [isLoading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    nom_organisation: "",
    type_organisation: "",
    secteur_activite_id: "",
    ville: "",
    pays: "",
    email_general: "",
    telephone_general: "",
    description: "",
  });

  const [secteurActivites, setSetecteurActivites] = useState<
    SecteurActiviteOut[]
  >([]);
  const [pays, setPays] = useState<
    {
      code: string;
      name: string;
    }[]
  >([]);

  const [membres, setMembres] = useState<
    Array<{
      id: string;
      email: string;
      role_systeme: "user";
      role_organisation: "employe";
      profil: {
        nom_complet: string;
        status_global: "partenaire";
      };
    }>
  >([]);

  useEffect(() => {
    async function getReferencceProfessionel() {
      try {
        const response = await Promise.all([
          await axios.get("/references/professionnelles"),
          await axios.get("/references/pays"),
        ]);

        if (response[0].status === 200) {
          const data = response[0].data;
          setSetecteurActivites(data.secteurs);
        }

        if (response[1].status === 200) {
          const data = response[1].data;
          console.log(data);
          setPays(data);
        }
      } catch (error) {
        console.error(error);
      }
    }
    getReferencceProfessionel();
  }, []);
  const handleAddMembre = () => {
    setMembres([
      ...membres,
      {
        id: Date.now().toString(),
        email: "",
        role_organisation: "employe",
        role_systeme: "user",
        profil: {
          nom_complet: "",
          status_global: "partenaire",
        },
      },
    ]);
  };

  const handleRemoveMembre = (id: string) => {
    setMembres(membres.filter((m) => m.id !== id));
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const payload = {
        ...formData,
        secteur_activite_id: formData.secteur_activite_id,
        membres: membres.map((membre) => ({
          ...membre,
          profil: {
            ...membre.profil,
            status_global: "partenaire",
          },
          // Omit 'id' by not including it
        })),
      };
      console.log(payload);
      const response = await axios.post("/organisations/", payload);

      if (response.status === 200) {
        toast.success("Organisation créée avec succès");
        // Reset form or navigate
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : "Erreur serveur";
      toast.error(message);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="container mx-auto p-4 md:p-6 max-w-4xl">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">
            {isEdit
              ? "Modifier l'organisation"
              : "Créer une nouvelle organisation"}
          </CardTitle>
          <CardDescription>
            Remplissez les informations de l'organisation
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-6">
          {/* Informations de base */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Informations de base</h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="nom_organisation">
                  Nom de l'organisation{" "}
                  <span className="text-destructive">*</span>
                </Label>
                <Input
                  id="nom_organisation"
                  placeholder="Ex: TotalEnergies"
                  value={formData.nom_organisation}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      nom_organisation: e.target.value,
                    })
                  }
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="type_organisation">
                  Type d'organisation{" "}
                  <span className="text-destructive">*</span>
                </Label>
                <Select
                  value={formData.type_organisation}
                  onValueChange={(value) =>
                    setFormData({ ...formData, type_organisation: value })
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Sélectionner le type" />
                  </SelectTrigger>
                  <SelectContent>
                    {typeOrganisationOptions.map((option) => (
                      <SelectItem key={option.value} value={option.value}>
                        {option.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="secteur_activite">Secteur d'activité</Label>
              <Select
                value={formData.secteur_activite_id}
                onValueChange={(value) =>
                  setFormData({ ...formData, secteur_activite_id: value })
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="Sélectionner le secteur" />
                </SelectTrigger>
                <SelectContent>
                  {secteurActivites.map((option) => (
                    <SelectItem key={option.id} value={option.id}>
                      {option.nom}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                placeholder="Décrivez l'organisation..."
                rows={4}
                value={formData.description}
                onChange={(e) =>
                  setFormData({ ...formData, description: e.target.value })
                }
              />
            </div>
          </div>

          <Separator />

          {/* Coordonnées */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Coordonnées</h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="ville">Ville</Label>
                <Input
                  id="ville"
                  placeholder="Ex: Paris"
                  value={formData.ville}
                  onChange={(e) =>
                    setFormData({ ...formData, ville: e.target.value })
                  }
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="pays">Pays</Label>
                <Select defaultValue={formData.pays} onValueChange={
                  (value) => setFormData({ ...formData, pays: value })
                }>
                  <SelectTrigger>
                    <SelectValue placeholder="Sélectionner le pays" />
                  </SelectTrigger>
                  <SelectContent>
                    {pays.map((option) => (
                      <SelectItem key={option.code} value={option.code}>
                        {option.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="email_general">Email général</Label>
                <Input
                  id="email_general"
                  type="email"
                  placeholder="contact@organisation.com"
                  value={formData.email_general}
                  onChange={(e) =>
                    setFormData({ ...formData, email_general: e.target.value })
                  }
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="telephone_general">Téléphone</Label>
                <Input
                  id="telephone_general"
                  type="tel"
                  placeholder="+237 650 00 00 00"
                  value={formData.telephone_general}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      telephone_general: e.target.value,
                    })
                  }
                />
              </div>
            </div>
          </div>

          <Separator />

          {/* Membres */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold">
                Membres de l'organisation
              </h3>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={handleAddMembre}
              >
                <UserPlus className="mr-2 h-4 w-4" />
                Ajouter un membre
              </Button>
            </div>

            {membres.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground border-2 border-dashed rounded-lg">
                <Users className="mx-auto h-12 w-12 mb-2 opacity-50" />
                <p className="text-sm">Aucun membre ajouté</p>
                <p className="text-xs">
                  Cliquez sur "Ajouter un membre" pour commencer
                </p>
              </div>
            ) : (
              <div className="space-y-3">
                {membres.map((membre, index) => (
                  <Card key={membre.id}>
                    <CardContent className="pt-4">
                      <div className="flex items-start justify-between mb-3">
                        <h4 className="font-medium text-sm">
                          Membre {index + 1}
                        </h4>
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          onClick={() => handleRemoveMembre(membre.id)}
                        >
                          <X className="h-4 w-4" />
                        </Button>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        <div className="space-y-2">
                          <Label htmlFor={`profil-nom-${membre.id}`}>
                            Nom complet
                          </Label>
                          <Input
                            id={`profil-nom-${membre.id}`}
                            placeholder="ex: John Doe"
                            onChange={(e) => {
                              setMembres(
                                membres.map((m) => {
                                  if (m.id === membre.id) {
                                    return {
                                      ...m,
                                      profil: {
                                        ...m.profil,
                                        nom_complet: e.target.value,
                                      },
                                    };
                                  }
                                  return m;
                                })
                              );
                            }}
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor={`profil-email-${membre.id}`}>
                            Email
                          </Label>
                          <Input
                            id={`profil-email-${membre.id}`}
                            placeholder="ex: Email"
                            onChange={(e) => {
                              setMembres(
                                membres.map((m) => {
                                  if (m.id === membre.id) {
                                    return {
                                      ...m,
                                      email: e.target.value,
                                      profil: {
                                        ...m.profil,
                                      },
                                    };
                                  }
                                  return m;
                                })
                              );
                            }}
                          />
                        </div>

                        <div className="space-y-2">
                          <Label htmlFor={`role-${membre.id}`}>Rôle</Label>
                          <Select defaultValue="employe">
                            <SelectTrigger>
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                              {roleOptions.map((option) => (
                                <SelectItem
                                  key={option.value}
                                  value={option.value}
                                >
                                  {option.label}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </div>
        </CardContent>

        <CardFooter className="flex flex-col-reverse sm:flex-row gap-3 border-t pt-6">
          <Button type="button" variant="outline" className="w-full sm:w-auto">
            Annuler
          </Button>
          <Button
            type="button"
            onClick={handleSubmit}
            disabled={isLoading}
            className="w-full sm:w-auto"
          >
            {isEdit ? "Enregistrer les modifications" : "Créer l'organisation"}
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
};

export default NetworkFormPage;
