import { Deferred, usePage } from "@inertiajs/react";
import { ProfileContent } from "../components/profile-content";
import type { UserProps } from "../types";
import { ProfileSkeleton } from "../components/profile-skeleton";

interface PageProps {
  user: UserProps;
}

export default function ProfileHome() {
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
