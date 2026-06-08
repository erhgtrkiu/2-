import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

old_loot = """                    const r = Math.random();
                    if (r < 0.40) {
                        loot = 'junk';
                    } else if (r < 0.45 && !state.hasHackerTool) {
                        loot = 'hacker_tool';
                    } else if (r < 0.65) {
                        loot = (rType === 'armory') ? 'ammo' : (Math.random() < 0.5 ? 'ammo' : 'water');
                    } else if (r < 0.75) {
                        loot = 'battery';
                    } else if (r < 0.85) {
                        loot = (rType === 'armory') ? 'ammo' : 'note';
                    } else {
                        loot = 'bandage';
                    }"""

new_loot = """                    const r = Math.random();
                    // REBALANCED LOOT
                    if (r < 0.20) {
                        loot = 'junk'; // 20% (was 40%)
                    } else if (r < 0.35 && !state.hasHackerTool) {
                        loot = 'hacker_tool'; // 15% chance (was 5%)
                    } else if (r < 0.55) {
                        loot = (rType === 'armory') ? 'ammo' : (Math.random() < 0.5 ? 'ammo' : 'water'); // 20%
                    } else if (r < 0.65) {
                        loot = 'battery'; // 10%
                    } else if (r < 0.80) {
                        loot = (rType === 'armory') ? 'ammo' : 'note'; // 15% (was 10%)
                    } else {
                        loot = 'bandage'; // 20% (was 15%)
                    }"""

c = c.replace(old_loot, new_loot)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Loot probabilities updated.")
