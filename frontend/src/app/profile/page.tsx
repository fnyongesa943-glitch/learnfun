'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { cn, calculateLevel } from '@/lib/utils';
import { useAuth } from '@/context/AuthContext';
import { useTheme } from '@/context/ThemeContext';
import Button from '@/components/ui/Button';
import Avatar from '@/components/ui/Avatar';
import Modal from '@/components/ui/Modal';
import toast from 'react-hot-toast';
import {
  User,
  Mail,
  GraduationCap,
  Lock,
  Sun,
  Moon,
  Monitor,
  Bell,
  Shield,
  Trash2,
  Save,
  Camera,
  Eye,
  EyeOff,
  CheckCircle2,
} from 'lucide-react';

const emojiAvatars = [
  '😎', '🚀', '🌟', '🎓', '💡', '🎨', '🌈', '🦸', '🧠', '📚',
  '🎯', '💪', '🔥', '⭐', '🏆', '🦁', '🐯', '🦅', '🐉', '🦋',
];

const staggerContainer = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.08 } },
};

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, delay: i * 0.08, ease: 'easeOut' },
  }),
};

export default function ProfilePage() {
  const { user, updateProfile, logout } = useAuth();
  const { theme, setTheme } = useTheme();
  const [name, setName] = useState(user?.name || '');
  const [grade, setGrade] = useState(user?.grade || '');
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [selectedAvatar, setSelectedAvatar] = useState(user?.avatar || '😎');
  const [showAvatarPicker, setShowAvatarPicker] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [notifications, setNotifications] = useState({
    email: true,
    push: true,
    quizReminders: true,
    weeklyReport: false,
  });
  const [saving, setSaving] = useState(false);

  const handleSaveProfile = async () => {
    setSaving(true);
    try {
      await updateProfile({ name, grade, avatar: selectedAvatar });
      toast.success('Profile updated successfully');
    } catch {
      toast.error('Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  const handleChangePassword = () => {
    if (!currentPassword) {
      toast.error('Please enter your current password');
      return;
    }
    if (newPassword.length < 6) {
      toast.error('New password must be at least 6 characters');
      return;
    }
    if (newPassword !== confirmPassword) {
      toast.error('Passwords do not match');
      return;
    }
    toast.success('Password updated successfully');
    setCurrentPassword('');
    setNewPassword('');
    setConfirmPassword('');
  };

  const handleDeleteAccount = () => {
    toast.success('Account deleted');
    logout();
  };

  const toggleNotification = (key: keyof typeof notifications) => {
    setNotifications((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="min-h-screen bg-surface-50 dark:bg-surface-900">
      <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          initial="hidden"
          animate="visible"
          variants={staggerContainer}
          className="space-y-8"
        >
          <motion.div variants={fadeUp}>
            <h1 className="text-2xl sm:text-3xl font-bold text-surface-900 dark:text-surface-50">
              Profile Settings
            </h1>
            <p className="text-surface-500 mt-1">
              Manage your account and preferences
            </p>
          </motion.div>

          <motion.div variants={fadeUp} className="flex flex-col sm:flex-row items-center gap-6 p-6 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700">
            <div className="relative">
              <button
                onClick={() => setShowAvatarPicker(true)}
                className="group relative flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-br from-primary-400 to-secondary-500 text-3xl shadow-lg"
                aria-label="Change avatar"
              >
                {selectedAvatar}
                <div className="absolute inset-0 flex items-center justify-center rounded-full bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity">
                  <Camera className="h-6 w-6 text-white" />
                </div>
              </button>
            </div>
            <div className="text-center sm:text-left">
              <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50">{user?.name}</h2>
              <p className="text-sm text-surface-500">{user?.email}</p>
              <div className="flex items-center gap-2 mt-1 justify-center sm:justify-start">
                <span className="text-xs font-medium text-primary-500">Level {user ? calculateLevel(user.points) : 1}</span>
                <span className="text-xs text-surface-400">|</span>
                <span className="text-xs text-surface-500">{user?.points || 0} points</span>
              </div>
            </div>
          </motion.div>

          <motion.div variants={fadeUp} className="p-6 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700">
            <h2 className="text-base font-semibold text-surface-900 dark:text-surface-50 mb-4 flex items-center gap-2">
              <User className="h-4 w-4 text-primary-500" />
              Personal Information
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-surface-500 mb-1.5">Full Name</label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-surface-400" />
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full pl-9 pr-4 py-2.5 rounded-lg bg-surface-50 dark:bg-surface-700 border border-surface-200 dark:border-surface-600 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                    aria-label="Full name"
                  />
                </div>
              </div>
              <div>
                <label className="block text-xs font-medium text-surface-500 mb-1.5">Email</label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-surface-400" />
                  <input
                    type="email"
                    value={user?.email || ''}
                    disabled
                    className="w-full pl-9 pr-4 py-2.5 rounded-lg bg-surface-100 dark:bg-surface-700 border border-surface-200 dark:border-surface-600 text-sm opacity-60 cursor-not-allowed"
                    aria-label="Email"
                  />
                </div>
              </div>
              <div>
                <label className="block text-xs font-medium text-surface-500 mb-1.5">Grade</label>
                <div className="relative">
                  <GraduationCap className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-surface-400" />
                  <select
                    value={grade}
                    onChange={(e) => setGrade(e.target.value)}
                    className="w-full pl-9 pr-4 py-2.5 rounded-lg bg-surface-50 dark:bg-surface-700 border border-surface-200 dark:border-surface-600 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 appearance-none"
                    aria-label="Grade"
                  >
                    {['PP1', 'PP2', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'].map((g) => (
                      <option key={g} value={g}>{g}</option>
                    ))}
                  </select>
                </div>
              </div>
              <Button onClick={handleSaveProfile} loading={saving} icon={<Save className="h-4 w-4" />}>
                Save Changes
              </Button>
            </div>
          </motion.div>

          <motion.div variants={fadeUp} className="p-6 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700">
            <h2 className="text-base font-semibold text-surface-900 dark:text-surface-50 mb-4 flex items-center gap-2">
              <Lock className="h-4 w-4 text-primary-500" />
              Change Password
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-surface-500 mb-1.5">Current Password</label>
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-lg bg-surface-50 dark:bg-surface-700 border border-surface-200 dark:border-surface-600 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                  aria-label="Current password"
                />
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-surface-500 mb-1.5">New Password</label>
                  <div className="relative">
                    <input
                      type={showPassword ? 'text' : 'password'}
                      value={newPassword}
                      onChange={(e) => setNewPassword(e.target.value)}
                      className="w-full px-4 py-2.5 rounded-lg bg-surface-50 dark:bg-surface-700 border border-surface-200 dark:border-surface-600 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                      aria-label="New password"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-xs font-medium text-surface-500 mb-1.5">Confirm Password</label>
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="w-full px-4 py-2.5 rounded-lg bg-surface-50 dark:bg-surface-700 border border-surface-200 dark:border-surface-600 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                    aria-label="Confirm password"
                  />
                </div>
              </div>
              <div className="flex items-center justify-between">
                <label className="flex items-center gap-2 text-sm text-surface-500 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={showPassword}
                    onChange={() => setShowPassword(!showPassword)}
                    className="rounded border-surface-300 text-primary-500 focus:ring-primary-500"
                  />
                  Show passwords
                </label>
                <Button variant="outline" size="sm" onClick={handleChangePassword}>
                  Update Password
                </Button>
              </div>
            </div>
          </motion.div>

          <motion.div variants={fadeUp} className="p-6 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700">
            <h2 className="text-base font-semibold text-surface-900 dark:text-surface-50 mb-4 flex items-center gap-2">
              <Sun className="h-4 w-4 text-primary-500" />
              Theme Preference
            </h2>
            <div className="flex gap-3">
              {[
                { id: 'light', icon: Sun, label: 'Light' },
                { id: 'dark', icon: Moon, label: 'Dark' },
                { id: 'system', icon: Monitor, label: 'System' },
              ].map((t) => {
                const Icon = t.icon;
                const isActive = theme === t.id;
                return (
                  <button
                    key={t.id}
                    onClick={() => setTheme(t.id)}
                    className={cn(
                      'flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all flex-1',
                      isActive
                        ? 'border-primary-500 bg-primary-50 dark:bg-primary-500/10'
                        : 'border-surface-200 dark:border-surface-700 hover:border-surface-300 dark:hover:border-surface-600'
                    )}
                    aria-label={t.label}
                  >
                    <Icon className={cn('h-6 w-6', isActive ? 'text-primary-500' : 'text-surface-400')} />
                    <span className={cn('text-xs font-medium', isActive ? 'text-primary-500' : 'text-surface-500')}>
                      {t.label}
                    </span>
                  </button>
                );
              })}
            </div>
          </motion.div>

          <motion.div variants={fadeUp} className="p-6 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700">
            <h2 className="text-base font-semibold text-surface-900 dark:text-surface-50 mb-4 flex items-center gap-2">
              <Bell className="h-4 w-4 text-primary-500" />
              Notification Settings
            </h2>
            <div className="space-y-3">
              {[
                { key: 'email' as const, label: 'Email notifications', desc: 'Receive updates via email' },
                { key: 'push' as const, label: 'Push notifications', desc: 'Receive push notifications' },
                { key: 'quizReminders' as const, label: 'Quiz reminders', desc: 'Get reminded about pending quizzes' },
                { key: 'weeklyReport' as const, label: 'Weekly report', desc: 'Receive weekly performance summary' },
              ].map((item) => (
                <label key={item.key} className="flex items-center justify-between p-3 rounded-lg hover:bg-surface-50 dark:hover:bg-surface-700/50 transition-colors cursor-pointer">
                  <div>
                    <p className="text-sm font-medium text-surface-900 dark:text-surface-50">{item.label}</p>
                    <p className="text-xs text-surface-500">{item.desc}</p>
                  </div>
                  <button
                    onClick={() => toggleNotification(item.key)}
                    className={cn(
                      'relative h-6 w-11 rounded-full transition-colors',
                      notifications[item.key] ? 'bg-primary-500' : 'bg-surface-300 dark:bg-surface-600'
                    )}
                    role="switch"
                    aria-checked={notifications[item.key]}
                    aria-label={item.label}
                  >
                    <motion.div
                      animate={{ x: notifications[item.key] ? 22 : 2 }}
                      transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                      className="absolute top-0.5 h-5 w-5 rounded-full bg-white shadow-sm"
                    />
                  </button>
                </label>
              ))}
            </div>
          </motion.div>

          <motion.div variants={fadeUp} className="p-6 rounded-xl bg-white dark:bg-surface-800 border border-danger-200 dark:border-danger-700/30">
            <h2 className="text-base font-semibold text-danger-600 dark:text-danger-400 mb-4 flex items-center gap-2">
              <Trash2 className="h-4 w-4" />
              Danger Zone
            </h2>
            <p className="text-sm text-surface-500 mb-4">
              Once you delete your account, there is no going back. Please be certain.
            </p>
            <Button variant="danger" onClick={() => setShowDeleteModal(true)} icon={<Trash2 className="h-4 w-4" />}>
              Delete Account
            </Button>
          </motion.div>
        </motion.div>
      </div>

      <Modal open={showAvatarPicker} onClose={() => setShowAvatarPicker(false)} title="Choose Avatar" size="sm">
        <div className="grid grid-cols-5 gap-3">
          {emojiAvatars.map((emoji) => (
            <button
              key={emoji}
              onClick={() => { setSelectedAvatar(emoji); setShowAvatarPicker(false); }}
              className={cn(
                'flex items-center justify-center h-12 w-12 rounded-xl text-2xl transition-all border-2',
                selectedAvatar === emoji
                  ? 'border-primary-500 bg-primary-50 dark:bg-primary-500/10 scale-110'
                  : 'border-surface-200 dark:border-surface-700 hover:border-primary-300 dark:hover:border-primary-600'
              )}
              aria-label={`Select avatar ${emoji}`}
            >
              {emoji}
            </button>
          ))}
        </div>
      </Modal>

      <Modal
        open={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        title="Delete Account?"
        description="This action cannot be undone. All your data will be permanently removed."
        size="sm"
      >
        <div className="flex gap-3">
          <Button variant="ghost" fullWidth onClick={() => setShowDeleteModal(false)}>
            Cancel
          </Button>
          <Button variant="danger" fullWidth onClick={handleDeleteAccount} icon={<Trash2 className="h-4 w-4" />}>
            Delete
          </Button>
        </div>
      </Modal>
    </div>
  );
}
