import json
import os
import re

transcript_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

views = []

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
        except Exception:
            continue
        
        step_index = data.get('step_index')
        created_at = data.get('created_at')
        step_type = data.get('type')
        content = data.get('content', '')
        
        if step_type == 'VIEW_FILE' and 'app.js' in content:
            # Check if this view response has StartLine and EndLine in content
            lines_match = re.search(r'Showing lines (\d+) to (\d+)', content)
            if lines_match:
                start = int(lines_match.group(1))
                end = int(lines_match.group(2))
                views.append({
                    'step': step_index,
                    'time': created_at,
                    'start': start,
                    'end': end,
                    'length': len(content)
                })

print(f"Found {len(views)} views of app.js:")
for v in views:
    print(f"  Step {v['step']} ({v['time']}): lines {v['start']} to {v['end']} (response len={v['length']})")
