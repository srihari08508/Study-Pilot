/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#14213D",       // deep desk-lamp navy background
        paper: "#FAF6EE",     // warm ledger paper for cards
        brass: "#C9A227",     // desk-lamp gold, primary accent
        forest: "#3F6349",    // ledger-green, success/on-track
        rust: "#A64B3D",      // red-pen, warnings/urgent
        mist: "#8A93A6",      // muted secondary text
        inkline: "#243354",   // slightly lighter navy for card surfaces on dark bg
      },
      fontFamily: {
        display: ["'Fraunces'", "serif"],
        body: ["'Inter'", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
    },
  },
  plugins: [],
};
