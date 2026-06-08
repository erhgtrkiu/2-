import sys

sys.stdout.reconfigure(encoding='utf-8')
print("Updating index.html...")

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add data-i18n to btn-search-kitchen
content = content.replace(
    '<button id="btn-search-kitchen" class="btn btn-room-action glow-yellow" style="display:none">Обыскать кухню</button>',
    '<button id="btn-search-kitchen" class="btn btn-room-action glow-yellow" style="display:none" data-i18n="room_kitchen_search">Обыскать кухню</button>'
)

# Remove trophy emoji from index.html achievement popup
content = content.replace(
    '<div class="achievement-popup-icon">🏆</div>',
    '<div class="achievement-popup-icon">★</div>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html updated successfully!")
