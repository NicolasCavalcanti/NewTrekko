import { Skeleton } from "@/components/ui/skeleton";

export function PageSkeleton() {
  return (
    <div className="min-h-screen bg-background">
      {/* Navbar placeholder */}
      <div className="h-16 border-b border-border px-4 flex items-center gap-4">
        <Skeleton className="h-8 w-32" />
        <div className="flex-1" />
        <Skeleton className="h-8 w-20" />
        <Skeleton className="h-8 w-20" />
        <Skeleton className="h-9 w-9 rounded-full" />
      </div>

      {/* Hero / main content area */}
      <div className="max-w-6xl mx-auto px-4 py-8 space-y-6">
        <Skeleton className="h-10 w-2/3 rounded-lg" />
        <Skeleton className="h-5 w-1/2 rounded" />

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 pt-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="space-y-3">
              <Skeleton className="h-48 w-full rounded-xl" />
              <Skeleton className="h-4 w-3/4 rounded" />
              <Skeleton className="h-4 w-1/2 rounded" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
