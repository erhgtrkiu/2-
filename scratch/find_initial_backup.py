import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
transcript_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

try:
    with open(transcript_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

print("Searching for backup actions at start of session...")
for line in lines:
    try:
        data = json.loads(line)
        step = data.get('step_index')
        if step and 8200 <= step <= 8300:
            type_ = data.get('type')
            if type_ in ['RUN_COMMAND', 'WRITE_TO_FILE']:
                content = data.get('content', '')
                if 'copy' in content.lower() or 'backup' in content.lower() or 'app.js' in content.lower():
                    print(f"Step {step} | Type: {type_}")
                    print(f"  Content: {content[:300].replace(chr(10), ' ')}")
    except Exception:
        pass
