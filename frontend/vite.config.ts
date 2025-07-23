import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss()
  ],
  build: { assetsDir: '.', // Output assets directly into the root of dist/
      rollupOptions: {
        output: {
          assetFileNames: '[name].[ext]',    // No hash
          chunkFileNames: '[name].js',       // No hash
          entryFileNames: '[name].js',       // No hash
        },
      },
  },
})
