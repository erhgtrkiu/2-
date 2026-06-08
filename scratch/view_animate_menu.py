with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
match = re.search(r'function\s+animateMenuNature.*?(?=function|\/\/\s*-)', text, re.DOTALL)
if match:
    print(match.group(0))
else:
    print("Not found")
