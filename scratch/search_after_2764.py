import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    with open(r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for idx in range(2710, len(lines)):
        line = lines[idx]
        if 'LORE_NOTES' in line:
            # check type of step
            data = json.loads(line)
            step_type = data.get('type')
            print(f"Line {idx} step_index {data.get('step_index')}: type={step_type}")
            # If it's a VIEW_FILE of app.js, let's see if we have the notes
            content = data.get('content', '')
            if 'Грязный листок' in content:
                print(f"  Content has 'Грязный листок', len={len(content)}")
                # save content to file
                with open(f'scratch/found_content_{idx}.txt', 'w', encoding='utf-8') as out:
                    out.write(content)
                print(f"  Saved to scratch/found_content_{idx}.txt")
except Exception as e:
    print("Error:", e)
