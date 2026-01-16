import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Calendar, Phone, ExternalLink } from "lucide-react";
import type { UserComplete } from "@/types/user";

export const ProfileSidebar = ({ profil }: { profil: UserComplete["profil"] }) => (
  <div className="lg:col-span-4 space-y-6 animate-fade">
    <Card className="shadow-sm border-none bg-muted/30">
      <CardHeader>
        <CardTitle className="text-lg">À propos</CardTitle>
      </CardHeader>
      <CardContent className="text-sm leading-relaxed text-muted-foreground">
        {profil.bio || "Aucune bio fournie."}
      </CardContent>
    </Card>

    <Card className="shadow-sm border-none">
      <CardHeader>
        <CardTitle className="text-lg">Informations</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {profil.statut_global == "alumni" && profil.annee_sortie && (
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground flex items-center gap-2">
              <Calendar className="size-4" /> Diplômé en
            </span>
            <span className="font-medium">{profil.annee_sortie.annee}</span>
          </div>
        )}

        <div className="flex justify-between text-sm">
          <span className="text-muted-foreground flex items-center gap-2">
            <Phone className="size-4" /> Contact
          </span>
          <span className="font-medium">{profil.telephone}</span>
        </div>
        <hr className="my-2 border-muted" />
        <div className="space-y-2">
          <p className="text-xs font-semibold uppercase text-muted-foreground">
            Réseaux
          </p>
          {profil.liens_reseaux?.map((lien) => (
            <a
              key={lien.id}
              href={lien.url}
              target="_blank"
              className="flex items-center justify-between p-2 rounded-lg hover:bg-muted transition-colors text-sm text-primary"
            >
              {lien.reseau.nom} <ExternalLink className="size-3" />
            </a>
          ))}
        </div>
      </CardContent>
    </Card>
  </div>
);
