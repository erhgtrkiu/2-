import re

with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'DEFAULT_KEY_BINDINGS' in line:
        print(f"{idx+1}: {line.strip()}")
        for j in range(1, 25):
            print(f"{idx+1+j}: {lines[idx+j].strip()}")
        break
