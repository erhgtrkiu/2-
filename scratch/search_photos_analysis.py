with open('C:/Users/m3615/samosbor_game/scratch/photos_analysis.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'=== STEP \d+ \((.*?)\) ===\nTHINKING:\n(.*?)(?=== STEP |\Z)', text, re.DOTALL)
for m in matches:
    step_type = m.group(1)
    thinking = m.group(2)
    if any(w in thinking.lower() for w in ['stairs', 'door', 'закрыт', 'лестн', 'не то', 'wrong', 'shaft']):
        print(f"=== {step_type} ===")
        print(thinking.strip()[:1000])
        print("="*60)
