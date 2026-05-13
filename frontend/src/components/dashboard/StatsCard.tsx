'use client';

import React, { useEffect, useRef } from 'react';
import { motion, useInView, useMotionValue, useSpring, useTransform } from 'framer-motion';
import { cn } from '@/lib/utils';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface StatsCardProps {
  icon: React.ReactNode;
  label: string;
  value: number;
  suffix?: string;
  trend?: { value: number; positive: boolean };
  gradient?: string;
  className?: string;
}

export default function StatsCard({
  icon,
  label,
  value,
  suffix = '',
  trend,
  gradient = 'from-primary-500 to-secondary-500',
  className,
}: StatsCardProps) {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true });
  const count = useMotionValue(0);
  const spring = useSpring(count, { stiffness: 80, damping: 20 });
  const rounded = useTransform(spring, (v) => Math.round(v));

  useEffect(() => {
    if (inView) {
      count.set(value);
    }
  }, [inView, value, count]);

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 20 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.5, ease: 'easeOut' }}
      className={cn(
        'relative overflow-hidden rounded-xl p-5 bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700 shadow-sm',
        className
      )}
    >
      <div className="flex items-start justify-between">
        <div className="space-y-2">
          <p className="text-sm text-surface-500 dark:text-surface-400">{label}</p>
          <div className="flex items-baseline gap-1">
            <motion.span className="text-2xl font-bold text-surface-900 dark:text-surface-50">
              {rounded}
            </motion.span>
            {suffix && (
              <span className="text-sm font-medium text-surface-500">{suffix}</span>
            )}
          </div>
          {trend && (
            <div
              className={cn(
                'flex items-center gap-1 text-xs font-medium',
                trend.positive ? 'text-success-500' : 'text-danger-500'
              )}
            >
              {trend.positive ? (
                <TrendingUp className="h-3.5 w-3.5" />
              ) : (
                <TrendingDown className="h-3.5 w-3.5" />
              )}
              <span>{trend.value}%</span>
              <span className="text-surface-400">vs last week</span>
            </div>
          )}
        </div>
        <div
          className={cn(
            'flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br text-white shadow-lg',
            gradient
          )}
        >
          {icon}
        </div>
      </div>
      <div
        className={cn(
          'absolute -bottom-4 -right-4 h-20 w-20 rounded-full opacity-10 bg-gradient-to-br',
          gradient
        )}
      />
    </motion.div>
  );
}
