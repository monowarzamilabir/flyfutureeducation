/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./apps/**/templates/**/*.html",
    "./apps/**/*.py",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          // "Ink" — primary text and dark sections.
          navy: "#101B3D",
          // "Cobalt" — primary interactive color (links, icons, route lines).
          blue: "#24428F",
          "blue-dark": "#16295C",
          // "Runway" — secondary accent, used sparingly.
          teal: "#0E7C6B",
          // "Brass" — the one warm accent; a seal/stamp color, not a highlight color.
          gold: "#B8862F",
          "gold-light": "#D9AE5C",
          // "Stamp" — rare, high-signal accent (visa-stamp red).
          stamp: "#A6321F",
          // "Paper" — cool ivory-grey section background.
          light: "#EEF1F6",
        },
      },
      fontFamily: {
        sans: ["'IBM Plex Sans'", "ui-sans-serif", "system-ui", "sans-serif"],
        display: ["'Bricolage Grotesque'", "'IBM Plex Sans'", "ui-sans-serif", "sans-serif"],
        mono: ["'IBM Plex Mono'", "ui-monospace", "SFMono-Regular", "monospace"],
      },
      boxShadow: {
        card: "0 1px 2px rgba(16,27,61,0.05), 0 10px 24px -16px rgba(16,27,61,0.18)",
        ticket: "0 20px 60px -20px rgba(16,27,61,0.45)",
      },
      backgroundImage: {
        "perf-h": "repeating-linear-gradient(90deg, rgba(16,27,61,0.16) 0 6px, transparent 6px 14px)",
        "perf-v": "repeating-linear-gradient(180deg, rgba(16,27,61,0.16) 0 6px, transparent 6px 14px)",
      },
    },
  },
  plugins: [],
};
