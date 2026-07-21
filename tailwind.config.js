/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './shoplink/index.html'],
  theme: {
    extend: {
      colors: {
        navy: { DEFAULT: '#16324F', deep: '#0F2438', soft: '#1B3A5B', muted: '#3D5A75' },
        teal: { DEFAULT: '#5FBFAE', bright: '#6FD3C0', deep: '#3E9C8B' },
        mist: '#F4F5F6',
      },
      fontFamily: {
        display: ['Sora', 'system-ui', 'sans-serif'],
        body: ['Inter', 'system-ui', 'sans-serif'],
      },
      maxWidth: { content: '76rem' },
    },
  },
};
