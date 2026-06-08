with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines[:150]):
    if 'let ' in line or 'var ' in line or 'const ' in line:
        print(f"{idx+1}: {line.strip()}")
