const fs = require('fs');
const path = require('path');

const dir = 'content/PCCST502';
const files = fs.readdirSync(dir).filter(f => f.startsWith('m1_') && f.endsWith('.md'));

for (const file of files) {
  const filePath = path.join(dir, file);
  let content = fs.readFileSync(filePath, 'utf-8');

  // Reformat quizzes
  // Match "::: quiz Q1: Title\nQuestion text" and replace with "::: quiz Question text"
  content = content.replace(/::: quiz (.*?)\n(.*?)\n/g, (match, p1, p2) => {
    if (p1.match(/^Q\d+:/)) {
       return `::: quiz ${p2}\n`;
    }
    return match;
  });

  // Replace (A), (B), (*C) with (), (), (*)
  content = content.replace(/^\(\*?[A-E]\)\s/gm, (match) => {
    return match.includes('*') ? '(*) ' : '() ';
  });

  // Reformat Active Recall Checkpoint to Active Recall Quizzes
  content = content.replace(/## (\d+)\. Active Recall Checkpoint/g, '## $1. Active Recall Quizzes');
  
  fs.writeFileSync(filePath, content, 'utf-8');
}
console.log('Reformatted ' + files.length + ' files.');
