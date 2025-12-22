import { Skeleton } from "@/components/ui/skeleton";
import { Card, CardContent } from "@/components/ui/card";

export const ProfileSkeleton = () => (
  <div className="bg-background pb-12 animate-pulse">
    {/* Banner Skeleton */}
    <div className="h-40 md:h-64 w-full bg-muted" />

    <div className="container mx-auto px-4">
      <div className="relative -mt-16 md:-mt-20 flex flex-col md:flex-row items-center gap-6">
        <Skeleton className="size-32 md:size-44 rounded-full border-4 border-background" />
        <div className="flex-1 space-y-2">
          <Skeleton className="h-10 w-64" />
          <Skeleton className="h-4 w-40" />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mt-12">
        <div className="lg:col-span-4 space-y-6">
          <Card>
            <CardContent className="p-6">
              <Skeleton className="h-24 w-full" />
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <Skeleton className="h-40 w-full" />
            </CardContent>
          </Card>
        </div>
        <div className="lg:col-span-8 space-y-6">
          <Skeleton className="h-10 w-full" />
          <Skeleton className="h-64 w-full" />
        </div>
      </div>
    </div>
  </div>
);
