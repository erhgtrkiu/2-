import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
log_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        try:
            data = json.loads(line, strict=False)
            if data.get('step_index') == 5716:
                print(f"Found step 5716 at line {idx}!")
                # Let's save it to step_5716.json
                with open(r'C:\Users\m3615\samosbor_game\scratch\step_5716.json', 'w', encoding='utf-8') as outf:
                    json.dump(data, outf, indent=2, ensure_ascii=False)
                print("Dumped step 5716 raw successfully")
        except Exception as e:
            pass
