import shutil
import os
import subprocess

original = r'C:\Users\m3615\samosbor_game\scratch\app_original.js'
test_file = r'C:\Users\m3615\samosbor_game\scratch\app_test_patch.js'

shutil.copy(original, test_file)
print("Copied original to test_file.")

with open(r'C:\Users\m3615\samosbor_game\scratch\build_translations.py', 'r', encoding='utf-8') as f:
    bt_code = f.read()

# Replace the exact line with double quotes
patched_bt_code = bt_code.replace(
    'app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app.js"))',
    f'app_path = r"{test_file}"'
)

bt_test_script = r'C:\Users\m3615\samosbor_game\scratch\build_translations_test.py'
with open(bt_test_script, 'w', encoding='utf-8') as f:
    f.write(patched_bt_code)

print("Wrote temporary builder script.")

res_run = subprocess.run(['python', bt_test_script], capture_output=True, text=True, encoding='utf-8')
print("Builder run return code:", res_run.returncode)
print("Builder stdout:\n", res_run.stdout)
if res_run.stderr:
    print("Builder stderr:\n", res_run.stderr)

# Now check syntax of test_file
res = subprocess.run(['node', '--check', test_file], capture_output=True, text=True, encoding='utf-8')
print("Syntax check exit code for patched file:", res.returncode)
if res.stderr:
    print("Patched file syntax error:\n", res.stderr)
else:
    print("SUCCESS! Patched file has no syntax errors.")
