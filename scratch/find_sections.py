import re

patterns = {
    'init3D': r'function init3D\b',
    'animateMenuNature': r'function animateMenuNature\b',
    'addVolumetricHandle': r'function addVolumetricHandle\b',
    'distributeLoot': r'function distributeLoot\b',
    'executeDevCommand': r'function executeDevCommand\b',
    'PerspectiveCamera': r'new THREE\.PerspectiveCamera\b',
    'shoot': r'function shoot\b',
    'muzzle': r'muzzle',
    'handle': r'addVolumetricHandle',
    'shaft': r'shaftL',
    'lantern': r'stairsLamp'
}

with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for name, pattern in patterns.items():
    print(f"=== Matches for: {name} ===")
    regex = re.compile(pattern)
    for idx, line in enumerate(lines):
        if regex.search(line):
            print(f"{idx+1}: {line.strip()[:100]}")
