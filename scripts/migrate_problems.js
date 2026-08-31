const fs = require('fs');
const path = require('path');

const srcFile = path.join(__dirname, '../content/problems.js');
const destDir = path.join(__dirname, '../content_md');

global.window = {};
let problemsByModule = {};

global.window.addProblemSet = function(moduleNum, probData) {
    if (!problemsByModule[moduleNum]) {
        problemsByModule[moduleNum] = [];
    }
    problemsByModule[moduleNum].push(probData);
};

const content = fs.readFileSync(srcFile, 'utf-8');

try {
    eval(content);
    
    for (const [modNum, problems] of Object.entries(problemsByModule)) {
        let md = `# Module ${modNum} Practice Problems\n\n`;
        md += `Master these exact numerical types for the university exam.\n\n`;
        
        problems.forEach(prob => {
            md += `## ${prob.type}: ${prob.title}\n\n`;
            md += `${prob.scenario}\n\n`;
            
            md += `::: toggle Show Step-by-Step Solution\n`;
            prob.steps.forEach((step, i) => {
                md += `**${step.title}**\n\n${step.body}\n\n`;
            });
            md += `:::\n\n---\n\n`;
        });
        
        const outName = `m${modNum}_99_practice.md`;
        fs.writeFileSync(path.join(destDir, outName), md, 'utf-8');
        console.log(`Created practice file: ${outName}`);
    }
} catch (e) {
    console.error(`Error parsing problems:`, e);
}
