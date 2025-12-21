// frontend/ts/pages/Maintenance.tsx
import { useRef } from "react";
import { Head } from "@inertiajs/react";
import { gsap } from "gsap";
import { useGSAP } from "@gsap/react";
import { Wrench, Clock } from "lucide-react";

gsap.registerPlugin(useGSAP);

export default function Maintenance() {
  const containerRef = useRef<HTMLDivElement>(null);
  const iconRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    const tl = gsap.timeline({ defaults: { ease: "power3.out" } });

    tl.from(containerRef.current, { opacity: 0, y: 40, duration: 1 });

    if (iconRef.current) {
      tl.from(
        iconRef.current,
        { scale: 0.5, opacity: 0, duration: 0.8 },
        "-=0.6"
      );

      // Animation de rotation lente et subtile de l'outil
      gsap.to(iconRef.current.querySelector("svg"), {
        rotation: 360,
        duration: 20,
        repeat: -1,
        ease: "none",
      });
    }
  }, []);

  return (
    <>
      <Head title="Maintenance en cours - ENSPM Hub" />

      <div className="min-h-screen bg-background flex items-center justify-center p-6">
        <div
          ref={containerRef}
          className="w-full max-w-lg text-center space-y-8"
        >
          {/* Icône animée */}
          <div ref={iconRef} className="flex justify-center mb-8">
            <div className="size-32 rounded-full bg-primary/10 flex items-center justify-center">
              <Wrench className="size-16 text-primary" />
            </div>
          </div>

          <h1 className="text-5xl font-bold text-foreground">
            Mode Maintenance
          </h1>
          <p className="text-xl text-muted-foreground">
            Nous sommes actuellement en train d'améliorer ENSPM Hub pour vous
            offrir une meilleure expérience.
          </p>

          <div className="flex flex-col gap-4 items-center">
            <div className="flex items-center gap-3 text-lg text-primary">
              <Clock className="size-6" />
              <span>Retour prévu dans quelques minutes</span>
            </div>

            <p className="text-muted-foreground">
              Merci de votre patience ! <br />
              L'équipe ENSPM Hub
            </p>

          </div>
        </div>
      </div>
    </>
  );
}
