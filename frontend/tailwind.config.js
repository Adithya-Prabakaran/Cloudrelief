/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#17191c",
        paper: "#ffffff",
        mist: "#f2f2f3",
        fog: "#fafafb",
        graphite: "#777b86",
        ash: "#979799",
        smoke: "#a3a6af",
        peach: "#fbe1d1",
        sienna: "#5d2a1a",
      },
      fontFamily: {
        serif: ["Fraunces", "ui-serif", "Georgia", "serif"],
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      letterSpacing: {
        tight: "-0.02em",
        tighter: "-0.045em",
        tightest: "-0.06em",
      },
      maxWidth: {
        page: "1200px",
      },
      boxShadow: {
        float: "0 12px 30px -12px rgb(23 25 28 / 0.12)",
      },
    },
  },
  plugins: [],
};
