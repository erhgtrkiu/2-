import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# =============================================
# REWRITE showLootUI to use room-overlay instead
# =============================================
old_show_start = "function showLootUI(items, doorIdx, containerKey) {"
old_show_end_marker = "    disableAllControls(true);\n}"

show_start = c.index(old_show_start)
# Find the closing of showLootUI - it ends with disableAllControls(true); }
show_search_area = c[show_start:show_start+2000]
show_end = show_start + show_search_area.index("    disableAllControls(true);\n}") + len("    disableAllControls(true);\n}")

new_show = """function showLootUI(items, doorIdx, containerKey) {
    console.log("showLootUI called", items);
    currentLootDoorIdx = doorIdx;
    currentLootContainerKey = containerKey;
    
    // Reuse the existing room-overlay that already works
    const roomOverlay = document.getElementById('room-overlay');
    const title = document.getElementById('room-title');
    const statusText = document.getElementById('room-status-text');
    const progressBar = document.getElementById('room-search-progress');
    
    // Hide progress bar
    progressBar.parentElement.style.display = 'none';
    
    if (containerKey === 'kitchenLootItems') {
        title.innerText = 'КУХНЯ: НАЙДЕННЫЕ ПРЕДМЕТЫ';
    } else {
        title.innerText = 'НАЙДЕННЫЕ ПРЕДМЕТЫ';
    }
    
    // Build loot HTML
    var html = '';
    if (!items || items.length === 0) {
        html = '<p style="color:#7f8c9d;padding:10px;">Пусто. Ничего полезного не найдено.</p>';
    } else {
        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            var btnHtml = '';
            if (item.type !== 'junk') {
                btnHtml = '<button onclick="takeLootItem(' + i + ')" style="background:rgba(0,200,100,0.15);border:1px solid rgba(0,200,100,0.4);color:#00ff66;padding:4px 14px;border-radius:3px;cursor:pointer;font-family:inherit;font-weight:bold;">Забрать</button>';
            } else {
                btnHtml = '<span style="color:#555;font-size:0.8rem">Хлам</span>';
            }
            html += '<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 10px;margin:4px 0;background:rgba(255,255,255,0.04);border-radius:3px;border-left:3px solid #ffcc00;">';
            html += '<span>' + (item.icon || '') + ' ' + item.label + '</span>' + btnHtml;
            html += '</div>';
        }
    }
    
    html += '<div style="display:flex;gap:8px;margin-top:12px;">';
    html += '<button onclick="takeAllLoot()" style="flex:1;padding:8px;background:rgba(255,204,0,0.1);border:1px solid #ffcc00;color:#ffcc00;cursor:pointer;font-family:inherit;font-weight:bold;border-radius:3px;">Забрать всё</button>';
    html += '<button onclick="closeLootUI()" style="flex:1;padding:8px;background:rgba(255,51,51,0.1);border:1px solid #ff3333;color:#ff3333;cursor:pointer;font-family:inherit;font-weight:bold;border-radius:3px;">Закрыть</button>';
    html += '</div>';
    
    statusText.innerHTML = html;
    
    // Show the overlay
    roomOverlay.className = '';
    roomOverlay.style.display = 'block';
}"""

c = c[:show_start] + new_show + c[show_end:]

# =============================================
# REWRITE closeLootUI to hide room-overlay
# =============================================
old_close_start = "function closeLootUI() {"
old_close_end_marker = "    disableAllControls(false);\n}"

close_start = c.index(old_close_start)
close_area = c[close_start:close_start+500]
close_end = close_start + close_area.index("    disableAllControls(false);\n}") + len("    disableAllControls(false);\n}")

new_close = """function closeLootUI() {
    const roomOverlay = document.getElementById('room-overlay');
    roomOverlay.className = 'overlay-hidden';
    roomOverlay.style.display = '';
    // Restore progress bar visibility for next search
    document.getElementById('room-search-progress').parentElement.style.display = '';
    currentLootDoorIdx = null;
    currentLootContainerKey = null;
    state.isSearching = false;
    disableAllControls(false);
}"""

c = c[:close_start] + new_close + c[close_end:]

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Rewrote showLootUI and closeLootUI to use existing room-overlay!")
