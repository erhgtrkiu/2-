import re

with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'function updateInventoryUI' in line or 'function updateHUD' in line:
        print(f"{idx+1}: {line.strip()}")
        # print next 30 lines
        for j in range(1, 30):
            print(f"{idx+1+j}: {lines[idx+j].strip()}")
