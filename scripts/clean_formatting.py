import os
import re

directory = "content/PCCST503"

for filename in os.listdir(directory):
    if not filename.endswith(".md"):
        continue
        
    filepath = os.path.join(directory, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    new_lines = []
    for line in lines:
        # If the line starts with exactly 4 spaces (or more) and has HTML, or just in general is theory text
        # Actually, let's just strip up to 4 leading spaces if it starts with spaces
        if line.startswith("    "):
            new_lines.append(line[4:])
        else:
            new_lines.append(line)
            
    # Also let's try to convert some basic HTML to Markdown for a cleaner look
    content = "".join(new_lines)
    content = content.replace("<p>", "").replace("</p>", "\n\n")
    content = content.replace("<strong>", "**").replace("</strong>", "**")
    content = content.replace("<i>", "*").replace("</i>", "*")
    content = content.replace("<em>", "*").replace("</em>", "*")
    content = content.replace("<br>", "\n")
    content = content.replace("<br/>", "\n")
    content = content.replace("<ul>", "").replace("</ul>", "")
    content = content.replace("<li>", "- ").replace("</li>", "")
    content = content.replace("<code>", "`").replace("</code>", "`")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Formatting cleanup completed.")
