import re

with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'document.querySelectorAll' in line:
        print(f"{idx+1}: {line.strip()[:120]}")
    elif 'querySelectorAll' in line:
        print(f"{idx+1}: {line.strip()[:120]}")
