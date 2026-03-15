export default function RiskLoading() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-pulse">
      <div className="h-7 bg-ve-slate rounded w-56 mb-2" />
      <div className="h-4 bg-ve-slate rounded w-44 mb-6" />

      <div className="h-14 bg-ve-slate border border-ve-border rounded-xl mb-6" />

      <div className="flex gap-2 mb-6">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="h-8 bg-ve-slate rounded-full w-20" />
        ))}
      </div>

      <div className="space-y-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="bg-ve-slate border border-ve-border rounded-xl p-5">
            <div className="flex justify-between mb-3">
              <div className="flex gap-2">
                <div className="h-6 bg-ve-border rounded w-16" />
                <div className="h-6 bg-ve-border rounded w-28" />
              </div>
              <div className="h-8 bg-ve-border rounded w-12" />
            </div>
            <div className="space-y-2">
              <div className="h-4 bg-ve-border rounded w-full" />
              <div className="h-4 bg-ve-border rounded w-4/5" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
