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
    "PCCST502": "Algorithm Design"
}

def transform_custom_widgets(markdown_text):
    toggle_pattern = r"::: toggle (.*?)\n(.*?)\n:::"
    replacement = r'<details class="interactive-toggle"><summary>\1</summary><div class="toggle-content">\2</div></details>'
    transformed_text = re.sub(toggle_pattern, replacement, markdown_text, flags=re.DOTALL)

    # Ensure paths point one level up since HTML files are now inside dist/<course_code>/
    manim_pattern = r"::: manim (.*?) :::"
    manim_html = r'<div class="video-container"><video controls preload="metadata"><source src="../../\1" type="video/mp4">Your browser does not support embedded HTML5 video.</video></div>'
    return re.sub(manim_pattern, manim_html, transformed_text)

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
            
            preprocessed_markdown = transform_custom_widgets(raw_markdown)
            rendered_html_body = md_processor.convert(preprocessed_markdown)
            
            target_path = os.path.join(course_out_dir, page["filename"])
            
            prev_page = pages[idx-1][1] if idx > 0 else None
            next_page = pages[idx+1][1] if idx < len(pages)-1 else None

            full_html_document = base_template.render(
                content=rendered_html_body,
                title=page["title"],
                current_id=page["id"],
                current_mod=mod_num,
                modules=modules,
                prev_page=prev_page,
                total_topics=len(pages),
                next_page=next_page,
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

    print("Static platform compilation completed successfully.")

if __name__ == "__main__":
    generate_static_platform()

