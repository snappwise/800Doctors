/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["*.html", "./templates/**/*.{html,js}", "static/scripts/*.{html,js}"],
  darkMode: 'selector',
  theme: {
    extend: {
      screens: {
        'xs': '320px',
      },
      dropShadow: {

      },
      colors: {
        'whatsapp': {
          '50': '#f0fdf4',
          '100': '#dcfce7',
          '200': '#bbf7d0',
          '300': '#86efad',
          '400': '#4ade81',
          '500': '#25d366',
          '600': '#16a34b',
          '700': '#15803e',
          '800': '#166534',
          '900': '#14532d',
          '950': '#052e16',
        },
        'primary': {
          '50': '#edf8ff',
          '100': '#d6eeff',
          '200': '#b5e3ff',
          '300': '#83d3ff',
          '400': '#48b9ff',
          '500': '#1e96ff',
          '600': '#0675ff',
          '700': '#0061ff', //main
          '800': '#084ac5',
          '900': '#0d439b',
          '950': '#0e295d',
        },
        'light-blue': {
          '50': '#f7faff', //main
          '100': '#dbe8fe',
          '200': '#bfd7fe',
          '300': '#93befd',
          '400': '#609bfa',
          '500': '#3b76f6',
          '600': '#2557eb',
          '700': '#1d42d8',
          '800': '#1e37af',
          '900': '#1e338a',
          '950': '#172154',
        },

      },
      fontFamily: {
        'poppins': 'Poppins, sans-serif',
      },
    },
  },
  plugins: [],
}