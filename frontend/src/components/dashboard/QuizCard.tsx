'use client';

import React from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { cn, getDifficultyColor, getGradeColor } from '@/lib/utils';
import Badge from '@/components/ui/Badge';
import { Clock, HelpCircle, Play, Sparkles, ArrowRight } from 'lucide-react';

interface QuizCardProps {
  id: string;
  title: string;
  description?: string;
  subject: string;
  subjectIcon?: React.ReactNode;
  grade?: string;
  difficulty: string;
  questionCount: number;
  timeLimit: number;
  attempted?: boolean;
  score?: number;
  progress?: number;
  color?: string;
}

export default function QuizCard({
  id,
  title,
  description,
  subject,
  subjectIcon,
  grade,
  difficulty,
  questionCount,
  timeLimit,
  attempted,
  score,
  progress,
  color = 'from-primary-400 to-secondary-500',
}: QuizCardProps) {
  return (
    <motion.div
      whileHover={{ y: -6, scale: 1.02 }}
      transition={{ type: 'spring', stiffness: 300, damping: 20 }}
      className="group relative overflow-hidden rounded-2xl bg-white/80 dark:bg-surface-800/80 backdrop-blur-sm border border-surface-200/50 dark:border-surface-700/50 shadow-sm hover:shadow-xl hover:shadow-primary-500/5 transition-all duration-300"
    >
      <div className={cn('h-2 w-full bg-gradient-to-r', color)} />
      <div className="absolute top-0 right-0 w-32 h-32 opacity-0 group-hover:opacity-100 transition-all duration-500">
        <div className={cn(
          'absolute top-0 right-0 w-full h-full rounded-bl-full blur-2xl opacity-20 bg-gradient-to-br',
          color
        )} />
      </div>
      <div className="relative z-10 p-5">
        <div className="flex items-center gap-2 mb-3">
          {subjectIcon ? (
            <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-surface-100 dark:bg-surface-700 text-surface-600 dark:text-surface-400">
              {subjectIcon}
            </span>
          ) : (
            <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-gradient-to-br from-primary-500/10 to-secondary-500/10 text-primary-600 dark:text-primary-400">
              <Sparkles className="h-3.5 w-3.5" />
            </span>
          )}
          <span className="text-xs font-semibold text-surface-400 uppercase tracking-wide">{subject}</span>
          {grade && (
            <span className={cn('text-xs font-medium px-1.5 py-0.5 rounded', getGradeColor(grade))}>
              {grade}
            </span>
          )}
        </div>

        <h3 className="text-base font-bold text-surface-900 dark:text-surface-50 mb-2 line-clamp-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
          {title}
        </h3>

        {description && (
          <p className="text-xs text-surface-500 mb-4 line-clamp-2">{description}</p>
        )}

        <div className="flex items-center flex-wrap gap-2 mb-4">
          <Badge variant={difficulty === 'easy' ? 'success' : difficulty === 'medium' ? 'warning' : 'danger'} size="sm">
            {difficulty}
          </Badge>
          <span className="flex items-center gap-1.5 text-xs text-surface-400 bg-surface-100 dark:bg-surface-700/50 px-2 py-1 rounded-lg">
            <HelpCircle className="h-3 w-3" />
            {questionCount} questions
          </span>
          <span className="flex items-center gap-1.5 text-xs text-surface-400 bg-surface-100 dark:bg-surface-700/50 px-2 py-1 rounded-lg">
            <Clock className="h-3 w-3" />
            {timeLimit}min
          </span>
        </div>

        {attempted && score !== undefined && (
          <div className="mb-4">
            <div className="flex items-center justify-between text-xs mb-1.5">
              <span className="text-surface-400 font-medium">Best score</span>
              <span className={cn('font-bold', score >= 80 ? 'text-success-500' : score >= 50 ? 'text-accent-500' : 'text-danger-500')}>
                {score}%
              </span>
            </div>
            <div className="h-2 rounded-full bg-surface-100 dark:bg-surface-700 overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${score}%` }}
                transition={{ duration: 0.8, ease: 'easeOut' }}
                className={cn('h-full rounded-full relative', score >= 80 ? 'bg-success-500' : score >= 50 ? 'bg-accent-500' : 'bg-danger-500')}
              >
                <div className="absolute inset-0 bg-white/20 rounded-full animate-pulse-slow" />
              </motion.div>
            </div>
          </div>
        )}

        {progress !== undefined && progress > 0 && (
          <div className="mb-4">
            <div className="flex items-center justify-between text-xs mb-1.5">
              <span className="text-surface-400 font-medium">Progress</span>
              <span className="text-primary-500 font-bold">{progress}%</span>
            </div>
            <div className="h-2 rounded-full bg-surface-100 dark:bg-surface-700 overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.8, ease: 'easeOut' }}
                className="h-full rounded-full bg-gradient-to-r from-primary-500 to-secondary-500 relative"
              >
                <div className="absolute inset-0 bg-white/20 rounded-full animate-pulse-slow" />
              </motion.div>
            </div>
          </div>
        )}

        <Link
          href={`/quizzes/${id}`}
          className="inline-flex items-center gap-2 text-sm font-semibold text-white bg-gradient-to-r from-primary-500 to-secondary-500 hover:from-primary-600 hover:to-secondary-600 px-4 py-2 rounded-xl shadow-lg shadow-primary-500/20 hover:shadow-xl hover:shadow-primary-500/30 transition-all duration-300 group/link"
          aria-label={`Start quiz: ${title}`}
        >
          <Play className="h-4 w-4" />
          <span>{attempted ? 'Retry Quiz' : 'Start Quiz'}</span>
          <ArrowRight className="h-3.5 w-3.5 group-hover/link:translate-x-0.5 transition-transform" />
        </Link>
      </div>
    </motion.div>
  );
}
