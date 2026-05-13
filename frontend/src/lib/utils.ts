import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: Date | string): string {
  const d = new Date(date);
  return d.toLocaleDateString('en-KE', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });
}

export function formatTime(seconds: number): string {
  const hrs = Math.floor(seconds / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;
  if (hrs > 0) return `${hrs}h ${mins}m`;
  if (mins > 0) return `${mins}m ${secs}s`;
  return `${secs}s`;
}

export function getGradeColor(grade: string): string {
  const colors: Record<string, string> = {
    PP1: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400',
    PP2: 'bg-teal-100 text-teal-700 dark:bg-teal-900/30 dark:text-teal-400',
    G1: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
    G2: 'bg-cyan-100 text-cyan-700 dark:bg-cyan-900/30 dark:text-cyan-400',
    G3: 'bg-sky-100 text-sky-700 dark:bg-sky-900/30 dark:text-sky-400',
    G4: 'bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-400',
    G5: 'bg-violet-100 text-violet-700 dark:bg-violet-900/30 dark:text-violet-400',
    G6: 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400',
    G7: 'bg-fuchsia-100 text-fuchsia-700 dark:bg-fuchsia-900/30 dark:text-fuchsia-400',
    G8: 'bg-pink-100 text-pink-700 dark:bg-pink-900/30 dark:text-pink-400',
    G9: 'bg-rose-100 text-rose-700 dark:bg-rose-900/30 dark:text-rose-400',
  };
  return colors[grade] || 'bg-surface-100 text-surface-700 dark:bg-surface-800 dark:text-surface-300';
}

export function getDifficultyColor(difficulty: string): string {
  const colors: Record<string, string> = {
    easy: 'text-success-500 bg-success-50 dark:bg-success-500/10',
    medium: 'text-accent-500 bg-accent-50 dark:bg-accent-500/10',
    hard: 'text-danger-500 bg-danger-50 dark:bg-danger-500/10',
  };
  return colors[difficulty] || 'text-surface-500 bg-surface-50 dark:bg-surface-800';
}

export function calculateLevel(points: number): number {
  return Math.floor(points / 100) + 1;
}

export function getProgressPercentage(completed: number, total: number): number {
  if (total === 0) return 0;
  return Math.round((completed / total) * 100);
}
