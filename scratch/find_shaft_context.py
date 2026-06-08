with open('C:/Users/m3615/samosbor_game/scratch/photos_analysis.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Find all occurrences of shaftL in the text and print their context
matches = re.finditer(r'shaftL', text, re.IGNORECASE)
for i, m in enumerate(matches):
    start = max(0, m.start() - 300)
    end = min(len(text), m.end() + 300)
    print(f"--- Occurrence {i+1} ---")
    print(text[start:end])
    print("=" * 60)
