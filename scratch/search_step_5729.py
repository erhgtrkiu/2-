with open('C:/Users/m3615/samosbor_game/scratch/step_5729_details.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'=== STEP \d+ \(PLANNER_RESPONSE\) ===\nTHINKING:\n(.*?)(?=== STEP |\Z)', text, re.DOTALL)
for m in matches:
    thinking = m.group(1)
    if any(w in thinking.lower() for w in ['stairs', 'door', 'закрыт', 'лестн', 'не то', 'право', 'лево', 'wrong']):
        print(thinking.strip()[:1000])
        print("="*60)
