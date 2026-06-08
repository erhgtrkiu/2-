import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
log_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        try:
            data = json.loads(line)
            if data.get('step_index') == 5145:
                for tc in data['tool_calls']:
                    args = tc.get('args', {})
                    chunks = json.loads(args.get('ReplacementChunks', '[]'))
                    for c_idx, chunk in enumerate(chunks):
                        print(f"=== Chunk {c_idx} ===")
                        print("StartLine:", chunk.get('StartLine'))
                        print("EndLine:", chunk.get('EndLine'))
                        print("TargetContent:", chunk.get('TargetContent'))
                        print("ReplacementContent:", chunk.get('ReplacementContent'))
        except Exception as e:
            pass
