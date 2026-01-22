/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  safelist: [
    'bg-blue-500',
    'bg-yellow-400',
    'bg-green-500',
    'bg-red-500',
    'hover:bg-blue-600',
    'hover:bg-yellow-500',
    'hover:bg-green-600',
    'hover:bg-red-600',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}