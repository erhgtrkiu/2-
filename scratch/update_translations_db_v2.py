import re

path = r'C:\Users\m3615\samosbor_game\scratch\build_translations.py'

with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

new_keys = {
    "ru": {
        "log_hack_blocked": "СИС: ДОСТУП ЗАБЛОКИРОВАН.",
        "log_samosbor_warn_1": "[!] ВНИМАНИЕ: Датчики зафиксировали приближение волны Самосбора!",
        "log_samosbor_warn_2": "[!] До активной фазы: ~20 секунд. Найдите укрытие!"
    },
    "en": {
        "log_hack_blocked": "SIS: ACCESS BLOCKED.",
        "log_samosbor_warn_1": "[!] WARNING: Sensors detected an approaching Samosbor wave!",
        "log_samosbor_warn_2": "[!] Active phase in: ~20 seconds. Find shelter!"
    },
    "zh": {
        "log_hack_blocked": "系统（SIS）：访问被拒绝。",
        "log_samosbor_warn_1": "[!] 警告：传感器检测到萨摩斯波尔波逼近！",
        "log_samosbor_warn_2": "[!] 距离活性期：~20 秒。请寻找掩体！"
    },
    "de": {
        "log_hack_blocked": "SIS: ZUGRIFF BLOCKIERT.",
        "log_samosbor_warn_1": "[!] WARNUNG: Sensoren haben eine sich nähernde Samosbor-Welle erkannt!",
        "log_samosbor_warn_2": "[!] Bis zur aktiven Phase: ~20 Sekunden. Suchen Sie Schutz!"
    },
    "it": {
        "log_hack_blocked": "SIS: ACCESSO BLOCCATO.",
        "log_samosbor_warn_1": "[!] ATTENZIONE: I sensori hanno rilevato un'onda di Samosbor in avvicinamento!",
        "log_samosbor_warn_2": "[!] Fino alla fase attiva: ~20 secondi. Trovate un riparo!"
    },
    "es": {
        "log_hack_blocked": "SIS: ACCESO BLOQUEADO.",
        "log_samosbor_warn_1": "[!] ADVERTENCIA: ¡Los sensores detectaron una ola de Samosbor acercándose!",
        "log_samosbor_warn_2": "[!] Hasta la fase activa: ~20 segundos. ¡Busquen refugio!"
    }
}

for lang, kv_pairs in new_keys.items():
    pattern = rf'"{lang}":\s*\{{(.*?)\n\s*\}}'
    match = re.search(pattern, code, re.DOTALL)
    if match:
        body = match.group(1)
        if "log_hack_blocked" not in body:
            added_lines = ""
            for k, v in kv_pairs.items():
                escaped_v = v.replace('"', '\\"')
                added_lines += f',\n        "{k}": "{escaped_v}"'
            new_body = body + added_lines
            old_str = f'"{lang}": {{{body}\n    }}'
            new_str = f'"{lang}": {{{new_body}\n    }}'
            code = code.replace(old_str, new_str)
            print(f"Added extra keys to {lang}.")
        else:
            print(f"Extra keys already in {lang}.")
    else:
        print(f"Could not find dictionary block for {lang}.")

with open(path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Translations update finished.")
