import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Users, GraduationCap } from "lucide-react";

export const MentorCTA = () => (
  <Card className="border-none shadow-md bg-gradient-to-br from-primary to-indigo-700 text-primary-foreground overflow-hidden relative">
    <CardHeader className="pb-2 relative z-10">
      <CardTitle className="text-lg flex items-center gap-2">
        <Users className="h-5 w-5" /> Trouver un mentor
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-4 relative z-10">
      <p className="text-sm text-indigo-100">
        Besoin de conseils pour votre carrière ? Échangez avec des diplômés
        expérimentés du réseau.
      </p>
      <Button variant="secondary" className="w-full font-bold shadow-sm">
        Explorer le programme
      </Button>
    </CardContent>
    <GraduationCap className="absolute -bottom-4 -right-4 h-24 w-24 opacity-20 rotate-12" />
  </Card>
);
