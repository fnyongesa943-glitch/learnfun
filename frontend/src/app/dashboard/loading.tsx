export default function DashboardLoading() {
  return (
    <div className="min-h-screen bg-surface-50 dark:bg-surface-900">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8 animate-pulse">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div className="space-y-3">
              <div className="h-8 w-64 bg-surface-200 dark:bg-surface-700 rounded-lg" />
              <div className="h-4 w-48 bg-surface-200 dark:bg-surface-700 rounded" />
            </div>
            <div className="flex gap-3">
              <div className="h-10 w-24 bg-surface-200 dark:bg-surface-700 rounded-xl" />
              <div className="h-10 w-28 bg-surface-200 dark:bg-surface-700 rounded-xl" />
            </div>
          </div>

          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-32 bg-surface-200 dark:bg-surface-700 rounded-xl" />
            ))}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2 space-y-6">
              <div className="h-80 bg-surface-200 dark:bg-surface-700 rounded-xl" />
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="h-44 bg-surface-200 dark:bg-surface-700 rounded-xl" />
                ))}
              </div>
            </div>
            <div className="space-y-6">
              {[...Array(2)].map((_, i) => (
                <div key={i} className="h-52 bg-surface-200 dark:bg-surface-700 rounded-xl" />
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
