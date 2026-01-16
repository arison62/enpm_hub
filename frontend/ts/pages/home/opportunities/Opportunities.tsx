import AppLayout from "@/components/layouts/app-layout";
import type { ReactNode } from "react";
import { InternalNavigator } from "@/components/internal-navigator";
import { InternalNavProvider } from "@/contexts/internal-nav-context";
import OpportunitiesHome from "./pages/opportunities-home";

function OpportunitiesPage() {
  return (
    <InternalNavProvider initialPage={OpportunitiesHome} initialTitle="Opportunités">
      <InternalNavigator />
    </InternalNavProvider>
  );
}

OpportunitiesPage.layout = (page: ReactNode) => <AppLayout>{page}</AppLayout>;

export default OpportunitiesPage;
