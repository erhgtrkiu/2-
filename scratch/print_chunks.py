import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\m3615\samosbor_game\scratch\step_5145.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for tc in data['tool_calls']:
    args = tc.get('args', {})
    chunks = args.get('ReplacementChunks')
    if isinstance(chunks, str):
        chunks = json.loads(chunks, strict=False)
    for c_idx, chunk in enumerate(chunks):
        print(f"=== Chunk {c_idx} ===")
        print("StartLine:", chunk.get('StartLine'))
        print("EndLine:", chunk.get('EndLine'))
        print("TargetContent:")
        print(chunk.get('TargetContent'))
        print("ReplacementContent:")
        print(chunk.get('ReplacementContent'))
        print("\n")
