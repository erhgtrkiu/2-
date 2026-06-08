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
        if step_index == 8928:
            print(f"--- STEP 8928 ---")
            tc = data.get('tool_calls', [])
            for t in tc:
                print("Tool:", t.get('name'))
                args = t.get('args', {})
                if isinstance(args, str):
                    try: args = json.loads(args)
                    except: pass
                if isinstance(args, dict):
                    print("Args TargetFile:", args.get('TargetFile'))
                    code = args.get('CodeContent', '')
                    print("Code length:", len(code))
                    print("Code sample:", repr(code[:200]))
                    print("Code end:", repr(code[-200:]))
            break
