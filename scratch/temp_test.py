import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx in range(429, min(len(lines), 480)):
    print(f"Line {idx+1}: {lines[idx].strip()}")
