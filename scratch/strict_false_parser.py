import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
log_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        try:
            # use strict=False to allow control characters (e.g. unescaped newlines in JSON strings)
            data = json.loads(line, strict=False)
            if data.get('step_index') == 5145:
                print(f"Found step 5145 at line {idx}!")
                with open(r'C:\Users\m3615\samosbor_game\scratch\step_5145.json', 'w', encoding='utf-8') as outf:
                    json.dump(data, outf, indent=2, ensure_ascii=False)
                print("Dumped to step_5145.json successfully")
        except Exception as e:
            pass
