/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    swcMinify: true,
    images: {
      remotePatterns: [
        {
          protocol: "https",
          hostname: "user-images.githubusercontent.com",
        },
      ],
    },
    async redirects() {
      return [
        {
          source: "/github",
          destination: "https://github.com/XiaohanYa/meme_lingo",
          permanent: false,
        },
        {
          source: "/deploy",
          destination: "https://vercel.com/templates/next.js/meme_lingo",
          permanent: false,
        },   
      ]
    }
  };
  
  module.exports = nextConfig;
  