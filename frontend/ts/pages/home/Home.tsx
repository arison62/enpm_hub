import AppLayout from "@/components/layouts/app-layout";
import PostCard from "./components/post-card";
import StoryCircle from "./components/story-circle";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Avatar } from "@/components/ui/avatar";
import type { ReactNode } from "react";

const mockStories = [
  { nom_complet: "Marie Kamga", photo_profil: "/avatars/1.jpg", hasNew: true },
  { nom_complet: "Jean Dupont", hasNew: true },
  { nom_complet: "Aïcha Njoya" },
  { nom_complet: "Paul Biya Jr" },
];

const mockPosts = [
  {
    author: {
      nom_complet: "Fatima Sow",
      poste: "Ingénieure chez SONATEL",
      photo_profil: "/avatars/fatima.jpg",
    },
    content:
      "Très fière d'avoir intégré l'équipe d'ingénieurs réseau chez SONATEL ! Merci à la communauté ENSPM Hub pour le soutien pendant mes recherches.",
    likes: 234,
    comments: 45,
  },
  {
    author: {
      nom_complet: "Fatima Sow",
      poste: "Ingénieure chez SONATEL",
      photo_profil: "/avatars/fatima.jpg",
    },
    content:
      "Très fière d'avoir intégré l'équipe d'ingénieurs réseau chez SONATEL ! Merci à la communauté ENSPM Hub pour le soutien pendant mes recherches.",
    likes: 234,
    comments: 45,
  },
  {
    author: {
      nom_complet: "Fatima Sow",
      poste: "Ingénieure chez SONATEL",
      photo_profil: "/avatars/fatima.jpg",
    },
    content:
      "Très fière d'avoir intégré l'équipe d'ingénieurs réseau chez SONATEL ! Merci à la communauté ENSPM Hub pour le soutien pendant mes recherches.",
    likes: 234,
    comments: 45,
  },
];

function HomePage() {
  return (
    <>
      <Card className="mb-6 p-4">
        <div className="flex gap-4 overflow-x-auto pb-2">
          <div className="flex flex-col items-center gap-2">
            <div className="size-16 rounded-full bg-muted border-2 border-dashed flex items-center justify-center">
              <span className="text-2xl">+</span>
            </div>
            <p className="text-xs">Votre story</p>
          </div>
          {mockStories.map((story, i) => (
            <StoryCircle key={i} user={story} hasNew={story.hasNew} />
          ))}
        </div>
      </Card>

      {/* Create Post */}
      <Card className="mb-6 p-4">
        <div className="flex gap-3">
          <Avatar className="size-10" />
          <Button
            variant="outline"
            className="flex-1 justify-start text-muted-foreground"
          >
            Partager une idée, une opportunité...
          </Button>
        </div>
      </Card>

      {/* Feed */}
      <div>
        {mockPosts.map((post, i) => (
          <PostCard key={i} post={post} />
        ))}
      </div>
    </>
  );
}

HomePage.layout = (page: ReactNode) => <AppLayout>{page}</AppLayout>;
export default HomePage;
