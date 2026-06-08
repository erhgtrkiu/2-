import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
log_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        try:
            data = json.loads(line, strict=False)
            content = data.get('content', '')
            if 'media__178066' in content:
                print(f"=== Step {data.get('step_index')} ===")
                # Print user inputs and models notes about these files
                if data.get('type') == 'USER_INPUT':
                    print(content)
                elif 'thinking' in data:
                    print("Thinking snippet:", data['thinking'][:300])
        except Exception as e:
            pass
