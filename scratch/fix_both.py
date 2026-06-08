import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Fix 1: pistol model path
old_path = "loader.load('source/USPS.glb'"
new_path = "loader.load('usp/source/USPS.glb'"
if old_path in c:
    c = c.replace(old_path, new_path)
    print("FIX 1: Pistol path fixed to usp/source/USPS.glb")
else:
    print("FIX 1: Path already correct or not found")

# Verify loot system functions exist
print("showLootUI exists:", "function showLootUI" in c)
print("generateRoomLootItems exists:", "function generateRoomLootItems" in c)
print("door.lootItems assignment:", "door.lootItems = generateRoomLootItems" in c)
print("closeLootUI exists:", "function closeLootUI" in c)
print("btn-take-all listener:", "btn-take-all" in c)
print("btn-close-loot listener:", "btn-close-loot" in c)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Done!")
