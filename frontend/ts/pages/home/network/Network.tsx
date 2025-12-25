import AppLayout from "@/components/layouts/app-layout";
import type { ReactNode } from "react";
import { InternalNavigator } from "@/components/internal-navigator";
import { InternalNavProvider } from "@/contexts/internal-nav-context";
import NetworkHome from "./pages/network-home";

function NetworkPage() {
  return (
    <InternalNavProvider initialPage={NetworkHome} initialTitle="Réseau">
      <InternalNavigator />
    </InternalNavProvider>
  );
}

NetworkPage.layout = (page: ReactNode) => <AppLayout>{page}</AppLayout>;

export default NetworkPage;
