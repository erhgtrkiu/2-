with open('C:/Users/m3615/samosbor_game/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'notes-modal' in line or 'modal' in line:
        print(f"{i+1}: {line.strip()}")
