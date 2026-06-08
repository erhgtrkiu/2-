import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\m3615\samosbor_game\scratch\step_5145.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

chunks_str = data['tool_calls'][0]['args']['ReplacementChunks']
print(chunks_str)
