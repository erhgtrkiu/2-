import os

root_dir = r'C:\Users\m3615'
for root, dirs, files in os.walk(root_dir):
    # Skip standard directories to avoid walking too deep
    for skip in ['.gemini', 'AppData', 'Downloads', 'Documents', 'Pictures', 'Desktop', 'Music', 'Videos', 'Searches', 'Links', 'Contacts', 'Saved Games', '3D Objects']:
        if skip in dirs:
            dirs.remove(skip)
            
    for file in files:
        if 'app' in file.lower() and file.endswith('.js'):
            path = os.path.join(root, file)
            try:
                size = os.path.getsize(path)
                print(f"Found JS file: {path} (size: {size} bytes)")
            except Exception:
                pass
