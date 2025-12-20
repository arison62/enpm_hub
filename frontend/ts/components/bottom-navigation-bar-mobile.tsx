import { useRef, useMemo } from "react";
import { gsap } from "gsap";
import { useGSAP } from "@gsap/react";
import { Link, usePage } from "@inertiajs/react";

interface NavItem {
  icon: React.ElementType;
  label: string;
  href: string;
}

export default function BottomNavigationBarMobile({
  items,
}: {
  items: NavItem[];
}) {
  const { url } = usePage();
  const containerRef = useRef<HTMLDivElement>(null);
  const indicatorRef = useRef<HTMLDivElement>(null);
  const isFirstRender = useRef(true);

  // Index de l'élément actif
  const activeIndex = useMemo(() => {
    const index = items.findIndex((item) => item.href === url);
    return index === -1 ? 0 : index;
  }, [url, items]);

  useGSAP(
    () => {
      if (!indicatorRef.current) return;

      // 1. Animation de la barre supérieure
      if (isFirstRender.current) {
        // Au chargement initial : placement immédiat sans glissement depuis le bord
        gsap.set(indicatorRef.current, {
          xPercent: activeIndex * 100,
        });
        isFirstRender.current = false;
      } else {
        // Au clic : glissement fluide (gauche <-> droite)
        gsap.to(indicatorRef.current, {
          xPercent: activeIndex * 100,
          duration: 0.3,
          ease: "power2.out", // Animation nerveuse et fluide
        });
      }

      // 2. Animation des icônes et labels
      items.forEach((_, i) => {
        const isActive = i === activeIndex;
        const icon = `.nav-item-${i} .nav-icon`;
        const label = `.nav-item-${i} .nav-label`;

        // L'icône monte légèrement
        gsap.to(icon, {
          y: isActive ? -2 : 0,
          scale: isActive ? 1.15 : 1,
          color: isActive ? "var(--primary, #3b82f6)" : "#94a3b8",
          duration: 0.4,
        });

        // Le texte apparaît en glissant vers le haut
        gsap.to(label, {
          opacity: isActive ? 1 : 0,
          y: isActive ? 0 : 8,
          duration: 0.3,
          ease: "power2.out",
        });
      });
    },
    { dependencies: [activeIndex], scope: containerRef }
  );

  return (
    <div
      ref={containerRef}
      className="h-16 bg-background border-t border-border flex items-center z-50 px-2"
    >
      {/* Barre d'indication supérieure */}
      <div
        className="absolute top-0 left-0 h-[3px] bg-primary transition-all shadow-[0_-2px_10px_rgba(59,130,246,0.5)]"
        ref={indicatorRef}
        style={{ width: `${100 / items.length}%` }}
      />

      {items.map((item, i) => {
        const isActive = url === item.href;
        return (
          <Link
            key={item.href}
            href={item.href}
            className={`nav-item-${i} relative flex flex-col items-center justify-center flex-1 h-full no-underline`}
          >
            <div className="nav-icon mb-1 transition-colors">
              <item.icon size={24} strokeWidth={isActive ? 2.5 : 2} />
            </div>

            <span
              className="nav-label text-[10px] font-bold uppercase tracking-widest text-primary"
              style={{ opacity: 0 }} // Géré par GSAP
            >
              {item.label}
            </span>
          </Link>
        );
      })}
    </div>
  );
}
