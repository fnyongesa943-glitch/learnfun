'use client';

import React from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { cn, getDifficultyColor, getGradeColor } from '@/lib/utils';
import Badge from '@/components/ui/Badge';
import { Clock, HelpCircle, Play } from 'lucide-react';

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
      whileHover={{ y: -4, boxShadow: '0 12px 24px rgba(99,102,241,0.1)' }}
      transition={{ type: 'spring', stiffness: 300 }}
      className="group relative overflow-hidden rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700 shadow-sm"
    >
      <div className={cn('h-1.5 w-full bg-gradient-to-r', color)} />
      <div className="p-5">
        <div className="flex items-center gap-2 mb-3">
          {subjectIcon && (
            <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-surface-100 dark:bg-surface-700 text-surface-600 dark:text-surface-400">
              {subjectIcon}
            </span>
          )}
          <span className="text-xs font-medium text-surface-500">{subject}</span>
          {grade && (
            <span className={cn('text-xs font-medium px-1.5 py-0.5 rounded', getGradeColor(grade))}>
              {grade}
            </span>
          )}
        </div>

        <h3 className="text-sm font-semibold text-surface-900 dark:text-surface-50 mb-2 line-clamp-2">
          {title}
        </h3>

        {description && (
          <p className="text-xs text-surface-500 mb-3 line-clamp-2">{description}</p>
        )}

        <div className="flex items-center flex-wrap gap-2 mb-4">
          <Badge variant={difficulty === 'easy' ? 'success' : difficulty === 'medium' ? 'warning' : 'danger'} size="sm">
            {difficulty}
          </Badge>
          <span className="flex items-center gap-1 text-xs text-surface-400">
            <HelpCircle className="h-3 w-3" />
            {questionCount} questions
          </span>
          <span className="flex items-center gap-1 text-xs text-surface-400">
            <Clock className="h-3 w-3" />
            {timeLimit}min
          </span>
        </div>

        {attempted && score !== undefined && (
          <div className="mb-3">
            <div className="flex items-center justify-between text-xs mb-1">
              <span className="text-surface-500">Best score</span>
              <span className={cn('font-medium', score >= 80 ? 'text-success-500' : score >= 50 ? 'text-accent-500' : 'text-danger-500')}>
                {score}%
              </span>
            </div>
            <div className="h-1.5 rounded-full bg-surface-100 dark:bg-surface-700 overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${score}%` }}
                transition={{ duration: 0.8, ease: 'easeOut' }}
                className={cn('h-full rounded-full', score >= 80 ? 'bg-success-500' : score >= 50 ? 'bg-accent-500' : 'bg-danger-500')}
              />
            </div>
          </div>
        )}

        {progress !== undefined && progress > 0 && (
          <div className="mb-3">
            <div className="flex items-center justify-between text-xs mb-1">
              <span className="text-surface-500">Progress</span>
              <span className="text-primary-500 font-medium">{progress}%</span>
            </div>
            <div className="h-1.5 rounded-full bg-surface-100 dark:bg-surface-700 overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.8, ease: 'easeOut' }}
                className="h-full rounded-full bg-primary-500"
              />
            </div>
          </div>
        )}

        <Link
          href={`/quizzes/${id}`}
          className="inline-flex items-center gap-1.5 text-xs font-medium text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 transition-colors"
          aria-label={`Start quiz: ${title}`}
        >
          <Play className="h-3.5 w-3.5" />
          {attempted ? 'Retry Quiz' : 'Start Quiz'}
        </Link>
      </div>
    </motion.div>
  );
}
