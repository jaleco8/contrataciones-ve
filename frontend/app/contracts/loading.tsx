export default function ContractsLoading() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-pulse">
      <div className="h-7 bg-ve-slate rounded w-48 mb-2" />
      <div className="h-4 bg-ve-slate rounded w-36 mb-6" />

      <div className="flex gap-2 mb-6">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="h-8 bg-ve-slate rounded-full w-20" />
        ))}
      </div>

      <div className="bg-ve-slate border border-ve-border rounded-xl overflow-hidden">
        <div className="border-b border-ve-border bg-ve-dark/50 h-10" />
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={i} className="border-b border-ve-border/50 px-4 py-4 flex gap-4">
            <div className="flex-1 space-y-2">
              <div className="h-3 bg-ve-border rounded w-24" />
              <div className="h-4 bg-ve-border rounded w-3/4" />
            </div>
            <div className="h-4 bg-ve-border rounded w-24 hidden md:block" />
            <div className="h-6 bg-ve-border rounded w-16" />
          </div>
        ))}
      </div>
    </div>
  );
}
