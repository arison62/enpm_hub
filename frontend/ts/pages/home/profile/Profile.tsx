import AppLayout from "@/components/layouts/app-layout";
import type { ReactNode } from "react";
import { InternalNavProvider } from "@/contexts/internal-nav-context";
import ProfileHome from "./pages/profile-home";
import { InternalNavigator } from "@/components/internal-navigator";


function ProfilePage() {
  return (
    <InternalNavProvider initialPage={ProfileHome} initialTitle="Profile">
      <InternalNavigator />
    </InternalNavProvider>
  );
}



ProfilePage.layout = (page : ReactNode) => <AppLayout>{page}</AppLayout>
export default ProfilePage;

