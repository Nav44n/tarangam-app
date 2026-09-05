const fs = require('fs');
let code = fs.readFileSync('scripts/build.js', 'utf-8');

// Fix Callouts to ALL be closed by default
code = code.replace(/const isOpen = type !== 'intuition';/g, 'const isOpen = false;');

// Fix ::: step to have both badge and title in summary
code = code.replace(
  /return \<details class="step-card"><summary class="step-badge">\$\{badge.trim\(\)\}<\/summary><div class="step-title">\$\{title.trim\(\)\}<\/div><div class="step-content">\$\{renderedContent\}<\/div><\/details>\;/g,
  'return <details class="step-card"><summary class="step-summary" style="cursor:pointer; list-style:none; outline:none;"><div class="step-badge" style="display:inline-flex; align-items:center; gap:6px;"> <span style="font-size:10px;">&#9662;</span></div><div class="step-title"></div></summary><div class="step-content"></div></details>;'
);

fs.writeFileSync('scripts/build.js', code);
