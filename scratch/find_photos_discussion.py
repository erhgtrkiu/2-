import json

log_path = 'C:/Users/m3615/.gemini/antigravity/brain/68589a5c-391d-4fb4-bd7d-f6ad216b12ae/.system_generated/logs/transcript.jsonl'

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            content = data.get('content', '')
            thinking = data.get('thinking', '')
            step = data.get('step_index')
            if 'фото 1' in content or 'фото 2' in content or 'photo_1' in content or 'photo_2' in content or 'photo 1' in content or 'photo 2' in content:
                print(f"Step {step}:")
                if content:
                    print("  Content:", content[:300].replace('\n', ' '))
                if thinking:
                    print("  Thinking contains photo ref")
        except:
            pass
