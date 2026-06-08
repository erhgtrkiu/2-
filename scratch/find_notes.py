import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

notes = {}
try:
    with open(r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            matches = re.findall(r'note_\d+_(?:title|content)', line)
            if matches:
                for match in matches:
                    val_match = re.search(rf'{match}\\\"\s*:\s*\\\"(.*?)\\\"', line)
                    if val_match:
                        notes[match] = val_match.group(1)
                    else:
                        val_match = re.search(rf'{match}\"\s*:\s*\"(.*?)\"', line)
                        if val_match:
                            notes[match] = val_match.group(1)
except Exception as e:
    print("Error:", e)

for k in sorted(notes.keys()):
    val = notes[k]
    val = val.replace('\\\\n', '\n').replace('\\n', '\n').replace('\\\"', '"')
    print(f"'{k}': {repr(val)},")
