with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start = -1
for i, line in enumerate(lines):
    if 'function animateMenuNature' in line:
        start = i
        break

if start != -1:
    for j in range(start, min(len(lines), start + 200)):
        print(f"{j+1}: {lines[j].strip()}")
else:
    print("Not found")
