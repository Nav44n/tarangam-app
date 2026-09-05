import fs from 'fs';
import path from 'path';
import { marked } from 'marked';
import { markedHighlight } from 'marked-highlight';
import hljs from 'highlight.js';

marked.use(markedHighlight({
  langPrefix: 'hljs language-',
  highlight(code, lang) {
    const language = hljs.getLanguage(lang) ? lang : 'plaintext';
    return hljs.highlight(code, { language }).value;
  }
}));

const CONTENT_DIR = 'content';
const OUTPUT_DIR = 'dist';
const TEMPLATE_PATH = path.join('templates', 'base.html');
const globalQuestionBank = [];

const COURSE_METADATA = {
  PCCST503: 'Machine Learning',
  PCCST501: 'Computer Networks',
  PCCST502: 'Design and Analysis of Algorithms',
  PBCST504: 'Microcontrollers',
  PECST522: 'Artificial Intelligence',
  PCCSL507: 'Networks Lab',
  PCCSL508: 'Machine Learning Lab'
};

const MODULE_NAMES = {
  PCCSL507: {
    0: 'Syllabus & Blueprint'
  },
  PCCSL508: {
    0: 'Syllabus & Blueprint'
  },
  PBCST504: {
    0: 'Syllabus & Blueprint',
    1: 'ARM Cortex-M Architecture',
    2: 'STM32 & Peripheral Programming',
    3: 'Protocols & USB Interface',
    4: 'IoT, RTOS & TrustZone'
  },
  PECST522: {
    0: 'Syllabus & Blueprint',
    1: 'Agents & Problem Solving',
    2: 'Search & Game Playing',
    3: 'Knowledge & Logic',
    4: 'Reinforcement Learning'
  },
  PCCST502: {
    0: 'Syllabus & Blueprint',
    1: 'Analysis & Recurrences',
    2: 'Graphs & Divide/Conquer',
    3: 'Greedy, DP & Backtracking',
    4: 'Branch/Bound & Complexity'
  },
  PCCST501: {
    0: 'Syllabus & Blueprint',
    1: 'Application Layer',
    2: 'Transport & Network Layer',
    3: 'Data Link Layer',
    4: 'Physical Layer & SNMP'
  },
  PCCST503: {
    0: 'Syllabus & Blueprint',
    1: 'Foundations & Regression',
    2: 'Classification & Trees',
    3: 'Neural Nets & SVMs',
    4: 'PCA & Ensembles'
  }
};

// Configure marked
marked.setOptions({
  gfm: true,
  breaks: false
});

function transformCustomWidgets(markdownText, pageData) {
  // 1. Admonition Callouts (Clickable Dropdowns: intuitions collapsed by default)
  const callouts = [
    { type: 'intuition', icon: '💡 The Intuition' },
    { type: 'pitfall', icon: '⚠️ Common Exam Trap' },
    { type: 'formula', icon: '📐 KTU Formula Vault' },
    { type: 'exam', icon: '🎯 KTU Exam Focus' }
  ];

  for (const { type, icon } of callouts) {
    const pattern = new RegExp(`::: callout-${type}(?:[ \\t]+(.*?))?\\n([\\s\\S]*?)\\n:::`, 'g');
    markdownText = markdownText.replace(pattern, (match, title, rawBody) => {
      const trimmedTitle = (title || '').trim();
      const renderedBody = marked.parse(rawBody.trim());
      const header = trimmedTitle ? `${icon}: ${trimmedTitle}` : icon;
      const isOpen = false; // All intuitions are clickable dropdowns (closed by default)
      const openAttr = isOpen ? ' open' : '';
      return `<details class="callout callout-${type}"${openAttr}><summary class="callout-header"><span class="callout-title">${header}</span><span class="callout-toggle-wrap"><span class="callout-hint"></span><span class="callout-chevron">&#9662;</span></span></summary><div class="callout-body">${renderedBody}</div></details>`;
    });
  }

  // 2. Interactive Quizzes with Clickable Dropdown Insight
  const quizPattern = /::: quiz ([\s\S]*?)\r?\n([\s\S]*?)\r?\n::: explanation\r?\n([\s\S]*?)\r?\n:::/g;
  markdownText = markdownText.replace(quizPattern, (match, qHeader, body, explanation) => {
    const lines = body.split('\n');
    let prompt = '';
    const options = [];

    for (let line of lines) {
      line = line.trim();
      if (!line) continue;
      if (line.startsWith('(*') && line.includes(')')) {
        const optText = line.substring(line.indexOf(')') + 1).trim();
        options.push({ text: optText, isCorrect: true });
      } else if (line.startsWith('(') && line.includes(')') && !line.startsWith('(*')) {
        const optText = line.substring(line.indexOf(')') + 1).trim();
        options.push({ text: optText, isCorrect: false });
      } else {
        prompt += line + ' ';
      }
    }

    let optionsHtml = '';
    const questionId = 'q-' + Math.random().toString(36).substr(2, 9);
    if (pageData) {
      globalQuestionBank.push({
        id: questionId,
        topicId: pageData.id,
        courseCode: pageData.course_code,
        topicTitle: pageData.title,
        url: pageData.course_code + '/' + pageData.filename,
        category: qHeader.trim(),
        prompt: prompt.trim(),
        options: options,
        explanation: explanation.trim()
      });
    }
    for (const { text, isCorrect } of options) {
      const correctAttr = isCorrect ? 'data-correct="true"' : 'data-correct="false"';
      optionsHtml += `<button class="quiz-option-btn" ${correctAttr}><span>${text}</span></button>\n`;
    }

    return `<div class="quiz-widget" id="${questionId}">
  <div class="quiz-header">
    <span class="quiz-category">${qHeader.trim()}</span>
    <span class="quiz-xp">+10 XP</span>
  </div>
  <div class="quiz-prompt">${prompt.trim()}</div>
  <div class="quiz-options">
    ${optionsHtml}
  </div>
  <details class="quiz-explanation-dropdown">
    <summary class="quiz-explanation-toggle">
      <div class="insight-badge-wrap">
        <span class="insight-badge">💡 Pedagogical Insight</span>
      </div>
      <div class="insight-action-text">
        <span class="insight-toggle-hint">Click to view/hide</span>
        <span class="insight-toggle-arrow">&#9662;</span>
      </div>
    </summary>
    <div class="quiz-explanation-content">
      ${marked.parse(explanation.trim())}
    </div>
  </details>
</div>`;
  });

  // 3. Stepped Numerical Solution Cards
  const stepPattern = /::: step \[(.*?)\] (.*?)\n([\s\S]*?)\n:::/g;
  markdownText = markdownText.replace(stepPattern, (match, badge, title, rawContent) => {
    const renderedContent = marked.parse(rawContent.trim());
    return `<details class="step-card"><summary class="step-badge">${badge.trim()}</summary><div class="step-title">${title.trim()}</div><div class="step-content">${renderedContent}</div></details>`;
  });

  // 4. Interactive Toggles
  const togglePattern = /::: toggle (.*?)\n([\s\S]*?)\n:::/g;
  markdownText = markdownText.replace(togglePattern, (match, summary, rawContent) => {
    const renderedContent = marked.parse(rawContent.trim());
    return `<details class="interactive-toggle"><summary>${summary.trim()}</summary><div class="toggle-content">${renderedContent}</div></details>`;
  });

  // 5. Multi-line Manim Video Studio Player
  const manimMultiPattern = /::: manim (.*?) (.*?)\n([\s\S]*?)\n:::/g;
  markdownText = markdownText.replace(manimMultiPattern, (match, videoSrc, title, obs) => {
    return `<div class="video-studio">
  <div class="video-studio-header">
    <span class="video-tag">🎬 60FPS MANIM SIMULATION &middot; ${title.trim()}</span>
    <div class="video-speed-controls">
      <button class="speed-btn" data-speed="0.75">0.75x</button>
      <button class="speed-btn active" data-speed="1.0">1.0x</button>
      <button class="speed-btn" data-speed="1.25">1.25x</button>
      <button class="speed-btn" data-speed="1.5">1.5x</button>
    </div>
  </div>
  <div class="video-frame-wrap">
    <video controls preload="metadata">
      <source src="../../${videoSrc.trim()}" type="video/mp4">
      Your browser does not support embedded video.
    </video>
  </div>
  <div class="video-studio-foot">
    <p class="video-caption"><strong>Key Insight:</strong> ${title.trim()}</p>
    <div class="video-observations"><strong>What to observe:</strong> ${obs.trim()}</div>
  </div>
</div>`;
  });

  // Single-line manim fallback
  const singleManim = /::: manim (.*?) :::/g;
  markdownText = markdownText.replace(singleManim, (match, videoSrc) => {
    return `<div class="video-studio">
  <div class="video-studio-header">
    <span class="video-tag">🎬 60FPS MANIM SIMULATION</span>
    <div class="video-speed-controls">
      <button class="speed-btn" data-speed="0.75">0.75x</button>
      <button class="speed-btn active" data-speed="1.0">1.0x</button>
      <button class="speed-btn" data-speed="1.25">1.25x</button>
      <button class="speed-btn" data-speed="1.5">1.5x</button>
    </div>
  </div>
  <div class="video-frame-wrap">
    <video controls preload="metadata">
      <source src="../../${videoSrc.trim()}" type="video/mp4">
      Your browser does not support embedded video.
    </video>
  </div>
</div>`;
  });

  return markdownText;
}

function renderNavTree(modules, currentMod, currentId, courseCode) {
  let html = '';
  for (const [modNum, mod] of Object.entries(modules)) {
    const isModZero = parseInt(modNum, 10) === 0;
    const isOpen = parseInt(modNum, 10) === parseInt(currentMod, 10) || isModZero;
    const badgeLabel = isModZero ? 'SYL' : `M${modNum}`;
    const badgeStyle = isModZero ? 'style="background:rgba(56,189,248,0.2); color:#38bdf8; font-weight:700;"' : '';
    html += `
      <div class="module-block ${isOpen ? 'open' : ''}" data-mod="${modNum}">
        <button class="module-head" onclick="this.parentElement.classList.toggle('open')">
          <span class="module-num" ${badgeStyle}>${badgeLabel}</span>
          <span>${mod.title}</span>
          <span class="chev">&#9656;</span>
        </button>
        <div class="topic-list">`;
    for (const topic of mod.topics) {
      const isActive = topic.id === currentId;
      const href = courseCode ? `../${courseCode}/${topic.filename}` : topic.filename;
      html += `
          <a href="${href}" class="topic-link ${isActive ? 'active' : ''}" id="topic-${topic.id}">
            <span class="topic-dot"></span>
            <span>${topic.title}</span>
          </a>`;
    }
    html += `
        </div>
      </div>`;
  }
  return html;
}

function compileMarkdownToHtml(rawMarkdown, pageData) {
  // 1. Normalize display equations indented with 4+ spaces so marked does not turn them into indented <pre><code> blocks
  let text = rawMarkdown.replace(/^[ ]{4,}(\$\$[\s\S]*?\$\$[ ]*)$/gm, (match, block) => {
    return '  ' + block.trim();
  });

  const mathTokens = [];
  const codeBlocks = [];
  const inlineCodes = [];

  // 2. Protect fenced code blocks (``` ... ```)
  text = text.replace(/```[\s\S]*?```/g, (m) => {
    const id = codeBlocks.length;
    codeBlocks.push(m);
    return `@@CODE_BLOCK_${id}@@`;
  });

  // 3. Protect inline code (`...`)
  text = text.replace(/`[^`\n]+?`/g, (m) => {
    const id = inlineCodes.length;
    inlineCodes.push(m);
    return `@@INLINE_CODE_${id}@@`;
  });

  // 4. Protect display math ($$...$$)
  text = text.replace(/\$\$([\s\S]*?)\$\$/g, (m) => {
    const id = mathTokens.length;
    mathTokens.push(m);
    return `@@MATH_DISPLAY_${id}@@`;
  });

  // 5. Protect inline math ($...$) - require non-space after opening $ and non-space before closing $
  text = text.replace(/\$([^\$\s](?:[^\$\n]*?[^\$\s])?)\$/g, (m) => {
    const id = mathTokens.length;
    mathTokens.push(m);
    return `@@MATH_INLINE_${id}@@`;
  });

  // 6. Restore code blocks and inline code so marked handles them normally
  text = text.replace(/@@INLINE_CODE_(\d+)@@/g, (m, id) => inlineCodes[parseInt(id, 10)]);
  text = text.replace(/@@CODE_BLOCK_(\d+)@@/g, (m, id) => codeBlocks[parseInt(id, 10)]);

  // 7. Transform custom widgets (callouts, quizzes, steps, toggles, manim)
  text = transformCustomWidgets(text, pageData);

  // 8. Parse markdown using marked
  let html = marked.parse(text);

  // 9. Restore all preserved math tokens byte-for-byte
  html = html.replace(/@@MATH_(?:DISPLAY|INLINE)_(\d+)@@/g, (m, id) => {
    let token = mathTokens[parseInt(id, 10)];
    return token.replace(/</g, '&lt;').replace(/>/g, '&gt;');
  });

  return html;
}

function renderTemplate(templateStr, data) {
  let result = templateStr;

  // Simple string replacements using function callbacks so $$ is never reduced to $
  result = result.replace(/\{\{\s*title\s*\}\}/g, () => data.title || '');
  result = result.replace(/\{\{\s*course_name\s*\}\}/g, () => data.course_name || '');
  result = result.replace(/\{\{\s*course_code\s*\}\}/g, () => data.course_code || '');
  result = result.replace(/\{\{\s*current_mod\s*\}\}/g, () => (data.current_mod !== undefined ? String(data.current_mod) : ''));
  result = result.replace(/\{\{\s*current_id\s*\}\}/g, () => data.current_id || '');
  result = result.replace(/\{\{\s*total_topics\s*\|\s*default\(0\)\s*\}\}/g, () => (data.total_topics !== undefined ? String(data.total_topics) : '0'));
  result = result.replace(/\{\{\s*total_topics\s*\}\}/g, () => (data.total_topics !== undefined ? String(data.total_topics) : '0'));
  result = result.replace(/\{\{\s*content\s*\|\s*safe\s*\}\}/g, () => data.content || '');

  // Render navigation module tree
  const navTreeHtml = renderNavTree(data.modules || {}, data.current_mod, data.current_id, data.course_code);
  result = result.replace(/\{\{\s*nav_tree\s*\|\s*safe\s*\}\}/g, () => navTreeHtml);
  // Also replace legacy template loop if present
  result = result.replace(/\{%\s*for mod_num, mod in modules\.items\(\)\s*%\}[\s\S]*?\{%\s*endfor\s*%\}\s*(?=<\/nav>)/g, () => navTreeHtml);

  // Render previous page link
  const prevPattern = /\{%\s*if prev_page\s*%\}([\s\S]*?)\{%\s*else\s*%\}([\s\S]*?)\{%\s*endif\s*%\}/;
  result = result.replace(prevPattern, (match, hasPrev, noPrev) => {
    if (data.prev_page) {
      return hasPrev
        .replace(/\{\{\s*prev_page\.filename\s*\}\}/g, () => data.prev_page.filename)
        .replace(/\{\{\s*prev_page\.title\s*\}\}/g, () => data.prev_page.title);
    }
    return noPrev;
  });

  // Render next page link
  const nextPattern = /\{%\s*if next_page\s*%\}([\s\S]*?)\{%\s*else\s*%\}([\s\S]*?)\{%\s*endif\s*%\}/;
  result = result.replace(nextPattern, (match, hasNext, noNext) => {
    if (data.next_page) {
      return hasNext
        .replace(/\{\{\s*next_page\.filename\s*\}\}/g, () => data.next_page.filename)
        .replace(/\{\{\s*next_page\.title\s*\}\}/g, () => data.next_page.title);
    }
    return noNext;
  });

  return result;
}

function formatTopicTitle(filename) {
  const cleanName = filename.replace(/\.md$/, '');
  if (cleanName.startsWith('m0_')) {
    const rawSubject = cleanName.replace(/^m0_\d*_+/i, '').replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    return `📋 ${rawSubject || 'Official Syllabus & Blueprint'}`;
  }
  const labMatch = cleanName.match(/^m(\d+)_99_practice_lab_(.*)$/i);
  if (labMatch) {
    const modNum = labMatch[1];
    const rawSubject = labMatch[2].replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    return `🧪 Practice Lab: M${modNum} ${rawSubject}`;
  }

  const probMatch = cleanName.match(/^m(\d+)_p(\d+)_(.*)$/i);
  if (probMatch) {
    const rawSubject = probMatch[3].replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    return `📝 Workbook: ${rawSubject}`;
  }

  const topicMatch = cleanName.match(/^m(\d+)_(\d+)_(.*)$/i);
  if (topicMatch) {
    const modNum = parseInt(topicMatch[1], 10);
    const topNum = parseInt(topicMatch[2], 10);
    const rawSubject = topicMatch[3].replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    return `${modNum}.${topNum} ${rawSubject}`;
  }

  return cleanName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

export function buildSite() {
  const templateStr = fs.readFileSync(TEMPLATE_PATH, 'utf-8');
  const coursesData = {};

  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  const courseDirs = fs.readdirSync(CONTENT_DIR);

  for (const courseCode of courseDirs) {
    const coursePath = path.join(CONTENT_DIR, courseCode);
    if (!fs.statSync(coursePath).isDirectory()) continue;

    const courseOutDir = path.join(OUTPUT_DIR, courseCode);
    if (!fs.existsSync(courseOutDir)) {
      fs.mkdirSync(courseOutDir, { recursive: true });
    }

    const courseName = COURSE_METADATA[courseCode] || courseCode;
    const modules = {};
    const pages = [];

    const files = fs.readdirSync(coursePath)
      .filter(f => f.endsWith('.md') && !f.startsWith('_'))
      .sort();

    for (const filename of files) {
      const modMatch = filename.match(/^m(\d+)_/);
      const modNum = modMatch ? parseInt(modMatch[1], 10) : 0;
      const rawMd = fs.readFileSync(path.join(coursePath, filename), 'utf-8');
      const h1Match = rawMd.match(/^#\s+(.+)$/m);
      const title = h1Match ? h1Match[1].trim() : formatTopicTitle(filename);
      const htmlFilename = filename.replace(/\.md$/, '.html');

      if (!modules[modNum]) {
        const modTitle = MODULE_NAMES[courseCode]?.[modNum] || `Module ${modNum}`;
        modules[modNum] = { num: modNum, title: modTitle, topics: [] };
      }

      const pageData = {
        id: filename.replace(/\.md$/, ''),
        title: title,
        filename: htmlFilename,
        source_path: path.join(coursePath, filename)
      };

      modules[modNum].topics.push(pageData);
      pages.push({ modNum, pageData });
    }

    // Render pages
    for (let idx = 0; idx < pages.length; idx++) {
      const { modNum, pageData: page } = pages[idx];
      const rawMarkdown = fs.readFileSync(page.source_path, 'utf-8');

      const wordCount = rawMarkdown.split(/\s+/).length;
      const readTime = Math.max(2, Math.round(wordCount / 180));

      const renderedHtmlBody = compileMarkdownToHtml(rawMarkdown, page);

      const prevPage = idx > 0 ? pages[idx - 1].pageData : null;
      const nextPage = idx < pages.length - 1 ? pages[idx + 1].pageData : null;

      const isSyllabus = modNum === 0;
      const badgeModText = isSyllabus ? 'SYLLABUS & BLUEPRINT' : `MODULE ${modNum}`;
      const quickJumpHtml = isSyllabus ? `
    <a href="#course-overview" class="jump-pill">📋 Overview</a>
    <a href="#course-objectives" class="jump-pill">🎯 Objectives</a>
    <a href="#module-by-module-syllabus-breakdown" class="jump-pill">📚 Modules (1–4)</a>
    <a href="#prescribed-reference-books-textbooks" class="jump-pill">📖 Textbooks</a>
    <a href="#course-assessment-method-cie-ese" class="jump-pill">⚖️ Evaluation (CIE/ESE)</a>
    <a href="#course-outcomes-cos" class="jump-pill">🎓 Outcomes (COs)</a>
    <a href="#co-po-mapping-table" class="jump-pill">🗺️ CO-PO Matrix</a>
      ` : `
    <a href="#the-intuition" class="jump-pill">💡 Intuition</a>
    <a href="#the-dimensions" class="jump-pill">📐 Dimensions</a>
    <a href="#foundations" class="jump-pill">🏛️ Foundations</a>
    <a href="#history" class="jump-pill">📜 History</a>
    <a href="#self-check" class="jump-pill">⚡ Self Check</a>
      `;

      const headerPrefix = `<div class="topic-header">
  <div class="topic-badges">
    <span class="badge badge-accent">${badgeModText}</span>
    <span class="badge">⏱️ ${readTime} MIN READ</span>
    <span class="badge badge-gold">🟢 BEGINNER FRIENDLY</span>
    <span class="badge">🎯 KTU 2024 SCHEME</span>
  </div>
  <div class="quick-jump-bar">
    ${quickJumpHtml}
  </div>
</div>\n`;

      const fullContent = headerPrefix + renderedHtmlBody;

      const fullHtmlDoc = renderTemplate(templateStr, {
        content: fullContent,
        title: page.title,
        current_id: page.id,
        current_mod: modNum,
        modules: modules,
        prev_page: prevPage,
        next_page: nextPage,
        total_topics: pages.length,
        course_code: courseCode,
        course_name: courseName
      });

      const targetPath = path.join(courseOutDir, page.filename);
      fs.writeFileSync(targetPath, fullHtmlDoc, 'utf-8');
    }

    coursesData[courseCode] = {
      name: courseName,
      modules: modules
    };
  }

  fs.writeFileSync(path.join(OUTPUT_DIR, 'navigation_index.json'), JSON.stringify(coursesData, null, 2), 'utf-8');

  // Copy style.css to dist
  if (fs.existsSync('style.css')) {
    fs.copyFileSync('style.css', path.join(OUTPUT_DIR, 'style.css'));
  }

  // Create .nojekyll in dist
  fs.writeFileSync(path.join(OUTPUT_DIR, '.nojekyll'), '', 'utf-8');

  // Copy root index.html to dist/index.html with adjusted paths for standalone hosting
  if (fs.existsSync('index.html')) {
    let rootIndex = fs.readFileSync('index.html', 'utf-8');
    // Replace "dist/" prefix for links inside dist/
    const standaloneIndex = rootIndex.replace(/href="dist\//g, 'href="');
    fs.writeFileSync(path.join(OUTPUT_DIR, 'index.html'), standaloneIndex, 'utf-8');
  }
  
  if (fs.existsSync('review.html')) {
    fs.cpSync('review.html', path.join(OUTPUT_DIR, 'review.html'));
  }
  if (fs.existsSync('shared.js')) {
    fs.cpSync('shared.js', path.join(OUTPUT_DIR, 'shared.js'));
  }
  if (fs.existsSync('style.css')) {
    fs.cpSync('style.css', path.join(OUTPUT_DIR, 'style.css'));
  }

  // Copy assets and media if they exist
  if (fs.existsSync('assets')) {
    fs.cpSync('assets', path.join(OUTPUT_DIR, 'assets'), { recursive: true });
  }
  if (fs.existsSync('media')) {
    fs.cpSync('media', path.join(OUTPUT_DIR, 'media'), { recursive: true });
  }

  fs.writeFileSync(path.join(OUTPUT_DIR, 'questionBank.json'), JSON.stringify(globalQuestionBank, null, 2));
  console.log('📚 Saved ' + globalQuestionBank.length + ' questions to questionBank.json');
  console.log('✅ Tarangam curriculum compilation completed successfully.');
}

buildSite();
