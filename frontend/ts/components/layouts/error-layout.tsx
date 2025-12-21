// frontend/ts/components/layouts/ErrorLayout.tsx
import { type ReactNode, useRef } from "react";
import { Head } from "@inertiajs/react";
import { gsap } from "gsap";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(useGSAP);

interface ErrorLayoutProps {
  children: ReactNode;
  title: string;
}

export default function ErrorLayout({ children, title }: ErrorLayoutProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    gsap.from(containerRef.current, {
      opacity: 0,
      y: 30,
      duration: 0.8,
      ease: "power3.out",
    });
  }, []);

  return (
    <>
      <Head title={title} />
      <div className="min-h-screen bg-background flex items-center justify-center p-6">
        <div
          ref={containerRef}
          className="w-full max-w-md text-center space-y-8"
        >
          {children}
        </div>
      </div>
    </>
  );
}
