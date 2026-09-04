const fs = require('fs');
const text = fs.readFileSync('content/PCCST502/m1_p01_asymptotics.md', 'utf-8');
const replaced = text.replace(/<div class="step-card">\s*<div class="step-badge">([\s\S]*?)<\/div>([\s\S]*?)<\/div>/g, '<details class="step-card">\n<summary class="step-badge">$1</summary>$2</details>');
console.log(replaced.match(/<details class="step-card">/g)?.length);
console.log(text.match(/<div class="step-card">/g)?.length);
