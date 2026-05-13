'use client';

import React from 'react';
import { cn } from '@/lib/utils';

interface AvatarProps {
  src?: string;
  alt?: string;
  initials?: string;
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  status?: 'online' | 'offline' | 'away';
  borderColor?: string;
  className?: string;
}

const sizeStyles = {
  xs: 'h-6 w-6 text-[10px]',
  sm: 'h-8 w-8 text-xs',
  md: 'h-10 w-10 text-sm',
  lg: 'h-12 w-12 text-base',
  xl: 'h-16 w-16 text-xl',
};

const statusSizes = {
  xs: 'h-1.5 w-1.5',
  sm: 'h-2 w-2',
  md: 'h-2.5 w-2.5',
  lg: 'h-3 w-3',
  xl: 'h-3.5 w-3.5',
};

const statusColors = {
  online: 'bg-success-500',
  offline: 'bg-surface-400',
  away: 'bg-accent-500',
};

export default function Avatar({
  src,
  alt = '',
  initials,
  size = 'md',
  status,
  borderColor,
  className,
}: AvatarProps) {
  const [error, setError] = React.useState(false);

  return (
    <div className={cn('relative inline-flex shrink-0', className)}>
      {src && !error ? (
        <img
          src={src}
          alt={alt}
          onError={() => setError(true)}
          className={cn(
            'rounded-full object-cover',
            sizeStyles[size],
            borderColor && `ring-2 ring-offset-2 dark:ring-offset-surface-900 ${borderColor}`
          )}
        />
      ) : (
        <div
          className={cn(
            'rounded-full flex items-center justify-center font-semibold bg-gradient-to-br from-primary-400 to-secondary-500 text-white',
            sizeStyles[size],
            borderColor && `ring-2 ring-offset-2 dark:ring-offset-surface-900 ${borderColor}`
          )}
        >
          {initials || alt?.charAt(0)?.toUpperCase() || '?'}
        </div>
      )}
      {status && (
        <span
          className={cn(
            'absolute bottom-0 right-0 rounded-full border-2 border-white dark:border-surface-900',
            statusSizes[size],
            statusColors[status]
          )}
        />
      )}
    </div>
  );
}

export function AvatarGroup({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={cn('flex -space-x-2', className)}>
      {React.Children.map(children, (child) =>
        React.cloneElement(child as React.ReactElement, { className: 'ring-2 ring-white dark:ring-surface-900' })
      )}
    </div>
  );
}
