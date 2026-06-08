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
        step_type = data.get('type')
        
        # Check for CODE_ACTION targeting app.js
        if step_type == 'CODE_ACTION':
            content = data.get('content', '')
            if 'app.js' in content:
                # print a summary of the code action
                lines = content.split('\n')
                diff_lines = [l for l in lines if l.startswith('+') or l.startswith('-')]
                print(f"Step {step_index} ({created_at}): CODE_ACTION for app.js. Total diff lines: {len(diff_lines)}")
                if diff_lines:
                    print(f"  First 3 diff lines: {diff_lines[:3]}")
                continue
                
        tool_calls = data.get('tool_calls', [])
        for tc in tool_calls:
            name = tc.get('name')
            if name in ('write_to_file', 'replace_file_content', 'multi_replace_file_content'):
                args = tc.get('args', {})
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except Exception:
                        pass
                
                target = args.get('TargetFile', '')
                if 'app.js' in target:
                    desc = args.get('Description', '') or args.get('Instruction', '')
                    print(f"Step {step_index} ({created_at}): {name} on app.js. Desc: {desc}")
