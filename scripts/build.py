import os
import json
import re
import markdown
from jinja2 import Environment, FileSystemLoader

CONTENT_DIR = "content"
OUTPUT_DIR = "dist"
TEMPLATE_DIR = "templates"

def transform_custom_widgets(markdown_text):
    toggle_pattern = r"::: toggle (.*?)\n(.*?)\n:::"
    replacement = r'<details class="interactive-toggle"><summary>\1</summary><div class="toggle-content">\2</div></details>'
    transformed_text = re.sub(toggle_pattern, replacement, markdown_text, flags=re.DOTALL)

    manim_pattern = r"::: manim (.*?) :::"
    manim_html = r'<div class="video-container"><video controls preload="metadata"><source src="../\1" type="video/mp4">Your browser does not support embedded HTML5 video.</video></div>'
    return re.sub(manim_pattern, manim_html, transformed_text)

def generate_static_platform():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    base_template = jinja_env.get_template("base.html")

    md_processor = markdown.Markdown(extensions=['fenced_code', 'tables', 'toc', 'attr_list'])

    # Build navigation structure
    modules = {}
    pages = []
    
    # First pass: collect all pages
    for root, _, filenames in os.walk(CONTENT_DIR):
        for filename in sorted(filenames):
            if filename.endswith(".md"):
                # E.g. m1_01_ml_vs_trad.md -> module 1
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
                    "source_path": os.path.join(root, filename)
                }
                modules[mod_num]["topics"].append(page_data)
                pages.append((mod_num, page_data))

    # Second pass: render pages
    for idx, (mod_num, page) in enumerate(pages):
        with open(page["source_path"], "r", encoding="utf-8") as f:
            raw_markdown = f.read()
        
        preprocessed_markdown = transform_custom_widgets(raw_markdown)
        rendered_html_body = md_processor.convert(preprocessed_markdown)
        
        target_path = os.path.join(OUTPUT_DIR, page["filename"])
        
        prev_page = pages[idx-1][1] if idx > 0 else None
        next_page = pages[idx+1][1] if idx < len(pages)-1 else None

        full_html_document = base_template.render(
            content=rendered_html_body,
            title=page["title"],
            current_id=page["id"],
            current_mod=mod_num,
            modules=modules,
            prev_page=prev_page,
            next_page=next_page
        )

        with open(target_path, "w", encoding="utf-8") as f:
            f.write(full_html_document)

    # Dump navigation index for client side if needed
    with open(os.path.join(OUTPUT_DIR, "navigation_index.json"), "w", encoding="utf-8") as nav_writer:
        json.dump(modules, nav_writer, indent=2)

    print("Static platform compilation completed successfully.")

if __name__ == "__main__":
    if not os.path.exists(CONTENT_DIR):
        os.makedirs(CONTENT_DIR)
    generate_static_platform()

