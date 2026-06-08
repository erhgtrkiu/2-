import sys
sys.path.append(r'C:\Users\m3615\samosbor_game\scratch')
import build_translations

sys.stdout.reconfigure(encoding='utf-8')

for lang in ['ru', 'en']:
    print(f"--- {lang.upper()} ---")
    lang_keys = build_translations.LANGUAGES[lang]
    for k, v in lang_keys.items():
        if 'ending3' in k.lower() or 'truth_dead' in k.lower() or 'go_ending3' in k.lower() or 'sub_' in k.lower() or 'hacker' in k.lower():
            print(f"  {k}: {v}")
