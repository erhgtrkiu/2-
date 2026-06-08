import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    with open(r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i in range(2670, 2690):
        if i >= len(lines):
            break
        line = lines[i]
        data = json.loads(line)
        print(f"Line {i}: type={data.get('type')}, source={data.get('source')}, status={data.get('status')}")
        tcalls = data.get('tool_calls', [])
        for tc in tcalls:
            print(f"  Tool: {tc.get('name')}")
            # check if ReplacementContent is in args
            args = tc.get('args', {})
            if 'ReplacementContent' in args:
                repl = args['ReplacementContent']
                print(f"    Repl len={len(repl)}")
                if 'LORE_NOTES' in repl:
                    print(f"    FOUND LORE_NOTES in ReplacementContent! Saving to scratch/lore_notes_found_{i}.js")
                    with open(f'scratch/lore_notes_found_{i}.js', 'w', encoding='utf-8') as out:
                        out.write(repl)
except Exception as e:
    print("Error:", e)
