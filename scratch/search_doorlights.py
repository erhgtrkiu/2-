import json

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
            name = tc.get('name')
            if name in ('replace_file_content', 'multi_replace_file_content', 'write_to_file'):
                args = tc.get('args', {})
                if isinstance(args, str):
                    try: args = json.loads(args)
                    except: pass
                if isinstance(args, dict):
                    # Check if 'doorLights' is in the arguments
                    args_str = json.dumps(args, ensure_ascii=False)
                    if 'doorLights' in args_str:
                        print(f"Step {step_index}: {name} contains 'doorLights'")
                        # Print some context or description
                        print("  Description:", args.get('Description'))
