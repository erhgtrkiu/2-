import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
log_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        try:
            data = json.loads(line)
            if 'tool_calls' in data:
                for tc in data['tool_calls']:
                    if 'replace_file_content' in tc.get('name', '') or 'write_to_file' in tc.get('name', ''):
                        args = tc.get('args', {})
                        if 'app.js' in str(args.get('TargetFile', '')):
                            print(f"=== Step {data.get('step_index')} ===")
                            print("Tool:", tc.get('name'))
                            print("Description:", args.get('Description'))
                            print("Instruction:", args.get('Instruction'))
        except Exception as e:
            pass
