import re

with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'data-i18n' in line.lower() or 'i18n' in line.lower():
        print(f"{idx+1}: {line.strip()[:120]}")
