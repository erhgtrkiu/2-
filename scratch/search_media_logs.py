import json

log_path = 'C:/Users/m3615/.gemini/antigravity/brain/68589a5c-391d-4fb4-bd7d-f6ad216b12ae/.system_generated/logs/transcript.jsonl'

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            content = data.get('content', '')
            if 'media__' in content or 'attachment' in line:
                print(f"=== Step {data.get('step_index')} ===")
                print(content[:500])
                print("-" * 50)
        except Exception as e:
            pass
