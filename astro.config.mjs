// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';

// https://astro.build/config
export default defineConfig({
  site: 'https://charleslikesdata.com',
  integrations: [react()],
  // Static output (default) — deploys to GitHub Pages as plain files.
});
