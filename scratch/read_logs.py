import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
log_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        try:
            data = json.loads(line)
            if data.get('type') == 'USER_INPUT':
                print(f"=== Step {data.get('step_index')} ===")
                print(data.get('content'))
                # Print any file references or details if available
                # like attachments
                if 'attachments' in data:
                    print("Attachments:", data['attachments'])
        except Exception as e:
            pass
