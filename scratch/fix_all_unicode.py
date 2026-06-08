import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace generateRoomLootItems entirely
old_gen_start = "function generateRoomLootItems(roomType, isKitchen) {"
old_gen_end = "    return items;\n}"

gen_start = c.index(old_gen_start)
gen_end = c.index(old_gen_end, gen_start) + len(old_gen_end)

new_gen = """function generateRoomLootItems(roomType, isKitchen) {
    const items = [];
    const count = isKitchen ? (1 + Math.floor(Math.random() * 2)) : (2 + Math.floor(Math.random() * 3));
    
    for (let i = 0; i < count; i++) {
        const r = Math.random();
        let item = null;
        
        if (isKitchen) {
            if (r < 0.30) item = {type: 'junk', label: 'Мусор', icon: '🗑️'};
            else if (r < 0.60) item = {type: 'water', count: 25, label: 'Фляга воды (+25%)', icon: '💧'};
            else if (r < 0.80) item = {type: 'bandage', count: 1, label: 'Бинт', icon: '🩹'};
            else item = {type: 'filter', count: 25, label: 'Фильтр (+25%)', icon: '💨'};
        } else {
            if (r < 0.12) item = {type: 'junk', label: 'Мусор', icon: '🗑️'};
            else if (r < 0.28) {
                const cnt = roomType === 'armory' ? 12 : 6;
                item = {type: 'ammo', count: cnt, label: 'Патроны (+' + cnt + ' шт.)', icon: '💥'};
            }
            else if (r < 0.42) item = {type: 'bandage', count: 1, label: 'Бинт', icon: '🩹'};
            else if (r < 0.56) item = {type: 'water', count: 30, label: 'Фляга воды (+30%)', icon: '💧'};
            else if (r < 0.68) item = {type: 'battery', count: 1, label: 'Батарейка', icon: '🔋'};
            else if (r < 0.78) item = {type: 'filter', count: 30, label: 'Фильтр (+30%)', icon: '💨'};
            else if (r < 0.88) item = {type: 'note', label: 'Записка', icon: '📜'};
            else if (r < 0.95 && !state.hasHackerTool) item = {type: 'hacker_tool', label: 'Дешифратор гермозатворов', icon: '🔓'};
            else item = {type: 'bandage', count: 1, label: 'Бинт', icon: '🩹'};
        }
        
        if (item) items.push(item);
    }
    return items;
}"""

c = c[:gen_start] + new_gen + c[gen_end:]

# Replace applyLootItem entirely
old_apply_start = "function applyLootItem(item) {"
old_apply_end = "    playSoundLoot();\n}"

apply_start = c.index(old_apply_start)
apply_end = c.index(old_apply_end, apply_start) + len(old_apply_end)

new_apply = """function applyLootItem(item) {
    switch (item.type) {
        case 'ammo':
            state.ammo = Math.min(MAX_AMMO, state.ammo + (item.count || 6));
            logToConsole('[НАХОДКА] Патроны (+' + (item.count || 6) + ' шт.)', 'loot');
            break;
        case 'bandage':
            state.bandages = (state.bandages || 0) + (item.count || 1);
            logToConsole('[НАХОДКА] Бинт (+' + (item.count || 1) + ')', 'loot');
            break;
        case 'water':
            state.bottleWater = Math.min(100, state.bottleWater + (item.count || 30));
            logToConsole('[НАХОДКА] Фляга воды (+' + (item.count || 30) + '%)', 'loot');
            break;
        case 'battery':
            state.batteries = (state.batteries || 0) + (item.count || 1);
            logToConsole('[НАХОДКА] Батарейка (+1)', 'loot');
            break;
        case 'filter':
            state.filter = Math.min(MAX_FILTER, state.filter + (item.count || 30));
            logToConsole('[НАХОДКА] Фильтр (+' + (item.count || 30) + '%)', 'loot');
            break;
        case 'note':
            if (state.notesCount < LORE_NOTES.length) {
                const nid = state.notesCount;
                state.notesCollected[nid] = true;
                state.notesCount++;
                const tab = document.getElementById('note-tab-' + nid);
                if (tab) { tab.classList.remove('btn-note-locked'); tab.innerText = LORE_NOTES[nid].title; }
                logToConsole('[НАХОДКА] Записка: "' + LORE_NOTES[nid].title + '"!', 'loot');
                openNotesModal(nid);
            }
            break;
        case 'hacker_tool':
            if (!state.hasHackerTool) {
                state.hasHackerTool = true;
                logToConsole('[НАХОДКА] ДЕШИФРАТОР ГЕРМОЗАТВОРОВ!', 'loot');
                updateInventoryUI();
            }
            break;
    }
    playSoundLoot();
}"""

c = c[:apply_start] + new_apply + c[apply_end:]

# Replace updateRoomButtons entirely
old_urb_start = "function updateRoomButtons() {"
old_urb_end_marker = "\n\nfunction lockRoom() {"

urb_start = c.index(old_urb_start)
urb_end = c.index(old_urb_end_marker, urb_start)

new_urb = """function updateRoomButtons() {
    if (state.location !== 'room' || state.focusedDoorIndex === null) return;
    const door = state.doors[state.focusedDoorIndex];
    if (!door) return;
    
    const searchBtn = document.getElementById('btn-search-room');
    const kitchenBtn = document.getElementById('btn-search-kitchen');
    
    if (door.roomType === 'bedroom_kitchen') {
        searchBtn.innerText = door.searched ? 'Спальня обыскана' : 'Обыскать спальню';
        kitchenBtn.style.display = '';
        kitchenBtn.innerText = door.kitchenSearched ? 'Кухня обыскана' : 'Обыскать кухню';
        
        if (door.searched) { searchBtn.disabled = true; searchBtn.classList.add('btn-disabled'); }
        else { searchBtn.disabled = false; searchBtn.classList.remove('btn-disabled'); }
        if (door.kitchenSearched) { kitchenBtn.disabled = true; kitchenBtn.classList.add('btn-disabled'); }
        else { kitchenBtn.disabled = false; kitchenBtn.classList.remove('btn-disabled'); }
    } else {
        kitchenBtn.style.display = 'none';
        searchBtn.innerText = door.searched ? 'Уже обыскано' : 'Обыскать мебель';
        if (door.searched) { searchBtn.disabled = true; searchBtn.classList.add('btn-disabled'); }
        else { searchBtn.disabled = false; searchBtn.classList.remove('btn-disabled'); }
    }
}"""

c = c[:urb_start] + new_urb + c[urb_end:]

# Fix the hacker_tool label in door generation
old_hacker_label = "door.lootItems.unshift({type: 'hacker_tool', label: '\\u0414\\u0435\\u0448\\u0438\\u0444\\u0440\\u0430\\u0442"
# Find the full line
lines = c.split('\n')
for i, line in enumerate(lines):
    if "door.lootItems.unshift" in line and "hacker_tool" in line:
        lines[i] = "                    door.lootItems.unshift({type: 'hacker_tool', label: 'Дешифратор гермозатворов', icon: '🔓'});"
        print(f"Fixed hacker_tool label at line {i+1}")
        break
c = '\n'.join(lines)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("All functions rewritten with proper UTF-8!")
