import json

transcript_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'
targets = {8590, 8672, 9198, 9288, 9446, 9506, 9579}

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            step = data.get('step_index')
            if step in targets:
                print(f"Step {step} at {data.get('created_at')} - Type {data.get('type')}")
        except:
            pass
