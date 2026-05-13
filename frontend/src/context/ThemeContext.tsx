'use client';

import { ThemeProvider, useTheme } from 'next-themes';
import { useEffect, useState, type ReactNode } from 'react';

export function ThemeContextProvider({ children }: { children: ReactNode }) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return <>{children}</>;
  }

  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
    </ThemeProvider>
  );
}

export { useTheme };
