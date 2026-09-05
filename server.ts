import express from 'express';
import path from 'path';
import fs from 'fs';
import { exec } from 'child_process';
import compression from 'compression';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);
const { ZipArchive } = require('archiver');


const app = express();
const PORT = 3000;
const distPath = path.join(process.cwd(), 'dist');

// Use compression for all responses
app.use(compression());
app.use(express.json());

let isBuilding = false;

// Ensure curriculum is compiled if dist/index.html is missing
function ensureDistBuilt() {
  const distIndex = path.join(distPath, 'index.html');
  if (!fs.existsSync(distIndex) && !isBuilding) {
    isBuilding = true;
    console.log('dist/index.html not found. Compiling curriculum...');
    const buildScript = path.join(process.cwd(), 'scripts', 'build.js');
    if (fs.existsSync(buildScript)) {
      exec('node scripts/build.js', (error, stdout, stderr) => {
        isBuilding = false;
        if (error) {
          console.error('Failed to compile curriculum on startup:', error);
          return;
        }
        console.log('Build completed successfully.');
      });
    } else {
      isBuilding = false;
    }
  }
}
ensureDistBuilt();

// Middleware for security and caching headers
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  // Cache assets heavily, typical for static sites
  if (req.url.startsWith('/assets/')) {
    res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
  } else {
    res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
  }
  next();
});

// Serve static assets from the dist directory
app.use(express.static(distPath, {
  extensions: ['html', 'htm'],
  index: 'index.html',
  maxAge: 0
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

// Download whole project zipped
app.get(['/api/download-project', '/download-project', '/download-project.zip'], (req, res) => {
  const timestamp = new Date().toISOString().split('T')[0];
  const zipFileName = `tarangam-project-${timestamp}.zip`;

  res.setHeader('Content-Type', 'application/zip');
  res.setHeader('Content-Disposition', `attachment; filename="${zipFileName}"`);
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');

  const archive = new ZipArchive({
    zlib: { level: 6 }
  });

  archive.on('error', (err: any) => {
    console.error('Error generating project zip:', err);
    if (!res.headersSent) {
      res.status(500).json({ error: 'Failed to create zip archive' });
    }
  });

  // Pipe archive data directly to client response
  archive.pipe(res);

  // Archive files from root directory, excluding heavy/temp/dependency folders
  archive.glob('**/*', {
    cwd: process.cwd(),
    ignore: [
      'node_modules/**',
      '.git/**',
      '.cache/**',
      '.npm/**',
      '.tmp/**',
      '**/*.log',
      '**/.DS_Store'
    ],
    dot: true
  });

  archive.finalize();
});

// Redirect course root (e.g. /PCCST502 or /PCCST502/) to its syllabus
const knownCourses = ['PCCST501', 'PCCST502', 'PCCST503', 'PBCST504', 'PECST522', 'PCCSL507', 'PCCSL508'];
for (const code of knownCourses) {
  app.get([`/${code}`, `/${code}/`], (req, res) => {
    res.redirect(`/${code}/m0_00_course_syllabus_and_blueprint.html`);
  });
}

// Fallback / 404 handler
app.use((req, res) => {
  const potentialHtml = path.join(distPath, req.path + '.html');
  if (fs.existsSync(potentialHtml) && fs.statSync(potentialHtml).isFile()) {
    return res.sendFile(potentialHtml);
  }
  const directFile = path.join(distPath, req.path);
  if (fs.existsSync(directFile) && fs.statSync(directFile).isFile()) {
    return res.sendFile(directFile);
  }
  // If this was a navigation/HTML request that did not match, redirect to home
  // This prevents the browser from getting stuck at an invalid subdirectory where relative links break
  if (req.method === 'GET' && (req.accepts('html') || !path.extname(req.path))) {
    return res.redirect('/');
  }
  res.status(404).send('Page not found');
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Tarangam server running at http://0.0.0.0:${PORT}`);
});
