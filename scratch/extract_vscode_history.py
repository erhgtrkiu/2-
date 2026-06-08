import os
import json
import glob
import shutil
from datetime import datetime

history_dir = r'C:\Users\m3615\AppData\Roaming\Code\User\History'
entries_files = glob.glob(os.path.join(history_dir, '*', 'entries.json'))

appjs_versions = []

for entries_file in entries_files:
    try:
        with open(entries_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Check if this history entry is for app.js
        resource = data.get('resource', '')
        if 'samosbor_game' in resource and 'app.js' in resource:
            folder_path = os.path.dirname(entries_file)
            for entry in data.get('entries', []):
                file_id = entry.get('id')
                timestamp = entry.get('timestamp')
                source = entry.get('source', 'unknown')
                
                # The actual file is saved as the 'id'
                version_path = os.path.join(folder_path, file_id)
                if os.path.exists(version_path):
                    size = os.path.getsize(version_path)
                    appjs_versions.append({
                        'path': version_path,
                        'timestamp': timestamp,
                        'size': size,
                        'source': source
                    })
    except Exception as e:
        pass

# Sort versions by timestamp descending
appjs_versions.sort(key=lambda x: x['timestamp'], reverse=True)

print(f"Found {len(appjs_versions)} versions of app.js in VS Code history.")
for i, v in enumerate(appjs_versions[:20]):
    dt = datetime.fromtimestamp(v['timestamp'] / 1000.0)
    print(f"{i+1}. Time: {dt.isoformat()}, Size: {v['size']}, Source: {v['source']}, Path: {v['path']}")

# Let's save the top 5 largest/most recent to scratch for review
out_dir = r'C:\Users\m3615\samosbor_game\scratch\vscode_backups'
os.makedirs(out_dir, exist_ok=True)
for i, v in enumerate(appjs_versions[:10]):
    dest = os.path.join(out_dir, f"app_backup_{i+1}_{v['size']}b.js")
    shutil.copy(v['path'], dest)
    
print(f"Copied top backups to {out_dir}")
