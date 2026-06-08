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
        if step_index in (7008, 7138):
            print(f"Step {step_index}: type={data.get('type')}, created_at={data.get('created_at')}")
            tc = data.get('tool_calls', [])
            for t in tc:
                print(f"  Tool {t.get('name')}")
                args = t.get('args', {})
                if isinstance(args, str):
                    try: args = json.loads(args)
                    except: pass
                if isinstance(args, dict):
                    print(f"    TargetFile: {args.get('TargetFile')}")
                    print(f"    CodeContent:\n{args.get('CodeContent')}")
                    print("-" * 50)
