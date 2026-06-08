import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
log_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if 'media__178066' in line:
            try:
                data = json.loads(line, strict=False)
                print(f"=== Line {idx}, Step {data.get('step_index')}, Type {data.get('type')} ===")
                content = data.get('content', '')
                if content:
                    print("Content:", content[:500])
                if 'tool_calls' in data:
                    print("Tool Calls:", json.dumps(data['tool_calls'], indent=2, ensure_ascii=False)[:500])
            except Exception as e:
                print("Error parsing line:", idx, e)
