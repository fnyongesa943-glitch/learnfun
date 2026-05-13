import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const protectedRoutes = [
  '/dashboard',
  '/quizzes',
  '/lessons',
  '/leaderboard',
  '/ai-tutor',
  '/analytics',
  '/profile',
  '/settings',
];

const publicRoutes = ['/', '/auth/login', '/auth/register'];

export function middleware(request: NextRequest) {
  const token = request.cookies.get('learnfun_token')?.value || request.headers.get('authorization')?.replace('Bearer ', '') || '';

  const { pathname } = request.nextUrl;

  const isProtected = protectedRoutes.some((route) => pathname.startsWith(route));
  const isPublic = publicRoutes.some((route) => pathname === route);

  if (!token && isProtected) {
    const loginUrl = new URL('/auth/login', request.url);
    loginUrl.searchParams.set('redirect', pathname);
    return NextResponse.redirect(loginUrl);
  }

  if (token && (pathname === '/auth/login' || pathname === '/auth/register')) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico|images|icons).*)',
  ],
};
