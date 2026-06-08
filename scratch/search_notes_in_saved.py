import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for fn in sorted(os.listdir('scratch')):
    if fn.startswith('found_content_') and fn.endswith('.txt'):
        path = os.path.join('scratch', fn)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            # print matches of note_\d+_content or similar
            # or LORE_NOTES
            if 'note_3_content' in content or 'note_4_content' in content:
                print(f"File {fn}: has note_3_content/note_4_content")
                # print matches of note_3_content and note_4_content
                for m in re.finditer(r"['\"](note_\d+_(title|content))['\"]\s*:\s*['\"](.*?)['\"]", content):
                    print(f"  {m.group(1)}: {m.group(3)[:100]}...")
            if 'const LORE_NOTES' in content:
                print(f"File {fn}: has const LORE_NOTES")
                # print around const LORE_NOTES
                idx = content.find('const LORE_NOTES')
                print(content[idx:idx+800])
        except Exception as e:
            print("Error in", fn, ":", e)
