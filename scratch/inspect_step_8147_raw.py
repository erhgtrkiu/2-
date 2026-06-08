import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

transcript_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
        except Exception:
            continue
        
        step_index = data.get('step_index')
        if step_index == 8147:
            print("Step 8147 JSON:")
            tc = data.get('tool_calls', [])
            for t in tc:
                args = t.get('args', {})
                if isinstance(args, str):
                    print("args is string, printing first 1000 chars:")
                    print(args[:1000])
                elif isinstance(args, dict):
                    print("args keys:", list(args.keys()))
                    chunks = args.get('ReplacementChunks', '')
                    print("ReplacementChunks type:", type(chunks))
                    if isinstance(chunks, str):
                        print("ReplacementChunks length:", len(chunks))
                        print("ReplacementChunks first 1000 chars:")
                        print(chunks[:1000])
                        print("ReplacementChunks last 1000 chars:")
                        print(chunks[-1000:])
                    elif isinstance(chunks, list):
                        print("ReplacementChunks items count:", len(chunks))
                        print("First item:", json.dumps(chunks[0], ensure_ascii=False)[:300])
            break
