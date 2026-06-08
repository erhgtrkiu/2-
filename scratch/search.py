import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\m3615\samosbor_game\app.js', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if "'room'" in line or '"room"' in line or 'state.location =' in line:
            if len(line.strip()) < 120:
                print(f'{idx}: {line.strip()}')
