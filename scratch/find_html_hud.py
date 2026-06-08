import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/m3615/samosbor_game/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'mask' in line or 'water' in line or 'btn' in line or 'inventory' in line:
        if '<div' in line or '<button' in line or 'id=' in line:
            print(f"{idx+1}: {line.strip()[:120]}")
