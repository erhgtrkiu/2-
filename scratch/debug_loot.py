import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Verify pistol path is correct
print("Pistol path correct:", "usp/source/USPS.glb" in c)

# Add debug logs to showLootUI
old_show = 'function showLootUI(items, doorIdx, containerKey) {'
new_show = 'function showLootUI(items, doorIdx, containerKey) {\n    console.log("LOOT UI CALLED!", items, doorIdx, containerKey);'
if old_show in c:
    c = c.replace(old_show, new_show, 1)
    print("Added debug log to showLootUI")

# Add debug log at the call site in searchRoom
old_call = """                // Show loot selection UI
                const containerKey = isKitchenSearch ? 'kitchenLootItems' : 'lootItems';
                const items = door[containerKey] || [];
                showLootUI(items, doorIdx, containerKey);"""
new_call = """                // Show loot selection UI
                const containerKey = isKitchenSearch ? 'kitchenLootItems' : 'lootItems';
                const items = door[containerKey] || [];
                console.log("CALLING showLootUI, containerKey:", containerKey, "items:", items, "door:", door);
                showLootUI(items, doorIdx, containerKey);"""
if old_call in c:
    c = c.replace(old_call, new_call, 1)
    print("Added debug log at call site")
else:
    print("ERROR: call site not found!")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Done!")
