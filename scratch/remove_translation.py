import re
import json

with open('app.js', encoding='utf-8') as f:
    content = f.read()

# Extract LANGUAGES['ru']
# We'll use a regex to grab the inside of "ru": { ... }
ru_match = re.search(r'"ru":\s*({.*?\n\s*})', content, re.DOTALL)
if ru_match:
    ru_json_str = ru_match.group(1)
    # The JSON string has some trailing commas or comments maybe?
    # Let's try to parse it with a simple parser or eval.
    # Actually, it's valid JS object, not necessarily strict JSON (keys might not be quoted, though they probably are).
    # Since I wrote it, keys are quoted.
    try:
        # In python, json.loads needs strict JSON.
        ru_dict = json.loads(ru_json_str)
    except:
        # fallback: manual parse
        ru_dict = {}
        for line in ru_json_str.split('\n'):
            m = re.search(r'"([^"]+)":\s*"([^"]+)"', line)
            if m:
                ru_dict[m.group(1)] = m.group(2)
else:
    print("Could not find ru dict")
    exit(1)

# Now find all t('key') or t('key', args) in content
def replace_t(match):
    key = match.group(1)
    args = match.group(2)
    val = ru_dict.get(key, key)
    
    if args:
        # args is something like `, num` or `, door.sector, door.sectorNum`
        # We need to construct a JS template string or concat if there are {0}, {1} in val.
        # However, it's easier to just do it in JS, or we replace {0} with `${num}` etc.
        # Let's check which strings have {0}
        args_list = [a.strip() for a in args.split(',') if a.strip()]
        for i, a in enumerate(args_list):
            val = val.replace(f"{{{i}}}", f"${{{a}}}")
        return f"`{val}`"
    else:
        return f"'{val}'"

# Replace t('key', ...)
# t\('([^']+)'(?:,\s*([^)]+))?\)
new_content = re.sub(r"t\('([^']+)'(?:,\s*([^)]+))?\)", replace_t, content)

# Remove LANGUAGES block
# It starts at const LANGUAGES = { and ends with }; before function t(
new_content = re.sub(r'const\s+LANGUAGES\s*=\s*\{.*?\n};\n+', '', new_content, flags=re.DOTALL)

# Remove function t(key, ...args) { ... }
new_content = re.sub(r'function\s+t\(key,\s*\.\.\.args\)\s*\{.*?\n\}\n+', '', new_content, flags=re.DOTALL)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Translation logic removed successfully.")
