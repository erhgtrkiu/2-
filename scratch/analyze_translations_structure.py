with open("scratch/build_translations.py", encoding="utf-8") as f:
    content = f.read()

print("Total characters:", len(content))
lines = content.splitlines()
print("Total lines:", len(lines))

for i, line in enumerate(lines):
    if not line.startswith(" ") and not line.startswith("    ") and not line.startswith("\"") and not line.startswith("{") and not line.startswith("}"):
        if len(line.strip()) > 0:
            print(f"Line {i+1}: {line}")
