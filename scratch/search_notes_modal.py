with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if any(x in line for x in ['openNotesModal', 'toggleBag', 'notes-modal', 'closeNotesModal']):
        print(f"{i+1}: {line.strip()}")
