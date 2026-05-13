'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface ProgressBarProps {
  value?: number;
  max?: number;
  label?: boolean;
  size?: 'sm' | 'md' | 'lg';
  indeterminate?: boolean;
  className?: string;
}

const sizeStyles = {
  sm: 'h-1.5',
  md: 'h-2.5',
  lg: 'h-4',
};

function getColorClass(percentage: number): string {
  if (percentage < 25) return 'bg-danger-500';
  if (percentage < 50) return 'bg-accent-500';
  if (percentage < 75) return 'bg-blue-500';
  return 'bg-success-500';
}

export default function ProgressBar({
  value = 0,
  max = 100,
  label = false,
  size = 'md',
  indeterminate = false,
  className,
}: ProgressBarProps) {
  const percentage = Math.min(Math.round((value / max) * 100), 100);

  return (
    <div className={cn('w-full', className)}>
      {label && (
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs text-surface-500">Progress</span>
          <span className="text-xs font-medium text-surface-700 dark:text-surface-300">
            {percentage}%
          </span>
        </div>
      )}
      <div
        className={cn(
          'w-full rounded-full bg-surface-100 dark:bg-surface-700 overflow-hidden',
          sizeStyles[size]
        )}
        role="progressbar"
        aria-valuenow={indeterminate ? undefined : value}
        aria-valuemin={0}
        aria-valuemax={max}
      >
        {indeterminate ? (
          <motion.div
            className={cn('h-full rounded-full bg-primary-500', sizeStyles[size])}
            animate={{ x: ['-100%', '200%'] }}
            transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut' }}
          />
        ) : (
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${percentage}%` }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
            className={cn(
              'h-full rounded-full transition-colors',
              getColorClass(percentage),
              sizeStyles[size]
            )}
          />
        )}
      </div>
    </div>
  );
}
