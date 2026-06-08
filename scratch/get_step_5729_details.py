import json

log_path = 'C:/Users/m3615/.gemini/antigravity/brain/68589a5c-391d-4fb4-bd7d-f6ad216b12ae/.system_generated/logs/transcript.jsonl'
output_path = 'C:/Users/m3615/samosbor_game/scratch/step_5729_details.txt'

with open(log_path, 'r', encoding='utf-8') as f, open(output_path, 'w', encoding='utf-8') as out:
    for line in f:
        try:
            data = json.loads(line)
            step = data.get('step_index')
            if step is not None and step >= 5729 and step < 5972:
                source = data.get('source')
                type_ = data.get('type')
                content = data.get('content', '')
                thinking = data.get('thinking', '')
                if source == 'MODEL' and (thinking or content):
                    out.write(f"=== STEP {step} ({type_}) ===\n")
                    if thinking:
                        out.write(f"THINKING:\n{thinking}\n")
                    if content:
                        out.write(f"CONTENT:\n{content}\n")
                    out.write("\n" + "="*40 + "\n\n")
        except Exception as e:
            pass
print("Done extracting step 5729 details.")
