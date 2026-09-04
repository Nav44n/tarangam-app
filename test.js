const text = `<div class="step-card">
<div class="step-badge">Step 1: Write down the formal mathematical definition</div>
**What are we doing?** We write down the target inequality we must satisfy to prove Big-$O$.  
</div>`;
const replaced = text.replace(/<div class="step-card">\s*<div class="step-badge">([\s\S]*?)<\/div>\s*([\s\S]*?)\s*<\/div>/g, 
  '<details class="step-card"><summary class="step-badge">$1</summary>\n$2\n</details>');
console.log(replaced);
