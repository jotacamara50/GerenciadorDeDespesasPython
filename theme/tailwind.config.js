// theme/tailwind.config.js

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',         // Para templates dentro da pasta 'theme'
    '../expenses/**/*.html',         // Para templates dentro da pasta 'expenses'
    '../templates/**/*.html',        // Para templates diretamente na pasta 'templates' na raiz do projeto
    './static/js/**/*.js',           // Se usar JS com classes Tailwind na pasta 'theme/static'
    '../static/js/**/*.js',          // <--- ESTA É A LINHA CRUCIAL PARA O main.js!
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}