with open('C:/Users/m3615/samosbor_game/scratch/app_original.js', 'r', encoding='utf-8') as f:
    orig = f.readlines()

with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    curr = f.readlines()

# find lines in both containing shaftL
print("ORIGINAL:")
for i, l in enumerate(orig):
    if 'shaft' in l or 'stairsCeiling' in l or 'stairsHoleWall' in l:
        print(f"{i+1}: {l.strip()}")

print("\nCURRENT:")
for i, l in enumerate(curr):
    if 'shaft' in l or 'stairsCeiling' in l or 'stairsHoleWall' in l:
        print(f"{i+1}: {l.strip()}")
