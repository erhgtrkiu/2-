import subprocess

path = r'C:\Users\m3615\samosbor_game\scratch\app_reconstructed.js'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's replace the first duplicate variables block
target = """// ---  :   ---
let hallwayCrawlerMesh = null;
let crawlerHealth = 2;
let deadLiquidatorMesh = null;
let deadLiquidatorSearched = false;
let ghostMesh = null;
let activeHackChannel = 'A';
let targetFrequencies = { A: 0, B: 0, C: 0 };
let hackSuccessCallback = null;
let hackActive = false;"""

if target in content:
    content = content.replace(target, "", 1) # only replace the first occurrence
    print("Removed first duplicate variables block.")
else:
    # Let's try matching with different characters
    import re
    # Match any comment line then hallwayCrawlerMesh up to hackActive
    pattern = r"//[^\n]*\nlet hallwayCrawlerMesh = null;\s*let crawlerHealth = 2;\s*let deadLiquidatorMesh = null;\s*let deadLiquidatorSearched = false;\s*let ghostMesh = null;\s*let activeHackChannel = 'A';\s*let targetFrequencies = \{ A: 0, B: 0, C: 0 \};\s*let hackSuccessCallback = null;\s*let hackActive = false;\s*"
    content, count = re.subn(pattern, "", content, count=1)
    print(f"Replaced pattern {count} times.")

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
