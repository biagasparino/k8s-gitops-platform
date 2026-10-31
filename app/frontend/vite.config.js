import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // local dev: forward /api to the FastAPI container/process
    proxy: { '/api': 'http://localhost:8000' },
  },
  test: { environment: 'jsdom', globals: true },
});
