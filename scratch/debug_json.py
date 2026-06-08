import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\m3615\samosbor_game\scratch\step_5145.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Type of data:", type(data))
print("Keys of data:", list(data.keys()))
if 'tool_calls' in data:
    for tc in data['tool_calls']:
        print("Tool Name:", tc.get('name'))
        args = tc.get('args', {})
        print("Args Keys:", list(args.keys()))
        print("Description:", args.get('Description'))
        print("Instruction:", args.get('Instruction'))
        if 'ReplacementChunks' in args:
            chunks = args['ReplacementChunks']
            print("Type of chunks:", type(chunks))
            if isinstance(chunks, list):
                print("Number of chunks:", len(chunks))
                for idx, c in enumerate(chunks):
                    print(f"Chunk {idx}: TargetContent length={len(c.get('TargetContent', ''))}, StartLine={c.get('StartLine')}, EndLine={c.get('EndLine')}")
                    # Print first 100 chars of ReplacementContent
                    print("ReplacementContent snippet:", repr(c.get('ReplacementContent', ''))[:150])
