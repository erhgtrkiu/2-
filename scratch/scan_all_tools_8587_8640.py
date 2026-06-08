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
        if step_index is not None and 8587 <= step_index <= 8640:
            print(f"Step {step_index}: {data.get('type')}")
            tc = data.get('tool_calls', [])
            for t in tc:
                print(f"  Tool call: {t.get('name')}")
                args = t.get('args', {})
                if isinstance(args, str):
                    try: args = json.loads(args)
                    except: pass
                if isinstance(args, dict):
                    print(f"    Args: {json.dumps(args, ensure_ascii=False)[:200]}")
