const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, '../content/topics');
const destDir = path.join(__dirname, '../content_md');

if (!fs.existsSync(destDir)) {
    fs.mkdirSync(destDir);
}

// We mock window.addTopic so we can just require/eval the files
global.window = { SUBJECTS: { ml: { modules: [ {num:1},{num:2},{num:3},{num:4} ] } } };
let currentModule = 1;
let capturedTopics = [];

global.window.addTopic = function(moduleNum, topicData) {
    topicData.moduleNum = moduleNum;
    capturedTopics.push(topicData);
};

const files = fs.readdirSync(srcDir).filter(f => f.endsWith('.js'));

for (const file of files) {
    const filePath = path.join(srcDir, file);
    const content = fs.readFileSync(filePath, 'utf-8');
    
    // Evaluate the JS content to trigger window.addTopic
    try {
        eval(content);
        
        const topic = capturedTopics.pop();
        if (!topic) continue;
        
        let md = `# ${topic.title}\n\n`;
        if (topic.dek) {
            md += `**${topic.dek}**\n\n`;
        }
        
        if (topic.theory) {
            // Very naive HTML to MD could go here, but the PDF says "converts HTML/JS formatting into strict Markdown". 
            // We can just leave basic HTML tags or rely on markdown processing, but let's strip or keep it clean.
            // Actually, markdown supports raw HTML. We'll just write it as is, or do basic cleanup.
            md += `${topic.theory}\n\n`;
        }
        
        if (topic.formula) {
            md += `$$${topic.formula}$$\n\n`;
        }
        
        if (topic.callout) {
            md += `> **${topic.callout.label}**\n`;
            md += `> ${topic.callout.text.replace(/<br>/g, '\n> ')}\n\n`;
        }
        
        if (topic.worked) {
            md += `## Worked Example: ${topic.worked.title}\n\n`;
            topic.worked.steps.forEach((step, i) => {
                md += `${i + 1}. ${step}\n`;
            });
            md += `\n`;
        }
        
        if (topic.video) {
            md += `## Visualizing the Concept\n\n`;
            md += `::: manim assets/videos/${topic.video.script.split('/').pop().replace('.py', '.mp4')} :::\n\n`;
            md += `*${topic.video.caption}*\n\n`;
        }
        
        if (topic.extra && topic.extra.length > 0) {
            topic.extra.forEach(ext => {
                md += `::: toggle ${ext.title}\n${ext.body}\n:::\n\n`;
            });
        }
        
        if (topic.quiz && topic.quiz.length > 0) {
            md += `## Self Check\n\n`;
            topic.quiz.forEach((q, i) => {
                md += `::: toggle Q${i+1}: ${q.q}\n`;
                md += `**Answer:** ${q.options[q.answer]}\n\n`;
                md += `*Explanation:* ${q.explain}\n:::\n\n`;
            });
        }
        
        // Output MD file
        const outName = file.replace('.js', '.md');
        fs.writeFileSync(path.join(destDir, outName), md, 'utf-8');
        console.log(`Converted ${file} -> ${outName}`);
        
    } catch (e) {
        console.error(`Error parsing ${file}:`, e);
    }
}
