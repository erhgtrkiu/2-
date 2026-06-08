import sys
sys.stdout.reconfigure(encoding='utf-8')

search_words = ['обыскать', 'облуты', 'loot', 'cabinet', 'table', 'shelf', 'search']
with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    for word in search_words:
        if word in line.lower():
            print(f"{idx+1}: {line.strip()[:100]}")
            break
