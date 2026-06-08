import re

with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'dev' in line.lower() and ('keydown' in line.lower() or 'keypress' in line.lower() or 'enter' in line.lower()):
        print(f"{idx+1}: {line.strip()[:100]}")
