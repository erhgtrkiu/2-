import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if any(w in line for w in ['пустот', 'лестни', 'салатов', 'стен', 'фото']):
            # Skip if it is a search script
            if 'find_notes' in line or 'find_notes_text' in line or 'raw_match.txt' in line:
                continue
            try:
                data = json.loads(line)
                content = data.get('content', '')
                if content and any(w in content for w in ['пустот', 'лестни', 'салатов', 'стен', 'фото']):
                    print(f"Line {idx}: source={data.get('source')}, len={len(line)}")
                    print("Content:")
                    print(content[:1000])
                    print("-" * 40)
            except Exception as e:
                pass
