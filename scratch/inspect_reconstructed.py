import os

path = r'C:\Users\m3615\samosbor_game\scratch\app_reconstructed.js'
if os.path.exists(path):
    print("File exists!")
    size = os.path.getsize(path)
    print("Size:", size)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.splitlines()
    print("Number of lines:", len(lines))
    print("First 20 lines:")
    for idx, l in enumerate(lines[:20]):
        print(f"{idx+1}: {l}")
    print("\nLast 20 lines:")
    for idx, l in enumerate(lines[-20:]):
        print(f"{len(lines)-20+idx+1}: {l}")
else:
    print("File does not exist.")
