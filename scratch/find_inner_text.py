import re

with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'innerText =' in line or 'innerHTML =' in line:
        if ('btn' in line or 'desc' in line or 'title' in line or 'status' in line) and not 'LORE_NOTES' in line:
            print(f"{idx+1}: {line.strip()[:120]}")
