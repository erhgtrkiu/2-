import re

with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'language' in line.lower() and 'function' in line.lower():
        print(f"{idx+1}: {line.strip()[:100]}")
    elif 't(' in line and 'function' in line:
        print(f"{idx+1}: {line.strip()[:100]}")
