import react from "@vitejs/plugin-react"; // You'll likely need this for React projects
import { defineConfig } from "vite";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [react(),
            tsconfigPaths()],

  ssr: {
    noExternal: ['react-bootstrap', 'framer-motion'], // tell Vite not to externalize this
  }
});
