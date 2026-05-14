export default function DashboardLoading() {
  return (
    <div className="min-h-screen bg-surface-50 dark:bg-surface-900 relative overflow-hidden">
      <div className="absolute inset-0 bg-grid dark:bg-grid-dark pointer-events-none" />
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8 animate-pulse">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div className="space-y-3">
              <div className="h-9 w-72 bg-gradient-to-r from-surface-200 to-surface-300 dark:from-surface-700 dark:to-surface-600 rounded-xl" />
              <div className="h-5 w-52 bg-surface-200 dark:bg-surface-700 rounded-lg" />
            </div>
            <div className="flex gap-3">
              <div className="h-14 w-28 bg-surface-200 dark:bg-surface-700 rounded-2xl" />
              <div className="h-14 w-28 bg-surface-200 dark:bg-surface-700 rounded-2xl" />
            </div>
          </div>

          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-32 bg-white/80 dark:bg-surface-800/80 rounded-2xl border border-surface-200/50 dark:border-surface-700/50" />
            ))}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2 space-y-6">
              <div className="h-80 bg-white/80 dark:bg-surface-800/80 rounded-2xl border border-surface-200/50 dark:border-surface-700/50" />
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="h-52 bg-white/80 dark:bg-surface-800/80 rounded-2xl border border-surface-200/50 dark:border-surface-700/50" />
                ))}
              </div>
            </div>
            <div className="space-y-6">
              {[...Array(2)].map((_, i) => (
                <div key={i} className="h-56 bg-white/80 dark:bg-surface-800/80 rounded-2xl border border-surface-200/50 dark:border-surface-700/50" />
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
