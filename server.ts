import express from 'express';
import path from 'path';
import fs from 'fs';
import { execSync } from 'child_process';

const app = express();
const PORT = 3000;
const distPath = path.join(process.cwd(), 'dist');

// Ensure curriculum is compiled if dist/index.html is missing
function ensureDistBuilt() {
  const distIndex = path.join(distPath, 'index.html');
  if (!fs.existsSync(distIndex)) {
    console.log('dist/index.html not found. Compiling curriculum...');
    try {
      const buildScript = path.join(process.cwd(), 'scripts', 'build.js');
      if (fs.existsSync(buildScript)) {
        execSync('node scripts/build.js', { stdio: 'inherit' });
      }
    } catch (err) {
      console.error('Failed to compile curriculum on startup:', err);
    }
  }
}

ensureDistBuilt();

// Middleware for caching and headers
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  next();
});

// Serve static assets from the dist directory
app.use(express.static(distPath, {
  extensions: ['html', 'htm'],
  index: 'index.html'
}));

// Route for root
app.get('/', (req, res) => {
  const distIndex = path.join(distPath, 'index.html');
  if (fs.existsSync(distIndex)) {
    return res.sendFile(distIndex);
  }
  const rootIndex = path.join(process.cwd(), 'index.html');
  if (fs.existsSync(rootIndex)) {
    return res.sendFile(rootIndex);
  }
  res.status(503).send('Site is compiling. Please refresh in a moment.');
});

// API health endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', app: 'Tarangam' });
});

// Fallback / 404 handler
app.use((req, res) => {
  // If requesting an html page that might not have .html extension
  const potentialHtml = path.join(distPath, req.path + '.html');
  if (fs.existsSync(potentialHtml)) {
    return res.sendFile(potentialHtml);
  }
  const distIndex = path.join(distPath, 'index.html');
  if (fs.existsSync(distIndex)) {
    return res.status(404).sendFile(distIndex);
  }
  const rootIndex = path.join(process.cwd(), 'index.html');
  if (fs.existsSync(rootIndex)) {
    return res.status(404).sendFile(rootIndex);
  }
  res.status(404).send('Page not found');
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Tarangam server running at http://0.0.0.0:${PORT}`);
});
