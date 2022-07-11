import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    proxy: {
      // string shorthand
      '/item': 'http://127.0.0.1:8000',
      '/graphql': 'http://127.0.0.1:8000',
    },
  },
  plugins: [react()]
})
