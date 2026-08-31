import os

CONTENT_DIR = os.path.join("content", "PCCST503")

# Re-read and fix any mangled \t or \theta in m1_01, m1_02, m1_03
for filename in os.listdir(CONTENT_DIR):
    if not filename.endswith(".md"): continue
    filepath = os.path.join(CONTENT_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Fix tab mangling
    content = content.replace("\text", r"\text")
    content = content.replace("    ext{", r"\text{")
    content = content.replace("   ext{", r"\text{")
    content = content.replace("  ext{", r"\text{")
    content = content.replace("	ext{", r"\text{")
    content = content.replace("   heta", r"\theta")
    content = content.replace("  heta", r"\theta")
    content = content.replace("	heta", r"\theta")
    content = content.replace(" imes", r"\times")
    content = content.replace("	imes", r"\times")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("TeX syntax restored across all Markdown files.")
