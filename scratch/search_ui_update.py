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
        tool_calls = data.get('tool_calls', [])
        for tc in tool_calls:
            args_str = json.dumps(tc.get('args', {}), ensure_ascii=False)
            if 'focusedSpawnDoor' in args_str or 'updateFocusedObjectUI' in args_str:
                print(f"Step {step_index}: contains search keywords")
                # Print replacement content snippet
                args = tc.get('args', {})
                if isinstance(args, str):
                    try: args = json.loads(args)
                    except: pass
                if isinstance(args, dict):
                    print("  Tool:", tc.get('name'))
                    print("  Description:", args.get('Description'))
                    # If it's a replacement, print the ReplacementContent
                    if 'ReplacementContent' in args:
                        print("  ReplacementContent:", repr(args.get('ReplacementContent')[:300]))
                    if 'ReplacementChunks' in args:
                        chunks = args['ReplacementChunks']
                        if isinstance(chunks, str):
                            print("  ReplacementChunks len:", len(chunks))
                            print("  ReplacementChunks snippet:", repr(chunks[:300]))
                        elif isinstance(chunks, list):
                            print("  ReplacementChunks list size:", len(chunks))
                            for idx, c in enumerate(chunks):
                                print(f"    Chunk {idx} Replacement:", repr(c.get('ReplacementContent')[:200]))
