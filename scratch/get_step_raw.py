import sys

sys.stdout.reconfigure(encoding='utf-8')
log_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if '"step_index": 5145' in line:
            print(f"Line {idx} matches step 5145!")
            # Let's write the line to a scratch text file to examine it or parse it
            with open(r'C:\Users\m3615\samosbor_game\scratch\step_5145.json', 'w', encoding='utf-8') as outf:
                outf.write(line)
            print("Wrote to step_5145.json")
