with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'pointerlock' in line.lower():
        print(f"{i+1}: {line.strip()}")
