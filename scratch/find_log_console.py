import re

with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'function logToConsole' in line:
        print(f"{idx+1}: {line.strip()}")
        for j in range(1, 40):
            print(f"{idx+1+j}: {lines[idx+j].strip()}")
        break
