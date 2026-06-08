import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    with open(r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            # We want steps where type is VIEW_FILE and Cwd/AbsolutePath is app.js
            # and let's check if 'LORE_NOTES' is in the line
            if 'VIEW_FILE' in line and 'app.js' in line and 'LORE_NOTES' in line:
                # Let's inspect the line
                data = json.loads(line)
                content = data.get('content', '')
                if 'Грязный листок бумаги' in content or 'РАПОРТ. Ликвидатор' in content:
                    print(f"Found match in VIEW_FILE at line {idx}, len={len(content)}")
                    # Let's print out lines around the notes
                    lines_in_content = content.split('\n')
                    for j, l in enumerate(lines_in_content):
                        if 'LORE_NOTES' in l or 'note_' in l or 'title:' in l:
                            # print j-2 to j+20
                            for k in range(max(0, j-2), min(len(lines_in_content), j+40)):
                                print(f"{k}: {lines_in_content[k]}")
                            print("=" * 40)
except Exception as e:
    print("Error:", e)
