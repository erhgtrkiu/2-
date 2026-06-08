import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
log_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        try:
            data = json.loads(line)
            content = data.get('content', '')
            if data.get('type') == 'USER_INPUT':
                if 'закры' in content.lower() or 'лестн' in content.lower() or 'stairs' in content.lower() or 'двер' in content.lower():
                    print(f"=== Step {data.get('step_index')} ===")
                    print(content)
        except Exception as e:
            pass
