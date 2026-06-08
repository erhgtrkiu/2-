import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    with open('scratch/found_args.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    rep = data.get('ReplacementContent', '')
    with open('scratch/lore_notes_russian.js', 'w', encoding='utf-8') as out:
        out.write(rep)
    print("Successfully wrote scratch/lore_notes_russian.js!")
except Exception as e:
    print("Error:", e)
