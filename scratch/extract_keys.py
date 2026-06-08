import re
import sys

# Reconfigure stdout to support UTF-8 print
sys.stdout.reconfigure(encoding='utf-8')

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract data-i18n attributes
keys = re.findall(r'data-i18n="([^"]+)"', content)
unique_keys = sorted(list(set(keys)))

print(f"Total keys found: {len(unique_keys)}")
print("Keys list:")
for key in unique_keys:
    print(f"  - {key}")
