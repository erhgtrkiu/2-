import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Find and replace the broken showLootUI function entirely
old_start = "function showLootUI(items, doorIdx, containerKey) {"
old_end = "}\n\nfunction takeLootItem(idx) {"

start_idx = c.index(old_start)
end_idx = c.index(old_end, start_idx)

new_func = """function showLootUI(items, doorIdx, containerKey) {
    console.log("LOOT UI CALLED!", items, doorIdx, containerKey);
    currentLootDoorIdx = doorIdx;
    currentLootContainerKey = containerKey;
    
    const overlay = document.getElementById('loot-overlay');
    const list = document.getElementById('loot-items-list');
    const title = document.getElementById('loot-title');
    
    if (containerKey === 'kitchenLootItems') {
        title.innerText = 'КУХНЯ: НАЙДЕННЫЕ ПРЕДМЕТЫ';
    } else {
        title.innerText = 'НАЙДЕННЫЕ ПРЕДМЕТЫ';
    }
    list.innerHTML = '';
    
    if (!items || items.length === 0) {
        list.innerHTML = '<div class="loot-empty-msg">Пусто. Ничего полезного не найдено.</div>';
    } else {
        items.forEach(function(item, idx) {
            const row = document.createElement('div');
            row.className = 'loot-item loot-' + item.type;
            
            var btnHtml = '';
            if (item.type !== 'junk') {
                btnHtml = '<button class="btn-take-item" data-idx="' + idx + '">Забрать</button>';
            } else {
                btnHtml = '<span style="color:#555;font-size:0.8rem">Хлам</span>';
            }
            
            row.innerHTML = '<span class="loot-item-name"><span class="loot-item-icon">' + (item.icon || '') + '</span>' + item.label + '</span>' + btnHtml;
            list.appendChild(row);
        });
    }
    
    overlay.className = '';
    overlay.style.display = 'block';
    disableAllControls(true);
}"""

c = c[:start_idx] + new_func + "\n\n" + c[end_idx:]

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("showLootUI rewritten with proper UTF-8 strings!")
