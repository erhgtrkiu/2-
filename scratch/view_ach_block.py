with open(r'C:\Users\m3615\samosbor_game\scratch\app_reconstructed.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for idx in range(295, min(len(lines), 400)):
    print(f"{idx+1}: {lines[idx]}", end="")
