with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines[:300]):
    if 'let ' in line or 'const ' in line:
        if '=' in line and not line.strip().startswith('//'):
            print(f"{i+1}: {line.strip()}")
