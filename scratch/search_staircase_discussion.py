import os

with open('C:/Users/m3615/samosbor_game/scratch/search_log.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Split into steps
steps = text.split('=== STEP ')
for step in steps:
    if not step.strip():
        continue
    header, *body = step.split(' ===\n')
    body_text = ' '.join(body)
    # Check if this step contains words related to staircase issues
    words = ['лестниц', 'закрыт', 'проход', 'дверь', 'всё ещё', 'не то']
    if any(w in body_text for w in words):
        print(f"=== STEP {header.strip()} ===")
        print(body_text.strip()[:1000])
        print("-" * 40)
