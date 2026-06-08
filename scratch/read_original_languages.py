import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    with open('scratch/app_original.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Let's search for LANGUAGES in app_original.js
    # We want to find the 'ru' language section and particularly all 'note_' keys.
    # Let's extract the 'ru' section of LANGUAGES.
    # It probably looks like: ru: { ... } or 'ru': { ... }
    ru_match = re.search(r"['\"]ru['\"]\s*:\s*\{(.*?)\}", content, re.DOTALL)
    if ru_match:
        ru_text = ru_match.group(1)
        print("Found 'ru' block in LANGUAGES:")
        # Find all keys starting with note_
        for m in re.finditer(r"['\"](note_\d+_(title|content))['\"]\s*:\s*['\"](.*?)['\"]", ru_text):
            print(f"'{m.group(1)}': {repr(m.group(3))},")
    else:
        print("Could not find 'ru' block in LANGUAGES. Let's look for note_ keys anywhere in app_original.js:")
        for m in re.finditer(r"['\"](note_\d+_(title|content))['\"]\s*:\s*['\"](.*?)['\"]", content):
            print(f"'{m.group(1)}': {repr(m.group(3))}")
except Exception as e:
    print("Error:", e)
