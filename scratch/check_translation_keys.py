import sys
sys.path.append(r'C:\Users\m3615\samosbor_game\scratch')
import build_translations

print("Languages:", list(build_translations.LANGUAGES.keys()))
for lang, keys in build_translations.LANGUAGES.items():
    print(f"Language {lang} has {len(keys)} keys.")
    # Check if some specific keys exist
    for key in ['ending_3_title', 'ending_3_desc', 'no_hacker_tool', 'sens_slider_label', 'hacker_warn']:
        print(f"  {key}: {keys.get(key)}")
