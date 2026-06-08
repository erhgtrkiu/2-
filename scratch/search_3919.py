import json

log_path = 'C:/Users/m3615/.gemini/antigravity/brain/68589a5c-391d-4fb4-bd7d-f6ad216b12ae/.system_generated/logs/transcript.jsonl'
output_path = 'C:/Users/m3615/samosbor_game/scratch/photos_3919.txt'

with open(log_path, 'r', encoding='utf-8') as f, open(output_path, 'w', encoding='utf-8') as out:
    for line in f:
        try:
            data = json.loads(line)
            content = data.get('content', '')
            thinking = data.get('thinking', '')
            if '1780650172051' in line or '1780650175430' in line:
                out.write(f"Step {data.get('step_index')}:\nThinking:\n{thinking}\nContent:\n{content}\n\n")
        except Exception as e:
            pass

print("Done searching 3919 photos.")
