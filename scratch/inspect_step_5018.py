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
        if step_index == 5018:
            tc = data.get('tool_calls', [])
            for t in tc:
                args = t.get('args', {})
                if isinstance(args, str):
                    args = json.loads(args)
                chunks_raw = args.get('ReplacementChunks', '')
                for idx in range(1720, 1745):
                    if idx < len(chunks_raw):
                        print(f"{idx}: {repr(chunks_raw[idx])}")
