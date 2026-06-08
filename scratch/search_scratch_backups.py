import os

scratch_dir = r'C:\Users\m3615\samosbor_game\scratch'
queries = ['setCutsceneMode', 'spawnSamosbor', 'cutsceneActive']

for root, dirs, files in os.walk(scratch_dir):
    for file in files:
        if file.endswith('.js') or file.endswith('.txt') or file.endswith('.py'):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                for q in queries:
                    if q in content:
                        print(f"Found '{q}' in {file} (path: {path})")
            except Exception:
                pass
