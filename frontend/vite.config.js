import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/auth': 'http://localhost:8000',
      '/journals': 'http://localhost:8000',
      '/chat': 'http://localhost:8000',
      '/emotions': 'http://localhost:8000',
      '/dashboard': 'http://localhost:8000',
      '/timeline': 'http://localhost:8000',
      '/users': 'http://localhost:8000',
    },
  },
})
