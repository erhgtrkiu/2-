with open(r'C:\Users\m3615\samosbor_game\scratch\app_reconstructed.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(min(len(lines), 60)):
    print(f"{i+1}: {lines[i]}", end="")
