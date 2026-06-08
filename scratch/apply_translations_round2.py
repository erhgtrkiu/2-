import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
print("Starting translations application script (Round 2)...")

RU_KEYS = """
        "true_ending_terminal_1": "> ДЕКОМПИЛЯЦИЯ КОШМАРА... ОК.",
        "true_ending_terminal_2": "> ПОДКЛЮЧЕНИЕ К РЕАЛЬНОМУ МИРУ... ОК.",
        "true_ending_terminal_3": "> ВОЗДУХ: ЧИСТЫЙ, ТРАВА: ЗЕЛЕНАЯ, НЕБО: СИНЕЕ.",
        "true_ending_terminal_4": "> ЗАДАЧА: СНОВА СДЕЛАЙТЕ СВОЙ ВЫБОР И БУДЬТЕ СВОБОДНЫ.",
        "log_door_locked": "Дверь заблокирована",
        "log_door_rusted_shut": "Ручка не поддается. Гермозатвор заклинен намертво ржавчиной.",
        "log_door_opened_name": "С лязгом замков дверь {0} открылась наружу.",
        "log_door_closed_name": "Вы заперли дверь {0}.",
        "log_inner_door_opened": "Внутренняя гермодверь открылась.",
        "log_inner_door_closed": "Внутренняя гермодверь закрылась.",
        "search_room_title": "ОБЫСК МЕБЕЛИ",
        "search_room_status": "Проверяем полки, перетряхиваем барахло...",
        "log_nest_monster_attack": "УЖАСНЫЙ ШОРОХ! Из шевелящейся слизи в углу на вас бросилась тварь!",
        "search_corpse_title": "ОБЫСК ТЕЛА ЛИКВИДАТОРА",
        "search_corpse_status": "Осматриваем разгрузочный жилет, ищем полезное снаряжение...",
        "log_loot_corpse_reward": "Вы нашли батарейку, патроны (+8) и фильтр противогаза (+40%) на теле ликвидатора."
"""

EN_KEYS = """
        "true_ending_terminal_1": "> DECOMPILING NIGHTMARE... OK.",
        "true_ending_terminal_2": "> CONNECTING TO REAL WORLD... OK.",
        "true_ending_terminal_3": "> AIR: CLEAN, GRASS: GREEN, SKY: BLUE.",
        "true_ending_terminal_4": "> TASK: MAKE YOUR CHOICE AGAIN AND BE FREE.",
        "log_door_locked": "Door is locked",
        "log_door_rusted_shut": "The handle won't budge. The hermetic gate is rusted shut.",
        "log_door_opened_name": "With a clang of locks, door {0} opened outward.",
        "log_door_closed_name": "You closed door {0}.",
        "log_inner_door_opened": "The inner hermetic door opened.",
        "log_inner_door_closed": "The inner hermetic door closed.",
        "search_room_title": "SEARCHING FURNITURE",
        "search_room_status": "Checking shelves, going through junk...",
        "log_nest_monster_attack": "TERRIBLE RUSTLE! From the moving slime in the corner, a beast lunged at you!",
        "search_corpse_title": "SEARCHING LIQUIDATOR'S BODY",
        "search_corpse_status": "Examining tactical vest, searching for useful gear...",
        "log_loot_corpse_reward": "You found a battery, ammo (+8) and a gas mask filter (+40%) on the liquidator's body."
"""

ZH_KEYS = """
        "true_ending_terminal_1": "> 解构梦魇... 成功。",
        "true_ending_terminal_2": "> 连接到真实世界... 成功。",
        "true_ending_terminal_3": "> 空气: 纯净, 青草: 翠绿, 天空: 蔚蓝。",
        "true_ending_terminal_4": "> 任务: 再次做出你的选择，重获自由。",
        "log_door_locked": "门被锁死",
        "log_door_rusted_shut": "门把手纹丝不动。密封防爆门被铁锈焊死。",
        "log_door_opened_name": "伴随着锁具的咔哒声，门 {0} 向外打开。",
        "log_door_closed_name": "你锁上了门 {0}。",
        "log_inner_door_opened": "内侧密封门打开了。",
        "log_inner_door_closed": "内侧密封门关闭了。",
        "search_room_title": "搜寻家具",
        "search_room_status": "正在检查搁板，整理杂物...",
        "log_nest_monster_attack": "可怕的沙沙声！一只怪物从角落里蠕动的粘液中朝你扑来！",
        "search_corpse_title": "搜寻清理人员尸体",
        "search_corpse_status": "正在检查战术背心，搜寻有用装备...",
        "log_loot_corpse_reward": "你在清理人员的尸体上找到了电池、弹药 (+8) 和防毒面具滤毒罐 (+40%)。"
"""

DE_KEYS = """
        "true_ending_terminal_1": "> ALBTRAUM DEKOMPILIEREN... OK.",
        "true_ending_terminal_2": "> VERBINDUNG ZUR REALEN WELT... OK.",
        "true_ending_terminal_3": "> LUFT: REIN, GRAS: GRÜN, HIMMEL: BLAU.",
        "true_ending_terminal_4": "> AUFGABE: TREFFEN SIE ERNEUT IHRE WAHL UND SEIEN SIE FREI.",
        "log_door_locked": "Tür verriegelt",
        "log_door_rusted_shut": "Der Griff lässt sich nicht bewegen. Das hermetische Tor ist verrostet.",
        "log_door_opened_name": "Mit einem Klirren der Schlösser öffnete sich Tür {0} nach außen.",
        "log_door_closed_name": "Sie haben Tür {0} geschlossen.",
        "log_inner_door_opened": "Die innere hermetische Tür öffnete sich.",
        "log_inner_door_closed": "Die innere hermetische Tür schloss sich.",
        "search_room_title": "MÖBEL DURCHSUCHEN",
        "search_room_status": "Regale überprüfen, Müll durchwühlen...",
        "log_nest_monster_attack": "SCHRECKLICHES RASCHELN! Aus dem sich bewegenden Schleim in der Ecke stürzte sich ein Biest auf Sie!",
        "search_corpse_title": "LIQUIDATORLEICHE DURCHSUCHEN",
        "search_corpse_status": "Taktische Weste untersuchen, nach nützlicher Ausrüstung suchen...",
        "log_loot_corpse_reward": "Sie haben eine Batterie, Munition (+8) und einen Gasmaskenfilter (+40%) auf der Leiche des Liquidators gefunden."
"""

IT_KEYS = """
        "true_ending_terminal_1": "> DECOMPILAZIONE INCUBO... OK.",
        "true_ending_terminal_2": "> CONNESSIONE AL MONDO REALE... OK.",
        "true_ending_terminal_3": "> ARIA: PULITA, ERBA: VERDE, CIELO: BLU.",
        "true_ending_terminal_4": "> OBIETTIVO: FAI DI NUOVO LA TUA SCELTA E SII LIBERO.",
        "log_door_locked": "Porta bloccata",
        "log_door_rusted_shut": "La maniglia non si muove. La porta ermetica è arrugginita.",
        "log_door_opened_name": "Con un clangore di serrature, la porta {0} si è aperta verso l'esterno.",
        "log_door_closed_name": "Hai chiuso la porta {0}.",
        "log_inner_door_opened": "La porta ermetica interna si è aperta.",
        "log_inner_door_closed": "La porta ermetica interna si è chiusa.",
        "search_room_title": "RICERCA NEI MOBILI",
        "search_room_status": "Controllando gli scaffali, frugando tra i rifiuti...",
        "log_nest_monster_attack": "TERRIBILE FRUSCIO! Dalla melma in movimento nell'angolo, una bestia si è lanciata su di te!",
        "search_corpse_title": "RICERCA SUL CORPO DEL LIQUIDATORE",
        "search_corpse_status": "Esaminando il gilet tattico, cercando attrezzatura utile...",
        "log_loot_corpse_reward": "Hai trovato una batteria, munizioni (+8) e un filtro per maschera antigas (+40%) sul corpo del liquidatore."
"""

ES_KEYS = """
        "true_ending_terminal_1": "> DECOMPILANDO PESADILLA... OK.",
        "true_ending_terminal_2": "> CONECTANDO AL MUNDO REAL... OK.",
        "true_ending_terminal_3": "> AIRE: LIMPIO, HIERBA: VERDE, CIELO: AZUL.",
        "true_ending_terminal_4": "> TAREA: HAZ TU ELECCIÓN OTRA VEZ Y SÉ LIBRE.",
        "log_door_locked": "Puerta bloqueada",
        "log_door_rusted_shut": "La manija no se mueve. La compuerta hermética está oxidada.",
        "log_door_opened_name": "Con un tintineo de cerraduras, la puerta {0} se abrió hacia afuera.",
        "log_door_closed_name": "Cerraste la puerta {0}.",
        "log_inner_door_opened": "La puerta hermética interna se abrió.",
        "log_inner_door_closed": "La puerta hermética interna se cerró.",
        "search_room_title": "BUSCANDO EN LOS MUEBLES",
        "search_room_status": "Revisando estantes, hurgando en la basura...",
        "log_nest_monster_attack": "¡RUGIDO TERRIBLE! ¡Desde el limo en movimiento en la esquina, una bestia se lanzó sobre ti!",
        "search_corpse_title": "BUSCANDO EN EL CUERPO DEL LIQUIDADOR",
        "search_corpse_status": "Examinando el chaleco táctico, buscando equipo útil...",
        "log_loot_corpse_reward": "Encontraste una batería, munición (+8) y un filtro de máscara de gas (+40%) en el cuerpo del liquidador."
"""

with open('app.js', 'r', encoding='utf-8') as f:
    content = f.read()

def inject_keys(content, target_key, new_keys_str):
    pattern = re.escape(target_key) + r'\s*:\s*".*?"'
    match = re.search(pattern, content)
    if not match:
        print(f"Warning: could not find target key {target_key} in content!")
        return content
    full_match = match.group(0)
    replacement = full_match + ",\n" + new_keys_str.strip()
    return content.replace(full_match, replacement, 1)

print("Injecting Round 2 localization keys...")
content = inject_keys(content, '"log_prefix_sys"', RU_KEYS)
content = inject_keys(content, '"log_prefix_sys"', EN_KEYS)
content = inject_keys(content, '"log_prefix_sys"', ZH_KEYS)
content = inject_keys(content, '"log_prefix_sys"', DE_KEYS)
content = inject_keys(content, '"log_prefix_sys"', IT_KEYS)
content = inject_keys(content, '"log_prefix_sys"', ES_KEYS)

print("Replacing remaining hardcoded strings in code logic...")
# openDoor locked
content = content.replace('logToConsole("Дверь заблокирована", "danger");', 'logToConsole(t("log_door_locked"), "danger");')
# openDoor rusted shut
content = content.replace('logToConsole("Ручка не поддается. Гермозатвор заклинен намертво ржавчиной.", "warn");', 'logToConsole(t("log_door_rusted_shut"), "warn");')
# openDoor success
content = content.replace('logToConsole(`С лязгом замков дверь ${door.name} открылась наружу.`, "action");', 'logToConsole(t("log_door_opened_name", door.name), "action");')
# closeDoor
content = content.replace('logToConsole(`Вы заперли дверь ${door.name}.`, "sys");', 'logToConsole(t("log_door_closed_name", door.name), "sys");')
# toggleInnerDoor
content = content.replace('logToConsole(door.innerOpened ? "Внутренняя гермодверь открылась." : "Внутренняя гермодверь закрылась.", "action");', 'logToConsole(door.innerOpened ? t("log_inner_door_opened") : t("log_inner_door_closed"), "action");')

# searchRoom UI
content = content.replace('title.innerText = "ОБЫСК МЕБЕЛИ";\n    status.innerText = "Проверяем полки, перетряхиваем барахло...";', 'title.innerText = t("search_room_title");\n    status.innerText = t("search_room_status");')
# searchRoom nest trigger
content = content.replace('logToConsole("УЖАСНЫЙ ШОРОХ! Из шевелящейся слизи в углу на вас бросилась тварь!", "danger");', 'logToConsole(t("log_nest_monster_attack"), "danger");')

# searchDeadLiquidator UI
content = content.replace('title.innerText = "ОБЫСК ТЕЛА ЛИКВИДАТОРА";\n    status.innerText = "Осматриваем разгрузочный жилет, ищем полезное снаряжение...";', 'title.innerText = t("search_corpse_title");\n    status.innerText = t("search_corpse_status");')
# searchDeadLiquidator reward log
content = content.replace('logToConsole("[НАХОДКА] Вы нашли батарейку, патроны (+8) и фильтр противогаза (+40%) на теле ликвидатора.", "loot");', 'logToConsole(t("log_loot_corpse_reward"), "loot");')

# showSubtitle hacker tools
content = content.replace('showSubtitle("Получается, вы и делаете самосборы и управляете всей хрущёвкой");', 'showSubtitle(t("sub_hacker_1"));')
content = content.replace('showSubtitle("Я ненавижу вас, вы твари!");', 'showSubtitle(t("sub_hacker_2"));')
content = content.replace('showSubtitle("СИС: Вы умрёте, а никто о вас даже не вспомнит. Мучительной смерти!");', 'showSubtitle(t("sub_hacker_3"));')

# btnDescend text in transition
content = content.replace("btnDescend.innerHTML = 'Застыть на месте и ждать';", "btnDescend.innerText = t('btn_descend_ending');")
content = content.replace("btnDescend.innerHTML = 'Идите на лестницу в конце коридора';", "btnDescend.innerText = t('btn_descend_default');")

# enableMenuWakeupTheme terminal texts
content = content.replace('`\n            <p class="blink-cursor">> ДЕКОМПИЛЯЦИЯ КОШМАРА... ОК.</p>\n            <p>> ПОДКЛЮЧЕНИЕ К РЕАЛЬНОМУ МИРУ... ОК.</p>\n            <p>> ВОЗДУХ: ЧИСТЫЙ, ТРАВА: ЗЕЛЕНАЯ, НЕБО: СИНЕЕ.</p>\n            <p class="glow-green">> ЗАДАЧА: СНОВА СДЕЛАЙТЕ СВОЙ ВЫБОР И БУДЬТЕ СВОБОДНЫ.</p>\n        `', '`\n            <p class="blink-cursor">` + t("true_ending_terminal_1") + `</p>\n            <p>` + t("true_ending_terminal_2") + `</p>\n            <p>` + t("true_ending_terminal_3") + `</p>\n            <p class="glow-green">` + t("true_ending_terminal_4") + `</p>\n        `')

# disableMenuWakeupTheme terminal texts
content = content.replace('`\n            <p class="blink-cursor">> ИНИЦИАЛИЗАЦИЯ ИНТЕРФЕЙСА ЛИКВИДАТОРА...</p>\n            <p>> ПОДКЛЮЧЕНИЕ К СЕТИ ГИГАХРУЩЕВКИ... ОК.</p>\n            <p>> СНАРЯЖЕНИЕ: ПИСТОЛЕТ (24), ПРОТИВОГАЗ, ВОДА, СУМКА.</p>\n            <p class="glow-green">> ЗАДАЧА: СПУСТИТЬСЯ НА 1-Й ЭТАЖ И ВЫЖИТЬ.</p>\n        `', '`\n            <p class="blink-cursor">` + t("init_interface") + `</p>\n            <p>` + t("network_ok") + `</p>\n            <p>` + t("equipment_info") + `</p>\n            <p class="glow-green">` + t("mission_info") + `</p>\n        `')

# Let's save app.js
with open('app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Round 2 finished applying translations and bindings successfully!")
