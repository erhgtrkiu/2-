import os

def main():
    path = r'scratch/build_translations.py'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the replacements for LANGUAGES mapping
    replacements = {
        # Russian
        '"log_samosbor_warn_2": "[!] До активной фазы: ~20 секунд. Найдите укрытие!"': 
        '"log_samosbor_warn_2": "[!] До активной фазы: ~20 секунд. Найдите укрытие!",\n        "log_sis_warn_1": "СИС: Что вы делаете? Вы на задании, спуститесь на 1 этаж",\n        "log_sis_warn_2": "СИС: Иван Лорим, перестаньте пытаться взломать дверь",\n        "log_sis_warn_3": "СИС: Последнее предупреждение"',

        # English
        '"log_samosbor_warn_2": "[!] Active phase in: ~20 seconds. Find shelter!"': 
        '"log_samosbor_warn_2": "[!] Active phase in: ~20 seconds. Find shelter!",\n        "log_sis_warn_1": "SIS: What are you doing? You are on a mission, descend to the 1st floor",\n        "log_sis_warn_2": "SIS: Ivan Lorim, stop trying to hack the door",\n        "log_sis_warn_3": "SIS: Last warning"',

        # Chinese
        '"log_samosbor_warn_2": "[!] 距离活性期：~20 秒。请寻找掩体！"': 
        '"log_samosbor_warn_2": "[!] 距离活性期：~20 秒。请寻找掩体！",\n        "log_sis_warn_1": "SIS: 你在干什么？你在执行任务，请降到1楼",\n        "log_sis_warn_2": "SIS: 伊万·洛里姆，停止尝试入侵大门",\n        "log_sis_warn_3": "SIS: 最后警告"',

        # German
        '"log_samosbor_warn_2": "[!] Bis zur aktiven Phase: ~20 Sekunden. Suchen Sie Schutz!"': 
        '"log_samosbor_warn_2": "[!] Bis zur aktiven Phase: ~20 Sekunden. Suchen Sie Schutz!",\n        "log_sis_warn_1": "SIS: Was tun Sie da? Sie sind auf einer Mission, steigen Sie in den 1. Stock ab",\n        "log_sis_warn_2": "SIS: Ivan Lorim, hören Sie auf, die Tür zu hacken",\n        "log_sis_warn_3": "SIS: Letzte Warnung"',

        # Italian
        '"log_samosbor_warn_2": "[!] Fino alla fase attiva: ~20 secondi. Trovate un riparo!"': 
        '"log_samosbor_warn_2": "[!] Fino alla fase attiva: ~20 secondi. Trovate un riparo!",\n        "log_sis_warn_1": "SIS: Cosa stai facendo? Sei in missione, scendi al 1° piano",\n        "log_sis_warn_2": "SIS: Ivan Lorim, smetti di provare ad hackerare la porta",\n        "log_sis_warn_3": "SIS: Ultimo avvertimento"',

        # Spanish
        '"log_samosbor_warn_2": "[!] Hasta la fase activa: ~20 segundos. ¡Busquen refugio!"': 
        '"log_samosbor_warn_2": "[!] Hasta la fase activa: ~20 segundos. ¡Busquen refugio!",\n        "log_sis_warn_1": "SIS: ¿Qué estás haciendo? Estás en una misión, desciende al 1er piso",\n        "log_sis_warn_2": "SIS: Ivan Lorim, deja de intentar hackear la puerta",\n        "log_sis_warn_3": "SIS: Última advertencia"'
    }

    for target, replacement in replacements.items():
        if target in content:
            content = content.replace(target, replacement)
        else:
            print(f"Warning: Target not found: {target}")

    # Add the truth_dead achievement to ACHIEVEMENTS block inside build_translations.py
    # Let's search for "awakened: {" and insert "truth_dead: {" before or after it.
    target_ach = """    awakened: {
        id: "awakened",
        get title() { return t('ach_awakened_title'); },
        get description() { 
            const isUnlocked = ACHIEVEMENTS.awakened ? ACHIEVEMENTS.awakened.unlocked : false;
            return isUnlocked ? t('ach_awakened_desc') : t('ach_secret_desc');
        },
        target: 1,
        unlocked: false,
        progress: 0,
        secret: true
    }"""

    replacement_ach = """    awakened: {
        id: "awakened",
        get title() { return t('ach_awakened_title'); },
        get description() { 
            const isUnlocked = ACHIEVEMENTS.awakened ? ACHIEVEMENTS.awakened.unlocked : false;
            return isUnlocked ? t('ach_awakened_desc') : t('ach_secret_desc');
        },
        target: 1,
        unlocked: false,
        progress: 0,
        secret: true
    },
    truth_dead: {
        id: "truth_dead",
        get title() { return t('ach_truth_dead_title'); },
        get description() { 
            const isUnlocked = ACHIEVEMENTS.truth_dead ? ACHIEVEMENTS.truth_dead.unlocked : false;
            return isUnlocked ? t('ach_truth_dead_desc') : t('ach_secret_desc');
        },
        target: 1,
        unlocked: false,
        progress: 0,
        secret: true
    }"""

    if target_ach in content:
        content = content.replace(target_ach, replacement_ach)
        print("Successfully added truth_dead achievement to build_translations.py")
    else:
        # Try a slightly different spacing/indentation match if needed
        print("Warning: Target achievements block not found in build_translations.py!")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("build_translations.py patched successfully!")

if __name__ == '__main__':
    main()
