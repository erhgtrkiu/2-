import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Match standard HTML tags: <tag attributes>Text</tag> or similar
# Let's find tags containing Cyrillic characters
# We can find tag boundaries and extract text between them.
# A simple regex for tag matching: <([a-zA-Z0-9\-]+)([^>]*)>([^<]*)
pattern = r'<([a-zA-Z0-9\-]+)([^>]*)>([^<]*)'
matches = re.finditer(pattern, content)

found = []
for m in matches:
    tag = m.group(1)
    attrs = m.group(2)
    text = m.group(3).strip()
    
    if re.search(r'[\u0400-\u04FF]', text):
        if 'data-i18n' not in attrs:
            # Check if it has an ID so it might be dynamically updated
            has_id = 'id=' in attrs
            found.append((tag, attrs, text, has_id))

print(f"Found {len(found)} tags containing Cyrillic characters without data-i18n:")
for tag, attrs, text, has_id in found:
    print(f"<{tag} {attrs.strip()}>: \"{text}\" (has id: {has_id})")
