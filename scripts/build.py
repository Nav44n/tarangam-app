import os
import json
import re
import markdown
from jinja2 import Environment, FileSystemLoader

CONTENT_DIR = "content"
OUTPUT_DIR = "dist"
TEMPLATE_DIR = "templates"

COURSE_METADATA = {
    "PCCST503": "Machine Learning",
    "PCCST501": "Computer Networks",
    "PCCST502": "Design and Analysis of Algorithms", "PECST522": "Artificial Intelligence"
}

def transform_custom_widgets(markdown_text, md_processor):
    # 1. Admonition Callouts
    for callout_type, icon in [
        ("intuition", "💡 The Intuition"),
        ("pitfall", "⚠️ Common Exam Trap"),
        ("formula", "📐 KTU Formula Vault"),
        ("exam", "🎯 KTU Exam Focus")
    ]:
        pattern = rf"::: callout-{callout_type} (.*?)\n(.*?)\n:::"
        def repl_callout(m, icon=icon, ctype=callout_type):
            title = m.group(1).strip()
            raw_body = m.group(2).strip()
            rendered_body = md_processor.convert(raw_body)
            header = f"{icon}: {title}" if title else icon
            return f'<div class="callout callout-{ctype}"><div class="callout-header">{header}</div><div class="callout-body">{rendered_body}</div></div>'
        markdown_text = re.sub(pattern, repl_callout, markdown_text, flags=re.DOTALL)

    # 2. Interactive Quizzes (Brilliant-style)
    quiz_pattern = r"::: quiz (.*?)\n(.*?)\n::: explanation\n(.*?)\n:::"
    def repl_quiz(m):
        q_header = m.group(1).strip()
        body = m.group(2).strip()
        explanation = m.group(3).strip()
        
        lines = body.split("\n")
        prompt = ""
        options = []
        
        for line in lines:
            line = line.strip()
            if not line: continue
            if line.startswith("(*") and ")" in line:
                opt_text = line[line.index(")")+1:].strip()
                options.append((opt_text, True))
            elif line.startswith("(") and ")" in line and not line.startswith("(*"):
                opt_text = line[line.index(")")+1:].strip()
                options.append((opt_text, False))
            else:
                prompt += line + " "

        options_html = ""
        for opt_text, is_correct in options:
            correct_attr = 'data-correct="true"' if is_correct else 'data-correct="false"'
            options_html += f'<button class="quiz-option-btn" {correct_attr}><span>{opt_text}</span></button>\n'

        return f'''<div class="quiz-widget">
  <div class="quiz-header">
    <span class="quiz-category">{q_header}</span>
    <span class="quiz-xp">+10 XP</span>
  </div>
  <div class="quiz-prompt">{prompt.strip()}</div>
  <div class="quiz-options">
    {options_html}
  </div>
  <div class="quiz-explanation">
    <strong>Pedagogical Insight:</strong> {explanation}
  </div>
</div>'''

    markdown_text = re.sub(quiz_pattern, repl_quiz, markdown_text, flags=re.DOTALL)

    # 3. Stepped Numerical Solution Cards
    step_pattern = r"::: step \[(.*?)\] (.*?)\n(.*?)\n:::"
    def repl_step(m):
        badge = m.group(1).strip()
        title = m.group(2).strip()
        raw_content = m.group(3).strip()
        rendered_content = md_processor.convert(raw_content)
        return f'<div class="step-card"><div class="step-badge">{badge}</div><div class="step-title">{title}</div><div class="step-content">{rendered_content}</div></div>'
    markdown_text = re.sub(step_pattern, repl_step, markdown_text, flags=re.DOTALL)

    # 4. Interactive Toggles
    toggle_pattern = r"::: toggle (.*?)\n(.*?)\n:::"
    def repl_toggle(m):
        summary = m.group(1).strip()
        raw_content = m.group(2).strip()
        rendered_content = md_processor.convert(raw_content)
        return f'<details class="interactive-toggle"><summary>{summary}</summary><div class="toggle-content">{rendered_content}</div></details>'
    markdown_text = re.sub(toggle_pattern, repl_toggle, markdown_text, flags=re.DOTALL)

    # 5. Multi-line Manim Video Studio Player
    manim_multi_pattern = r"::: manim (.*?) (.*?)\n(.*?)\n:::"
    def repl_manim_multi(m):
        video_src = m.group(1).strip()
        title = m.group(2).strip()
        obs = m.group(3).strip()
        return f'''<div class="video-studio">
  <div class="video-studio-header">
    <span class="video-tag">🎬 60FPS MANIM SIMULATION &middot; {title}</span>
    <div class="video-speed-controls">
      <button class="speed-btn" data-speed="0.75">0.75x</button>
      <button class="speed-btn active" data-speed="1.0">1.0x</button>
      <button class="speed-btn" data-speed="1.25">1.25x</button>
      <button class="speed-btn" data-speed="1.5">1.5x</button>
    </div>
  </div>
  <div class="video-frame-wrap">
    <video controls preload="metadata">
      <source src="../../{video_src}" type="video/mp4">
      Your browser does not support embedded video.
    </video>
  </div>
  <div class="video-studio-foot">
    <p class="video-caption"><strong>Key Insight:</strong> {title}</p>
    <div class="video-observations"><strong>What to observe:</strong> {obs}</div>
  </div>
</div>'''
    markdown_text = re.sub(manim_multi_pattern, repl_manim_multi, markdown_text, flags=re.DOTALL)

    # Single-line manim fallback
    single_manim = r"::: manim (.*?) :::"
    single_repl = r'''<div class="video-studio">
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
      <source src="../../\1" type="video/mp4">
      Your browser does not support embedded video.
    </video>
  </div>
</div>'''
    markdown_text = re.sub(single_manim, single_repl, markdown_text)

    return markdown_text

def generate_static_platform():
    jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    base_template = jinja_env.get_template("base.html")
    md_processor = markdown.Markdown(extensions=['fenced_code', 'tables', 'toc', 'attr_list'])

    courses_data = {}

    for course_code in os.listdir(CONTENT_DIR):
        course_path = os.path.join(CONTENT_DIR, course_code)
        if not os.path.isdir(course_path): continue
        
        course_out_dir = os.path.join(OUTPUT_DIR, course_code)
        os.makedirs(course_out_dir, exist_ok=True)
        
        course_name = COURSE_METADATA.get(course_code, course_code)
        modules = {}
        pages = []
        
        for filename in sorted(os.listdir(course_path)):
            if filename.endswith(".md"):
                mod_match = re.match(r"m(\d+)_", filename)
                mod_num = int(mod_match.group(1)) if mod_match else 0
                title = filename.replace(".md", "").replace("_", " ").title()
                html_filename = filename.replace(".md", ".html")
                
                if mod_num not in modules:
                    modules[mod_num] = {"num": mod_num, "title": f"Module {mod_num}", "topics": []}
                
                page_data = {
                    "id": filename.replace(".md", ""),
                    "title": title,
                    "filename": html_filename,
                    "source_path": os.path.join(course_path, filename)
                }
                modules[mod_num]["topics"].append(page_data)
                pages.append((mod_num, page_data))
                
        # Render pages for this course
        for idx, (mod_num, page) in enumerate(pages):
            with open(page["source_path"], "r", encoding="utf-8") as f:
                raw_markdown = f.read()
            
            # Estimate read time (avg 200 wpm)
            word_count = len(raw_markdown.split())
            read_time = max(2, round(word_count / 180))
            
            preprocessed_markdown = transform_custom_widgets(raw_markdown, md_processor)
            rendered_html_body = md_processor.convert(preprocessed_markdown)
            
            target_path = os.path.join(course_out_dir, page["filename"])
            
            prev_page = pages[idx-1][1] if idx > 0 else None
            next_page = pages[idx+1][1] if idx < len(pages)-1 else None

            # Add hero header if not present
            header_prefix = f'''<div class="topic-header">
  <div class="topic-badges">
    <span class="badge badge-accent">MODULE {mod_num}</span>
    <span class="badge">⏱️ {read_time} MIN READ</span>
    <span class="badge badge-gold">🟢 BEGINNER FRIENDLY</span>
    <span class="badge">🎯 KTU 2024 SCHEME</span>
  </div>
  <div class="quick-jump-bar">
    <a href="#the-intuition" class="jump-pill">💡 Intuition</a>
    <a href="#the-math" class="jump-pill">📐 The Math</a>
    <a href="#worked-example" class="jump-pill">✍️ Worked Example</a>
    <a href="#simulation" class="jump-pill">🎬 Simulation</a>
    <a href="#self-check" class="jump-pill">⚡ Self Check</a>
  </div>
</div>
'''
            full_content = header_prefix + rendered_html_body

            full_html_document = base_template.render(
                content=full_content,
                title=page["title"],
                current_id=page["id"],
                current_mod=mod_num,
                modules=modules,
                prev_page=prev_page,
                next_page=next_page,
                total_topics=len(pages),
                course_code=course_code,
                course_name=course_name
            )

            with open(target_path, "w", encoding="utf-8") as f:
                f.write(full_html_document)
                
        courses_data[course_code] = {
            "name": course_name,
            "modules": modules
        }

    with open(os.path.join(OUTPUT_DIR, "navigation_index.json"), "w", encoding="utf-8") as nav_writer:
        json.dump(courses_data, nav_writer, indent=2)

    print("Production static platform compilation completed successfully.")

if __name__ == "__main__":
    generate_static_platform()


