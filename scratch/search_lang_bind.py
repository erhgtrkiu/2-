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
            if 'settings-language-select' in args_str:
                print(f"Step {step_index}: contains settings-language-select")
                args = tc.get('args', {})
                if isinstance(args, str):
                    try: args = json.loads(args)
                    except: pass
                if isinstance(args, dict):
                    print("  Tool:", tc.get('name'))
                    print("  Description:", args.get('Description'))
                    # Print snippet of ReplacementContent or CodeContent
                    code = args.get('ReplacementContent') or args.get('CodeContent') or ""
                    if code:
                        print("  Code snippet:")
                        print(code[:800])
                    # If it's ReplacementChunks
                    chunks = args.get('ReplacementChunks', [])
                    if isinstance(chunks, list):
                        for c in chunks:
                            rep = c.get('ReplacementContent', '')
                            if 'settings-language-select' in rep:
                                print("  Chunk Replacement snippet:")
                                print(rep[:800])
            elif 'change' in args_str and ('lang' in args_str or 'select' in args_str):
                # Print index
                pass
