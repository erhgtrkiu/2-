import json
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    transcript_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'
    
    steps_to_inspect = [5235, 5716, 6538, 6804, 8038, 8147, 8209]
    
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
            except Exception:
                continue
            step_index = data.get('step_index')
            if step_index in steps_to_inspect:
                print(f"=== Step {step_index} ===")
                tool_calls = data.get('tool_calls', [])
                for tc in tool_calls:
                    args = tc.get('args', {})
                    chunks = args.get('ReplacementChunks', '')
                    print(f"Chunks type: {type(chunks)}")
                    if isinstance(chunks, str):
                        print(f"Raw string length: {len(chunks)}")
                        # Print first 200 and last 200 chars
                        print(f"Start: {repr(chunks[:200])}")
                        print(f"End: {repr(chunks[-200:])}")
                    else:
                        print(f"Chunks is not a string (parsed as list/dict). Length = {len(chunks)}")

if __name__ == '__main__':
    main()
