import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\m3615\samosbor_game\scratch\step_5716.json', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's search for "stairs" or "shaft" in the raw text file
idx = 0
while True:
    pos = text.lower().find("shaft", idx)
    if pos == -1:
        break
    print(f"--- Found 'shaft' at pos {pos} ---")
    print(text[max(0, pos - 150):min(len(text), pos + 150)])
    idx = pos + 5
