with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'animateMenuNature' in line or 'drawProceduralNature' in line:
        print(f"{i+1}: {line.strip()}")
