import re

with open('C:/Users/m3615/samosbor_game/scratch/photos_analysis.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# find all occurrences of "фото" or "photo" or "void" or "stairs" and print their steps/thinking
pattern = re.compile(r'(фото|photo|void|stairs|shaft)', re.IGNORECASE)

# split by "=== STEP"
steps = text.split('=== STEP')
results = []

for step in steps:
    if not step.strip():
        continue
    step_header = step.split('===')[0].strip()
    # check if any keyword is in this step
    matches = pattern.findall(step)
    if matches:
        # extract thinking block
        thinking = ""
        if "THINKING:" in step:
            thinking = step.split("THINKING:")[1].split("CONTENT:")[0].split("========================================")[0].strip()
        
        # let's look for specific discussion about staircase, void, shaft, etc.
        if any(k in thinking.lower() for k in ['stairs', 'shaft', 'void', 'пустот', 'ceiling', 'потолок', 'стен']):
            results.append(f"=== STEP {step_header} ===\nTHINKING:\n{thinking}\n")

with open('C:/Users/m3615/samosbor_game/scratch/filtered_thinking.txt', 'w', encoding='utf-8') as out:
    out.write("\n\n".join(results[:50]))

print("Done filtering thinking.")
