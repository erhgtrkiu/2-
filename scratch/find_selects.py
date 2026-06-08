with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'select' in line.lower() and ('event' in line.lower() or 'change' in line.lower() or 'el.' in line.lower() or 'document' in line.lower()):
        print(f"{idx+1}: {line.strip()[:120]}")
