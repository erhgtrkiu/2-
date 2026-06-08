import re

with open(r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if 'note_0_title' in line and len(line) > 5000:
            print(f"Line {idx} length: {len(line)}")
            # Let's write the first matching long line to a text file to read it
            with open('scratch/found_long_line.json', 'w', encoding='utf-8') as out:
                out.write(line)
            print("Wrote line to scratch/found_long_line.json")
            break
