import json
import os

transcript_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
        except Exception:
            continue
        
        step_index = data.get('step_index')
        if step_index == 103:
            print(f"Step 103: type={data.get('type')}")
            tc = data.get('tool_calls', [])
            for t in tc:
                print(f"  Tool {t.get('name')}")
                args = t.get('args', {})
                print(f"  args type: {type(args)}")
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except Exception as e:
                        print(f"  parse error: {e}")
                
                if isinstance(args, dict):
                    print("  args keys:", list(args.keys()))
                    for k in ['TargetContent', 'ReplacementContent']:
                        val = args.get(k, '')
                        print(f"    {k} type: {type(val)}, length: {len(val)}")
                        print(f"    {k} repr: {repr(val)}")
                        print(f"    {k} starts with quote? {val.startswith(chr(34)) or val.startswith(chr(39))}")
