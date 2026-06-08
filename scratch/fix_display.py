import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Fix showLootUI: explicitly set display:block instead of relying on class removal
old_show_end = """    overlay.className = '';
    disableAllControls(true);"""

new_show_end = """    overlay.className = '';
    overlay.style.display = 'block';
    disableAllControls(true);"""

if old_show_end in c:
    c = c.replace(old_show_end, new_show_end, 1)
    print("FIX: Added explicit display:block to showLootUI")
else:
    print("ERROR: showLootUI end block not found")

# Fix closeLootUI: explicitly set display:none
old_close = """    overlay.className = 'overlay-hidden';"""
new_close = """    overlay.className = 'overlay-hidden';
    overlay.style.display = 'none';"""

if old_close in c:
    c = c.replace(old_close, new_close, 1)
    print("FIX: Added explicit display:none to closeLootUI")
else:
    print("ERROR: closeLootUI block not found")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Done!")
