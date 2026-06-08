import json

with open(r'C:\Users\m3615\samosbor_game\scratch\step_5018_chunks.txt', 'r', encoding='utf-8') as f:
    content = f.read()

print("Content length:", len(content))
try:
    json.loads(content)
    print("Parsed successfully with json.loads!")
except Exception as e:
    print("json.loads failed:", e)
    # Let's inspect the character at the error position
    import re
    m = re.search(r'char (\d+)', str(e))
    if m:
        pos = int(m.group(1))
        print(f"Error at char {pos}")
        start = max(0, pos - 50)
        end = min(len(content), pos + 50)
        print("Context around error:")
        print("Index:", list(range(start, end)))
        print("Chars:", [content[i] for i in range(start, end)])
        print("String repr:", repr(content[start:end]))
        print(f"Char at error: {repr(content[pos])}")
