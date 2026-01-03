import { Briefcase, MapPin, Calendar, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Empty,
  EmptyHeader,
  EmptyTitle,
  EmptyDescription,
  EmptyContent,
  EmptyMedia,
} from "@/components/ui/empty";
import type { ExperienceProfessionnelleOut } from "@/types/user";

export default function ExperiencesTab({
  experiences,
  isOwnProfile = false,
}: {
  experiences: ExperienceProfessionnelleOut[];
  isOwnProfile?: boolean;
}) {
  // État vide utilisant les composants Shadcn UI
  if (!experiences || experiences.length === 0) {
    return (
      <Empty className="py-12 border-2 border-dashed">
        <EmptyMedia>
          <Briefcase className="h-12 w-12 text-muted-foreground/40" />
        </EmptyMedia>
        <EmptyHeader>
          <EmptyTitle>Aucun parcours professionnel</EmptyTitle>
          <EmptyDescription>
            {isOwnProfile
              ? "Valorisez votre profil en ajoutant vos expériences passées et actuelles."
              : "Cet utilisateur n'a pas encore renseigné ses expériences professionnelles."}
          </EmptyDescription>
        </EmptyHeader>
        {isOwnProfile && (
          <EmptyContent>
            <Button variant="outline" size="sm" className="gap-2">
              <Plus className="h-4 w-4" />
              Ajouter une expérience
            </Button>
          </EmptyContent>
        )}
      </Empty>
    );
  }

  return (
    <div className="animate-in fade-in duration-500">
      {experiences.map((exp, index) => (
        <div key={exp.id} className="group flex gap-4">
          {/* COLONNE GAUCHE : Indicateur visuel (Point et Ligne) */}
          <div className="flex flex-col items-center flex-shrink-0">
            {/* Le cercle entourant l'icône */}
            <div className="relative z-10 flex items-center justify-center w-12 h-12 rounded-full border-2 border-slate-100 bg-white group-hover:border-blue-200 group-hover:shadow-sm transition-all duration-300">
              <Briefcase className="h-5 w-5 text-slate-400 group-hover:text-blue-600 transition-colors" />
            </div>

            {/* La ligne verticale (affichée sauf pour le dernier élément) */}
            {index !== experiences.length - 1 && (
              <div
                className="w-[2px] flex-grow bg-slate-100 group-hover:bg-blue-100 transition-colors"
                aria-hidden="true"
              />
            )}
          </div>

          {/* COLONNE DROITE : Contenu textuel */}
          <div
            className={`flex-1 ${
              index !== experiences.length - 1 ? "pb-10" : "pb-4"
            }`}
          >
            <div className="flex flex-col md:flex-row md:justify-between md:items-start gap-2">
              <div>
                <h3 className="text-lg font-bold text-slate-900 group-hover:text-blue-700 transition-colors">
                  {exp.titre_poste}
                </h3>

                <div className="flex items-center gap-1.5 mt-0.5">
                  <span className="font-semibold text-slate-700">
                    {exp.nom_entreprise}
                  </span>
                </div>

                <div className="flex flex-wrap items-center gap-x-4 gap-y-2 mt-2 text-sm text-muted-foreground">
                  <div className="flex items-center gap-1.5 bg-slate-50 px-2 py-1 rounded-md border border-slate-100">
                    <Calendar className="h-3.5 w-3.5 text-slate-400" />
                    <span className="text-slate-600">
                      {new Date(exp.date_debut).toLocaleDateString("fr-FR", {
                        year: "numeric",
                        month: "long",
                      })}{" "}
                      –{" "}
                      {exp.est_poste_actuel
                        ? "Aujourd'hui"
                        : exp.date_fin
                        ? new Date(exp.date_fin).toLocaleDateString("fr-FR", {
                            year: "numeric",
                            month: "long",
                          })
                        : ""}
                    </span>
                    <span className="mx-1 text-slate-300">•</span>
                    <span className="font-medium text-blue-600/80 italic">
                      {exp.duree_texte}
                    </span>
                  </div>

                  {exp.lieu && (
                    <div className="flex items-center gap-1.5">
                      <MapPin className="h-3.5 w-3.5 text-slate-400" />
                      <span>{exp.lieu}</span>
                    </div>
                  )}
                </div>
              </div>

              {exp.est_poste_actuel && (
                <span className="inline-flex items-center px-3 py-1 rounded-full text-[10px] uppercase tracking-wider font-bold bg-green-50 text-green-700 border border-green-200">
                  Poste actuel
                </span>
              )}
            </div>

            {exp.description && (
              <div className="mt-4 text-sm text-slate-600 leading-relaxed whitespace-pre-line bg-slate-50/30 p-4 rounded-xl border border-slate-100/50 group-hover:border-slate-200 transition-colors">
                {exp.description}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
