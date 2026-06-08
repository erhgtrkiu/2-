import sys

sys.stdout.reconfigure(encoding='utf-8')

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    app_lines = f.readlines()

print("PISTOL references:")
for i, l in enumerate(app_lines):
    if 'pistol' in l.lower() and ('name' in l.lower() or 'add(' in l.lower() or 'load' in l.lower()):
        print(f"app.js {i+1}: {l.strip()}")

index_path = r'C:\Users\m3615\samosbor_game\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    idx_lines = f.readlines()

print("\nHUD / INTERFACE references in index.html:")
for i, l in enumerate(idx_lines):
    if 'id=' in l and ('hud' in l.lower() or 'interface' in l.lower()):
        print(f"index.html {i+1}: {l.strip()}")
