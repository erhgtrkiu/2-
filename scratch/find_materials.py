import re

with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

standard_regex = re.compile(r'new THREE\.MeshStandardMaterial')
basic_regex = re.compile(r'new THREE\.MeshBasicMaterial')

for idx, line in enumerate(lines):
    if standard_regex.search(line) or basic_regex.search(line):
        print(f"{idx+1}: {line.strip()}")
