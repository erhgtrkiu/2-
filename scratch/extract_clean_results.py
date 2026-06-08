import json

log_path = 'C:/Users/m3615/.gemini/antigravity/brain/68589a5c-391d-4fb4-bd7d-f6ad216b12ae/.system_generated/logs/transcript.jsonl'
output_path = 'C:/Users/m3615/samosbor_game/scratch/clean_results.txt'

with open(log_path, 'r', encoding='utf-8') as f, open(output_path, 'w', encoding='utf-8') as out:
    for line in f:
        try:
            data = json.loads(line)
            if data.get('type') == 'USER_INPUT':
                step = data.get('step_index')
                content = data.get('content', '')
                out.write(f"=== STEP {step} ===\n{content}\n\n")
        except Exception as e:
            pass
print("Done extracting clean results.")
