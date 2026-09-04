const fs = require('fs');
let code = fs.readFileSync('scripts/build.js', 'utf-8');

const injection = `
  // 4. Transform Step Cards into collapsible details
  markdownText = markdownText.replace(/<div class="step-card">\\s*<div class="step-badge">([\\s\\S]*?)<\\/div>([\\s\\S]*?)<\\/div>/g, 
    '<details class="step-card">\\n<summary class="step-badge">$1</summary>\\n\\n$2\\n\\n</details>'
  );

  return markdownText;`;

code = code.replace('  return markdownText;', injection);
fs.writeFileSync('scripts/build.js', code);
