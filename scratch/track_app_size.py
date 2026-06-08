import json
import re

transcript_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

try:
    with open(transcript_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except Exception as e:
    print(f"Error: {e}")
    exit(1)

print("Tracking app.js file sizes from view_file tool outputs:")
for line in lines:
    try:
        data = json.loads(line)
        step = data.get('step_index')
        type_ = data.get('type')
        content = data.get('content', '')
        
        if type_ == 'VIEW_FILE' and 'app.js' in content:
            match = re.search(r'Total Bytes: (\d+)', content)
            if match:
                size = match.group(1)
                # Find if it specifies the path
                path_match = re.search(r'File Path: `([^`]+)`', content)
                path = path_match.group(1) if path_match else "unknown"
                if 'samosbor_game/app.js' in path or 'samosbor_game\\app.js' in path:
                    print(f"Step {step} | Size: {size} bytes | Path: {path}")
    except Exception:
        pass
