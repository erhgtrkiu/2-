import json

transcript_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
        except Exception:
            continue
        
        step_index = data.get('step_index')
        if step_index is not None and step_index >= 8000:
            tool_calls = data.get('tool_calls', [])
            for tc in tool_calls:
                name = tc.get('name')
                args = tc.get('args', {})
                if isinstance(args, str):
                    try: args = json.loads(args)
                    except: pass
                if isinstance(args, dict):
                    target = args.get('TargetFile', '')
                    if 'app.js' in target:
                        print(f"Step {step_index}: {name} to {target}")
                        if name == 'write_to_file':
                            print(f"  Code content length: {len(args.get('CodeContent', ''))}")
                            print(f"  Description: {args.get('Description')}")
                        elif name == 'replace_file_content':
                            print(f"  TargetContent length: {len(args.get('TargetContent', ''))}")
                            print(f"  ReplacementContent length: {len(args.get('ReplacementContent', ''))}")
                            print(f"  Description: {args.get('Description')}")
                        elif name == 'multi_replace_file_content':
                            print(f"  Chunks length: {len(args.get('ReplacementChunks', []))}")
                            print(f"  Description: {args.get('Description')}")
