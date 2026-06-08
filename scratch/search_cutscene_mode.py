import json

transcript_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
        except Exception:
            continue
        
        step_index = data.get('step_index')
        tool_calls = data.get('tool_calls', [])
        for tc in tool_calls:
            name = tc.get('name')
            args_str = json.dumps(tc.get('args', {}), ensure_ascii=False)
            if 'setCutsceneMode' in args_str:
                print(f"Step {step_index}: {name} contains 'setCutsceneMode'")
