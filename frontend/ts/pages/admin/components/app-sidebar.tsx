import * as React from "react";
import {
  IconAffiliate,
  IconBriefcase,
  IconDashboard,
  IconFileDescription,
  IconFilePencil,
  IconFolder,
  IconHelp,
  IconInnerShadowTop,
  IconSearch,
  IconSettings,
  IconSpeakerphone,
  IconUsers,
} from "@tabler/icons-react";

import { NavOpportunities } from "@/pages/admin/components/nav-opportunities";
import { NavMain } from "@/pages/admin/components/nav-main";
import { NavSecondary } from "@/pages/admin/components/nav-secondary";
import { NavUser } from "@/pages/admin/components/nav-user";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { NavFeeds } from "./nav-feeds";

const data = {
  user: {
    name: "shadcn",
    email: "m@example.com",
    avatar: "/avatars/shadcn.jpg",
  },
  navMain: [
    {
      title: "Dashboard",
      url: "/admin",
      icon: IconDashboard,
    },
    {
      title: "Utilisateurs",
      url: "/admin/users",
      icon: IconUsers,
    },
    {
      title: "Organisations",
      url: "/admin/organisations",
      icon: IconAffiliate,
    },
  ],
  navSecondary: [
    {
      title: "Settings",
      url: "#",
      icon: IconSettings,
    },
    {
      title: "Get Help",
      url: "#",
      icon: IconHelp,
    },
    {
      title: "Search",
      url: "#",
      icon: IconSearch,
    },
  ],
  opportunities: [
    {
      name: "Stages",
      url: "admin/internships",
      icon: IconFolder,
    },
    {
      name: "Emplois",
      url: "admin/jobs",
      icon: IconBriefcase,
    },
    {
      name: "Formations",
      url: "admin/trainings",
      icon: IconFileDescription,
    },
  ],
  feeds: [
    {
      name: "Postes",
      url: "admin/posts",
      icon: IconFilePencil,
    },
    {
      name: "Annonces",
      url: "admin/ads",
      icon: IconSpeakerphone,
    },
  ],
};

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="offcanvas" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              className="data-[slot=sidebar-menu-button]:!p-1.5"
            >
              <a href="#">
                <IconInnerShadowTop className="!size-5" />
                <span className="text-base font-semibold">ENSPM Hub</span>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={data.navMain} />
        <NavOpportunities items={data.opportunities} />
        <NavFeeds items={data.feeds} />
        <NavSecondary items={data.navSecondary} className="mt-auto" />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={data.user} />
      </SidebarFooter>
    </Sidebar>
  );
}
