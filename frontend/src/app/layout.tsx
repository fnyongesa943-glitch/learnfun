import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { ThemeContextProvider } from '@/context/ThemeContext';
import { AuthProvider } from '@/context/AuthContext';
import Layout from '@/components/layout/Layout';
import './globals.css';

const inter = Inter({ subsets: ['latin'], display: 'swap' });

export const metadata: Metadata = {
  title: 'LearnFun - CBC Interactive Learning Platform',
  description: 'Interactive learning platform for CBC curriculum. Quizzes, lessons, AI tutor for grades PP1 to G9.',
  keywords: ['CBC', 'Kenya', 'education', 'quizzes', 'learning', 'kids', 'grades'],
  openGraph: {
    title: 'LearnFun - CBC Interactive Learning Platform',
    description: 'Interactive learning platform for CBC curriculum.',
    type: 'website',
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeContextProvider>
          <AuthProvider>
            <Layout>{children}</Layout>
          </AuthProvider>
        </ThemeContextProvider>
      </body>
    </html>
  );
}
