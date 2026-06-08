import re

with open('C:/Users/m3615/samosbor_game/scratch/photos_analysis.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's search for references to media__1780650172051 or media__1780650175430
# or words like "photo" or "void" or "stairs" or "passage" or "passage to the stairs"
matches = re.findall(r'(\n(?:[^\n]*\n){0,10}[^\n]*(?:media__1780650172051|media__1780650175430|Photo_1|Photo_2|фото 1|фото 2)[^\n]*(?:\n[^\n]*){0,10})', text, re.IGNORECASE)

print(f"Found {len(matches)} matches")
with open('C:/Users/m3615/samosbor_game/scratch/photos_matching.txt', 'w', encoding='utf-8') as out:
    for i, m in enumerate(matches[:50]):
        out.write(f"--- MATCH {i+1} ---\n{m}\n\n")
