import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\m3615\samosbor_game\scratch\step_5716.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for tc in data['tool_calls']:
    args = tc.get('args', {})
    chunks = args.get('ReplacementChunks')
    if isinstance(chunks, str):
        chunks = json.loads(chunks, strict=False)
    for c_idx, chunk in enumerate(chunks):
        target = chunk.get('TargetContent', '')
        repl = chunk.get('ReplacementContent', '')
        if 'shaft' in target.lower() or 'stairs' in target.lower() or 'wall' in target.lower():
            print(f"=== Chunk {c_idx} (Stairs/Wall) ===")
            print("StartLine:", chunk.get('StartLine'))
            print("EndLine:", chunk.get('EndLine'))
            print("Target:")
            print(target)
            print("Replacement:")
            print(repl)
            print("-" * 60)
