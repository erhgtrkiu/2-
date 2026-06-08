with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# find function definitions or blocks containing collision checks
matches = re.findall(r'function\s+\w*collision\w*\(.*?\)\s*\{.*?\}', text, re.DOTALL | re.IGNORECASE)
for m in matches:
    print(m[:500])
    print("-" * 40)
