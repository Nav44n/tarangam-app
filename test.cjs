const fs = require('fs');
const files = fs.readdirSync('dist/PECST522');
for (const file of files) {
  if (file.endsWith('.html')) {
    const content = fs.readFileSync('dist/PECST522/' + file, 'utf8');
    if (content.includes('AI Tutor') || content.includes('ai-tutor')) {
      console.log('Found in ' + file);
    }
  }
}
console.log('Search done');
