import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

changes = 0

# ==========================================================
# 1. CHANGE DOOR GENERATION: single loot -> lootItems array
# ==========================================================
old_door_loot = """            if (door.type === 'apartment') {
                let loot = null;
                if (floorNum === 1320 && !spawnedHackerTool1320 && !state.hasHackerTool) {
                    loot = 'hacker_tool';
                    spawnedHackerTool1320 = true;
                } else {
                    const r = Math.random();
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
                    }
                }
                door.loot = loot;
            }"""

new_door_loot = """            if (door.type === 'apartment') {
                // Generate multiple loot items for main room
                door.lootItems = generateRoomLootItems(rType, false);
                // Guaranteed hacker_tool on floor 1320
                if (floorNum === 1320 && !spawnedHackerTool1320 && !state.hasHackerTool) {
                    door.lootItems.unshift({type: 'hacker_tool', label: '\\u0414\\u0435\\u0448\\u0438\\u0444\\u0440\\u0430\\u0442\\u043e\\u0440 \\u0433\\u0435\\u0440\\u043c\\u043e\\u0437\\u0430\\u0442\\u0432\\u043e\\u0440\\u043e\\u0432', icon: '\\ud83d\\udd13'});
                    spawnedHackerTool1320 = true;
                }
                // For bedroom_kitchen apartments, generate kitchen loot too
                if (rType === 'bedroom_kitchen') {
                    door.kitchenLootItems = generateRoomLootItems(rType, true);
                    door.kitchenSearched = false;
                }
            }"""

if old_door_loot in c:
    c = c.replace(old_door_loot, new_door_loot)
    changes += 1
    print("1. Door loot generation replaced.")
else:
    print("ERROR: Could not find door loot generation block!")

# ==========================================================
# 2. ADD generateRoomLootItems() function after distributeLoot
# ==========================================================
new_functions = """

// === LOOT SYSTEM: Multi-item generation ===
const LOOT_ICONS = {
    ammo: '\\ud83d\\udca5', bandage: '\\ud83e\\ude79', water: '\\ud83d\\udca7', battery: '\\ud83d\\udd0b',
    note: '\\ud83d\\udcdc', hacker_tool: '\\ud83d\\udd13', filter: '\\ud83d\\udca8', junk: '\\ud83d\\uddd1\\ufe0f'
};

function generateRoomLootItems(roomType, isKitchen) {
    const items = [];
    const count = isKitchen ? (1 + Math.floor(Math.random() * 2)) : (2 + Math.floor(Math.random() * 3));
    
    for (let i = 0; i < count; i++) {
        const r = Math.random();
        let item = null;
        
        if (isKitchen) {
            if (r < 0.30) item = {type: 'junk', label: '\\u041c\\u0443\\u0441\\u043e\\u0440', icon: '\\ud83d\\uddd1\\ufe0f'};
            else if (r < 0.60) item = {type: 'water', count: 25, label: '\\u0424\\u043b\\u044f\\u0433\\u0430 \\u0432\\u043e\\u0434\\u044b (+25%)', icon: '\\ud83d\\udca7'};
            else if (r < 0.80) item = {type: 'bandage', count: 1, label: '\\u0411\\u0438\\u043d\\u0442', icon: '\\ud83e\\ude79'};
            else item = {type: 'filter', count: 25, label: '\\u0424\\u0438\\u043b\\u044c\\u0442\\u0440 (+25%)', icon: '\\ud83d\\udca8'};
        } else {
            if (r < 0.12) item = {type: 'junk', label: '\\u041c\\u0443\\u0441\\u043e\\u0440', icon: '\\ud83d\\uddd1\\ufe0f'};
            else if (r < 0.28) {
                const cnt = roomType === 'armory' ? 12 : 6;
                item = {type: 'ammo', count: cnt, label: '\\u041f\\u0430\\u0442\\u0440\\u043e\\u043d\\u044b (+' + cnt + ' \\u0448\\u0442.)', icon: '\\ud83d\\udca5'};
            }
            else if (r < 0.42) item = {type: 'bandage', count: 1, label: '\\u0411\\u0438\\u043d\\u0442', icon: '\\ud83e\\ude79'};
            else if (r < 0.56) item = {type: 'water', count: 30, label: '\\u0424\\u043b\\u044f\\u0433\\u0430 \\u0432\\u043e\\u0434\\u044b (+30%)', icon: '\\ud83d\\udca7'};
            else if (r < 0.68) item = {type: 'battery', count: 1, label: '\\u0411\\u0430\\u0442\\u0430\\u0440\\u0435\\u0439\\u043a\\u0430', icon: '\\ud83d\\udd0b'};
            else if (r < 0.78) item = {type: 'filter', count: 30, label: '\\u0424\\u0438\\u043b\\u044c\\u0442\\u0440 (+30%)', icon: '\\ud83d\\udca8'};
            else if (r < 0.88) item = {type: 'note', label: '\\u0417\\u0430\\u043f\\u0438\\u0441\\u043a\\u0430', icon: '\\ud83d\\udcdc'};
            else if (r < 0.95 && !state.hasHackerTool) item = {type: 'hacker_tool', label: '\\u0414\\u0435\\u0448\\u0438\\u0444\\u0440\\u0430\\u0442\\u043e\\u0440 \\u0433\\u0435\\u0440\\u043c\\u043e\\u0437\\u0430\\u0442\\u0432\\u043e\\u0440\\u043e\\u0432', icon: '\\ud83d\\udd13'};
            else item = {type: 'bandage', count: 1, label: '\\u0411\\u0438\\u043d\\u0442', icon: '\\ud83e\\ude79'};
        }
        
        if (item) items.push(item);
    }
    return items;
}

// === LOOT UI ===
let currentLootDoorIdx = null;
let currentLootContainerKey = null;

function showLootUI(items, doorIdx, containerKey) {
    currentLootDoorIdx = doorIdx;
    currentLootContainerKey = containerKey;
    
    const overlay = document.getElementById('loot-overlay');
    const list = document.getElementById('loot-items-list');
    const title = document.getElementById('loot-title');
    
    title.innerText = containerKey === 'kitchenLootItems' ? '\\u041a\\u0423\\u0425\\u041d\\u042f: \\u041d\\u0410\\u0419\\u0414\\u0415\\u041d\\u041d\\u042b\\u0415 \\u041f\\u0420\\u0415\\u0414\\u041c\\u0415\\u0422\\u042b' : '\\u041d\\u0410\\u0419\\u0414\\u0415\\u041d\\u041d\\u042b\\u0415 \\u041f\\u0420\\u0415\\u0414\\u041c\\u0415\\u0422\\u042b';
    list.innerHTML = '';
    
    if (!items || items.length === 0) {
        list.innerHTML = '<div class="loot-empty-msg">\\u041f\\u0443\\u0441\\u0442\\u043e. \\u041d\\u0438\\u0447\\u0435\\u0433\\u043e \\u043f\\u043e\\u043b\\u0435\\u0437\\u043d\\u043e\\u0433\\u043e \\u043d\\u0435 \\u043d\\u0430\\u0439\\u0434\\u0435\\u043d\\u043e.</div>';
    } else {
        items.forEach((item, idx) => {
            const row = document.createElement('div');
            row.className = 'loot-item loot-' + item.type;
            row.innerHTML = `
                <span class="loot-item-name"><span class="loot-item-icon">${item.icon || ''}</span>${item.label}</span>
                ${item.type !== 'junk' ? '<button class="btn-take-item" data-idx="' + idx + '">\\u0417\\u0430\\u0431\\u0440\\u0430\\u0442\\u044c</button>' : '<span style="color:#555;font-size:0.8rem">\\u0425\\u043b\\u0430\\u043c</span>'}
            `;
            list.appendChild(row);
        });
    }
    
    overlay.className = '';
    disableAllControls(true);
}

function takeLootItem(idx) {
    if (currentLootDoorIdx === null) return;
    const door = state.doors[currentLootDoorIdx];
    if (!door) return;
    const items = door[currentLootContainerKey];
    if (!items || idx >= items.length) return;
    
    const item = items[idx];
    if (!item) return;
    
    // Apply item effect
    applyLootItem(item);
    
    // Remove from container
    items.splice(idx, 1);
    
    // Refresh UI
    showLootUI(items, currentLootDoorIdx, currentLootContainerKey);
    updateHUD();
}

function takeAllLoot() {
    if (currentLootDoorIdx === null) return;
    const door = state.doors[currentLootDoorIdx];
    if (!door) return;
    const items = door[currentLootContainerKey];
    if (!items) return;
    
    // Take all non-junk items
    const toRemove = [];
    for (let i = items.length - 1; i >= 0; i--) {
        if (items[i].type !== 'junk') {
            applyLootItem(items[i]);
            toRemove.push(i);
        }
    }
    toRemove.forEach(i => items.splice(i, 1));
    
    closeLootUI();
    updateHUD();
}

function applyLootItem(item) {
    switch (item.type) {
        case 'ammo':
            state.ammo = Math.min(MAX_AMMO, state.ammo + (item.count || 6));
            logToConsole('[\\u041d\\u0410\\u0425\\u041e\\u0414\\u041a\\u0410] \\u041f\\u0430\\u0442\\u0440\\u043e\\u043d\\u044b (+' + (item.count || 6) + ' \\u0448\\u0442.)', 'loot');
            break;
        case 'bandage':
            state.bandages = (state.bandages || 0) + (item.count || 1);
            logToConsole('[\\u041d\\u0410\\u0425\\u041e\\u0414\\u041a\\u0410] \\u0411\\u0438\\u043d\\u0442 (+' + (item.count || 1) + ')', 'loot');
            break;
        case 'water':
            state.bottleWater = Math.min(100, state.bottleWater + (item.count || 30));
            logToConsole('[\\u041d\\u0410\\u0425\\u041e\\u0414\\u041a\\u0410] \\u0424\\u043b\\u044f\\u0433\\u0430 \\u0432\\u043e\\u0434\\u044b (+' + (item.count || 30) + '%)', 'loot');
            break;
        case 'battery':
            state.batteries = (state.batteries || 0) + (item.count || 1);
            logToConsole('[\\u041d\\u0410\\u0425\\u041e\\u0414\\u041a\\u0410] \\u0411\\u0430\\u0442\\u0430\\u0440\\u0435\\u0439\\u043a\\u0430 (+1)', 'loot');
            break;
        case 'filter':
            state.filter = Math.min(MAX_FILTER, state.filter + (item.count || 30));
            logToConsole('[\\u041d\\u0410\\u0425\\u041e\\u0414\\u041a\\u0410] \\u0424\\u0438\\u043b\\u044c\\u0442\\u0440 (+' + (item.count || 30) + '%)', 'loot');
            break;
        case 'note':
            if (state.notesCount < LORE_NOTES.length) {
                const nid = state.notesCount;
                state.notesCollected[nid] = true;
                state.notesCount++;
                const tab = document.getElementById('note-tab-' + nid);
                if (tab) { tab.classList.remove('btn-note-locked'); tab.innerText = LORE_NOTES[nid].title; }
                logToConsole('[\\u041d\\u0410\\u0425\\u041e\\u0414\\u041a\\u0410] \\u0417\\u0430\\u043f\\u0438\\u0441\\u043a\\u0430: "' + LORE_NOTES[nid].title + '"!', 'loot');
                openNotesModal(nid);
            }
            break;
        case 'hacker_tool':
            if (!state.hasHackerTool) {
                state.hasHackerTool = true;
                logToConsole('[\\u041d\\u0410\\u0425\\u041e\\u0414\\u041a\\u0410] \\u0414\\u0415\\u0428\\u0418\\u0424\\u0420\\u0410\\u0422\\u041e\\u0420 \\u0413\\u0415\\u0420\\u041c\\u041e\\u0417\\u0410\\u0422\\u0412\\u041e\\u0420\\u041e\\u0412!', 'loot');
                updateInventoryUI();
            }
            break;
    }
    playSoundLoot();
}

function closeLootUI() {
    const overlay = document.getElementById('loot-overlay');
    overlay.className = 'overlay-hidden';
    currentLootDoorIdx = null;
    currentLootContainerKey = null;
    state.isSearching = false;
    disableAllControls(false);
}
"""

# Insert after distributeLoot function closing
old_after_dist = "\nfunction lockRoom() {"
if old_after_dist in c:
    c = c.replace(old_after_dist, new_functions + "\nfunction lockRoom() {")
    changes += 1
    print("2. New loot functions inserted.")
else:
    print("ERROR: Could not find lockRoom function!")

# ==========================================================
# 3. MODIFY searchRoom() - show loot UI instead of distributeLoot
# ==========================================================
old_search_complete = """            roomOverlay.className = 'overlay-hidden';
            door.searched = true;
            state.isSearching = false;
            disableAllControls(false);
            
            // Проверяем событие Гнезда Твари
            if (door.roomType === 'nest' && Math.random() < 0.50) {
                logToConsole("УЖАСНЫЙ ШОРОХ! Из шевелящейся слизи в углу на вас бросилась тварь!", "danger");
                state.health = Math.max(0, state.health - 20);
                playSoundDamage();
                if (state.health <= 0) {
                    triggerGameOver("stairs_monster");
                    return;
                }
                // Спавним тварь в коридоре перед этой дверью
                const layout = DOOR_LAYOUT[doorIdx];
                spawnHallwayCrawler(layout.z, layout.x < 0 ? -2.5 : 2.5);
            } else {
                distributeLoot(doorIdx);
            }
            updateHUD();"""

new_search_complete = """            roomOverlay.className = 'overlay-hidden';
            
            const isKitchenSearch = state._searchingKitchen || false;
            if (isKitchenSearch) {
                door.kitchenSearched = true;
            } else {
                door.searched = true;
            }
            
            // Проверяем событие Гнезда Твари
            if (door.roomType === 'nest' && Math.random() < 0.50) {
                state.isSearching = false;
                disableAllControls(false);
                logToConsole("УЖАСНЫЙ ШОРОХ! Из шевелящейся слизи в углу на вас бросилась тварь!", "danger");
                state.health = Math.max(0, state.health - 20);
                playSoundDamage();
                if (state.health <= 0) {
                    triggerGameOver("stairs_monster");
                    return;
                }
                const layout = DOOR_LAYOUT[doorIdx];
                spawnHallwayCrawler(layout.z, layout.x < 0 ? -2.5 : 2.5);
            } else {
                // Show loot selection UI
                const containerKey = isKitchenSearch ? 'kitchenLootItems' : 'lootItems';
                const items = door[containerKey] || [];
                showLootUI(items, doorIdx, containerKey);
            }
            updateHUD();
            updateRoomButtons();"""

if old_search_complete in c:
    c = c.replace(old_search_complete, new_search_complete)
    changes += 1
    print("3. searchRoom completion replaced.")
else:
    print("ERROR: Could not find searchRoom completion block!")

# ==========================================================
# 4. MODIFY searchRoom() check - support kitchen search
# ==========================================================
old_search_check = """    const door = state.doors[doorIdx];
    if (!door || door.searched) return;"""

new_search_check = """    const door = state.doors[doorIdx];
    const isKitchenSearch = state._searchingKitchen || false;
    if (!door || (isKitchenSearch ? door.kitchenSearched : door.searched)) return;"""

if old_search_check in c:
    c = c.replace(old_search_check, new_search_check)
    changes += 1
    print("4. searchRoom check replaced.")
else:
    print("ERROR: Could not find searchRoom check!")

# ==========================================================
# 5. ADD kitchen search button logic and updateRoomButtons()
# ==========================================================
# Find where btn-search-room event listener is wired up
# We need to add event listeners for new buttons

# Add updateRoomButtons function + event listeners after closeLootUI
# We'll inject the event listeners near the end where other buttons are wired

# First add the updateRoomButtons function right before lockRoom
update_room_btns_fn = """
function updateRoomButtons() {
    if (state.location !== 'room' || state.focusedDoorIndex === null) return;
    const door = state.doors[state.focusedDoorIndex];
    if (!door) return;
    
    const searchBtn = document.getElementById('btn-search-room');
    const kitchenBtn = document.getElementById('btn-search-kitchen');
    
    // Show kitchen button for bedroom_kitchen rooms
    if (door.roomType === 'bedroom_kitchen') {
        searchBtn.innerText = door.searched ? '\\u0421\\u043f\\u0430\\u043b\\u044c\\u043d\\u044f \\u043e\\u0431\\u044b\\u0441\\u043a\\u0430\\u043d\\u0430' : '\\u041e\\u0431\\u044b\\u0441\\u043a\\u0430\\u0442\\u044c \\u0441\\u043f\\u0430\\u043b\\u044c\\u043d\\u044e';
        kitchenBtn.style.display = '';
        kitchenBtn.innerText = door.kitchenSearched ? '\\u041a\\u0443\\u0445\\u043d\\u044f \\u043e\\u0431\\u044b\\u0441\\u043a\\u0430\\u043d\\u0430' : '\\u041e\\u0431\\u044b\\u0441\\u043a\\u0430\\u0442\\u044c \\u043a\\u0443\\u0445\\u043d\\u044e';
        
        if (door.searched) { searchBtn.disabled = true; searchBtn.classList.add('btn-disabled'); }
        else { searchBtn.disabled = false; searchBtn.classList.remove('btn-disabled'); }
        if (door.kitchenSearched) { kitchenBtn.disabled = true; kitchenBtn.classList.add('btn-disabled'); }
        else { kitchenBtn.disabled = false; kitchenBtn.classList.remove('btn-disabled'); }
    } else {
        kitchenBtn.style.display = 'none';
        searchBtn.innerText = door.searched ? '\\u0423\\u0436\\u0435 \\u043e\\u0431\\u044b\\u0441\\u043a\\u0430\\u043d\\u043e' : '\\u041e\\u0431\\u044b\\u0441\\u043a\\u0430\\u0442\\u044c \\u043c\\u0435\\u0431\\u0435\\u043b\\u044c';
        if (door.searched) { searchBtn.disabled = true; searchBtn.classList.add('btn-disabled'); }
        else { searchBtn.disabled = false; searchBtn.classList.remove('btn-disabled'); }
    }
}

"""

c = c.replace("\nfunction lockRoom() {", update_room_btns_fn + "function lockRoom() {")
changes += 1
print("5. updateRoomButtons function inserted.")

# ==========================================================
# 6. ADD event listeners for loot UI buttons and kitchen search
# ==========================================================
# Find where btn-search-room listener is attached
old_event_search = """document.getElementById('btn-search-room').addEventListener('click', searchRoom);"""

# Replace with: original + kitchen + loot buttons + delegation on loot items
# Wait, let me check if this exact string exists. Let me search differently.
# Actually from the code I saw, the search button might use a different pattern.
# Let me search for it.

# Let me try a different approach - inject the listeners right after where 
# existing button listeners are set up. Look for btn-listen listener.

# From line 7920: document.getElementById('btn-listen').addEventListener('click', listenToFocused);
old_listen_event = """document.getElementById('btn-listen').addEventListener('click', listenToFocused);"""

new_listen_event = """document.getElementById('btn-listen').addEventListener('click', listenToFocused);
    
    // Loot UI event listeners
    document.getElementById('btn-search-kitchen').addEventListener('click', function() {
        state._searchingKitchen = true;
        searchRoom();
    });
    
    // Wrap original search to set flag
    const origSearchBtn = document.getElementById('btn-search-room');
    origSearchBtn.addEventListener('click', function() {
        state._searchingKitchen = false;
    });
    
    document.getElementById('btn-take-all').addEventListener('click', takeAllLoot);
    document.getElementById('btn-close-loot').addEventListener('click', closeLootUI);
    
    // Event delegation for individual "Take" buttons
    document.getElementById('loot-items-list').addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-take-item')) {
            const idx = parseInt(e.target.getAttribute('data-idx'));
            if (!isNaN(idx)) takeLootItem(idx);
        }
    });"""

if old_listen_event in c:
    c = c.replace(old_listen_event, new_listen_event, 1)
    changes += 1
    print("6. Event listeners for loot UI added.")
else:
    print("ERROR: Could not find btn-listen event listener!")

# ==========================================================
# 7. CALL updateRoomButtons when entering a room
# ==========================================================
# When player enters a room, the room-actions-bar appears.
# We need to call updateRoomButtons() at that point.
# From line 4170: state.location = newLoc;
# After that we can call updateRoomButtons

old_enter_room = """    state.location = newLoc;
            state.focusedDoorIndex = insideRoomIdx;"""

new_enter_room = """    state.location = newLoc;
            state.focusedDoorIndex = insideRoomIdx;
            if (newLoc === 'room') updateRoomButtons();"""

if old_enter_room in c:
    c = c.replace(old_enter_room, new_enter_room, 1)
    changes += 1
    print("7. updateRoomButtons called on room entry.")
else:
    # Try with different whitespace
    print("WARNING: Could not find room entry block, trying alternative...")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print(f"\nDone! {changes} changes applied.")
