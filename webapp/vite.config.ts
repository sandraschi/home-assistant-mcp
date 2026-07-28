import path from "path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  resolve: { alias: { "@": path.resolve(__dirname, "./src") } },
  server: {
    allowedHosts: ["goliath"],
    host: true,
    proxy: {
      "/api": { target: "http://localhost:10796", changeOrigin: true },
    },
  },
});
