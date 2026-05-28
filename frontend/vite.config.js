import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    // Proxy API calls to the Python backend during development
    proxy: {
      "/receipts": "http://localhost:8000",
      "/insights": "http://localhost:8000",
    },
  },
});
