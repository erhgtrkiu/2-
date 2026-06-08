keywords = ['stairs', 'staircase', 'ceiling', 'shaftl', 'shafth', 'void', 'пустот', 'shaft']
with open('C:/Users/m3615/samosbor_game/scratch/photos_analysis.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

output_lines = []
for i, line in enumerate(lines):
    line_lower = line.lower()
    if any(k in line_lower for k in keywords):
        # print context (3 lines before and after)
        start = max(0, i - 3)
        end = min(len(lines), i + 4)
        output_lines.append(f"--- Line {i} ---")
        for j in range(start, end):
            output_lines.append(f"{j}: {lines[j].strip()}")
        output_lines.append("")

with open('C:/Users/m3615/samosbor_game/scratch/staircase_search_results.txt', 'w', encoding='utf-8') as out:
    out.write("\n".join(output_lines[:200])) # cap to avoid huge files

print("Done searching staircase in photos analysis.")
