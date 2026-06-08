with open('C:/Users/m3615/samosbor_game/scratch/photos_analysis.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'void|пустот|салатов|зелен|лампа|зеленая', text, re.IGNORECASE)
printed = set()
with open('C:/Users/m3615/samosbor_game/scratch/void_search_results.txt', 'w', encoding='utf-8') as out:
    for m in matches:
        start_pos = max(0, m.start() - 250)
        end_pos = min(len(text), m.end() + 250)
        snippet = text[start_pos:end_pos]
        step_match = re.search(r'=== STEP (\d+) ', text[max(0, m.start()-5000):m.start()])
        step_num = step_match.group(1) if step_match else "unknown"
        key = (step_num, snippet[:50])
        if key not in printed:
            out.write(f"=== STEP {step_num} ===\n{snippet}\n")
            out.write("=" * 60 + "\n\n")
            printed.add(key)
print("Done writing void search results.")
