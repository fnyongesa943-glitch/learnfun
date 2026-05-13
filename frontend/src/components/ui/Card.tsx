'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface CardProps {
  variant?: 'default' | 'interactive' | 'bordered' | 'flat';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  icon?: React.ReactNode;
  title?: string;
  subtitle?: string;
  footer?: React.ReactNode;
  glass?: boolean;
  className?: string;
  children?: React.ReactNode;
  onClick?: () => void;
}

const paddingVariants = {
  none: '',
  sm: 'p-3',
  md: 'p-5',
  lg: 'p-7',
};

const variantStyles = {
  default: 'bg-white dark:bg-surface-800 shadow-sm border border-surface-200 dark:border-surface-700',
  interactive:
    'bg-white dark:bg-surface-800 shadow-sm border border-surface-200 dark:border-surface-700 cursor-pointer',
  bordered: 'border-2 border-surface-200 dark:border-surface-700',
  flat: 'bg-surface-50 dark:bg-surface-800/50',
};

export default function Card({
  variant = 'default',
  padding = 'md',
  icon,
  title,
  subtitle,
  footer,
  glass = false,
  className,
  children,
  onClick,
}: CardProps) {
  const Component = variant === 'interactive' ? motion.div : 'div';
  const motionProps =
    variant === 'interactive'
      ? {
          whileHover: { y: -4, boxShadow: '0 12px 24px rgba(99,102,241,0.1)' },
          whileTap: { y: -2 },
          transition: { type: 'spring', stiffness: 300 },
        }
      : {};

  return (
    <Component
      className={cn(
        'rounded-xl overflow-hidden',
        variantStyles[variant],
        paddingVariants[padding],
        glass && 'glass-card',
        className
      )}
      onClick={onClick}
      {...motionProps}
    >
      {(icon || title || subtitle) && (
        <div className="flex items-start gap-3 mb-3">
          {icon && <div className="shrink-0">{icon}</div>}
          <div className="flex-1 min-w-0">
            {title && (
              <h3 className="text-sm font-semibold text-surface-900 dark:text-surface-50">
                {title}
              </h3>
            )}
            {subtitle && (
              <p className="text-xs text-surface-500 mt-0.5">{subtitle}</p>
            )}
          </div>
        </div>
      )}
      {children}
      {footer && (
        <div className="mt-4 pt-3 border-t border-surface-100 dark:border-surface-700">
          {footer}
        </div>
      )}
    </Component>
  );
}
