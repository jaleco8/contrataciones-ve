export default function SuppliersLoading() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-pulse">
      <div className="h-7 bg-ve-slate rounded w-56 mb-2" />
      <div className="h-4 bg-ve-slate rounded w-44 mb-6" />

      <div className="flex gap-2 mb-6">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="h-8 bg-ve-slate rounded-full w-24" />
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="bg-ve-slate border border-ve-border rounded-xl p-5">
            <div className="flex justify-between mb-3">
              <div className="space-y-2 flex-1">
                <div className="h-4 bg-ve-border rounded w-3/4" />
                <div className="h-3 bg-ve-border rounded w-24" />
              </div>
              <div className="h-6 bg-ve-border rounded w-16" />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="h-16 bg-ve-border/50 rounded-lg" />
              <div className="h-16 bg-ve-border/50 rounded-lg" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
