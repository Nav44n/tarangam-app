with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace('content: " ";', 'content: "\\u25bc";')
css = css.replace('content: "?";', 'content: "\\u25bc";')

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)
