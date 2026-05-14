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
      whileHover={{ y: -4, scale: 1.02 }}
      className={cn(
        'group relative overflow-hidden rounded-2xl p-5',
        'bg-white/80 dark:bg-surface-800/80 backdrop-blur-sm',
        'border border-surface-200/50 dark:border-surface-700/50',
        'shadow-sm hover:shadow-xl hover:shadow-primary-500/5',
        'transition-all duration-300',
        className
      )}
    >
      <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500">
        <div className={cn(
          'absolute -top-1/2 -right-1/2 h-full w-full rounded-full blur-3xl opacity-20 bg-gradient-to-br',
          gradient
        )} />
      </div>
      <div className="relative z-10">
        <div className="flex items-start justify-between">
          <div className="space-y-2.5">
            <p className="text-sm font-medium text-surface-400 dark:text-surface-500 tracking-wide uppercase">
              {label}
            </p>
            <div className="flex items-baseline gap-1">
              <motion.span className="text-3xl font-extrabold text-surface-900 dark:text-surface-50 tracking-tight">
                {rounded}
              </motion.span>
              {suffix && (
                <span className="text-lg font-semibold text-surface-400">{suffix}</span>
              )}
            </div>
            {trend && (
              <div
                className={cn(
                  'flex items-center gap-1.5 text-xs font-semibold',
                  trend.positive ? 'text-success-500' : 'text-danger-500'
                )}
              >
                <div className={cn(
                  'flex items-center justify-center h-5 w-5 rounded-full',
                  trend.positive ? 'bg-success-500/10' : 'bg-danger-500/10'
                )}>
                  {trend.positive ? (
                    <TrendingUp className="h-3 w-3" />
                  ) : (
                    <TrendingDown className="h-3 w-3" />
                  )}
                </div>
                <span>{trend.value}%</span>
                <span className="text-surface-400 font-normal">vs last week</span>
              </div>
            )}
          </div>
          <div
            className={cn(
              'flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br text-white shadow-lg shadow-primary-500/10',
              'group-hover:scale-110 group-hover:shadow-xl group-hover:shadow-primary-500/20',
              'transition-all duration-300',
              gradient
            )}
          >
            {icon}
          </div>
        </div>
      </div>
      <div
        className={cn(
          'absolute -bottom-4 -right-4 h-24 w-24 rounded-full opacity-5 bg-gradient-to-br',
          gradient
        )}
      />
    </motion.div>
  );
}
