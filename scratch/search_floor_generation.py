with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'floorMat' in line or 'BoxGeometry' in line or 'Mesh' in line:
        if 'floor' in line.lower() or 'ceiling' in line.lower():
            if 'buildFloor' in lines[max(0, i-50):i+10]: # print context near buildFloor
                print(f"{i+1}: {line.strip()}")
