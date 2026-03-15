export default function DashboardLoading() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-pulse">
      {/* Hero skeleton */}
      <div className="mb-10">
        <div className="h-8 bg-ve-slate rounded w-64 mb-2" />
        <div className="h-4 bg-ve-slate rounded w-48" />
      </div>

      {/* Stats grid skeleton */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-10">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="bg-ve-slate border border-ve-border rounded-xl p-5">
            <div className="h-8 w-8 bg-ve-border rounded-lg mb-3" />
            <div className="h-8 bg-ve-border rounded w-16 mb-2" />
            <div className="h-3 bg-ve-border rounded w-24" />
          </div>
        ))}
      </div>

      {/* Content grid skeleton */}
      <div className="grid lg:grid-cols-2 gap-6">
        {Array.from({ length: 2 }).map((_, i) => (
          <div key={i} className="bg-ve-slate border border-ve-border rounded-xl p-6">
            <div className="h-4 bg-ve-border rounded w-40 mb-5" />
            <div className="space-y-3">
              {Array.from({ length: 4 }).map((_, j) => (
                <div key={j} className="h-16 bg-ve-border/50 rounded-lg" />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
