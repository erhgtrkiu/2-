import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    with open(r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            if 'РАПОРТ. Ликвидатор' in line or 'Блок 1290' in line:
                print(f"Found match at line {idx}, length={len(line)}")
                # Let's save this entire line to a file
                with open(f'scratch/raw_line_{idx}.txt', 'w', encoding='utf-8') as out:
                    out.write(line)
                print(f"Saved line {idx} to scratch/raw_line_{idx}.txt")
except Exception as e:
    print("Error:", e)
