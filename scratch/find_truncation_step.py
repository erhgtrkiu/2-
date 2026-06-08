import json
import os
import re

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
        content = data.get('content', '')
        
        # We are looking for VIEW_FILE responses that contain app.js and show line count
        if step_type == 'VIEW_FILE' and 'app.js' in content:
            lines_match = re.search(r'Total Lines:\s*(\d+)', content)
            bytes_match = re.search(r'Total Bytes:\s*(\d+)', content)
            if lines_match or bytes_match:
                lines = lines_match.group(1) if lines_match else "unknown"
                bytes_count = bytes_match.group(1) if bytes_match else "unknown"
                print(f"Step {step_index} ({created_at}): view_file response for app.js has {lines} lines, {bytes_count} bytes")
