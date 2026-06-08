import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

transcript_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
        except Exception:
            continue
        
        step_index = data.get('step_index')
        if step_index in (8094, 8171, 8182, 8531):
            print(f"--- STEP {step_index} ---")
            tc = data.get('tool_calls', [])
            for t in tc:
                args = t.get('args', {})
                if isinstance(args, str):
                    try: args = json.loads(args)
                    except: pass
                if isinstance(args, dict):
                    print("Tool:", t.get('name'))
                    print("ReplacementContent snippet:\n", args.get('ReplacementContent'))
                    print("TargetContent snippet:\n", args.get('TargetContent'))
