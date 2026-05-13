'use client';

import React from 'react';
import { cn } from '@/lib/utils';

interface BadgeProps {
  variant?: 'primary' | 'success' | 'warning' | 'danger' | 'info';
  size?: 'sm' | 'md';
  dot?: boolean;
  pulse?: boolean;
  className?: string;
  children: React.ReactNode;
}

const variantStyles = {
  primary:
    'bg-primary-100 text-primary-700 dark:bg-primary-500/20 dark:text-primary-400 border-primary-200 dark:border-primary-700/30',
  success:
    'bg-success-50 text-success-600 dark:bg-success-500/20 dark:text-success-400 border-success-200 dark:border-success-700/30',
  warning:
    'bg-accent-100 text-accent-700 dark:bg-accent-500/20 dark:text-accent-400 border-accent-200 dark:border-accent-700/30',
  danger:
    'bg-danger-50 text-danger-600 dark:bg-danger-500/20 dark:text-danger-400 border-danger-200 dark:border-danger-700/30',
  info:
    'bg-blue-50 text-blue-700 dark:bg-blue-500/20 dark:text-blue-400 border-blue-200 dark:border-blue-700/30',
};

const sizeStyles = {
  sm: 'px-2 py-0.5 text-xs',
  md: 'px-2.5 py-1 text-sm',
};

const dotColors = {
  primary: 'bg-primary-500',
  success: 'bg-success-500',
  warning: 'bg-accent-500',
  danger: 'bg-danger-500',
  info: 'bg-blue-500',
};

export default function Badge({
  variant = 'primary',
  size = 'sm',
  dot = false,
  pulse = false,
  className,
  children,
}: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full border font-medium',
        variantStyles[variant],
        sizeStyles[size],
        className
      )}
    >
      {dot && (
        <span
          className={cn(
            'h-1.5 w-1.5 rounded-full',
            dotColors[variant],
            pulse && 'animate-pulse'
          )}
        />
      )}
      {children}
    </span>
  );
}
