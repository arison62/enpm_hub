import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";
import { useInternalNav } from "@/contexts/internal-nav-context";
import { NavHeader } from "@/components/internal-nav-header";

export const InternalNavigator = () => {
  const { stack } = useInternalNav();
  const containerRef = useRef<HTMLDivElement>(null);
  const lastStackCount = useRef(stack.length);

  useGSAP(
    () => {
      const pages = gsap.utils.toArray<HTMLElement>(".internal-page");
      const isPush = stack.length > lastStackCount.current;
      const isPop = stack.length < lastStackCount.current;

      const topPage = pages[pages.length - 1];
      const prevPage = pages[pages.length - 2];

      if (isPush && topPage) {
        // Animation d'entrée (Glisse vers la gauche)
        gsap.fromTo(
          topPage,
          { x: "100%", opacity: 0 },
          { x: "0%", opacity: 1, duration: 0.5, ease: "power3.out" }
        );
        if (prevPage) {
          gsap.to(prevPage, {
            x: "-30%",
            opacity: 0.5,
            duration: 0.5,
            ease: "power3.out",
          });
        }
      }

      if (isPop && prevPage) {
        // La page actuelle (celle qui va disparaître) est déjà gérée par React
        // Mais on anime le retour de la page précédente
        gsap.fromTo(
          prevPage,
          { x: "-30%", opacity: 0.5 },
          { x: "0%", opacity: 1, duration: 0.4, ease: "power3.out" }
        );
      }

      lastStackCount.current = stack.length;
    },
    { dependencies: [stack.length], scope: containerRef }
  );

  return (
    <div>
      <NavHeader />
      <main ref={containerRef} className="flex-1bg-muted/20">
        {stack.map((item, index) => {
          const Component = item.component;
          const isVisible = index === stack.length - 1;

          if (!isVisible) return null; // Optimisation : on ne rend que la dernière page

          return (
            <div
              key={item.id}
              className="w-full h-full internal-page"
              style={{ zIndex: index }}
            >
              <Component {...item.props} />
            </div>
          );
        })}
      </main>
    </div>
  );
};
