import json
import sys

transcript_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
        except Exception:
            continue
        
        step_index = data.get('step_index')
        if step_index == 5018:
            print(f"--- STEP 5018 ---")
            tc = data.get('tool_calls', [])
            for t in tc:
                args = t.get('args', {})
                print("Type of args:", type(args))
                if isinstance(args, str):
                    print("args starts with:", repr(args[:100]))
                    print("args length:", len(args))
                    # Let's write the raw args to a file so we can view it
                    with open(r'C:\Users\m3615\samosbor_game\scratch\step_5018_args.txt', 'w', encoding='utf-8') as out:
                        out.write(args)
                    print("Wrote args to step_5018_args.txt")
                    
                    # Let's print around character 1733
                    sub = args[max(0, 1700):min(len(args), 1760)]
                    print("Snippet around 1733:", repr(sub))
                elif isinstance(args, dict):
                    chunks = args.get('ReplacementChunks', '')
                    print("Type of chunks:", type(chunks))
                    if isinstance(chunks, str):
                        print("chunks length:", len(chunks))
                        with open(r'C:\Users\m3615\samosbor_game\scratch\step_5018_chunks.txt', 'w', encoding='utf-8') as out:
                            out.write(chunks)
                        print("Wrote chunks to step_5018_chunks.txt")
                        sub = chunks[max(0, 1700):min(len(chunks), 1760)]
                        print("Snippet around 1733 in chunks:", repr(sub))
            break
