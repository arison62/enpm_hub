// src/Pages/Profile/Edit.tsx
import { useRef, useState, useEffect } from "react";
import { usePage } from "@inertiajs/react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Switch } from "@/components/ui/switch";
import {
  ChevronsUpDown,
  Check,
} from "lucide-react";
import { toast } from "sonner";
import type { UserComplete } from "@/types/user";
import axios from "@/lib/axios";
import type { PaysOut, ReferencesAcademiquesOut } from "@/types/base";
import { useAuthStore } from "@/stores/authStore";
import Axios from "axios";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import { cn } from "@/lib/utils";

gsap.registerPlugin(useGSAP);

export default function ProfileEdit() {
  const { user } = usePage().props as unknown as { user: UserComplete };
  const setUser = useAuthStore((state) => state.setUser);
  const profil = user.profil;

  const [basicInfo, setBasicInfo] = useState({
    nom_complet: profil.nom_complet || "",
    titre_id: profil.titre?.id || null,
    bio: profil.bio || null,
  });

  const [educationInfo, setEducationInfo] = useState({
    annee_sortie_id: profil.annee_sortie?.id || null,
    domaine_id: profil.domaine?.id || null,
  });

  const [contactInfo, setContactInfo] = useState({
    pays: profil.pays || null,
    ville: profil.ville || null,
    adresse: profil.adresse || null,
    telephone: profil.telephone || null,
  });

  const [professionalInfo, setProfessionalInfo] = useState({
    travailleur: profil.travailleur || false,
  });
  const [references, setReferences] = useState<ReferencesAcademiquesOut | null>(
    null
  );
  const [countries, setCountries] = useState<PaysOut[]>([]);

  const [photo, setPhoto] = useState(profil.photo_profil);
  const [isLoading, setIsLoading] = useState({
    basic: false,
    education: false,
    contact: false,
    professional: false,
    links: false,
    photo: false,
    references: false,
    pays: false,
  });

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
    async function getReferencesAcademique() {
      setIsLoading((prev) => ({ ...prev, references: true }));
      try {
        const response = await axios.get("/references/academiques");
        if (response.status === 200) {
          const data = response.data as ReferencesAcademiquesOut;
          setReferences(data);
        }
      } catch (error) {
        console.error(error);
      } finally {
        setIsLoading((prev) => ({ ...prev, references: false }));
      }
    }
    async function getAllCountries() {
      setIsLoading((prev) => ({ ...prev, countries: true }));
      try {
        const response = await axios.get("/references/pays");
        if (response.status === 200) {
          const data = response.data as PaysOut[];
          setCountries(data);
        }
      } catch (error) {
        console.error(error);
      } finally {
        setIsLoading((prev) => ({ ...prev, countries: false }));
      }
    }
    getAllCountries();
    getReferencesAcademique();
  }, []);
  // Helper to submit section
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const submitSection = async (section: string, data: any) => {
    setIsLoading((prev) => ({ ...prev, [section]: true }));
    try {
      console.log(data);
      const response = await axios.put(`/users/${user.id}`, {
        profil: data,
      });

      if (response.status === 200) {
        setUser(response.data);
        toast.success("Mise à jour effectuée avec succès");
      }
    } catch (error) {
      if (Axios.isAxiosError(error)) {
        toast.error(
          error.response?.data?.detail ||
            "Une erreur s'est produite lors de la mise à jour."
        );
      } else if (error instanceof Error) {
        toast.error("Une erreur s'est produite lors de la mise à jour.");
      }

      console.error(error);
    } finally {
      setIsLoading((prev) => ({ ...prev, [section]: false }));
    }
  };

  // Photo Upload (assuming endpoint POST /api/v1/users/{id}/photo)
  const handlePhotoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setIsLoading((prev) => ({ ...prev, photo: true }));

    axios
      .post(`/users/${user.id}/photo`, formData)
      .then((response) => {
        if (response.status === 200) {
          setPhoto(response.data.photo_profil);
          toast.success("Photo de profil mise à jour avec succès");
        }
      })
      .catch((error) => {
        console.error(error);
        toast.error(
          "Une erreur s'est produite lors de la mise à jour de la photo de profil."
        );
      })
      .finally(() => {
        setIsLoading((prev) => ({ ...prev, photo: false }));
      });
  };

  return (
    <>
      <main
        ref={containerRef}
        className="container mx-auto flex-1 px-4 py-6 md:px-6 md:py-8 max-w-2xl lg:max-w-4xl"
      >
        <div className="space-y-8">
          {/* Photo de Profil */}
          <Card>
            <CardHeader>
              <CardTitle>Photo de Profil</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col items-center gap-4">
              <Avatar className="size-32">
                <AvatarImage src={photo || undefined} alt="Photo de profil" />
                <AvatarFallback>{profil.nom_complet[0]}</AvatarFallback>
              </Avatar>
              <Label htmlFor="photo-upload">
                <Button variant="outline" disabled={isLoading.photo} asChild>
                  <span>
                    {isLoading.photo ? "Téléchargement..." : "Changer la photo"}
                  </span>
                </Button>
              </Label>
              <input
                id="photo-upload"
                type="file"
                accept="image/*"
                className="hidden"
                onChange={handlePhotoUpload}
              />
            </CardContent>
          </Card>

          {/* Infos Basiques (Toujours ouvert) */}
          <Card>
            <CardHeader>
              <CardTitle>Informations Basiques</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="nom_complet">Nom Complet</Label>
                <Input
                  id="nom_complet"
                  value={basicInfo.nom_complet}
                  onChange={(e) =>
                    setBasicInfo({
                      ...basicInfo,
                      nom_complet: e.target.value,
                    })
                  }
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="titre">Titre</Label>

                <Select
                  onValueChange={(e) =>
                    setBasicInfo({ ...basicInfo, titre_id: e })
                  }
                  defaultValue={basicInfo.titre_id || ""}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Ajouter un titre" />
                  </SelectTrigger>
                  <SelectContent>
                    {references?.titres?.map((titre) => (
                      <SelectItem key={titre.id} value={titre.id}>
                        {titre.titre}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="bio">Bio</Label>
                <Textarea
                  id="bio"
                  value={basicInfo.bio || undefined}
                  onChange={(e) =>
                    setBasicInfo({ ...basicInfo, bio: e.target.value })
                  }
                  rows={4}
                />
              </div>
              <Button
                onClick={() => submitSection("basic", basicInfo)}
                disabled={isLoading.basic}
              >
                {isLoading.basic
                  ? "Enregistrement..."
                  : "Enregistrer les infos basiques"}
              </Button>
            </CardContent>
          </Card>

          {/* Accordion pour sections secondaires */}
          <Accordion type="single" collapsible className="space-y-4">
            {/* Éducation */}
            {user.profil.statut_global == "alumni" && (
              <AccordionItem value="education">
                <AccordionTrigger>Éducation</AccordionTrigger>
                <AccordionContent className="space-y-6 pt-4">
                  <div className="space-y-2">
                    <Label htmlFor="annee_sortie">Promotion</Label>

                    <Select
                      onValueChange={(e) =>
                        setEducationInfo({
                          ...educationInfo,
                          annee_sortie_id: e,
                        })
                      }
                      defaultValue={educationInfo.annee_sortie_id || ""}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Votre promotion" />
                      </SelectTrigger>
                      <SelectContent>
                        {references?.annees_promotion?.map((annee_sortie) => (
                          <SelectItem
                            key={annee_sortie.id}
                            value={annee_sortie.id}
                          >
                            {annee_sortie.annee}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="domaine">Domaine</Label>

                    <Select
                      onValueChange={(e) =>
                        setEducationInfo({
                          ...educationInfo,
                          domaine_id: e,
                        })
                      }
                      defaultValue={educationInfo.domaine_id || ""}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Votre domaine" />
                      </SelectTrigger>
                      <SelectContent>
                        {references?.domaines?.map((domaine) => (
                          <SelectItem key={domaine.id} value={domaine.id}>
                            {domaine.nom}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <Button
                    onClick={() => submitSection("education", educationInfo)}
                    disabled={isLoading.education}
                  >
                    {isLoading.education
                      ? "Enregistrement..."
                      : "Enregistrer l'éducation"}
                  </Button>
                </AccordionContent>
              </AccordionItem>
            )}

            {/* Contact */}
            <AccordionItem value="contact">
              <AccordionTrigger>Contact</AccordionTrigger>
              <AccordionContent className="space-y-6 pt-4">
                <div className="space-y-2">
                  <Label htmlFor="telephone">Téléphone</Label>
                  <Input
                    id="telephone"
                    value={contactInfo.telephone || undefined}
                    onChange={(e) =>
                      setContactInfo({
                        ...contactInfo,
                        telephone: e.target.value,
                      })
                    }
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="pays">Pays</Label>
                  <Popover>
                    <PopoverTrigger asChild>
                      <Button
                        variant="outline"
                        role="combobox"
                        className="w-[200px] justify-between"
                      >
                        {contactInfo.pays
                          ? countries.find(
                              (pays) => pays.code === contactInfo.pays
                            )?.name
                          : "Veuillez choisir un pays"}
                        <ChevronsUpDown className="opacity-50" />
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-[200px] p-0">
                      <Command>
                        <CommandInput placeholder="Rechercher un pays..." />
                        <CommandList>
                          <CommandEmpty>Aucun pays trouvé</CommandEmpty>
                          <CommandGroup>
                            {countries.map((pays) => (
                              <CommandItem
                                key={pays.code}
                                value={pays.name}
                                onSelect={() => {
                                  setContactInfo({
                                    ...contactInfo,
                                    pays: pays.code,
                                  });
                                }}
                              >
                                {pays.name}
                                <Check
                                  className={cn(
                                    "ml-auto",
                                    contactInfo.pays == pays.code
                                      ? "opacity-100"
                                      : "opacity-0"
                                  )}
                                />
                              </CommandItem>
                            ))}
                          </CommandGroup>
                        </CommandList>
                      </Command>
                    </PopoverContent>
                  </Popover>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="ville">Ville</Label>
                  <Input
                    id="ville"
                    value={contactInfo.ville || undefined}
                    onChange={(e) =>
                      setContactInfo({
                        ...contactInfo,
                        ville: e.target.value,
                      })
                    }
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="adresse">Adresse Complet</Label>
                  <Input
                    id="adresse"
                    value={contactInfo.adresse || undefined}
                    onChange={(e) =>
                      setContactInfo({
                        ...contactInfo,
                        adresse: e.target.value,
                      })
                    }
                  />
                </div>

                <Button
                  onClick={() => submitSection("contact", contactInfo)}
                  disabled={isLoading.contact}
                >
                  {isLoading.contact
                    ? "Enregistrement..."
                    : "Enregistrer le contact"}
                </Button>
              </AccordionContent>
            </AccordionItem>

            {/* Professionnel */}
            <AccordionItem value="professional">
              <AccordionTrigger>Statut Professionnel</AccordionTrigger>
              <AccordionContent className="space-y-6 pt-4">
                <div className="flex items-center space-x-2">
                  <Switch
                    id="travailleur"
                    checked={professionalInfo.travailleur}
                    onCheckedChange={(checked) =>
                      setProfessionalInfo({
                        ...professionalInfo,
                        travailleur: checked,
                      })
                    }
                  />
                  <Label htmlFor="travailleur">Actuellement employé</Label>
                </div>
                <Button
                  onClick={() =>
                    submitSection("professional", professionalInfo)
                  }
                  disabled={isLoading.professional}
                >
                  {isLoading.professional
                    ? "Enregistrement..."
                    : "Enregistrer le statut pro"}
                </Button>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>
      </main>
    </>
  );
}
