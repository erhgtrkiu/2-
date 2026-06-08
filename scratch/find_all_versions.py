import os
from datetime import datetime

directories = [
    r"C:\Users\m3615\samosbor_game",
    r"C:\Users\m3615\samosbor_game\scratch",
    r"C:\Users\m3615\OneDrive\Desktop",
    r"C:\Users\m3615\OneDrive\Desktop\ssss",
    r"C:\Users\m3615\OneDrive\Desktop\ы",
    r"C:\Users\m3615\OneDrive\Desktop\a",
    r"C:\Users\m3615",
]

found_files = []

for d in directories:
    if not os.path.exists(d):
        continue
    # List files in the directory (non-recursively for deep directories like C:\Users\m3615)
    try:
        for filename in os.listdir(d):
            if filename.lower().startswith("app") and filename.lower().endswith(".js"):
                filepath = os.path.join(d, filename)
                stat = os.stat(filepath)
                mtime = datetime.fromtimestamp(stat.st_mtime).isoformat()
                found_files.append((filepath, stat.st_size, mtime))
            elif filename.lower().startswith("index") and filename.lower().endswith(".html"):
                filepath = os.path.join(d, filename)
                stat = os.stat(filepath)
                mtime = datetime.fromtimestamp(stat.st_mtime).isoformat()
                found_files.append((filepath, stat.st_size, mtime))
    except Exception as e:
        print(f"Error reading {d}: {e}")

# Sort by modification time descending
found_files = sorted(found_files, key=lambda x: x[2], reverse=True)

for path, size, mtime in found_files:
    print(f"Path: {path}\n  Size: {size} bytes\n  Modified: {mtime}\n")
