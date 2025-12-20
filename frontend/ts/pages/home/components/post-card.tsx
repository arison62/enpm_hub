// frontend/ts/pages/home/components/post-card.tsx

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Heart, MessageCircle, Share2, MoreHorizontal } from "lucide-react";
import { useGSAP } from "@gsap/react";
import { gsap } from "gsap";
import { useRef } from "react";

interface PostCardProps {
  post: {
    author: { nom_complet: string; photo_profil?: string; poste?: string };
    content: string;
    image?: string;
    likes: number;
    comments: number;
  };
}

export default function PostCard({ post }: PostCardProps) {
  const cardRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    gsap.from(cardRef.current, {
      opacity: 0,
      y: 30,
      duration: 0.6,
      ease: "power2.out",
    });
  });

  return (
    <Card ref={cardRef} className="mb-6">
      <CardHeader className="flex flex-row items-start gap-4">
        <Avatar>
          <AvatarImage src={post.author.photo_profil} />
          <AvatarFallback>{post.author.nom_complet[0]}</AvatarFallback>
        </Avatar>
        <div className="flex-1">
          <p className="font-semibold">{post.author.nom_complet}</p>
          <p className="text-sm text-muted-foreground">{post.author.poste}</p>
        </div>
        <Button variant="ghost" size="icon">
          <MoreHorizontal className="size-4" />
        </Button>
      </CardHeader>
      <CardContent>
        <p className="mb-4">{post.content}</p>
        {post.image && (
          <img
            src={post.image}
            alt="Post"
            className="rounded-lg w-full object-cover max-h-96"
          />
        )}
        <div className="flex items-center justify-between mt-4 pt-4 border-t">
          <Button variant="ghost" size="sm" className="gap-2">
            <Heart className="size-4" /> {post.likes}
          </Button>
          <Button variant="ghost" size="sm" className="gap-2">
            <MessageCircle className="size-4" /> {post.comments}
          </Button>
          <Button variant="ghost" size="sm">
            <Share2 className="size-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
