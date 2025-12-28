import React, { useState, useRef } from "react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardFooter,
} from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import {
  Heart,
  MessageCircle,
  Share2,
  Calendar,
  Briefcase,
  Users,
  FileText,
  ArrowRight,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import AppLayout from "@/components/layouts/app-layout";

const HomePage = () => {
  const containerRef = useRef<HTMLDivElement>(null);

  // Animation d'entrée
  useGSAP(
    () => {
      const tl = gsap.timeline();
      tl.from(".animate-in", {
        y: 30,
        opacity: 0,
        stagger: 0.1,
        duration: 0.8,
        ease: "power3.out",
      });
    },
    { scope: containerRef }
  );

  const [posts] = useState([
    {
      id: "1",
      auteur: { nom: "Alice Smith", photo: null },
      contenu:
        "Ravi de voir les dernières avancées en IA appliquées au Génie Civil !",
      likes: 42,
      commentaires: [],
      liked: false,
    },
    {
      id: "2",
      auteur: { nom: "Bob Johnson", photo: null },
      contenu: "Super moment d’échange lors du dernier meetup Alumni à Maroua.",
      likes: 28,
      commentaires: [{ auteur: "Jane", texte: "C’était top !" }],
      liked: true,
    },
  ]);

  return (
    <div
      className="min-h-screen bg-slate-50/50 dark:bg-zinc-950"
      ref={containerRef}
    >
      <div className="container mx-auto px-4 py-6 max-w-7xl">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* SIDEBAR GAUCHE - Masquée sur mobile, Sticky sur Desktop */}
          <aside className="hidden lg:block lg:col-span-3 sticky top-20 space-y-6 animate-in">
            <Card className="overflow-hidden shadow-sm border-none">
              <div className="h-16 bg-gradient-to-r from-blue-600 to-indigo-600" />
              <CardContent className="relative pt-0">
                <Avatar className="absolute top-[-2rem] left-4 size-16 border-4 border-white dark:border-zinc-900 shadow-sm">
                  <AvatarFallback className="bg-blue-100 text-blue-700 font-bold">
                    JD
                  </AvatarFallback>
                </Avatar>
                <div className="pt-10 space-y-1">
                  <h2 className="font-bold text-base">John Doe</h2>
                  <p className="text-xs text-muted-foreground leading-tight">
                    Ingénieur Génie Civil @ ENSPM Alumni
                  </p>
                </div>
                <Separator className="my-4" />
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">
                      Vues du profil
                    </span>
                    <span className="font-medium text-blue-600">124</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Connexions</span>
                    <span className="font-medium text-blue-600">500+</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="shadow-sm border-none">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-semibold flex items-center gap-2">
                  <Calendar className="h-4 w-4 text-blue-600" />
                  Événements
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {[1, 2].map((_, i) => (
                  <div key={i} className="group cursor-pointer">
                    <p className="text-xs font-medium group-hover:text-blue-600 transition-colors">
                      Conférence sur l'IA
                    </p>
                    <p className="text-[10px] text-muted-foreground">
                      15 Jan 2026 • En ligne
                    </p>
                  </div>
                ))}
                <Button
                  variant="ghost"
                  size="sm"
                  className="w-full text-xs h-8"
                >
                  Voir tout
                </Button>
              </CardContent>
            </Card>
          </aside>

          {/* CONTENU CENTRAL - Seul cet élément définit le scroll principal */}
          <main className="lg:col-span-6 space-y-6">
            {/* STATS SIMPLIFIÉES */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 animate-in">
              {[
                { label: "Membres", value: "1.2k", icon: Users },
                { label: "Posts", value: "256", icon: FileText },
                { label: "Events", value: "12", icon: Calendar },
                { label: "Jobs", value: "45", icon: Briefcase },
              ].map((stat, i) => (
                <div
                  key={i}
                  className="bg-white dark:bg-zinc-900 p-3 rounded-xl border border-slate-200 dark:border-zinc-800 flex items-center gap-3 shadow-sm"
                >
                  <div className="p-2 bg-slate-50 dark:bg-zinc-800 rounded-lg">
                    <stat.icon className="h-4 w-4 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-sm font-bold">{stat.value}</p>
                    <p className="text-[10px] text-muted-foreground uppercase tracking-wider">
                      {stat.label}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            {/* FEED */}
            <div className="space-y-4 animate-in">
              {posts.map((post) => (
                <Card key={post.id} className="shadow-sm border-none">
                  <CardHeader className="pb-3 flex-row items-center gap-3">
                    <Avatar className="h-10 w-10">
                      <AvatarFallback className="bg-slate-200">
                        {post.auteur.nom[0]}
                      </AvatarFallback>
                    </Avatar>
                    <div>
                      <p className="text-sm font-semibold">{post.auteur.nom}</p>
                      <p className="text-[10px] text-muted-foreground">
                        Il y a 2 heures
                      </p>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm leading-relaxed">{post.contenu}</p>
                  </CardContent>
                  <Separator />
                  <CardFooter className="py-2 flex justify-between">
                    <Button variant="ghost" size="sm" className="text-xs gap-2">
                      <Heart
                        className={cn(
                          "h-4 w-4",
                          post.liked && "fill-red-500 text-red-500"
                        )}
                      />
                      {post.likes}
                    </Button>
                    <Button variant="ghost" size="sm" className="text-xs gap-2">
                      <MessageCircle className="h-4 w-4" />
                      {post.commentaires.length}
                    </Button>
                    <Button variant="ghost" size="sm" className="text-xs gap-2">
                      <Share2 className="h-4 w-4" />
                      Partager
                    </Button>
                  </CardFooter>
                </Card>
              ))}
            </div>
          </main>

          {/* SIDEBAR DROITE - Masquée sur mobile, Sticky sur Desktop */}
          <aside className="hidden lg:block lg:col-span-3 sticky top-20 animate-in">
            <Card className="shadow-sm border-none">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-semibold flex items-center justify-between">
                  Opportunités
                  <Briefcase className="h-4 w-4 text-blue-600" />
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {[1, 2, 3].map((_, i) => (
                  <div key={i} className="space-y-1 group cursor-pointer">
                    <h4 className="text-xs font-bold group-hover:text-blue-600 transition-colors">
                      Ingénieur Logiciel Fullstack
                    </h4>
                    <p className="text-[10px] text-muted-foreground">
                      Tech Corp • Yaoundé
                    </p>
                    <Badge variant="secondary" className="text-[9px] h-4">
                      CDI
                    </Badge>
                  </div>
                ))}
                <Separator />
                <Button
                  variant="outline"
                  className="w-full text-xs h-9 border-blue-100 text-blue-600 hover:bg-blue-50"
                >
                  Toutes les offres <ArrowRight className="ml-2 h-3 w-3" />
                </Button>
              </CardContent>
            </Card>
          </aside>
        </div>
      </div>
    </div>
  );
};

HomePage.layout = (page: React.ReactNode) => <AppLayout>{page}</AppLayout>;

export default HomePage;
