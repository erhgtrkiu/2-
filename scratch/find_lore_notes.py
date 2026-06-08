import re

with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'LORE_NOTES = [' in line or 'let LORE_NOTES =' in line or 'const LORE_NOTES =' in line:
        print(f"{idx+1}: {line.strip()}")
        # print next 10 lines
        for j in range(1, 10):
            print(f"{idx+1+j}: {lines[idx+j].strip()}")
        break
