import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    with open('scratch/found_content_3138.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Let's find 'const LORE_NOTES = [' and search until '];'
    # Wait, let's write a regex that matches from 'const LORE_NOTES = [' to '];'
    match = re.search(r'const LORE_NOTES = \[(.*?)^\];', content, re.DOTALL | re.MULTILINE)
    if match:
        print("Found LORE_NOTES:")
        print("const LORE_NOTES = [" + match.group(1) + "];")
    else:
        # Let's print the lines that contain 'LORE_NOTES' or lines 1 to 200 of content
        print("LORE_NOTES block not matched by regex. Printing first 100 lines of content:")
        lines = content.split('\n')
        for idx, line in enumerate(lines[:150]):
            print(f"{idx+1}: {line}")
except Exception as e:
    print("Error:", e)
