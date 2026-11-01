import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";
import tailwindcss from "@tailwindcss/vite";

// True SPA build — outputs to dist/ with index.html for static hosting and publisher
export default defineConfig({
  base: "./",
  plugins: [tsconfigPaths(), react(), tailwindcss()],
});
