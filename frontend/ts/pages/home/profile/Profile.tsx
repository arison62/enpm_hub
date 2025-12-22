import { Deferred, usePage } from "@inertiajs/react";
import { ProfileContent } from "./components/profile-content";
import { ProfileSkeleton } from "./components/profile-skeleton";
import { type UserProps } from "./types";
import AppLayout from "@/components/layouts/app-layout";
import type { ReactNode } from "react";

interface PageProps {
  user: UserProps; 
}

function ProfilePage() {
  return (
    <Deferred data="user" fallback={<ProfileSkeleton />}>
      <ProfileContentWrapper />
    </Deferred>
  );
}


const ProfileContentWrapper = () => {
    const { user } = usePage().props as unknown as PageProps;
  return <ProfileContent user={user} />;
};

ProfilePage.layout = (page : ReactNode) => <AppLayout>{page}</AppLayout>
export default ProfilePage;

