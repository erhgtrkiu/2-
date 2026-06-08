import os

def check_dir(dir_path):
    if not os.path.exists(dir_path):
        return []
    print(f"Searching in {dir_path}...")
    matches = []
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    if 'cutsceneActive' in content:
                        mtime = os.path.getmtime(path)
                        matches.append((path, len(content), mtime))
            except Exception:
                pass
    return matches

def main():
    paths_to_check = [
        os.path.expandvars(r'%APPDATA%\Code\User\History'),
        os.path.expandvars(r'%APPDATA%\Cursor\User\History'),
        os.path.expandvars(r'%APPDATA%\VSCodium\User\History'),
        os.path.expandvars(r'%USERPROFILE%\.cursor\User\History'),
        os.path.expandvars(r'%USERPROFILE%\.vscode\User\History'),
    ]
    
    all_matches = []
    for p in paths_to_check:
        all_matches.extend(check_dir(p))
        
    all_matches.sort(key=lambda x: x[2], reverse=True)
    
    print(f"Found {len(all_matches)} matching files:")
    for path, size, mtime in all_matches[:30]:
        import datetime
        dt = datetime.datetime.fromtimestamp(mtime)
        print(f"  - {path} (Size: {size}, Time: {dt})")

if __name__ == '__main__':
    main()
