import json

log_path = 'C:/Users/m3615/.gemini/antigravity/brain/68589a5c-391d-4fb4-bd7d-f6ad216b12ae/.system_generated/logs/transcript.jsonl'

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            step = data.get('step_index')
            if step is not None and step >= 3919 and step <= 3940:
                print(f"=== STEP {step} ({data.get('type')}, {data.get('source')}) ===")
                content = data.get('content', '')
                if content:
                    print("CONTENT:")
                    print(content[:1500])
                thinking = data.get('thinking', '')
                if thinking:
                    print("THINKING:")
                    print(thinking[:1000])
                print("\n" + "="*40 + "\n")
        except:
            pass
