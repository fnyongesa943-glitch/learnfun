/** @type {import('next').NextConfig} */
const nextConfig = {
  images: { domains: ['lh3.googleusercontent.com', 'avatars.githubusercontent.com'] },
  reactStrictMode: true,
  compiler: { removeConsole: process.env.NODE_ENV === 'production' },
};
module.exports = nextConfig;
