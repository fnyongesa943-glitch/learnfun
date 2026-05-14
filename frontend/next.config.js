/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'lh3.googleusercontent.com' },
      { protocol: 'https', hostname: 'avatars.githubusercontent.com' },
    ],
  },
  reactStrictMode: true,
  compiler: { removeConsole: process.env.NODE_ENV === 'production' },
};
module.exports = nextConfig;
