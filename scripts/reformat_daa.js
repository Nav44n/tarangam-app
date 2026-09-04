const fs = require('fs');
const path = require('path');

const dir = 'content/PCCST502';
const files = fs.readdirSync(dir).filter(f => f.startsWith('m1_') && f.endsWith('.md'));

for (const file of files) {
  const filePath = path.join(dir, file);
  let content = fs.readFileSync(filePath, 'utf-8');

  // Reformat quizzes
  content = content.replace(/::: quiz (.*?)\n(.*?)\n/g, (match, p1, p2) => {
    return `::: quiz ${p2}\n`;
  });

  content = content.replace(/\(\*?[A-E]\)\s/g, (match) => {
    return match.includes('*') ? '(*) ' : '() ';
  });

  // Reformat Active Recall Checkpoint to Active Recall Quizzes
  content = content.replace(/## (\d+)\. Active Recall Checkpoint/g, '## $1. Active Recall Quizzes');
  
  // Also remove "Worked Example / Step-by-Step Scenario" maybe?
  // Let's just keep the headers and only fix the quizzes to match the exact format requested.

  fs.writeFileSync(filePath, content, 'utf-8');
}
console.log('Reformatted ' + files.length + ' files.');
