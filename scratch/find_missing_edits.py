import json
import os
from datetime import datetime

transcript_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

start_time = datetime.fromisoformat("2026-06-03T21:32:18+00:00")
end_time = datetime.fromisoformat("2026-06-05T15:28:00+00:00")

edits = []

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line, strict=False)
        except Exception:
            continue
        
        step_index = data.get('step_index')
        created_at = data.get('created_at')
        if not created_at:
            continue
        
        cleaned = created_at.replace('Z', '+00:00')
        time_parsed = datetime.fromisoformat(cleaned)
        
        if start_time <= time_parsed <= end_time:
            tool_calls = data.get('tool_calls', [])
            for tc in tool_calls:
                name = tc.get('name')
                if name in ('replace_file_content', 'multi_replace_file_content', 'write_to_file'):
                    args = tc.get('args', {})
                    if isinstance(args, str):
                        try: args = json.loads(args, strict=False)
                        except: pass
                    
                    if isinstance(args, dict):
                        target = args.get('TargetFile', '')
                        if 'app.js' in target and not 'inspect_old_app.js' in target and not 'replace_textures_in_app.js' in target:
                            edits.append({
                                'step': step_index,
                                'time': created_at,
                                'tool': name,
                                'desc': args.get('Description', '') or args.get('Instruction', '')
                            })

print(f"Found {len(edits)} edits in the gap:")
for e in edits:
    print(f"  Step {e['step']} ({e['time']}): {e['tool']} - {e['desc']}")
