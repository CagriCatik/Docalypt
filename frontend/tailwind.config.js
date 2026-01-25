/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'doc-bg': 'var(--color-doc-bg)',
        'doc-sidebar': 'var(--color-doc-sidebar)',
        'doc-border': 'var(--color-doc-border)',
        'doc-accent': 'var(--color-doc-accent)',
        'doc-text': 'var(--color-doc-text)',
        'doc-text-dim': 'var(--color-doc-text-dim)',
      }
    },
  },
  plugins: [],
}
