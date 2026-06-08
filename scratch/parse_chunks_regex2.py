import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\m3615\samosbor_game\scratch\step_5145.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

chunks_str = data['tool_calls'][0]['args']['ReplacementChunks']
print("Length of chunks_str:", len(chunks_str))

# Let's search for "stairs" or "shaft" in chunks_str case-insensitively, starting at index 2000
import re
for match in re.finditer(r'(stairs|shaft|wall|mesh|hole|geom|door|pivot|buildfloor)', chunks_str, re.IGNORECASE):
    if match.start() < 2000:
        continue
    start = max(0, match.start() - 100)
    end = min(len(chunks_str), match.end() + 100)
    print(f"=== Found '{match.group()}' at {match.start()} ===")
    print(chunks_str[start:end])
    print("-" * 50)
