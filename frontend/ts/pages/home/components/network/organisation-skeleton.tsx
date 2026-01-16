import { Skeleton } from "@/components/ui/skeleton";
import { Card, CardContent, CardHeader } from "@/components/ui/card";

export function OrganisationCardSkeleton() {
  return (
    <Card className="h-[180px]">
      <CardHeader className="pb-3">
        <div className="flex items-center gap-3">
          <Skeleton className="h-10 w-10 rounded-full" />
          <div className="space-y-2 flex-1">
            <Skeleton className="h-4 w-[120px]" />
            <Skeleton className="h-3 w-[80px]" />
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex gap-2">
          <Skeleton className="h-5 w-16" />
          <Skeleton className="h-5 w-20" />
        </div>
        <div className="flex justify-between items-center mt-2">
          <Skeleton className="h-4 w-16" />
          <Skeleton className="h-7 w-20" />
        </div>
      </CardContent>
    </Card>
  );
}

export function SidebarSkeleton() {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <Skeleton className="h-5 w-32" />
        </CardHeader>
        <CardContent className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="flex items-center gap-3">
              <Skeleton className="h-10 w-10 rounded-full" />
              <div className="space-y-2">
                <Skeleton className="h-3 w-24" />
                <Skeleton className="h-3 w-12" />
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
