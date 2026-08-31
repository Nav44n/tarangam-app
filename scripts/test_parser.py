import re

def transform_custom_widgets(markdown_text):
    # 1. Admonition Callouts
    for callout_type, icon in [
        ("intuition", "💡 The Intuition"),
        ("pitfall", "⚠️ Common Exam Trap"),
        ("formula", "📐 KTU Formula Sheet"),
        ("exam", "🎯 KTU Exam Focus")
    ]:
        pattern = rf"::: callout-{callout_type} (.*?)\n(.*?)\n:::"
        def repl_callout(m, icon=icon, ctype=callout_type):
            title = m.group(1).strip()
            content = m.group(2).strip()
            header = f"{icon}: {title}" if title else icon
            return f'<div class="callout callout-{ctype}"><div class="callout-header">{header}</div><div class="callout-body">{content}</div></div>'
        markdown_text = re.sub(pattern, repl_callout, markdown_text, flags=re.DOTALL)

    # 2. Interactive Quizzes
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
                # Correct option: (*B) Text
                opt_text = line[line.index(")")+1:].strip()
                options.append((opt_text, True))
            elif line.startswith("(") and ")" in line and not line.startswith("(*"):
                # Wrong option: (A) Text
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

    # 3. Interactive Toggles (legacy fallback)
    toggle_pattern = r"::: toggle (.*?)\n(.*?)\n:::"
    replacement = r'<details class="interactive-toggle"><summary>\1</summary><div class="toggle-content">\2</div></details>'
    markdown_text = re.sub(toggle_pattern, replacement, markdown_text, flags=re.DOTALL)

    # 4. Stepped Numerical Solution Cards
    step_pattern = r"::: step \[(.*?)\] (.*?)\n(.*?)\n:::"
    def repl_step(m):
        badge = m.group(1).strip()
        title = m.group(2).strip()
        content = m.group(3).strip()
        return f'<div class="step-card"><div class="step-badge">{badge}</div><div class="step-title">{title}</div><div class="step-content">{content}</div></div>'
    markdown_text = re.sub(step_pattern, repl_step, markdown_text, flags=re.DOTALL)

    # 5. Manim Video Studio Player
    manim_pattern = r"::: manim (.*?) (.*?)\n(.*?)\n:::"
    def repl_manim(m):
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
    markdown_text = re.sub(manim_pattern, repl_manim, markdown_text, flags=re.DOTALL)

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

print("Test parser compiled.")
