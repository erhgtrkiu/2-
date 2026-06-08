import subprocess
import os

path = r'C:\Users\m3615\samosbor_game\scratch\app_reconstructed.js'

def run_syntax_check():
    res = subprocess.run(['node', '--check', path], capture_output=True, text=True, encoding='utf-8')
    return res.returncode, res.stdout, res.stderr

code, stdout, stderr = run_syntax_check()
print("Exit code:", code)
if stderr:
    print("Stderr:\n", stderr)
    # Let's extract line number
    import re
    m = re.search(r'app_reconstructed\.js:(\d+)', stderr)
    if m:
        line_num = int(m.group(1))
        print(f"Error at line {line_num}:")
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        start = max(0, line_num - 10)
        end = min(len(lines), line_num + 10)
        for idx in range(start, end):
            prefix = "-->" if idx == line_num - 1 else "   "
            print(f"{prefix} {idx+1}: {lines[idx]}", end="")
else:
    print("No syntax errors!")
