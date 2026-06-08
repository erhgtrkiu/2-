import re

with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

brace_count = 0
found_start = False
for idx, line in enumerate(lines):
    if 'const LANGUAGES =' in line:
        found_start = True
    if found_start:
        brace_count += line.count('{')
        brace_count -= line.count('}')
        if brace_count == 0:
            print(f"LANGUAGES ends at line {idx+1}: {line.strip()}")
            break
