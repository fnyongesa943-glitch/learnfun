'use client';

import React from 'react';
import Link from 'next/link';
import { motion, useScroll, useTransform } from 'framer-motion';
import { useAuth } from '@/context/AuthContext';
import {
  BookOpen,
  Bot,
  BarChart3,
  ArrowRight,
  ChevronRight,
  Star,
  Zap,
  GraduationCap,
  Users,
  Sparkles,
  Rocket,
  Quote,
} from 'lucide-react';

const fadeUp = {
  hidden: { opacity: 0, y: 40 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, delay: i * 0.15, ease: 'easeOut' },
  }),
};

const staggerContainer = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.15 } },
};

const cardHover = {
  rest: { y: 0, boxShadow: '0 4px 12px rgba(0,0,0,0.05)' },
  hover: { y: -8, boxShadow: '0 20px 40px rgba(99,102,241,0.15)', transition: { type: 'spring', stiffness: 300 } },
};

const floatingIcons = [
  { icon: BookOpen, color: 'text-primary-400', x: '10%', y: '20%', delay: 0, duration: 3 },
  { icon: Star, color: 'text-accent-400', x: '85%', y: '15%', delay: 0.5, duration: 4 },
  { icon: Rocket, color: 'text-secondary-400', x: '80%', y: '70%', delay: 1, duration: 3.5 },
  { icon: Sparkles, color: 'text-primary-300', x: '15%', y: '75%', delay: 0.3, duration: 2.8 },
  { icon: GraduationCap, color: 'text-secondary-300', x: '50%', y: '10%', delay: 0.8, duration: 3.2 },
];

export default function LandingPage() {
  const { user } = useAuth();
  const { scrollYProgress } = useScroll();
  const heroOpacity = useTransform(scrollYProgress, [0, 0.15], [1, 0]);
  const heroY = useTransform(scrollYProgress, [0, 0.15], [0, 50]);
  return (
    <div className="overflow-hidden">
      <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-50 via-white to-secondary-50 dark:from-surface-900 dark:via-surface-900 dark:to-surface-800" />

        <div className="absolute inset-0 opacity-30 dark:opacity-10">
          <div className="absolute top-20 left-10 w-72 h-72 bg-primary-400 rounded-full blur-[128px]" />
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-secondary-400 rounded-full blur-[128px]" />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-accent-300 rounded-full blur-[128px]" />
        </div>

        <motion.div style={{ opacity: heroOpacity, y: heroY }} className="relative z-10 mx-auto max-w-6xl px-4 text-center">
          {floatingIcons.map((item, i) => (
            <motion.div
              key={i}
              className={`absolute hidden lg:block ${item.color}`}
              style={{ left: item.x, top: item.y }}
              animate={{ y: [-10, 10, -10], rotate: [0, 5, -5, 0] }}
              transition={{ duration: item.duration, repeat: Infinity, delay: item.delay, ease: 'easeInOut' }}
            >
              <item.icon className="h-8 w-8" />
            </motion.div>
          ))}

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-6 inline-flex items-center gap-2 rounded-full border border-primary-200 dark:border-primary-700/50 bg-primary-50 dark:bg-primary-500/10 px-4 py-1.5 text-sm text-primary-600 dark:text-primary-400"
          >
            <Sparkles className="h-4 w-4" />
            <span>Aligned with CBC Curriculum</span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.15 }}
            className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-display font-extrabold leading-tight mb-6"
          >
            <span className="text-surface-900 dark:text-surface-50">Learn </span>
            <span className="text-gradient">Smarter</span>
            <br />
            <span className="text-surface-900 dark:text-surface-50">Play </span>
            <span className="text-gradient">Harder</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="mx-auto max-w-2xl text-lg sm:text-xl text-surface-600 dark:text-surface-400 mb-10"
          >
            Master the CBC curriculum with interactive quizzes, smart AI tutoring, and
            personalized learning paths. Learning has never been this fun!
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.45 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4"
          >
            <Link
              href={user ? '/dashboard' : '/auth/register'}
              className="group relative inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-primary-500 to-secondary-500 px-8 py-3.5 text-base font-semibold text-white shadow-lg shadow-primary-500/25 hover:shadow-xl hover:shadow-primary-500/30 transition-all duration-300 hover:-translate-y-0.5"
              aria-label="Get started"
            >
              <span>{user ? 'Go to Dashboard' : 'Get Started Free'}</span>
              <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-0.5" />
              <div className="absolute inset-0 rounded-xl bg-white opacity-0 group-hover:opacity-10 transition-opacity" />
            </Link>
            <Link
              href="/auth/login"
              className="group inline-flex items-center gap-2 rounded-xl border border-surface-300 dark:border-surface-600 px-8 py-3.5 text-base font-semibold text-surface-700 dark:text-surface-300 hover:bg-surface-100 dark:hover:bg-surface-800 transition-all duration-300 hover:-translate-y-0.5"
              aria-label="Sign in"
            >
              Sign In
              <ChevronRight className="h-5 w-5 transition-transform group-hover:translate-x-0.5" />
            </Link>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.7 }}
            className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8 max-w-3xl mx-auto"
          >
            {[
              { num: '500+', label: 'Quizzes' },
              { num: '11', label: 'Grades' },
              { num: '16+', label: 'Subjects' },
              { num: 'AI', label: 'Powered' },
            ].map((stat, i) => (
              <div key={i} className="text-center">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: 'spring', stiffness: 300, delay: 0.8 + i * 0.1 }}
                  className="text-2xl sm:text-3xl font-bold text-gradient mb-1"
                >
                  {stat.num}
                </motion.div>
                <div className="text-xs sm:text-sm text-surface-500">{stat.label}</div>
              </div>
            ))}
          </motion.div>
        </motion.div>

        <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-white dark:from-surface-900 to-transparent" />
      </section>

      <section className="py-24 relative">
        <div className="mx-auto max-w-6xl px-4">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: '-100px' }}
            variants={staggerContainer}
            className="text-center mb-16"
          >
            <motion.span variants={fadeUp} className="inline-block text-sm font-semibold text-primary-500 mb-3 tracking-wider uppercase">
              Features
            </motion.span>
            <motion.h2 variants={fadeUp} className="text-3xl sm:text-4xl font-bold text-surface-900 dark:text-surface-50 mb-4">
              Everything you need to excel
            </motion.h2>
            <motion.p variants={fadeUp} className="text-surface-600 dark:text-surface-400 max-w-2xl mx-auto">
              Our platform combines engaging content with smart technology to create
              the ultimate learning experience.
            </motion.p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: BookOpen,
                title: 'Interactive Quizzes',
                description: 'Engage with thousands of CBC-aligned quizzes across all subjects and grades with instant feedback.',
                gradient: 'from-primary-500 to-blue-500',
                shadow: 'shadow-primary-500/20',
              },
              {
                icon: Bot,
                title: 'Smart AI Tutor',
                description: 'Get personalized help from our AI tutor that adapts to your learning style and pace.',
                gradient: 'from-secondary-500 to-purple-500',
                shadow: 'shadow-secondary-500/20',
              },
              {
                icon: BarChart3,
                title: 'Track Progress',
                description: 'Monitor your improvement with detailed analytics and personalized recommendations.',
                gradient: 'from-accent-500 to-orange-500',
                shadow: 'shadow-accent-500/20',
              },
            ].map((feature, i) => (
              <motion.div
                key={i}
                initial="rest"
                whileHover="hover"
                variants={cardHover}
                className="glass-card rounded-2xl p-8 cursor-default"
              >
                <div className={`inline-flex p-3 rounded-xl bg-gradient-to-br ${feature.gradient} text-white mb-5 shadow-lg ${feature.shadow}`}>
                  <feature.icon className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-bold text-surface-900 dark:text-surface-50 mb-3">
                  {feature.title}
                </h3>
                <p className="text-surface-600 dark:text-surface-400 leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-24 relative bg-surface-50 dark:bg-surface-800/50">
        <div className="mx-auto max-w-6xl px-4">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: '-100px' }}
            variants={staggerContainer}
            className="text-center mb-16"
          >
            <motion.span variants={fadeUp} className="inline-block text-sm font-semibold text-primary-500 mb-3 tracking-wider uppercase">
              How It Works
            </motion.span>
            <motion.h2 variants={fadeUp} className="text-3xl sm:text-4xl font-bold text-surface-900 dark:text-surface-50 mb-4">
              Start learning in 3 easy steps
            </motion.h2>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              { step: '01', title: 'Create Account', desc: 'Sign up for free and set your grade level. No credit card required.', icon: Users },
              { step: '02', title: 'Take Quizzes', desc: 'Choose from hundreds of interactive quizzes tailored to your curriculum.', icon: Zap },
              { step: '03', title: 'Track Growth', desc: 'Monitor your progress, earn points, and level up as you learn.', icon: Star },
            ].map((item, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.15 }}
                className="relative text-center p-8"
              >
                <div className="text-5xl font-black text-primary-200 dark:text-primary-800 mb-4">
                  {item.step}
                </div>
                <div className="inline-flex p-3 rounded-xl bg-gradient-to-br from-primary-500 to-secondary-500 text-white mb-4">
                  <item.icon className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-bold text-surface-900 dark:text-surface-50 mb-2">
                  {item.title}
                </h3>
                <p className="text-surface-600 dark:text-surface-400">{item.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-24">
        <div className="mx-auto max-w-6xl px-4">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: '-100px' }}
            variants={staggerContainer}
            className="text-center mb-16"
          >
            <motion.span variants={fadeUp} className="inline-block text-sm font-semibold text-primary-500 mb-3 tracking-wider uppercase">
              Testimonials
            </motion.span>
            <motion.h2 variants={fadeUp} className="text-3xl sm:text-4xl font-bold text-surface-900 dark:text-surface-50 mb-4">
              What students & parents say
            </motion.h2>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[1, 2, 3].map((_, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
                className="glass-card rounded-2xl p-6"
              >
                <Quote className="h-8 w-8 text-primary-300 dark:text-primary-700 mb-3" />
                <p className="text-surface-600 dark:text-surface-400 mb-4 leading-relaxed">
                  {i === 0 && 'LearnFun has made learning so much fun for my daughter. She looks forward to her quizzes every day!'}
                  {i === 1 && 'The AI tutor is amazing! It helps me understand topics I struggle with at my own pace.'}
                  {i === 2 && 'Finally a platform that truly understands the CBC curriculum. Highly recommended for all parents.'}
                </p>
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 rounded-full bg-gradient-to-br from-primary-400 to-secondary-500 flex items-center justify-center text-white font-bold text-sm">
                    {['MJ', 'PK', 'RN'][i]}
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-surface-900 dark:text-surface-50">
                      {['Mary Wanjiku', 'Peter Kamau', 'Ruth Njoroge'][i]}
                    </p>
                    <p className="text-xs text-surface-500">
                      {['Parent', 'Student - G6', 'Parent'][i]}
                    </p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-24 relative bg-gradient-to-br from-primary-500 to-secondary-600 overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-10 left-10 w-60 h-60 bg-white rounded-full blur-[100px]" />
          <div className="absolute bottom-10 right-10 w-80 h-80 bg-white rounded-full blur-[100px]" />
        </div>
        <div className="relative z-10 mx-auto max-w-4xl px-4 text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
              Ready to transform your learning journey?
            </h2>
            <p className="text-primary-100 text-lg mb-8 max-w-2xl mx-auto">
              Join thousands of students already learning smarter with LearnFun.
              Start for free today!
            </p>
            <Link
              href="/auth/register"
              className="inline-flex items-center gap-2 rounded-xl bg-white px-8 py-3.5 text-base font-semibold text-primary-600 hover:bg-primary-50 shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-0.5"
              aria-label="Get started free"
            >
              Get Started Free
              <ArrowRight className="h-5 w-5" />
            </Link>
          </motion.div>
        </div>
      </section>

      <footer className="bg-surface-900 dark:bg-surface-950 text-surface-400 py-16">
        <div className="mx-auto max-w-6xl px-4">
          <div className="grid md:grid-cols-4 gap-8 mb-12">
            <div className="col-span-2 md:col-span-1">
              <div className="flex items-center gap-2 mb-4">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-primary-400 to-secondary-500 text-white text-sm font-bold">
                  L
                </div>
                <span className="text-lg font-bold text-white">LearnFun</span>
              </div>
              <p className="text-sm text-surface-500 leading-relaxed">
                Making CBC learning fun and interactive for every Kenyan student.
              </p>
            </div>
            <div>
              <h4 className="text-sm font-semibold text-surface-200 mb-4">Platform</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="/quizzes" className="hover:text-surface-200 transition-colors">Quizzes</Link></li>
                <li><Link href="/lessons" className="hover:text-surface-200 transition-colors">Lessons</Link></li>
                <li><Link href="/leaderboard" className="hover:text-surface-200 transition-colors">Leaderboard</Link></li>
                <li><Link href="/ai-tutor" className="hover:text-surface-200 transition-colors">AI Tutor</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="text-sm font-semibold text-surface-200 mb-4">Company</h4>
              <ul className="space-y-2 text-sm">
                <li><span className="hover:text-surface-200 transition-colors cursor-pointer">About</span></li>
                <li><span className="hover:text-surface-200 transition-colors cursor-pointer">Blog</span></li>
                <li><span className="hover:text-surface-200 transition-colors cursor-pointer">Contact</span></li>
                <li><span className="hover:text-surface-200 transition-colors cursor-pointer">Privacy</span></li>
              </ul>
            </div>
            <div>
              <h4 className="text-sm font-semibold text-surface-200 mb-4">Support</h4>
              <ul className="space-y-2 text-sm">
                <li><span className="hover:text-surface-200 transition-colors cursor-pointer">Help Center</span></li>
                <li><span className="hover:text-surface-200 transition-colors cursor-pointer">FAQs</span></li>
                <li><span className="hover:text-surface-200 transition-colors cursor-pointer">Terms</span></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-surface-800 pt-8 text-center text-xs text-surface-600">
            &copy; {new Date().getFullYear()} LearnFun. All rights reserved. Made with ❤️ for Kenyan students.
          </div>
        </div>
      </footer>
    </div>
  );
}
