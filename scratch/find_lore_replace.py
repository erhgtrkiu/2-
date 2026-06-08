import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    with open(r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            if 'const LORE_NOTES = [' in line and 'ReplacementContent' in line:
                data = json.loads(line)
                for tc in data.get('tool_calls', []):
                    args = tc.get('args', {})
                    repl = args.get('ReplacementContent', '')
                    if 'const LORE_NOTES = [' in repl:
                        print(f"Found at line {idx}, len={len(repl)}")
                        # If it is truncated in the transcript, we'll see if it has the full notes
                        # Let's save it to a file
                        with open(f'scratch/lore_notes_{idx}.js', 'w', encoding='utf-8') as out:
                            out.write(repl)
                        print(f"Saved to scratch/lore_notes_{idx}.js")
except Exception as e:
    print("Error:", e)
