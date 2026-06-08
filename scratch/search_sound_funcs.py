with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'function playSound' in line or 'playSound' in line:
        if line.strip().startswith('function') or 'const' in line or 'let' in line:
            print(f"{i+1}: {line.strip()}")
