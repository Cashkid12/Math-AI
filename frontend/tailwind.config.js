/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#000000',
        accent: '#000000',
        dark: {
          bg: '#ffffff',
          card: '#ffffff',
          border: '#000000',
        },
        light: {
          bg: '#ffffff',
          card: '#ffffff',
          border: '#000000',
        },
        text: {
          primary: '#000000',
          secondary: '#666666',
          muted: '#999999',
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
