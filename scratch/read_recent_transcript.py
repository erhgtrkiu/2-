import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
transcript_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

try:
    with open(transcript_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except Exception as e:
    print(f"Error reading transcript: {e}")
    sys.exit(1)

print(f"Total lines: {len(lines)}")
# Show last 20 steps
for line in lines[-20:]:
    try:
        data = json.loads(line)
        step = data.get('step_index')
        source = data.get('source')
        type_ = data.get('type')
        print(f"Step {step} | Source: {source} | Type: {type_}")
        if 'content' in data and data['content']:
            content_preview = data['content'][:300].replace('\n', ' ')
            print(f"  Content: {content_preview}")
        if 'tool_calls' in data and data['tool_calls']:
            for tc in data['tool_calls']:
                print(f"  Tool Call: {tc.get('name')} -> {tc.get('args', {}).get('TargetFile') or tc.get('args', {}).get('CommandLine') or tc.get('args')}")
    except Exception as e:
        print(f"Error parsing line: {e}")
