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
        created_at = data.get('created_at')
        tool_calls = data.get('tool_calls', [])
        
        for tc in tool_calls:
            name = tc.get('name')
            if name == 'write_to_file':
                args = tc.get('args', {})
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except Exception:
                        pass
                
                target = args.get('TargetFile', '')
                if 'app.js' in target:
                    content_len = len(args.get('CodeContent', ''))
                    desc = args.get('Description', '')
                    print(f"Step {step_index} ({created_at}): write_to_file on app.js, length={content_len}, desc={desc}")
