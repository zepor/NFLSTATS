import { defineConfig, splitVendorChunkPlugin } from "vite";
import react from "@vitejs/plugin-react";
import svgrPlugin from "vite-plugin-svgr";
import { ViteEjsPlugin } from "vite-plugin-ejs";
import { nodePolyfills } from "vite-plugin-node-polyfills";
import { resolve } from "path";

export default defineConfig({
  server: {
    hmr: {
      overlay: false,
    },
  }, 
  plugins: [
    react(),
    svgrPlugin(),
    ViteEjsPlugin(),
    nodePolyfills({
      protocolImports: true,
    }),
    splitVendorChunkPlugin(),
  ],
  build: {
    cssCodeSplit: true,
    chunkSizeWarningLimit: 3000,
    rollupOptions: {
      input: {
        main: resolve(__dirname, "index.html"),
        light: resolve(__dirname, "src/assets/scss/light.scss"),
        dark: resolve(__dirname, "src/assets/scss/dark.scss"),
        team: resolve(__dirname, "src/assets/scss/team-theme.scss"),
      },
      output: {
        assetFileNames: "assets/[name][extname]",
        manualChunks(id) {
          if (id.includes('node_modules/apexcharts')) {
            return 'apexcharts';
          }
          if (id.includes('node_modules/chart.js') || id.includes('node_modules/react-chartjs-2')) {
            return 'chartjs';
          }
          if (id.includes('node_modules/google-map-react')) {
            return 'googlemaps';
          }
          if (id.includes('node_modules/jsvectormap') || id.includes('src/vendor/us_aea_en.js') || id.includes('src/vendor/world.js')) {
            return 'vectormaps';
          }
          if (id.includes('node_modules/@fullcalendar')) {
            return 'fullcalendar';
          }
        },
      },
    },
  },
});