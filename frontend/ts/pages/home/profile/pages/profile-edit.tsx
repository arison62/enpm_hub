// src/Pages/Profile/Edit.tsx
import { useRef, useState } from "react";
import { Head, Link, router, usePage } from "@inertiajs/react";
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
import { Trash2, Plus, ExternalLink, Edit2 } from "lucide-react";
import { toast } from "sonner";

gsap.registerPlugin(useGSAP);

interface LienReseau {
  id?: string;
  nom_reseau: string;
  url: string;
  est_actif?: boolean;
}

interface ProfilData {
  nom_complet: string;
  matricule?: string;
  titre?: string;
  statut_global?: string;
  travailleur?: boolean;
  annee_sortie?: number;
  telephone?: string;
  domaine?: string;
  bio?: string;
  adresse?: string;
  photo_profil?: string;
  liens_reseaux?: LienReseau[];
}

interface UserProps {
  id: string;
  email: string;
  role_systeme: "user" | "admin_site" | "super_admin";
  est_actif: boolean;
  last_login: string;
  created_at: string;
  updated_at: string;
  profil: ProfilData;
}

export default function ProfileEdit() {
  // Props from Inertia (user data pre-filled)
  const { user } = usePage().props as { user: UserProps };
  const profil = user.profil;

  // States for each section (independent editing)
  const [basicInfo, setBasicInfo] = useState({
    nom_complet: profil.nom_complet,
    titre: profil.titre || "",
    bio: profil.bio || "",
  });

  const [educationInfo, setEducationInfo] = useState({
    statut_global: profil.statut_global || "",
    annee_sortie: profil.annee_sortie || 0,
    domaine: profil.domaine || "",
  });

  const [contactInfo, setContactInfo] = useState({
    telephone: profil.telephone || "",
    adresse: profil.adresse || "",
  });

  const [professionalInfo, setProfessionalInfo] = useState({
    travailleur: profil.travailleur || false,
    // Add poste if available in schema
  });

  const [socialLinks, setSocialLinks] = useState<LienReseau[]>(
    profil.liens_reseaux || []
  );
  const [newLink, setNewLink] = useState({ nom_reseau: "", url: "" });
  const [editingLinkId, setEditingLinkId] = useState<string | null>(null);

  const [photo, setPhoto] = useState(profil.photo_profil);
  const [isLoading, setIsLoading] = useState({
    basic: false,
    education: false,
    contact: false,
    professional: false,
    links: false,
    photo: false,
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

  // Helper to submit section
  const submitSection = async (section: string, data: any) => {
    setIsLoading((prev) => ({ ...prev, [section]: true }));
    router.patch(`/api/v1/users/${user.id}/profil`, data, {
      onSuccess: () => {
        toast(`Section ${section} mise à jour.`);
      },
      onError: (errors) => {
        toast("Échec de la mise à jour.");
      },
      onFinish: () => {
        setIsLoading((prev) => ({ ...prev, [section]: false }));
      },
    });
  };

  // Add or Edit Social Link
  const handleAddOrEditLink = () => {
    if (!newLink.nom_reseau || !newLink.url) return;

    let updatedLinks;
    if (editingLinkId) {
      updatedLinks = socialLinks.map((link) =>
        link.id === editingLinkId ? { ...link, ...newLink } : link
      );
    } else {
      updatedLinks = [...socialLinks, { ...newLink }];
    }

    setSocialLinks(updatedLinks);
    submitSection("links", { liens_reseaux: updatedLinks });
    setNewLink({ nom_reseau: "", url: "" });
    setEditingLinkId(null);
  };

  // Remove Social Link
  const handleRemoveLink = (id: string) => {
    const updatedLinks = socialLinks.filter((link) => link.id !== id);
    setSocialLinks(updatedLinks);
    submitSection("links", { liens_reseaux: updatedLinks });
  };

  // Photo Upload (assuming endpoint POST /api/v1/users/{id}/photo)
  const handlePhotoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("photo_profil", file);

    setIsLoading((prev) => ({ ...prev, photo: true }));
    router.post(`/api/v1/users/${user.id}/photo`, formData, {
      onSuccess: (page) => {
        setPhoto(page.props.user.profil.photo_profil); // Update from response
        toast("Photo mise à jour.");
      },
      onError: () => {
        toast("Échec du téléchargement.");
      },
      onFinish: () => {
        setIsLoading((prev) => ({ ...prev, photo: false }));
      },
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
                <AvatarImage src={photo} alt="Photo de profil" />
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
                <Input
                  id="titre"
                  value={basicInfo.titre}
                  onChange={(e) =>
                    setBasicInfo({ ...basicInfo, titre: e.target.value })
                  }
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="bio">Bio</Label>
                <Textarea
                  id="bio"
                  value={basicInfo.bio}
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
            <AccordionItem value="education">
              <AccordionTrigger>Éducation & Statut</AccordionTrigger>
              <AccordionContent className="space-y-6 pt-4">
                <div className="space-y-2">
                  <Label htmlFor="statut_global">Statut Global</Label>
                  <Select
                    value={educationInfo.statut_global}
                    onValueChange={(value) =>
                      setEducationInfo({
                        ...educationInfo,
                        statut_global: value,
                      })
                    }
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Sélectionnez votre statut" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="etudiant">Étudiant</SelectItem>
                      <SelectItem value="alumni">Alumni</SelectItem>
                      <SelectItem value="enseignant">Enseignant</SelectItem>
                      <SelectItem value="personnel_admin">
                        Personnel Admin
                      </SelectItem>
                      <SelectItem value="personnel_technique">
                        Personnel Technique
                      </SelectItem>
                      <SelectItem value="partenaire">Partenaire</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="annee_sortie">Année de Sortie</Label>
                  <Input
                    id="annee_sortie"
                    type="number"
                    value={educationInfo.annee_sortie}
                    onChange={(e) =>
                      setEducationInfo({
                        ...educationInfo,
                        annee_sortie: parseInt(e.target.value),
                      })
                    }
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="domaine">Domaine</Label>
                  <Input
                    id="domaine"
                    value={educationInfo.domaine}
                    onChange={(e) =>
                      setEducationInfo({
                        ...educationInfo,
                        domaine: e.target.value,
                      })
                    }
                  />
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

            {/* Contact */}
            <AccordionItem value="contact">
              <AccordionTrigger>Contact</AccordionTrigger>
              <AccordionContent className="space-y-6 pt-4">
                <div className="space-y-2">
                  <Label htmlFor="telephone">Téléphone</Label>
                  <Input
                    id="telephone"
                    value={contactInfo.telephone}
                    onChange={(e) =>
                      setContactInfo({
                        ...contactInfo,
                        telephone: e.target.value,
                      })
                    }
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="adresse">Adresse</Label>
                  <Input
                    id="adresse"
                    value={contactInfo.adresse}
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

            {/* Liens Réseaux */}
            <AccordionItem value="social">
              <AccordionTrigger>Réseaux Sociaux</AccordionTrigger>
              <AccordionContent className="space-y-6 pt-4">
                {/* Liste des liens existants */}
                {socialLinks.map((link) => (
                  <div
                    key={link.id || link.url}
                    className="flex items-center gap-2"
                  >
                    <Input
                      value={link.nom_reseau}
                      className="flex-1"
                      disabled
                    />
                    <Input value={link.url} className="flex-1" disabled />
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => {
                        setNewLink({
                          nom_reseau: link.nom_reseau,
                          url: link.url,
                        });
                        setEditingLinkId(link.id!);
                      }}
                    >
                      <Edit2 className="size-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => handleRemoveLink(link.id!)}
                    >
                      <Trash2 className="size-4" />
                    </Button>
                  </div>
                ))}

                {/* Formulaire d'ajout/édition */}
                <div className="space-y-2">
                  <Label>Ajouter/Modifier un Lien</Label>
                  <div className="flex gap-2">
                    <Input
                      placeholder="Nom du réseau (ex. LinkedIn)"
                      value={newLink.nom_reseau}
                      onChange={(e) =>
                        setNewLink({ ...newLink, nom_reseau: e.target.value })
                      }
                    />
                    <Input
                      placeholder="URL"
                      value={newLink.url}
                      onChange={(e) =>
                        setNewLink({ ...newLink, url: e.target.value })
                      }
                    />
                  </div>
                  <Button
                    onClick={handleAddOrEditLink}
                    disabled={isLoading.links}
                  >
                    {isLoading.links
                      ? "Enregistrement..."
                      : editingLinkId
                      ? "Modifier"
                      : "Ajouter"}
                  </Button>
                </div>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>
      </main>
    </>
  );
}
