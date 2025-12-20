// frontend/ts/pages/home/components/story-circle.tsx

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

interface StoryCircleProps {
  user: { nom_complet: string; photo_profil?: string };
  hasNew?: boolean;
}

export default function StoryCircle({
  user,
  hasNew = false,
}: StoryCircleProps) {
  return (
    <div className="flex flex-col items-center gap-2">
      <div
        className={`relative ${
          hasNew
            ? "p-1 bg-gradient-to-tr from-yellow-400 to-pink-600 rounded-full"
            : ""
        }`}
      >
        <Avatar className="size-16 border-4 border-background">
          <AvatarImage src={user.photo_profil} />
          <AvatarFallback>{user.nom_complet[0]}</AvatarFallback>
        </Avatar>
        {hasNew && (
          <div className="absolute bottom-0 right-0 size-4 rounded-full bg-primary border-2 border-background" />
        )}
      </div>
      <p className="text-xs text-center max-w-16 truncate">
        {user.nom_complet.split(" ")[0]}
      </p>
    </div>
  );
}
