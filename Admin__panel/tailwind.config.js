/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        vitaBlue: {
          900:'#071f32',
          800:'#0b3350',
          700:'#0f4d7a',
          600:'#126aa8',
          500:'#157fc3'
        },
        vitaGold: '#F0C419',
        vitaBg: '#f7f8fb',
        vitaCardBorder: '#e6e8ee'
      },
      boxShadow: {
        soft: '0 2px 10px rgba(0,0,0,0.06)'
      }
    }
  },
  plugins: [require('@tailwindcss/forms'), require('daisyui')],
  daisyui: {
    themes: [
      {
        vitagita: {
          'primary': '#F0C419',
          'secondary': '#0b3350',
          'accent': '#F0C419',
          'neutral': '#071f32',
          'base-100': '#ffffff',
          'base-200': '#f7f8fb',
          'info': '#126aa8',
          'success': '#22c55e',
          'warning': '#f59e0b',
          'error': '#ef4444'
        }
      }
    ]
  }
}
