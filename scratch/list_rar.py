import zipfile
import sys
import subprocess
import json

# Since it is a RAR archive, zipfile won't work. We need to run 7z l and parse the output in python.
sys.stdout.reconfigure(encoding='utf-8')

extractor = r"C:\Program Files\7-Zip\7z.exe"
rar_path = r"C:\Users\m3615\samosbor_game.rar"

res = subprocess.run([extractor, "l", rar_path], capture_output=True, text=True, errors='ignore')

# Parse stdout
lines = res.stdout.split('\n')
for l in lines:
    if 'samosbor_game\\' in l:
        # Check if it is a python file, css, html or text file (i.e. not chrome profile)
        parts = l.split(None, 5)
        if len(parts) >= 6:
            filepath = parts[-1].strip()
            # We don't want chrome_profile files
            if 'chrome_profile' not in filepath:
                print(filepath)
