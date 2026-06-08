import json
import os

transcript_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
        except Exception:
            continue
        
        step_index = data.get('step_index')
        created_at = data.get('created_at')
        content = data.get('content', '')
        
        if 'cycleDuration' in content or 'cycleDuration' in str(data):
            # Print step type and a small snippet
            print(f"Step {step_index} ({created_at}): type={data.get('type')}")
            tc = data.get('tool_calls', [])
            for t in tc:
                if 'cycleDuration' in str(t):
                    print(f"  Tool call: {t.get('name')}")
