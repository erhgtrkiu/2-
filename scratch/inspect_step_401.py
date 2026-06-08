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
        if step_index == 401:
            print(f"Step 401: type={data.get('type')}")
            tc = data.get('tool_calls', [])
            for t in tc:
                print(f"  Tool {t.get('name')}")
                args = t.get('args', {})
                if isinstance(args, str):
                    print(f"    args is string of length {len(args)}")
                    # Try to parse it
                    try:
                        args = json.loads(args)
                        print(f"    parsed args keys: {list(args.keys())}")
                        chunks = args.get('ReplacementChunks', [])
                        print(f"    chunks type: {type(chunks)}, length: {len(chunks)}")
                        if chunks:
                            print(f"    First chunk type: {type(chunks[0])}")
                            print(f"    First chunk value: {repr(chunks[0])}")
                    except Exception as e:
                        print(f"    parse error: {e}")
                else:
                    print(f"    args is dict, keys: {list(args.keys())}")
                    chunks = args.get('ReplacementChunks', [])
                    print(f"    chunks type: {type(chunks)}, length: {len(chunks)}")
                    if chunks:
                        print(f"    First chunk type: {type(chunks[0])}")
                        print(f"    First chunk value: {repr(chunks[0])}")
