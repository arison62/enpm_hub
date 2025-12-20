import React, { useRef, useMemo } from "react";
import { Link, usePage } from "@inertiajs/react";
import { gsap } from "gsap";
import { useGSAP } from "@gsap/react";
import { cn } from "@/lib/utils";

interface NavItem {
  icon: React.ElementType;
  label: string;
  href: string;
  badge?: boolean;
}

export default function DesktopNavLinks({
  items,
  className,
}: {
  items: NavItem[];
  className?: string;
}) {
  const { url } = usePage();
  const containerRef = useRef<HTMLDivElement>(null);
  const indicatorRef = useRef<HTMLDivElement>(null);
  const itemsRef = useRef<(HTMLAnchorElement | null)[]>([]);
  const isFirstRender = useRef(true);

  // Calcul de l'index actif basé sur l'URL actuelle
  const activeIndex = useMemo(() => {
    return items.findIndex((item) => item.href === url);
  }, [url, items]);

  useGSAP(
    () => {
      // Si aucun item n'est actif, on cache l'indicateur
      if (activeIndex === -1 || !indicatorRef.current) {
        gsap.to(indicatorRef.current, { opacity: 0, duration: 0.3 });
        return;
      }

      const activeEl = itemsRef.current[activeIndex];
      const container = containerRef.current;
      if (!activeEl || !container) return;

      // Calcul précis de la position et largeur de l'élément actif
      const itemRect = activeEl.getBoundingClientRect();
      const containerRect = container.getBoundingClientRect();
      const xPosition = itemRect.left - containerRect.left;
      const itemWidth = itemRect.width;

      if (isFirstRender.current) {
        // Premier rendu : placement instantané
        gsap.set(indicatorRef.current, {
          x: xPosition,
          width: itemWidth,
          opacity: 1,
        });
        isFirstRender.current = false;
      } else {
        // Navigation : glissement fluide de la barre
        gsap.to(indicatorRef.current, {
          x: xPosition,
          width: itemWidth,
          opacity: 1,
          duration: 0.6,
          ease: "elastic.out(1, 0.8)", // Effet haut de gamme
        });
      }

      // Animation subtile des couleurs des liens
      items.forEach((_, i) => {
        gsap.to(itemsRef.current[i], {
          color: i === activeIndex ? "var(--primary)" : "#64748b",
          duration: 0.3,
        });
      });
    },
    { dependencies: [activeIndex], scope: containerRef }
  );

  return (
    <nav ref={containerRef} className={cn("relative flex items-center gap-1 h-full", className)}>
      {/* Barre d'indication (Indicateur horizontal) */}
      <div
        ref={indicatorRef}
        className="absolute bottom-[-2px] left-0 h-[2.5px] bg-primary rounded-full shadow-[0_0_10px_rgba(59,130,246,0.3)] pointer-events-none"
        style={{ opacity: 0 }}
      />

      {items.map((item, i) => (
        <Link
          key={item.href}
          href={item.href}
          ref={(el) => {
            if (el instanceof HTMLAnchorElement || el === null) {
              itemsRef.current[i] = el;
            }
          }}
          className="relative px-4 py-2 flex flex-col xl:flex-row items-center gap-2 text-sm font-medium transition-colors hover:text-primary group no-underline"
        >
          <item.icon className="size-4" strokeWidth={2.5} />
          <span>{item.label}</span>

          {item.badge && (
            <span className="absolute top-1 right-2 size-2 rounded-full bg-destructive" />
          )}
        </Link>
      ))}
    </nav>
  );
}
