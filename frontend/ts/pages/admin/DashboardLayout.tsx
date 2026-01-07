import { useEffect } from "react";
import { AppSidebar } from "./components/app-sidebar";
import { SiteHeader } from "./components/site-header";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { useAuthStore } from "@/stores/authStore";
import { router } from "@inertiajs/react";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user } = useAuthStore();
  useEffect(() => {
    // Seulement les admin et super admin peuvent accéder au dashboard
    if (user && !["admin_site", "super_admin"].includes(user.role_systeme)) {
      router.visit("/home"); // Rediriger vers la page d'accueil
    } else if (!user) {
      router.visit("/login"); // Rediriger vers la page de login
    }
  }, [user]);
  return (
    <SidebarProvider
      style={
        {
          "--sidebar-width": "calc(var(--spacing) * 72)",
          "--header-height": "calc(var(--spacing) * 12)",
        } as React.CSSProperties
      }
    >
      <AppSidebar variant="inset" />
      <SidebarInset>
        <SiteHeader />
        {children}
        <div className="flex flex-1 flex-col">{children}</div>
      </SidebarInset>
    </SidebarProvider>
  );
}
