import type { OrganisationOut } from "@/types/organisation";

import {
  Card,
  CardHeader,
  CardContent,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

interface OrganisationCardProps {
  org: OrganisationOut;
  onClick: (slug: string) => void;
  follow: () => void;
}

export function OrganisationCard({ org, onClick, follow }: OrganisationCardProps) {
  return (
    <Card
      className="cursor-pointer hover:shadow-md transition-all duration-200 organisation-card overflow-hidden h-full flex flex-col"
      onClick={() => onClick(org.slug)}
    >
      <CardHeader className="pb-3">
        <div className="flex items-center gap-3">
          <Avatar className="h-10 w-10 border">
            <AvatarImage src={org.logo || ""} alt={org.nom_organisation} />
            <AvatarFallback>{org.nom_organisation[0]}</AvatarFallback>
          </Avatar>
          <div className="flex-1 min-w-0">
            <CardTitle className="text-base font-semibold truncate">
              {org.nom_organisation}
            </CardTitle>
            <CardDescription className="text-xs mt-0.5 capitalize">
              {org.type_organisation.replace("_", " ")}
            </CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent className="pt-0 space-y-3 flex-1 flex flex-col justify-between">
        <div className="flex flex-wrap gap-1">
          <Badge variant="secondary" className="text-[10px] px-1.5 py-0">
            {org.secteur_activite?.nom || "Général"}
          </Badge>
          <Badge variant="outline" className="text-[10px] px-1.5 py-0">
            {org.ville}
          </Badge>
        </div>

        <div className="flex justify-between items-center text-xs text-muted-foreground pt-2">
          <span>{org.nombre_abonnes.toLocaleString()} abonnés</span>
          <Button
            variant={org.est_suivi ? "outline" : "default"}
            size="sm"
            disabled={org.est_suivi}
            className="h-7 px-3 text-xs"
            onClick={(e) => {
              e.stopPropagation();
              follow();
            }}
          >
            {org.est_suivi ? "Suivi" : "Suivre"}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
