import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# We need to fix the guaranteed hacker tool spawn.
# Instead of relying on `idx === 0`, we will use a tracker variable outside the loop.
old_gen = """    // Генерация дверей
    state.currentFloorDoors.forEach((door, idx) => {
        if (door.type === 'apartment') {
            const rTypeRand = Math.random();
            let rType = 'bedroom';
            let rNum = Math.floor(Math.random() * 90 + 10);"""

new_gen = """    // Генерация дверей
    let spawnedHackerTool1320 = false;
    state.currentFloorDoors.forEach((door, idx) => {
        if (door.type === 'apartment') {
            const rTypeRand = Math.random();
            let rType = 'bedroom';
            let rNum = Math.floor(Math.random() * 90 + 10);"""

c = c.replace(old_gen, new_gen)

old_loot_check = """            if (door.type === 'apartment') {
                let loot = null;
                if (floorNum === 1320 && idx === 0) {
                    loot = 'hacker_tool';
                } else {"""

new_loot_check = """            if (door.type === 'apartment') {
                let loot = null;
                if (floorNum === 1320 && !spawnedHackerTool1320 && !state.hasHackerTool) {
                    loot = 'hacker_tool';
                    spawnedHackerTool1320 = true;
                } else {"""

c = c.replace(old_loot_check, new_loot_check)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed guaranteed hacker tool spawn bug.")
