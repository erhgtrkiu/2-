import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# We want to scan the transcript.jsonl file for Russian translations of notes
ru_notes = {}
try:
    with open(r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            # Check if this line has note keys and Russian characters
            if 'note_0_title' in line:
                # Let's extract any JSON-like key-value pairs matching note_\d+_(title|content)
                # E.g. "note_0_title": "..." or \"note_0_title\"
                for m in re.finditer(r'note_(\d+)_(title|content)', line):
                    note_id = int(m.group(1))
                    field = m.group(2)
                    key = f"note_{note_id}_{field}"
                    
                    # Search after this key for the value
                    start_pos = m.end()
                    sub = line[start_pos:start_pos+3000]
                    val_match = re.search(r'^\\*"\s*:\s*\\*"(.*?)\\*"', sub)
                    if val_match:
                        val = val_match.group(1)
                        # check if it has Russian characters (Cyrillic: \u0400-\u04FF)
                        if re.search(r'[\u0400-\u04FF]', val):
                            # We want the longest Russian value found for this key
                            if len(val) > len(ru_notes.get(key, '')):
                                ru_notes[key] = val
                    else:
                        val_match = re.search(r'^"\s*:\s*"(.*?)"', sub)
                        if val_match:
                            val = val_match.group(1)
                            if re.search(r'[\u0400-\u04FF]', val):
                                if len(val) > len(ru_notes.get(key, '')):
                                    ru_notes[key] = val
except Exception as e:
    print("Error:", e)

for k in sorted(ru_notes.keys()):
    v = ru_notes[k]
    v = v.replace('\\\\n', '\n').replace('\\n', '\n').replace('\\\"', '"').replace('\\r', '')
    print(f"'{k}': {repr(v)},")
