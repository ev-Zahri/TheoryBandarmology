/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "primary": "#49e619",
        "background-light": "#f6f8f6",
        "background-dark": "#0f172a",
        "card-dark": "#1e293b",
        "border-dark": "#334155",
        "loss": "#ef4444",
      },
      fontFamily: {
        "display": ["Manrope", "sans-serif"],
        "mono": ["JetBrains Mono", "monospace"],
      },
      borderRadius: {
        "DEFAULT": "1rem",
        "lg": "2rem",
        "xl": "3rem",
        "full": "9999px"
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
