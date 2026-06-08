import subprocess
import os

path = r'C:\Users\m3615\samosbor_game\scratch\app_reconstructed.js'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: duplicate doorLights/playerFlashlight declarations
duplicate_block = """//   
let doorLights = [];
let playerFlashlight = null;

//   
let doorLights = {};"""

# Let's search for this pattern and replace it
if duplicate_block in content:
    content = content.replace(duplicate_block, """// Глобальные переменные света
let doorLights = {};""")
    print("Fixed duplicate doorLights declarations.")
else:
    # Also check if it's there with different comments
    # Let's replace the first let doorLights = [];
    content = content.replace("let doorLights = [];\nlet playerFlashlight = null;", "")
    print("Fixed duplicate doorLights/playerFlashlight via fallback.")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

def run_syntax_check():
    res = subprocess.run(['node', '--check', path], capture_output=True, text=True, encoding='utf-8')
    return res.returncode, res.stdout, res.stderr

code, stdout, stderr = run_syntax_check()
print("Syntax check exit code:", code)
if stderr:
    print("Stderr:\n", stderr)
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
    print("SUCCESS: No more syntax errors!")
