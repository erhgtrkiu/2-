import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    with open(r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Let's search around line 2705
    for i in range(2680, 2750):
        if i >= len(lines):
            break
        line = lines[i]
        if 'LORE_NOTES' in line and ('tool_calls' in line or 'replace_file_content' in line):
            print(f"Found LORE_NOTES in line {i}:")
            data = json.loads(line)
            # Check tool calls
            for tc in data.get('tool_calls', []):
                args = tc.get('args', {})
                code = args.get('CodeContent', '')
                if 'LORE_NOTES' in code:
                    print(code[:2000])
                    print("...")
                repl = args.get('ReplacementContent', '')
                if 'LORE_NOTES' in repl:
                    print(repl[:4000])
                    print("...")
                    
except Exception as e:
    print("Error:", e)
