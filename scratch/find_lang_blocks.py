import re

with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines[:1600]):
    if re.search(r'^\s*"(ru|en|zh|de|it|es)":\s*\{', line):
        print(f"{idx+1}: {line.strip()}")
