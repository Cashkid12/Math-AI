/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1A73E8',
        accent: '#00C896',
        dark: {
          bg: '#0E1117',
          card: '#1A1F2E',
          border: '#2E3440',
        },
        light: {
          bg: '#F9FAFB',
          card: '#FFFFFF',
          border: '#E5E7EB',
        }
      },
      fontFamily: {
        poppins: ['Poppins', 'sans-serif'],
        montserrat: ['Montserrat', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
