import json
import re
import sys

with open(r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('scratch/saved_all_matches.txt', 'w', encoding='utf-8') as out:
    for idx, line in enumerate(lines):
        if 'note_0_title' in line:
            # Let's search if this line contains a large block of translations
            for match in re.finditer(r'note_0_title', line):
                pos = match.start()
                start = max(0, pos - 100)
                end = min(len(line), pos + 2000)
                out.write(f"Match at line {idx}, pos {pos}:\n")
                out.write(line[start:end])
                out.write("\n" + "=" * 80 + "\n")
print("Saved all matches to scratch/saved_all_matches.txt")
