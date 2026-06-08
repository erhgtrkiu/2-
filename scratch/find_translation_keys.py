import sys
sys.path.append(r'C:\Users\m3615\samosbor_game\scratch')
import build_translations

ru_keys = build_translations.LANGUAGES['ru']
print("Russian keys containing ending/ach/hacker/dialogue/cutscene:")
for k, v in ru_keys.items():
    if any(x in k.lower() for x in ['ending', 'ach', 'hacker', 'dialogue', 'cutscene', 'siren', 'samosbor', 'subtitle']):
        print(f"  {k}: {v}")
