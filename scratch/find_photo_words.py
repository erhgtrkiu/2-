with open('C:/Users/m3615/samosbor_game/scratch/photos_analysis.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Find sections discussing Photo 1 or Photo 2
matches = re.finditer(r'photo 1|photo 2|фото 1|фото 2', text, re.IGNORECASE)
printed = set()
for m in matches:
    start_pos = max(0, m.start() - 400)
    end_pos = min(len(text), m.end() + 600)
    snippet = text[start_pos:end_pos]
    # find step index in context
    step_match = re.search(r'=== STEP (\d+) ', text[max(0, m.start()-5000):m.start()])
    step_num = step_match.group(1) if step_match else "unknown"
    if step_num not in printed:
        print(f"=== STEP {step_num} ===")
        print(snippet)
        print("=" * 60)
        printed.add(step_num)
