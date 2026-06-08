with open('C:/Users/m3615/samosbor_game/index.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'action-grid' in line or 'btn-action' in line:
        print(f"{idx+1}: {line.strip()}")
        # print next 10 lines
        for j in range(1, 15):
            if idx+j < len(lines):
                print(f"{idx+1+j}: {lines[idx+j].strip()}")
        break
