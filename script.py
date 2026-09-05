import os, re

def convert_steps_to_details(content):
    tokens = re.split(r'(</?div[^>]*>)', content)
    
    stack = []
    for i, token in enumerate(tokens):
        if token.startswith('<div'):
            if 'step-card' in token:
                tokens[i] = token.replace('<div', '<details', 1)
                stack.append('details')
            elif 'step-badge' in token:
                tokens[i] = token.replace('<div', '<summary', 1)
                stack.append('summary')
            else:
                stack.append('div')
        elif token.startswith('</div'):
            if stack:
                popped = stack.pop()
                if popped == 'details':
                    tokens[i] = '</details>'
                elif popped == 'summary':
                    tokens[i] = '</summary>'
    
    return ''.join(tokens)

count = 0
for root, dirs, files in os.walk('content'):
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                original = file.read()
            
            converted = convert_steps_to_details(original)
            
            if original != converted:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(converted)
                count += 1

print('Total converted:', count)
