import re

path = r'C:\Users\m3615\samosbor_game\scratch\build_translations.py'

with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

# Define the new keys to inject for each language
new_keys = {
    "ru": {
        "go_ending3_title": "ОСОЗНАЛ, НО УМЕР",
        "go_ending3_desc": "<p>Вы попытались узнать правду, скрытую за гермодверью.</p><p>За это СИС организовала персональный Самосбор.</p><p>Вас больше нет. И никто о вас даже не вспомнит.</p>",
        "ach_truth_dead_title": "Понять правду, но поплатиться за неё жизнью",
        "ach_truth_dead_desc": "Попытаться взломать гермодверь на спавне и узнать правду от СИС.",
        "go_badge_ending3": "Секретная концовка",
        "hacker_warn": "У меня нет дешифратора гермозатворов",
        "sub_hacker_1": "Получается, вы и делаете самосборы и управляете всей хрущёвкой",
        "sub_hacker_2": "Я ненавижу вас, вы твари!",
        "sub_hacker_3": "СИС: Вы умрёте, а никто о вас даже не вспомнит. Мучительной смерти!",
        "sens_slider_label": "ЧУВСТВИТЕЛЬНОСТЬ МЫШИ"
    },
    "en": {
        "go_ending3_title": "REALISED, BUT DIED",
        "go_ending3_desc": "<p>You tried to find the truth hidden behind the blast door.</p><p>For this, the SIS organized a personal Samosbor.</p><p>You are no more. And no one will even remember you.</p>",
        "ach_truth_dead_title": "Find the truth, but pay with your life",
        "ach_truth_dead_desc": "Try to hack the spawn door and learn the truth from the SIS.",
        "go_badge_ending3": "Secret Ending",
        "hacker_warn": "I don't have a gate decrypter",
        "sub_hacker_1": "So you are the ones making Samosbors and controlling the whole Gigahrush",
        "sub_hacker_2": "I hate you, you bastards!",
        "sub_hacker_3": "SIS: You will die, and no one will even remember you. Have a painful death!",
        "sens_slider_label": "MOUSE SENSITIVITY"
    },
    "zh": {
        "go_ending3_title": "大白于天下，但死亡",
        "go_ending3_desc": "<p>你试图寻找隐藏在防爆门后面的真相。</p><p>为此，系统（SIS）组织了一次针对你的个人萨摩斯波尔。</p><p>你已不复存在。没有人会记得你。</p>",
        "ach_truth_dead_title": "寻找真相，但付出生命代价",
        "ach_truth_dead_desc": "尝试入侵出生点大门并从系统（SIS）处得知真相。",
        "go_badge_ending3": "秘密结局",
        "hacker_warn": "我没有大门解码器",
        "sub_hacker_1": "原来是你们制造了萨摩斯波尔并控制了整个赫鲁晓夫楼",
        "sub_hacker_2": "我恨你们，你们这些畜生！",
        "sub_hacker_3": "系统（SIS）：你会死，而且没有人会记得你。痛苦地死吧！",
        "sens_slider_label": "鼠标灵敏度"
    },
    "de": {
        "go_ending3_title": "ERKANNT, ABER GESTORBEN",
        "go_ending3_desc": "<p>Du hast versucht, die Wahrheit hinter dem Schutzschott herauszufinden.</p><p>Dafür hat das SIS einen persönlichen Samosbor organisiert.</p><p>Du bist nicht mehr. Und niemand wird sich an dich erinnern.</p>",
        "ach_truth_dead_title": "Finde die Wahrheit, bezahle mit dem Leben",
        "ach_truth_dead_desc": "Versuche, das Startschott zu hacken und erfahre die Wahrheit vom SIS.",
        "go_badge_ending3": "Geheimes Ende",
        "hacker_warn": "Ich habe keinen Dekodierer für Schutzschotte",
        "sub_hacker_1": "Ihr seid also diejenigen, die die Samosbors veranstalten und den gesamten Gigachruschtschow kontrollieren",
        "sub_hacker_2": "Ich hasse euch, ihr Ungeheuer!",
        "sub_hacker_3": "SIS: Du wirst sterben und niemand wird sich an dich erinnern. Stirb qualvoll!",
        "sens_slider_label": "MAUSEMPFINDLICHKEIT"
    },
    "it": {
        "go_ending3_title": "REALIZZATO, MA MORTO",
        "go_ending3_desc": "<p>Hai provato a scoprire la verità nascosta dietro il portellone blindato.</p><p>Per questo, il SIS ha organizzato un Samosbor personale.</p><p>Non ci sei più. E nessuno si ricorderà di te.</p>",
        "ach_truth_dead_title": "Trova la verità, paga con la vita",
        "ach_truth_dead_desc": "Prova ad hackerare la porta blindata iniziale e impara la verità dal SIS.",
        "go_badge_ending3": "Finale Segreto",
        "hacker_warn": "Non ho il decrittatore per le porte blindate",
        "sub_hacker_1": "Quindi siete voi a causare i Samosbor e a controllare l'intero Gigachruscev",
        "sub_hacker_2": "Vi odio, bastardi!",
        "sub_hacker_3": "SIS: Morirai e nessuno si ricorderà di te. Fai una morte dolorosa!",
        "sens_slider_label": "SENSIBILITÀ MOUSE"
    },
    "es": {
        "go_ending3_title": "CONSCIENTE, PERO MUERTO",
        "go_ending3_desc": "<p>Intentaste buscar la verdad oculta detrás de la puerta blindada.</p><p>Por esto, el SIS organizó un Samosbor personal.</p><p>Ya no existes. Y nadie te recordará.</p>",
        "ach_truth_dead_title": "Encuentra la verdad, paga con tu vida",
        "ach_truth_dead_desc": "Intenta hackear la puerta blindada inicial y averigua la verdad del SIS.",
        "go_badge_ending3": "Final Secreto",
        "hacker_warn": "No tengo un decodificador de puertas blindadas",
        "sub_hacker_1": "Así que ustedes son los que hacen los Samosbors y controlan todo el Gigahrush",
        "sub_hacker_2": "¡Los odio, monstruos!",
        "sub_hacker_3": "SIS: Morirás y nadie te recordará. ¡Ten una muerte dolorosa!",
        "sens_slider_label": "SENSIBILIDAD DE RATÓN"
    }
}

# For each language, find its dictionary block in the script and insert the new keys at the end.
# We can search for '"language_code": {' or 'LANGUAGES = {' and then find the closing bracket
# Or just insert them by modifying the code string programmatically.
# Let's locate the language blocks:
# "ru": {
#     ...
# },
# In python dict format:
#     "ru": {
#         "menu_title": "С А М О С Б О Р",
#         ...
#     },

for lang, kv_pairs in new_keys.items():
    pattern = rf'"{lang}":\s*\{{(.*?)\n\s*\}}'
    match = re.search(pattern, code, re.DOTALL)
    if match:
        body = match.group(1)
        # Check if they are already there
        if "go_ending3_title" not in body:
            # Format the new entries to add
            added_lines = ""
            for k, v in kv_pairs.items():
                # Escape quotes inside value
                escaped_v = v.replace('"', '\\"')
                added_lines += f',\n        "{k}": "{escaped_v}"'
            # Insert before the end of the body
            new_body = body + added_lines
            # Replace in code
            old_str = f'"{lang}": {{{body}\n    }}'
            new_str = f'"{lang}": {{{new_body}\n    }}'
            code = code.replace(old_str, new_str)
            print(f"Added keys to {lang}.")
        else:
            print(f"Keys already in {lang}.")
    else:
        print(f"Could not find dictionary block for {lang}.")

with open(path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Translations update finished.")
