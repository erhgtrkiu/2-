import sys
import os
import re
import shutil
import json
import ast

sys.stdout.reconfigure(encoding='utf-8')

print("Starting complete translation application script (V5)...")

# 1. Restore app.js from backup
backup_path = 'scratch/app_backup_before_clean.js'
if os.path.exists(backup_path):
    shutil.copy2(backup_path, 'app.js')
    print("Restored app.js from scratch/app_backup_before_clean.js")
else:
    print("Error: Backup file scratch/app_backup_before_clean.js not found!")
    sys.exit(1)

# 2. Load base LANGUAGES from build_translations.py
sys.path.append('scratch')
from build_translations import LANGUAGES

# 3. Function to extract variables safely using AST
def extract_vars_from_file(filepath):
    res = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    # check if the value is a constant string
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        res[target.id] = node.value.value
    return res

vars1 = extract_vars_from_file('scratch/apply_translations.py')
vars2 = extract_vars_from_file('scratch/apply_translations_round2.py')

def parse_keys_str(keys_str):
    res = {}
    pattern = r'"([a-zA-Z0-9_]+)"\s*:\s*"((?:[^"\\]|\\.)*)"'
    for k, v in re.findall(pattern, keys_str):
        v_clean = v.replace('\\"', '"')
        res[k] = v_clean
    return res

# Custom keys to add (including all the new ones for floor events, crawler sounds, etc.)
CUSTOM_KEYS = {
    "ru": {
        "bag_hacker_yes": "ЕСТЬ",
        "bag_hacker_no": "НЕТ",
        "settings_press_key": "Нажмите клавишу...",
        "log_approach_furniture_warn": "Подойдите к серванту или столу вплотную, чтобы обыскать их.",
        "log_listening_door": "Ликвидатор прислонился к двери {0} и слушает...",
        "listen_sounds_scary": "Скрежет, глухое утробное шипение!",
        "listen_sounds_wind": "Свист воздуха, далекий гул вентиляции",
        "listen_sounds_empty": "Только тяжелое эхо пустых комнат",
        "log_note_found": "[НАХОДКА] Найдена старая записка: \"{0}\"!",
        "log_found_hacker_tool": "[НАХОДКА] Вы нашли ВЗЛОМЩИК ГЕРМОДВЕРЕЙ! Теперь вы можете открывать лестничные затворы.",
        "log_found_battery": "[НАХОДКА] Найдена батарейка для взломщика (+1 шт., всего: {0}).",
        "log_found_water": "[НАХОДКА] Найдена фляга чистой синтезированной воды (+50% запаса).",
        "log_found_ammo": "[НАХОДКА] Найдены пистолетные патроны (+{0} шт.).",
        "log_found_filter": "[НАХОДКА] Найден новый патрон фильтра для противогаза (+50% заряда).",
        "log_found_bandage": "[НАХОДКА] Найден кровоостанавливающий бинт (+1 шт., всего: {0}).",
        "log_found_nothing": "Вы обыскали углы, но нашли лишь серую бетонную пыль (ничего нет).",
        "btn_descend_ending": "Застыть на месте и ждать",
        "btn_descend_default": "Идите на лестницу в конце коридора",
        "log_prefix_action": "[ДЕЙСТ]",
        "go_badge_death": "Смерть",
        "game_title": "Самосбор: Ликвидатор 1324",
        "focus_corpse_title": "ТЕЛО ЛИКВИДАТОРА",
        "focus_corpse_desc": "Погибший ликвидатор в форме. Обыскать подсумки (клавиша R).",
        "focus_corpse_btn": "Обыскать тело",
        "focus_spawn_door_title": "ГЕРМОЗАТВОР СЕКТОРА",
        "focus_spawn_door_desc": "Внешний шлюз сектора. Массивная сталь. Нажмите B для дешифровки.",
        "focus_spawn_door_btn": "Попытаться взломать",
        "focus_stairs_door_title": "ГЕРМОЗАТВОР ЛЕСТНИЦЫ",
        "focus_stairs_door_desc_locked": "Заблокировано центральной системой ГИГАХРУЩА.",
        "focus_stairs_door_btn_try": "Попробовать взломать",
        "focus_stairs_door_desc_open": "Затвор открыт. Проход на лестницу свободен.",
        "focus_stairs_door_btn_close": "Закрыть затвор",
        "focus_stairs_door_desc_closed": "Массивный гермозатвор заперт! Нажмите B для взлома.",
        "focus_stairs_door_btn_hack": "Взломать затвор",
        "focus_door_desc_open": "Дверь открыта. Вы можете зайти внутрь (пройдите WASD).",
        "focus_door_btn_close": "Закрыть дверь",
        "focus_door_desc_closed": "Гермодверь закрыта. Подойдите вплотную.",
        "focus_door_btn_open": "Открыть дверь",
        "focus_object_none": "ОБЪЕКТ НЕ ВЫБРАН",
        "focus_object_desc": "Подойдите к двери или объекту взаимодействия",
        "focus_btn_default": "Взаимодействовать",
        # New translation keys (V5)
        "log_event_flicker": "Свет на этом этаже нестабилен. Энергосеть перегружена.",
        "log_event_gas_leak": "ВНИМАНИЕ: Слышно шипение труб. В коридоре утечка газа Самосбора!",
        "log_event_corpse": "На полу впереди лежит неподвижное тело ликвидатора...",
        "log_event_ghost": "Леденящий сквозняк... В глубине коридора промелькнул силуэт.",
        "log_crawler_sound": "Вы слышите жуткий, шуршащий звук когтей по бетону откуда-то впереди...",
        "log_crawler_attack": "ТВАРЬ НАПАЛА НА ВАС! Своими жвалами она прокусила вам скафандр!",
        "log_stairs_up_blocked": "Верхние этажи заблокированы гермозатвором. Прохода нет.",
        "log_gasmask_protects_but_corrodes": "Противогаз защищает от газа, но химикаты разъедают костюм...",
        "note_title_num": "Записка {0}",
        "log_web_audio_error": "Не удалось запустить Web Audio API: ",
        "sdk_offline_demo": "РЕЖИМ: ОФФЛАЙН (ДЕМО)",
        "sdk_ready": "SDK ГОТОВ",
        "sdk_demo": "РЕЖИМ: ДЕМО",
        "sdk_offline": "РЕЖИМ: ОФФЛАЙН",
        "transition_floor_num": "ЭТАЖ {0}",
        "battery_qty": "{0} шт",
        "log_enter_apt_clean": "Вы вошли в {0}. На стене висит знак Ликвидаторов. Под ногами рассыпаны гильзы.",
        "log_enter_apt_gas": "Вы вошли в {0}. Воздух здесь едкий и желтоватый. Счетчик Гейгера тихо потрескивает! (Фильтр тратится быстрее)",
        "log_enter_apt_slime": "Вы вошли в {0}. В углу копошится склизкая биомасса. Старайтесь не шуметь!",
        "log_enter_apt_default": "Вы вошли в квартиру. Вокруг обычная серая обстановка советской квартиры-хрущевки.",
        "log_ghost_dissolve": "Призрак закричал от боли и растаял в луче света вашего фонаря!",
        "log_ghost_whisper_1": "Призрак шепчет: 'Здесь нет выхода... только бесконечные этажи...'",
        "log_ghost_whisper_2": "Призрак шепчет: 'Они видят тебя... они всегда видят...'",
        "log_ghost_whisper_3": "Призрак шепчет: 'Остановись... прими Самосбор...'",
        "log_ghost_whisper_4": "Призрак шепчет: 'Ликвидатор 1324... твоя смена окончена...'"
    },
    "en": {
        "bag_hacker_yes": "YES",
        "bag_hacker_no": "NO",
        "settings_press_key": "Press any key...",
        "log_approach_furniture_warn": "Get close to the sideboard or table to search it.",
        "log_listening_door": "The liquidator leaned against door {0} and listens...",
        "listen_sounds_scary": "Scraping, a low guttural hissing!",
        "listen_sounds_wind": "Whistling of air, distant hum of ventilation",
        "listen_sounds_empty": "Only the heavy echo of empty rooms",
        "log_note_found": "[FIND] Found an old note: \"{0}\"!",
        "log_found_hacker_tool": "[FIND] You found the BLAST DOOR DECRYPTER! Now you can open stairwell gates.",
        "log_found_battery": "[FIND] Found a battery for the decrypter (+1 pc., total: {0}).",
        "log_found_water": "[FIND] Found a flask of clean synthesized water (+50% stock).",
        "log_found_ammo": "[FIND] Found pistol ammo (+{0} pcs.).",
        "log_found_filter": "[FIND] Found a new gas mask filter cartridge (+50% charge).",
        "log_found_bandage": "[FIND] Found a hemostatic bandage (+1 pc., total: {0}).",
        "log_found_nothing": "You searched the corners but found only gray concrete dust (nothing there).",
        "btn_descend_ending": "Freeze and wait",
        "btn_descend_default": "Go to the stairs at the end of the hallway",
        "log_prefix_action": "[ACT]",
        "go_badge_death": "Death",
        "game_title": "Samosbor: Liquidator 1324",
        "focus_corpse_title": "LIQUIDATOR'S BODY",
        "focus_corpse_desc": "Dead liquidator in uniform. Search pouches (R key).",
        "focus_corpse_btn": "Search body",
        "focus_spawn_door_title": "SECTOR BLAST GATE",
        "focus_spawn_door_desc": "Sector outer lock. Massive steel. Press B to decrypt.",
        "focus_spawn_door_btn": "Try to hack",
        "focus_stairs_door_title": "STAIRWELL BLAST GATE",
        "focus_stairs_door_desc_locked": "Locked by GIGA-KHRUSHCHEVKA central system.",
        "focus_stairs_door_btn_try": "Try hacking",
        "focus_stairs_door_desc_open": "Gate is open. The passage to the stairs is clear.",
        "focus_stairs_door_btn_close": "Close gate",
        "focus_stairs_door_desc_closed": "Massive blast gate is locked! Press B to hack.",
        "focus_stairs_door_btn_hack": "Hack gate",
        "focus_door_desc_open": "Door is open. You can go inside (walk WASD).",
        "focus_door_btn_close": "Close door",
        "focus_door_desc_closed": "Blast door is closed. Get close.",
        "focus_door_btn_open": "Open door",
        "focus_object_none": "OBJECT NOT SELECTED",
        "focus_object_desc": "Approach a door or interactive object",
        "focus_btn_default": "Interact",
        # New translation keys (V5)
        "log_event_flicker": "The light on this floor is unstable. The power grid is overloaded.",
        "log_event_gas_leak": "WARNING: Hissing of pipes heard. There is a Samosbor gas leak in the hallway!",
        "log_event_corpse": "A motionless body of a liquidator lies on the floor ahead...",
        "log_event_ghost": "A chilling draft... A silhouette flashed in the depths of the hallway.",
        "log_crawler_sound": "You hear a creepy, rustling sound of claws on concrete from somewhere ahead...",
        "log_crawler_attack": "THE BEAST ATTACKED YOU! It bit through your suit with its mandibles!",
        "log_stairs_up_blocked": "Upper floors are blocked by a hermetic gate. No passage.",
        "log_gasmask_protects_but_corrodes": "The gas mask protects against gas, but chemicals corrode the suit...",
        "note_title_num": "Note {0}",
        "log_web_audio_error": "Failed to start Web Audio API: ",
        "sdk_offline_demo": "MODE: OFFLINE (DEMO)",
        "sdk_ready": "SDK READY",
        "sdk_demo": "MODE: DEMO",
        "sdk_offline": "MODE: OFFLINE",
        "transition_floor_num": "FLOOR {0}",
        "battery_qty": "{0} pcs",
        "log_enter_apt_clean": "You entered {0}. A Liquidators sign hangs on the wall. Spent shells are scattered underfoot.",
        "log_enter_apt_gas": "You entered {0}. The air here is acrid and yellowish. The Geiger counter is ticking quietly! (Filter depletes faster)",
        "log_enter_apt_slime": "You entered {0}. A slimy biomass is writhing in the corner. Try not to make noise!",
        "log_enter_apt_default": "You entered an apartment. Around is the usual gray atmosphere of a Soviet Khrushchevka apartment.",
        "log_ghost_dissolve": "The ghost screamed in pain and dissolved in your flashlight's beam!",
        "log_ghost_whisper_1": "The ghost whispers: 'There is no exit here... only endless floors...'",
        "log_ghost_whisper_2": "The ghost whispers: 'They see you... they always see...'",
        "log_ghost_whisper_3": "The ghost whispers: 'Stop... embrace the Samosbor...'",
        "log_ghost_whisper_4": "The ghost whispers: 'Liquidator 1324... your shift is over...'"
    },
    "zh": {
        "bag_hacker_yes": "有",
        "bag_hacker_no": "无",
        "settings_press_key": "按任意键...",
        "log_approach_furniture_warn": "靠近碗柜或桌子进行搜寻。",
        "log_listening_door": "清理员正靠在门 {0} 上倾听...",
        "listen_sounds_scary": "刮擦声，低沉的喉音嘶嘶声！",
        "listen_sounds_wind": "空气啸叫声，远处的通风轰鸣声",
        "listen_sounds_empty": "只有空荡房间的沉重回音",
        "log_note_found": "[发现] 找到一张旧便签: \"{0}\"!",
        "log_found_hacker_tool": "[发现] 你找到了闸门破解器！现在你可以打开楼梯通道了。",
        "log_found_battery": "[发现] 找到了破解器电池 (+1 个，总计: {0})。",
        "log_found_water": "[发现] 找到了干净的合成水壶 (+50% 存量)。",
        "log_found_ammo": "[发现] 找到了手枪弹药 (+{0} 发)。",
        "log_found_filter": "[发现] 找到了新的防毒面具滤毒罐 (+50% 电量)。",
        "log_found_bandage": "[发现] 找到了止血绷带 (+1 个，总计: {0})。",
        "log_found_nothing": "你搜寻了角落，但只发现了灰色的混凝土粉尘 (什么也没有)。",
        "btn_descend_ending": "呆在原地等待",
        "btn_descend_default": "走向走廊尽头的楼梯",
        "log_prefix_action": "[行动]",
        "go_badge_death": "死亡",
        "game_title": "萨摩斯堡: 清理员 1324",
        "focus_corpse_title": "清理人员尸体",
        "focus_corpse_desc": "身穿制服的已故清理人员。搜寻小袋 (R 键)。",
        "focus_corpse_btn": "搜寻尸体",
        "focus_spawn_door_title": "分区密封闸门",
        "focus_spawn_door_desc": "分区外侧气密舱。沉重的钢材。按 B 进行解密。",
        "focus_spawn_door_btn": "尝试破解",
        "focus_stairs_door_title": "楼梯井密封闸门",
        "focus_stairs_door_desc_locked": "被巨型赫鲁晓夫楼中央系统锁死。",
        "focus_stairs_door_btn_try": "尝试破解",
        "focus_stairs_door_desc_open": "闸门已开。去往楼梯的通道已畅通。",
        "focus_stairs_door_btn_close": "关闭闸门",
        "focus_stairs_door_desc_closed": "沉重的密封闸门已锁！按 B 进行破解。",
        "focus_stairs_door_btn_hack": "破解闸门",
        "focus_door_desc_open": "门已开。你可以进入内部 (通过 WASD 行走)。",
        "focus_door_btn_close": "关闭门",
        "focus_door_desc_closed": "密封门已关。请靠近。",
        "focus_door_btn_open": "打开门",
        "focus_object_none": "未选择对象",
        "focus_object_desc": "靠近门或可交互对象",
        "focus_btn_default": "交互",
        # New translation keys (V5)
        "log_event_flicker": "该楼层的灯光不稳定。电网过载。",
        "log_event_gas_leak": "警告：听到管道声音。走廊里有萨摩斯堡气体泄漏！",
        "log_event_corpse": "前方地板上躺着一具一动不动的清理人员尸体...",
        "log_event_ghost": "冰冷的微风... 走廊深处闪过一个黑影。",
        "log_crawler_sound": "你听到前方传来爪子在混凝土上爬行的诡异沙沙声...",
        "log_crawler_attack": "怪物袭击了你！它的上颚咬穿了你的防护服！",
        "log_stairs_up_blocked": "上层已被防爆门封锁。无法通行。",
        "log_gasmask_protects_but_corrodes": "防毒面具可以防止吸入有害气体，但化学物质会腐蚀防护服……",
        "note_title_num": "便签 {0}",
        "log_web_audio_error": "无法启动 Web Audio API： ",
        "sdk_offline_demo": "模式：离线（演示）",
        "sdk_ready": "SDK 就绪",
        "sdk_demo": "模式：演示",
        "sdk_offline": "模式：离线",
        "transition_floor_num": "楼层 {0}",
        "battery_qty": "{0} 个",
        "log_enter_apt_clean": "你进入了{0}。墙上挂着清理人员的标志。脚下散落着弹壳。",
        "log_enter_apt_gas": "你进入了{0}。那里的空气辛辣发黄。盖革计数器在静静地嗒嗒作响！（滤毒罐消耗更快）",
        "log_enter_apt_slime": "你进入了{0}。角落里有黏糊糊的生物质在蠕动。尽量不要发出噪音！",
        "log_enter_apt_default": "你进入了一套公寓。周围是苏式赫鲁晓夫楼公寓一贯的灰色氛围。",
        "log_ghost_dissolve": "幽灵痛苦地尖叫，在你的手电筒光束中消散了！",
        "log_ghost_whisper_1": "幽灵低语道：“这里没有出口……只有无尽的楼层……”",
        "log_ghost_whisper_2": "幽灵低语道：“他们看着你……他们一直在看着……”",
        "log_ghost_whisper_3": "幽灵低语道：“停下……拥抱萨摩斯堡吧……”",
        "log_ghost_whisper_4": "幽灵低语道：“清理人员1324……你的轮班结束了……”"
    },
    "de": {
        "bag_hacker_yes": "JA",
        "bag_hacker_no": "NEIN",
        "settings_press_key": "Taste drücken...",
        "log_approach_furniture_warn": "Nähern Sie sich dem Schrank oder Tisch, um ihn zu durchsuchen.",
        "log_listening_door": "Der Liquidator lehnt sich an Tür {0} und lauscht...",
        "listen_sounds_scary": "Schaben, ein tiefes kehliges Zischen!",
        "listen_sounds_wind": "Pfeifen der Luft, fernes Summen der Belüftung",
        "listen_sounds_empty": "Nur das schwere Echo leerer Räume",
        "log_note_found": "[FUND] Eine alte Notiz gefunden: \"{0}\"!",
        "log_found_hacker_tool": "[FUND] Sie haben den SCHUTZSCHOTT-DECODER gefunden! Jetzt können Sie Treppentore öffnen.",
        "log_found_battery": "[FUND] Batterie für den Decoder gefunden (+1 Stk., gesamt: {0}).",
        "log_found_water": "[FUND] Eine Feldflasche mit reinem synthetisiertem Wasser gefunden (+50% Vorrat).",
        "log_found_ammo": "[FUND] Pistolenmunition gefunden (+{0} Stk.).",
        "log_found_filter": "[FUND] Neue Filterpatrone für Gasmaske gefunden (+50% Ladung).",
        "log_found_bandage": "[FUND] Blutstillende Bandage gefunden (+1 Stk., gesamt: {0}).",
        "log_found_nothing": "Sie haben die Ecken durchsucht, aber nur grauen Betonstaub gefunden (nichts da).",
        "btn_descend_ending": "Innehalten und warten",
        "btn_descend_default": "Gehen Sie zur Treppe am Ende des Flurs",
        "log_prefix_action": "[AKT]",
        "go_badge_death": "Tod",
        "game_title": "Samosbor: Liquidator 1324",
        "focus_corpse_title": "LIQUIDATORLEICHE",
        "focus_corpse_desc": "Toter Liquidator in Uniform. Taschen durchsuchen (Taste R).",
        "focus_corpse_btn": "Leiche durchsuchen",
        "focus_spawn_door_title": "SEKTORSCHUTZSCHOTT",
        "focus_spawn_door_desc": "Äußere Sektorschleuse. Massiver Stahl. Drücken Sie B zur Entschlüsselung.",
        "focus_spawn_door_btn": "Hacken versuchen",
        "focus_stairs_door_title": "TREPPENHAUSSCHUTZSCHOTT",
        "focus_stairs_door_desc_locked": "Vom GIGA-CHRUSCHTSCHOWKA-Zentralsystem verriegelt.",
        "focus_stairs_door_btn_try": "Hacken probieren",
        "focus_stairs_door_desc_open": "Tor ist offen. Der Durchgang zur Treppe ist frei.",
        "focus_stairs_door_btn_close": "Tor schließen",
        "focus_stairs_door_desc_closed": "Massives Schutzschott ist verriegelt! Drücken Sie B zum Hacken.",
        "focus_stairs_door_btn_hack": "Tor hacken",
        "focus_door_desc_open": "Tür ist offen. Sie können hineingehen (WASD benutzen).",
        "focus_door_btn_close": "Tür schließen",
        "focus_door_desc_closed": "Panzertür ist geschlossen. Nähern Sie sich.",
        "focus_door_btn_open": "Tür öffnen",
        "focus_object_none": "KEIN OBJEKT AUSGEWÄHLT",
        "focus_object_desc": "Nähern Sie sich einer Tür oder einem interaktiven Objekt",
        "focus_btn_default": "Interagieren",
        # New translation keys (V5)
        "log_event_flicker": "Das Licht auf dieser Etage ist instabil. Das Stromnetz ist überlastet.",
        "log_event_gas_leak": "WARNUNG: Zischen von Rohren zu hören. Es gibt ein Samosbor-Gasleck im Flur!",
        "log_event_corpse": "Eine reglose Leiche eines Liquidators liegt auf dem Boden voraus...",
        "log_event_ghost": "Ein eisiger Zug... Eine Silhouette huschte in den Tiefen des Flurs vorbei.",
        "log_crawler_sound": "Du hörst das schaurige, raschelnde Geräusch von Krallen auf Beton von irgendwo da vorne...",
        "log_crawler_attack": "DIE BESTIE HAT DICH ANGEGRIFFEN! Sie hat mit ihren Mandibeln deinen Schutzanzug durchgebissen!",
        "log_stairs_up_blocked": "Die oberen Stockwerke sind durch ein hermetisches Tor blockiert. Kein Durchgang.",
        "log_gasmask_protects_but_corrodes": "Die Gasmaske schützt vor Gas, aber Chemikalien zerfressen den Anzug...",
        "note_title_num": "Notiz {0}",
        "log_web_audio_error": "Web Audio API konnte nicht gestartet werden: ",
        "sdk_offline_demo": "MODUS: OFFLINE (DEMO)",
        "sdk_ready": "SDK BEREIT",
        "sdk_demo": "MODUS: DEMO",
        "sdk_offline": "MODUS: OFFLINE",
        "transition_floor_num": "ETAGE {0}",
        "battery_qty": "{0} Stk.",
        "log_enter_apt_clean": "Du hast {0} betreten. An der Wand hängt ein Liquidatorenschild. Patronenhülsen liegen verstreut unter den Füßen.",
        "log_enter_apt_gas": "Du hast {0} betreten. Die Luft hier ist beißend und gelblich. Der Geigerzähler tickt leise! (Filter verbraucht sich schneller)",
        "log_enter_apt_slime": "Du hast {0} betreten. In der Ecke wimmelt eine schleimige Biomasse. Versuche, keinen Lärm zu machen!",
        "log_enter_apt_default": "Du hast eine Wohnung betreten. Ringsum herrscht die übliche graue Atmosphäre einer sowjetischen Chruschtschowka-Wohnung.",
        "log_ghost_dissolve": "Der Geist schrie vor Schmerz und löste sich im Lichtstrahl deiner Taschenlampe auf!",
        "log_ghost_whisper_1": "Der Geist flüstert: 'Es gibt keinen Ausgang... nur unendliche Stockwerke...'",
        "log_ghost_whisper_2": "Der Geist flüstert: 'Sie sehen dich... sie sehen dich immer...'",
        "log_ghost_whisper_3": "Der Geist flüstert: 'Hör auf... nimm den Samosbor an...'",
        "log_ghost_whisper_4": "Der Geist flüstert: 'Liquidator 1324... deine Schicht ist vorbei...'"
    },
    "it": {
        "bag_hacker_yes": "SÌ",
        "bag_hacker_no": "NO",
        "settings_press_key": "Premi un tasto...",
        "log_approach_furniture_warn": "Avvicinati alla credenza o al tavolo per cercarvi.",
        "log_listening_door": "Il liquidatore si è appoggiato alla porta {0} e ascolta...",
        "listen_sounds_scary": "Un raschiamento, un basso fischio gutturale!",
        "listen_sounds_wind": "Fischio dell'aria, lontano ronzio della ventilazione",
        "listen_sounds_empty": "Solo il pesante eco di stanze vuote",
        "log_note_found": "[BOTTINO] Trovata una vecchia nota: \"{0}\"!",
        "log_found_hacker_tool": "[BOTTINO] Hai trovato il DECRITTATORE PORTE! Ora puoi aprire i cancelli delle scale.",
        "log_found_battery": "[BOTTINO] Trovata una batteria per il decrittatore (+1 pz, totale: {0}).",
        "log_found_water": "[BOTTINO] Trovata una fiaschetta di acqua sintetizzata pulita (+50% riserva).",
        "log_found_ammo": "[BOTTINO] Trovate munizioni per pistola (+{0} pz).",
        "log_found_filter": "[BOTTINO] Trovata una nuova cartuccia del filtro per la maschera antigas (+50% carica).",
        "log_found_bandage": "[BOTTINO] Trovata una benda emostatica (+1 pz, totale: {0}).",
        "log_found_nothing": "Hai cercato negli angoli, ma hai trovato solo polvere di cemento grigia (niente).",
        "btn_descend_ending": "Resta immobile e aspetta",
        "btn_descend_default": "Vai alle scale in fondo al corridoio",
        "log_prefix_action": "[AZIO]",
        "go_badge_death": "Morte",
        "game_title": "Samosbor: Liquidatore 1324",
        "focus_corpse_title": "CORPO DEL LIQUIDATORE",
        "focus_corpse_desc": "Liquidatore deceduto in divisa. Cerca nelle tasche (tasto R).",
        "focus_corpse_btn": "Cerca sul corpo",
        "focus_spawn_door_title": "PORTA ERMETICA DEL SETTORE",
        "focus_spawn_door_desc": "Chiusura esterna del settore. Acciaio massiccio. Premi B per decrittare.",
        "focus_spawn_door_btn": "Prova a violare",
        "focus_stairs_door_title": "PORTA ERMETICA VANO SCALE",
        "focus_stairs_door_desc_locked": "Bloccato dal sistema centrale della GIGA-KHRUSHCHEVKA.",
        "focus_stairs_door_btn_try": "Prova ad hackerare",
        "focus_stairs_door_desc_open": "La porta è aperta. Il passaggio per le scale è libero.",
        "focus_stairs_door_btn_close": "Chiudi porta",
        "focus_stairs_door_desc_closed": "La porta ermetica massiccia è bloccata! Premi B per hackerare.",
        "focus_stairs_door_btn_hack": "Hachera porta",
        "focus_door_desc_open": "La porta è aperta. Puoi entrare (usa WASD).",
        "focus_door_btn_close": "Chiudi porta",
        "focus_door_desc_closed": "La porta blindata è chiusa. Avvicinati.",
        "focus_door_btn_open": "Apri porta",
        "focus_object_none": "NESSUN OGGETTO SELEZIONATO",
        "focus_object_desc": "Avvicinati a una porta o a un oggetto interattivo",
        "focus_btn_default": "Interagisci",
        # New translation keys (V5)
        "log_event_flicker": "La luce su questo piano è instabile. La rete elettrica è sovraccarica.",
        "log_event_gas_leak": "ATTENZIONE: Si sente il fischio dei tubi. C'è una fuga di gas Samosbor nel corridoio!",
        "log_event_corpse": "Un corpo immobile di un liquidatore giace sul pavimento davanti...",
        "log_event_ghost": "Una corrente gelida... Una sagoma è passata in fondo al corridoio.",
        "log_crawler_sound": "Senti un inquietante fruscio di artigli sul cemento da qualche parte davanti...",
        "log_crawler_attack": "LA BEAST TI HA ATTACCATO! Ha trapassato la tua tuta con le sue mandibole!",
        "log_stairs_up_blocked": "I piani superiori sono bloccati da una porta ermetica. Nessun passaggio.",
        "log_gasmask_protects_but_corrodes": "La maschera antigas protegge dal gas, ma le sostanze chimiche corrodono la tuta...",
        "note_title_num": "Nota {0}",
        "log_web_audio_error": "Impossibile avviare Web Audio API: ",
        "sdk_offline_demo": "MODALITÀ: OFFLINE (DEMO)",
        "sdk_ready": "SDK PRONTO",
        "sdk_demo": "MODALITÀ: DEMO",
        "sdk_offline": "MODALITÀ: OFFLINE",
        "transition_floor_num": "PIANO {0}",
        "battery_qty": "{0} pz",
        "log_enter_apt_clean": "Sei entrato in {0}. Un cartello dei Liquidatori è appeso al muro. Bossoli vuoti sono sparsi a terra.",
        "log_enter_apt_gas": "Sei entrato in {0}. L'aria qui è acre e giallastra. Il contatore Geiger ticchetta silenziosamente! (Il filtro si consuma più velocemente)",
        "log_enter_apt_slime": "Sei entrato in {0}. Una biomassa viscida si agita nell'angolo. Cerca di non fare rumore!",
        "log_enter_apt_default": "Sei entrato in un appartamento. Tutto intorno c'è la solita atmosfera grigia di un appartamento sovietico Chruščëvka.",
        "log_ghost_dissolve": "Il fantasma ha gridato per il dolore e si è dissolto nel fascio della tua torcia!",
        "log_ghost_whisper_1": "Il fantasma sussurra: 'Non c'è via d'uscita... solo piani infiniti...'",
        "log_ghost_whisper_2": "Il fantasma sussurra: 'Ti vedono... vedono sempre...'",
        "log_ghost_whisper_3": "Il fantasma sussurra: 'Fermati... accetta il Samosbor...'",
        "log_ghost_whisper_4": "Il fantasma sussurra: 'Liquidatore 1324... il tuo turno è finito...'"
    },
    "es": {
        "bag_hacker_yes": "SÍ",
        "bag_hacker_no": "NO",
        "settings_press_key": "Presione una tecla...",
        "log_approach_furniture_warn": "Acércate a la alacena o mesa para buscar.",
        "log_listening_door": "El liquidador se apoyó contra la puerta {0} y escucha...",
        "listen_sounds_scary": "¡Raspado, un siseo gutural bajo!",
        "listen_sounds_wind": "Silbido del aire, lejano zumbido de la ventilación",
        "listen_sounds_empty": "Solo el eco pesado de habitaciones vacías",
        "log_note_found": "[HALLAZGO] ¡Encontró una nota antigua: \"{0}\"!",
        "log_found_hacker_tool": "[HALLAZGO] ¡Encontraste el DESCIFRADOR DE COMPUERTAS! Ahora puedes abrir las compuertas de las escaleras.",
        "log_found_battery": "[HALLAZGO] Encontraste una batería para el descifrador (+1 ud., total: {0}).",
        "log_found_water": "[HALLAZGO] Encontraste un frasco de agua sintetizada limpia (+50% reserva).",
        "log_found_ammo": "[HALLAZGO] Encontraste munición de pistola (+{0} uds.).",
        "log_found_filter": "[HALLAZGO] Encontraste un nuevo cartucho de filtro de máscara de gas (+50% carga).",
        "log_found_bandage": "[HALLAZGO] Encontraste un vendaje hemostático (+1 ud., total: {0}).",
        "log_found_nothing": "Buscaste en las esquinas pero solo encontraste polvo de concreto gris (nada allí).",
        "btn_descend_ending": "Congelarse y esperar",
        "btn_descend_default": "Vaya a las escaleras al final del pasillo",
        "log_prefix_action": "[ACC]",
        "go_badge_death": "Muerte",
        "game_title": "Samosbor: Liquidador 1324",
        "focus_corpse_title": "CUERPO DEL LIQUIDADOR",
        "focus_corpse_desc": "Liquidador fallecido en uniforme. Buscar en las bolsas (tecla R).",
        "focus_corpse_btn": "Buscar en el cuerpo",
        "focus_spawn_door_title": "COMPUERTA DE SECTOR",
        "focus_spawn_door_desc": "Esclusa exterior del sector. Acero macizo. Presione B para descifrar.",
        "focus_spawn_door_btn": "Intentar hackear",
        "focus_stairs_door_title": "COMPUERTA DE ESCALERA",
        "focus_stairs_door_desc_locked": "Bloqueado por el sistema central de la GIGA-KHRUSHCHEVKA.",
        "focus_stairs_door_btn_try": "Probar a hackear",
        "focus_stairs_door_desc_open": "¡La compuerta está abierta! El paso a las escaleras está libre.",
        "focus_stairs_door_btn_close": "Cerrar compuerta",
        "focus_stairs_door_desc_closed": "¡La compuerta maciza está cerrada! Presione B para hackear.",
        "focus_stairs_door_btn_hack": "Hackear compuerta",
        "focus_door_desc_open": "La puerta está abierta. Puedes entrar (usa WASD).",
        "focus_door_btn_close": "Cerrar puerta",
        "focus_door_desc_closed": "La puerta blindada está cerrada. Acércate.",
        "focus_door_btn_open": "Abrir puerta",
        "focus_object_none": "OBJETO NO SELECCIONADO",
        "focus_object_desc": "Acérquese a una puerta u objeto interactivo",
        "focus_btn_default": "Interactuar",
        # New translation keys (V5)
        "log_event_flicker": "La luz en este piso es inestable. La red eléctrica está sobrecargada.",
        "log_event_gas_leak": "ADVERTENCIA: Se escucha un siseo de tuberías. ¡Hay una fuga de gas Samosbor en el pasillo!",
        "log_event_corpse": "Un cuerpo inmóvil de un liquidador yace en el suelo más adelante...",
        "log_event_ghost": "Una corriente helada... Una silueta pasó rápidamente en las profundidades del pasillo.",
        "log_crawler_sound": "Escuchas un espeluznante crujido de garras sobre el concreto en algún lugar más adelante...",
        "log_crawler_attack": "¡LA BESTIA TE ATACÓ! ¡Atravesó tu traje con sus mandíbulas!",
        "log_stairs_up_blocked": "Los pisos superiores están bloqueados por una compuerta hermética. No hay paso.",
        "log_gasmask_protects_but_corrodes": "La máscara antigas protege contra el gas, pero los productos químicos corroen el traje...",
        "note_title_num": "Nota {0}",
        "log_web_audio_error": "No se pudo iniciar Web Audio API: ",
        "sdk_offline_demo": "MODO: OFFLINE (DEMO)",
        "sdk_ready": "SDK LISTO",
        "sdk_demo": "MODO: DEMO",
        "sdk_offline": "MODO: OFFLINE",
        "transition_floor_num": "PISO {0}",
        "battery_qty": "{0} uds",
        "log_enter_apt_clean": "Entraste a {0}. Un cartel de Liquidadores cuelga de la pared. Cartuchos vacíos están esparcidos bajo los pies.",
        "log_enter_apt_gas": "Entraste a {0}. El aire aquí es acre y amarillento. ¡El contador Geiger está haciendo clic silenciosamente! (El filtro se agota más rápido)",
        "log_enter_apt_slime": "Entraste a {0}. Una biomasa viscosa se retuerce en la esquina. ¡Trata de no hacer ruido!",
        "log_enter_apt_default": "Entraste a un departamento. Alrededor está la habitual atmósfera gris de un apartamento soviético de Khrushchevka.",
        "log_ghost_dissolve": "¡El ghost gritó de dolor y se disolvió en el haz de tu linterna!",
        "log_ghost_whisper_1": "El ghost susurra: 'No hay salida aquí... solo pisos interminables...'",
        "log_ghost_whisper_2": "El ghost susurra: 'Te ven... siempre ven...'",
        "log_ghost_whisper_3": "El ghost susurra: 'Detente... acepta el Samosbor...'",
        "log_ghost_whisper_4": "El ghost susurra: 'Liquidador 1324... tu turno terminó...'"
    }
}

# 4. Merge all keys into LANGUAGES
for lang in ["ru", "en", "zh", "de", "it", "es"]:
    keys_str_1 = vars1[f"{lang.upper()}_KEYS"]
    keys_str_2 = vars2[f"{lang.upper()}_KEYS"]
    
    dict1 = parse_keys_str(keys_str_1)
    dict2 = parse_keys_str(keys_str_2)
    custom_dict = CUSTOM_KEYS[lang]
    
    LANGUAGES[lang].update(dict1)
    LANGUAGES[lang].update(dict2)
    LANGUAGES[lang].update(custom_dict)
    
    print(f"Language '{lang}' has now {len(LANGUAGES[lang])} total keys.")

# 5. Read restored app.js content
with open('app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove pre-existing LANGUAGES and t() blocks
lang_start = content.find("const LANGUAGES = ")
lore_start = content.find("const LORE_NOTES = ")
if lang_start != -1 and lore_start != -1 and lang_start < lore_start:
    content = content[:lang_start] + content[lore_start:]
    print("Deleted old LANGUAGES and t() blocks")

# Build updated LANGUAGES JS block
languages_js = "const LANGUAGES = " + json.dumps(LANGUAGES, ensure_ascii=False, indent=4) + ";\n\n"

# Add the t() function implementation
t_func = """function t(key, ...args) {
    const lang = (state && state.language) || 'ru';
    const db = LANGUAGES[lang] || LANGUAGES['ru'];
    let val = db[key];
    if (val === undefined) {
        val = LANGUAGES['ru'][key];
    }
    if (val === undefined) {
        return key;
    }
    if (args.length > 0) {
        for (let i = 0; i < args.length; i++) {
            val = val.replace(`{${i}}`, args[i]);
        }
    }
    return val;
}

"""

# Re-locate LORE_NOTES and ACHIEVEMENTS
lore_start_idx = content.find("const LORE_NOTES = Array.from")
if lore_start_idx == -1:
    lore_start_idx = content.find("const LORE_NOTES = [")
ach_start_idx = content.find("const ACHIEVEMENTS = {")
ach_end_idx = content.find("};", ach_start_idx) + 2

if lore_start_idx == -1 or ach_start_idx == -1 or ach_end_idx == -1:
    print("Error: Could not locate LORE_NOTES or ACHIEVEMENTS!")
    sys.exit(1)

new_lore_and_ach = """const LORE_NOTES = Array.from({ length: 10 }, (_, id) => ({
    id,
    get title() { return t(`note_${id}_title`); },
    get content() { 
        let raw = t(`note_${id}_content`);
        if (id === 5) {
            return raw.replace('{0}', state.floor);
        }
        return raw;
    }
}));

const ACHIEVEMENTS = {
    awakened: {
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
    deceived: {
        id: "deceived",
        get title() { return t('ach_deceived_title'); },
        get description() { 
            const isUnlocked = ACHIEVEMENTS.deceived ? ACHIEVEMENTS.deceived.unlocked : false;
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
    }
};"""

patched_content = content[:lore_start_idx] + languages_js + t_func + new_lore_and_ach + content[ach_end_idx:]

# Patch ACTION_LABELS
action_labels_pattern = r"const ACTION_LABELS = \{[\s\S]*?\};"
new_action_labels = """const ACTION_LABELS = {
    get MoveForward() { return t('act_move_forward'); },
    get MoveBackward() { return t('act_move_backward'); },
    get MoveLeft() { return t('act_move_left'); },
    get MoveRight() { return t('act_move_right'); },
    get Sprint() { return t('act_sprint'); },
    get Interact() { return t('act_interact'); },
    get Flashlight() { return t('act_flashlight'); },
    get Listen() { return t('act_listen'); },
    get GasMask() { return t('act_gasmask'); },
    get Water() { return t('act_water'); },
    get Bag() { return t('act_bag'); },
    get Search() { return t('act_search'); },
    get HackerTool() { return t('act_hackertool'); },
    get Pause() { return t('act_pause'); }
};"""
patched_content = re.sub(action_labels_pattern, new_action_labels, patched_content)

print("Applied LANGUAGES, t(), LORE_NOTES, ACHIEVEMENTS, and ACTION_LABELS patches")

# Replace remaining hardcoded code logic strings:

# 1. openDoor locked log
patched_content = patched_content.replace(
    'logToConsole("Дверь заблокирована", "danger");',
    'logToConsole(t("log_door_locked"), "danger");'
)

# 2. openDoor rusted shut log
patched_content = patched_content.replace(
    'logToConsole("Ручка не поддается. Гермозатвор заклинен намертво ржавчиной.", "warn");',
    'logToConsole(t("log_door_rusted_shut"), "warn");'
)

# 3. openDoor success log
patched_content = patched_content.replace(
    'logToConsole(`С лязгом замков дверь ${door.name} открылась наружу.`, "action");',
    'logToConsole(t("log_door_opened_name", door.name), "action");'
)

# 4. closeDoor log
patched_content = patched_content.replace(
    'logToConsole(`Вы заперли дверь ${door.name}.`, "sys");',
    'logToConsole(t("log_door_closed_name", door.name), "sys");'
)

# 5. toggleInnerDoor log
patched_content = patched_content.replace(
    'logToConsole(door.innerOpened ? "Внутренняя гермодверь открылась." : "Внутренняя гермодверь закрылась.", "action");',
    'logToConsole(door.innerOpened ? t("log_inner_door_opened") : t("log_inner_door_closed"), "action");'
)

# 6. searchRoom UI title & status
patched_content = patched_content.replace(
    'title.innerText = "ОБЫСК МЕБЕЛИ";\n    status.innerText = "Проверяем полки, перетряхиваем барахло...";',
    'title.innerText = t("search_room_title");\n    status.innerText = t("search_room_status");'
)

# 7. searchRoom nest trigger log
patched_content = patched_content.replace(
    'logToConsole("УЖАСНЫЙ ШОРОХ! Из шевелящейся слизи в углу на вас бросилась тварь!", "danger");',
    'logToConsole(t("log_nest_monster_attack"), "danger");'
)

# 8. searchDeadLiquidator UI title & status
patched_content = patched_content.replace(
    'title.innerText = "ОБЫСК ТЕЛА ЛИКВИДАТОРА";\n    status.innerText = "Осматриваем разгрузочный жилет, ищем полезное снаряжение...";',
    'title.innerText = t("search_corpse_title");\n    status.innerText = t("search_corpse_status");'
)

# 9. searchDeadLiquidator reward log
patched_content = patched_content.replace(
    'logToConsole("[НАХОДКА] Вы нашли батарейку, патроны (+8) и фильтр противогаза (+40%) на теле ликвидатора.", "loot");',
    'logToConsole(t("log_loot_corpse_reward"), "loot");'
)

# 10. showSubtitle hacker tools
patched_content = patched_content.replace(
    'showSubtitle("Получается, вы и делаете самосборы и управляете всей хрущёвкой");',
    'showSubtitle(t("sub_hacker_1"));'
)
patched_content = patched_content.replace(
    'showSubtitle("Я ненавижу вас, вы твари!");',
    'showSubtitle(t("sub_hacker_2"));'
)
patched_content = patched_content.replace(
    'showSubtitle("СИС: Вы умрёте, а никто о вас даже не вспомнит. Мучительной смерти!");',
    'showSubtitle(t("sub_hacker_3"));'
)

# 11. btnDescend text in transition
patched_content = patched_content.replace(
    "btnDescend.innerHTML = 'Застыть на месте и ждать';",
    "btnDescend.innerText = t('btn_descend_ending');"
)
patched_content = patched_content.replace(
    "btnDescend.innerHTML = 'Идите на лестницу в конце коридора';",
    "btnDescend.innerText = t('btn_descend_default');"
)

# 12. enableMenuWakeupTheme terminal texts
patched_content = patched_content.replace(
    '`\n            <p class="blink-cursor">> ДЕКОМПИЛЯЦИЯ КОШМАРА... ОК.</p>\n            <p>> ПОДКЛЮЧЕНИЕ К РЕАЛЬНОМУ МИРУ... ОК.</p>\n            <p>> ВОЗДУХ: ЧИСТЫЙ, ТРАВА: ЗЕЛЕНАЯ, НЕБО: СИНЕЕ.</p>\n            <p class="glow-green">> ЗАДАЧА: СНОВА СДЕЛАЙТЕ СВОЙ ВЫБОР И БУДЬТЕ СВОБОДНЫ.</p>\n        `',
    '`\n            <p class="blink-cursor">` + t("true_ending_terminal_1") + `</p>\n            <p>` + t("true_ending_terminal_2") + `</p>\n            <p>` + t("true_ending_terminal_3") + `</p>\n            <p class="glow-green">` + t("true_ending_terminal_4") + `</p>\n        `'
)

# 13. disableMenuWakeupTheme terminal texts
patched_content = patched_content.replace(
    '`\n            <p class="blink-cursor">> ИНИЦИАЛИЗАЦИЯ ИНТЕРФЕЙСА ЛИКВИДАТОРА...</p>\n            <p>> ПОДКЛЮЧЕНИЕ К СЕТИ ГИГАХРУЩЕВКИ... ОК.</p>\n            <p>> СНАРЯЖЕНИЕ: ПИСТОЛЕТ (24), ПРОТИВОГАЗ, ВОДА, СУМКА.</p>\n            <p class="glow-green">> ЗАДАЧА: СПУСТИТЬСЯ НА 1-Й ЭТАЖ И ВЫЖИТЬ.</p>\n        `',
    '`\n            <p class="blink-cursor">` + t("init_interface") + `</p>\n            <p>` + t("network_ok") + `</p>\n            <p>` + t("equipment_info") + `</p>\n            <p class="glow-green">` + t("mission_info") + `</p>\n        `'
)

# 14. Game over death badge text
patched_content = patched_content.replace(
    'let badgeText = "Смерть";',
    'let badgeText = t("go_badge_death");'
)

# 15. bagHacker yes/no text
patched_content = patched_content.replace(
    'bagHacker.innerText = state.hasHackerTool ? "ЕСТЬ" : "НЕТ";',
    'bagHacker.innerText = state.hasHackerTool ? t("bag_hacker_yes") : t("bag_hacker_no");'
)

# 17. settings controls text
patched_content = patched_content.replace(
    "btn.innerText = 'Нажмите клавишу...';",
    "btn.innerText = t('settings_press_key');"
)

# 18. approach sideboard/table log
patched_content = patched_content.replace(
    'logToConsole("Подойдите к серванту или столу вплотную, чтобы обыскать их.", "warn");',
    'logToConsole(t("log_approach_furniture_warn"), "warn");'
)

# 19. listener listening door log
patched_content = patched_content.replace(
    'logToConsole(`Ликвидатор прислонился к двери ${door.name} и слушает...`, "action");',
    'logToConsole(t("log_listening_door", door.name), "action");'
)

# 20. listening subtext messages
patched_content = patched_content.replace(
    'subtext.innerText = "Скрежет, глухое утробное шипение!";',
    'subtext.innerText = t("listen_sounds_scary");'
)
patched_content = patched_content.replace(
    'subtext.innerText = "Свист воздуха, далекий гул вентиляции";',
    'subtext.innerText = t("listen_sounds_wind");'
)
patched_content = patched_content.replace(
    'subtext.innerText = "Только тяжелое эхо пустых комнат";',
    'subtext.innerText = t("listen_sounds_empty");'
)

# 21. find note log
patched_content = patched_content.replace(
    'logToConsole(`[НАХОДКА] Найдена старая записка: "${LORE_NOTES[nextNoteId].title}"!`, "loot");',
    'logToConsole(t("log_note_found", LORE_NOTES[nextNoteId].title), "loot");'
)

# 22. find hacker tool log
patched_content = patched_content.replace(
    'logToConsole("[НАХОДКА] Вы нашли ВЗЛОМЩИК ГЕРМОДВЕРЕЙ! Теперь вы можете открывать лестничные затворы.", "loot");',
    'logToConsole(t("log_found_hacker_tool"), "loot");'
)

# 23. find battery log
patched_content = patched_content.replace(
    'logToConsole(`[НАХОДКА] Найдена батарейка для взломщика (+1 шт., всего: ${state.batteries}).`, "loot");',
    'logToConsole(t("log_found_battery", state.batteries), "loot");'
)

# 24. find water log
patched_content = patched_content.replace(
    'logToConsole("Найдена фляга чистой синтезированной воды (+50% запаса).", "loot");',
    'logToConsole(t("log_found_water"), "loot");'
)

# 25. find ammo log
patched_content = patched_content.replace(
    'logToConsole(`[НАХОДКА] Найдены пистолетные патроны (+${count} шт.).`, "loot");',
    'logToConsole(t("log_found_ammo", count), "loot");'
)

# 26. find filter log
patched_content = patched_content.replace(
    'logToConsole("Найден новый патрон фильтра для противогаза (+50% заряда).", "loot");',
    'logToConsole(t("log_found_filter"), "loot");'
)

# 27. find bandage log
patched_content = patched_content.replace(
    'logToConsole(`[НАХОДКА] Найден кровоостанавливающий бинт (+1 шт., всего: ${state.bandages}).`, "loot");',
    'logToConsole(t("log_found_bandage", state.bandages), "loot");'
)

# 28. found nothing log
patched_content = patched_content.replace(
    'logToConsole("Вы обыскали углы, но нашли лишь серую бетонную пыль (ничего нет).", "warn");',
    'logToConsole(t("log_found_nothing"), "warn");'
)

# 29. logToConsole prefixes translation
log_to_console_prefix_old = """    let colorClass = '';
    let prefix = '';
    switch (type) {
        case 'sys':
            colorClass = 'log-sys';
            prefix = '[СИС]';
            break;
        case 'action':
            colorClass = 'log-action';
            prefix = '[ДЕЙСТ]';
            break;
        case 'warn':
            colorClass = 'log-warn';
            prefix = '[ВНИМАНИЕ]';
            break;
        case 'danger':
            colorClass = 'log-danger';
            prefix = '[ОПАСНОСТЬ]';
            break;
        case 'loot':
            colorClass = 'log-loot';
            prefix = '[НАХОДКА]';
            break;
        default:
            colorClass = 'log-sys';
            prefix = '[СИС]';
    }"""

log_to_console_prefix_new = """    let colorClass = '';
    let prefix = '';
    switch (type) {
        case 'sys':
            colorClass = 'log-sys';
            prefix = t('log_prefix_sys');
            break;
        case 'action':
            colorClass = 'log-action';
            prefix = t('log_prefix_action');
            break;
        case 'warn':
            colorClass = 'log-warn';
            prefix = t('log_prefix_warn');
            break;
        case 'danger':
            colorClass = 'log-danger';
            prefix = t('log_prefix_danger');
            break;
        case 'loot':
            colorClass = 'log-loot';
            prefix = t('log_prefix_loot');
            break;
        default:
            colorClass = 'log-sys';
            prefix = t('log_prefix_sys');
    }"""
patched_content = patched_content.replace(log_to_console_prefix_old, log_to_console_prefix_new)

# 30. updateFocusedObjectUI localization replacement
old_focused_object_ui = """function updateFocusedObjectUI(force = false) {
    if (!force && 
        state.focusedDoorIndex === lastFocusedDoorIndex && 
        state.focusedStairsDoor === lastFocusedStairsDoor && 
        state.focusedCorpse === lastFocusedCorpse &&
        state.focusedSpawnDoor === lastFocusedSpawnDoor) {
        return;
    }
    
    lastFocusedDoorIndex = state.focusedDoorIndex;
    lastFocusedStairsDoor = state.focusedStairsDoor;
    lastFocusedCorpse = state.focusedCorpse;
    lastFocusedSpawnDoor = state.focusedSpawnDoor;
    
    const title = document.getElementById('focused-object-name');
    const desc = document.getElementById('focused-object-state');
    const btnListen = document.getElementById('btn-listen');
    const btnOpen = document.getElementById('btn-open-door');
    
    if (!title || !desc || !btnListen || !btnOpen) return;
    
    if (state.focusedCorpse) {
        title.innerText = "ТЕЛО ЛИКВИДАТОРА";
        desc.innerText = "Погибший ликвидатор в форме. Обыскать подсумки (клавиша R).";
        btnOpen.removeAttribute('disabled');
        btnOpen.classList.remove('btn-disabled');
        btnOpen.innerText = "Обыскать тело";
        btnListen.setAttribute('disabled', 'true');
        btnListen.classList.add('btn-disabled');
        return;
    }
    
    if (state.focusedSpawnDoor) {
        title.innerText = "ГЕРМОЗАТВОР СЕКТОРА";
        desc.innerText = "Внешний шлюз сектора. Массивная сталь. Нажмите B для дешифровки.";
        btnOpen.removeAttribute('disabled');
        btnOpen.classList.remove('btn-disabled');
        btnOpen.innerText = "Попытаться взломать";
        btnListen.setAttribute('disabled', 'true');
        btnListen.classList.add('btn-disabled');
        return;
    }
    
    if (state.focusedStairsDoor) {
        const sdState = getOrGenerateStairsDoor(state.floor);
        title.innerText = "ГЕРМОЗАТВОР ЛЕСТНИЦЫ";
        if (state.floor === 1) {
            desc.innerText = "Заблокировано центральной системой ГИГАХРУЩА.";
            btnOpen.removeAttribute('disabled');
            btnOpen.classList.remove('btn-disabled');
            btnOpen.innerText = "Попробовать взломать";
        } else if (sdState.opened) {
            desc.innerText = "Затвор открыт. Проход на лестницу свободен.";
            btnOpen.removeAttribute('disabled');
            btnOpen.classList.remove('btn-disabled');
            btnOpen.innerText = "Закрыть затвор";
        } else {
            desc.innerText = "Массивный гермозатвор заперт! Нажмите B для взлома.";
            btnOpen.removeAttribute('disabled');
            btnOpen.classList.remove('btn-disabled');
            btnOpen.innerText = "Взломать затвор";
        }
        btnListen.setAttribute('disabled', 'true');
        btnListen.classList.add('btn-disabled');
        return;
    }
    
    if (state.focusedDoorIndex !== null) {
        const door = state.doors[state.focusedDoorIndex];
        title.innerText = door.name.toUpperCase();
        
        if (door.opened) {
            desc.innerText = "Дверь открыта. Вы можете зайти внутрь (пройдите WASD).";
            btnListen.setAttribute('disabled', 'true');
            btnListen.classList.add('btn-disabled');
            btnOpen.removeAttribute('disabled');
            btnOpen.classList.remove('btn-disabled');
            btnOpen.innerText = "Закрыть дверь";
        } else {
            desc.innerText = "Гермодверь закрыта. Подойдите вплотную.";
            btnListen.removeAttribute('disabled');
            btnListen.classList.remove('btn-disabled');
            btnOpen.removeAttribute('disabled');
            btnOpen.classList.remove('btn-disabled');
            btnOpen.innerText = "Открыть дверь";
        }
    } else {
        title.innerText = "ОБЪЕКТ НЕ ВЫБРАН";
        desc.innerText = "Подойдите к двери или объекту взаимодействия";
        btnListen.setAttribute('disabled', 'true');
        btnListen.classList.add('btn-disabled');
        btnOpen.setAttribute('disabled', 'true');
        btnOpen.classList.add('btn-disabled');
        btnOpen.innerText = "Взаимодействовать";
    }
}"""

new_focused_object_ui = """function updateFocusedObjectUI(force = false) {
    if (!force && 
        state.focusedDoorIndex === lastFocusedDoorIndex && 
        state.focusedStairsDoor === lastFocusedStairsDoor && 
        state.focusedCorpse === lastFocusedCorpse &&
        state.focusedSpawnDoor === lastFocusedSpawnDoor) {
        return;
    }
    
    lastFocusedDoorIndex = state.focusedDoorIndex;
    lastFocusedStairsDoor = state.focusedStairsDoor;
    lastFocusedCorpse = state.focusedCorpse;
    lastFocusedSpawnDoor = state.focusedSpawnDoor;
    
    const title = document.getElementById('focused-object-name');
    const desc = document.getElementById('focused-object-state');
    const btnListen = document.getElementById('btn-listen');
    const btnOpen = document.getElementById('btn-open-door');
    
    if (!title || !desc || !btnListen || !btnOpen) return;
    
    if (state.focusedCorpse) {
        title.innerText = t("focus_corpse_title");
        desc.innerText = t("focus_corpse_desc");
        btnOpen.removeAttribute('disabled');
        btnOpen.classList.remove('btn-disabled');
        btnOpen.innerText = t("focus_corpse_btn");
        btnListen.setAttribute('disabled', 'true');
        btnListen.classList.add('btn-disabled');
        return;
    }
    
    if (state.focusedSpawnDoor) {
        title.innerText = t("focus_spawn_door_title");
        desc.innerText = t("focus_spawn_door_desc");
        btnOpen.removeAttribute('disabled');
        btnOpen.classList.remove('btn-disabled');
        btnOpen.innerText = t("focus_spawn_door_btn");
        btnListen.setAttribute('disabled', 'true');
        btnListen.classList.add('btn-disabled');
        return;
    }
    
    if (state.focusedStairsDoor) {
        const sdState = getOrGenerateStairsDoor(state.floor);
        title.innerText = t("focus_stairs_door_title");
        if (state.floor === 1) {
            desc.innerText = t("focus_stairs_door_desc_locked");
            btnOpen.removeAttribute('disabled');
            btnOpen.classList.remove('btn-disabled');
            btnOpen.innerText = t("focus_stairs_door_btn_try");
        } else if (sdState.opened) {
            desc.innerText = t("focus_stairs_door_desc_open");
            btnOpen.removeAttribute('disabled');
            btnOpen.classList.remove('btn-disabled');
            btnOpen.innerText = t("focus_stairs_door_btn_close");
        } else {
            desc.innerText = t("focus_stairs_door_desc_closed");
            btnOpen.removeAttribute('disabled');
            btnOpen.classList.remove('btn-disabled');
            btnOpen.innerText = t("focus_stairs_door_btn_hack");
        }
        btnListen.setAttribute('disabled', 'true');
        btnListen.classList.add('btn-disabled');
        return;
    }
    
    if (state.focusedDoorIndex !== null) {
        const door = state.doors[state.focusedDoorIndex];
        title.innerText = getLocalizedDoorName(door).toUpperCase();
        
        if (door.opened) {
            desc.innerText = t("focus_door_desc_open");
            btnListen.setAttribute('disabled', 'true');
            btnListen.classList.add('btn-disabled');
            btnOpen.removeAttribute('disabled');
            btnOpen.classList.remove('btn-disabled');
            btnOpen.innerText = t("focus_door_btn_close");
        } else {
            desc.innerText = t("focus_door_desc_closed");
            btnListen.removeAttribute('disabled');
            btnListen.classList.remove('btn-disabled');
            btnOpen.removeAttribute('disabled');
            btnOpen.classList.remove('btn-disabled');
            btnOpen.innerText = t("focus_door_btn_open");
        }
    } else {
        title.innerText = t("focus_object_none");
        desc.innerText = t("focus_object_desc");
        btnListen.setAttribute('disabled', 'true');
        btnListen.classList.add('btn-disabled');
        btnOpen.setAttribute('disabled', 'true');
        btnOpen.classList.add('btn-disabled');
        btnOpen.innerText = t("focus_btn_default");
    }
}"""
patched_content = patched_content.replace(old_focused_object_ui, new_focused_object_ui)

# 31. update applyLanguage to initialize and update state.language and set page title
apply_lang_old = """function applyLanguage(lang) {
    if (typeof LANGUAGES === 'undefined' || !LANGUAGES[lang]) return;
    const t_dict = LANGUAGES[lang];"""

apply_lang_new = """function applyLanguage(lang) {
    if (typeof LANGUAGES === 'undefined' || !LANGUAGES[lang]) return;
    if (typeof state !== 'undefined') {
        state.language = lang;
    }
    const t_dict = LANGUAGES[lang];
    if (t_dict['game_title']) {
        document.title = t_dict['game_title'];
    }"""
patched_content = patched_content.replace(apply_lang_old, apply_lang_new)


# ================== NEW V5 REPLACEMENTS FOR EXHAUSTIVE TRANSLATIONS ==================

# 32. Floor event logs
patched_content = patched_content.replace(
    'logToConsole("Свет на этом этаже нестабилен. Энергосеть перегружена.", "warn");',
    'logToConsole(t("log_event_flicker"), "warn");'
)
patched_content = patched_content.replace(
    'logToConsole("ВНИМАНИЕ: Слышно шипение труб. В коридоре утечка газа Самосбора!", "danger");',
    'logToConsole(t("log_event_gas_leak"), "danger");'
)
patched_content = patched_content.replace(
    'logToConsole("На полу впереди лежит неподвижное тело ликвидатора...", "sys");',
    'logToConsole(t("log_event_corpse"), "sys");'
)
patched_content = patched_content.replace(
    'logToConsole("Леденящий сквозняк... В глубине коридора промелькнул силуэт.", "sys");',
    'logToConsole(t("log_event_ghost"), "sys");'
)

# 33. Crawler sounds and attack
patched_content = patched_content.replace(
    'logToConsole("Вы слышите жуткий, шуршащий звук когтей по бетону откуда-то впереди...", "warn");',
    'logToConsole(t("log_crawler_sound"), "warn");'
)
patched_content = patched_content.replace(
    'logToConsole("ТВАРЬ НАПАЛА НА ВАС! Своими жвалами она прокусила вам скафандр!", "danger");',
    'logToConsole(t("log_crawler_attack"), "danger");'
)

# 34. Upper floor blocked and floor climb
patched_content = patched_content.replace(
    'logToConsole("Верхние этажи заблокированы гермозатвором. Прохода нет.", "warn");',
    'logToConsole(t("log_stairs_up_blocked"), "warn");'
)
patched_content = patched_content.replace(
    'logToConsole(`Вы поднялись на этаж ${state.floor}.`, "sys");',
    'logToConsole(t("log_ascend_floor", state.floor), "sys");'
)

# 35. Gas mask corrosion warn during active Samosbor
patched_content = patched_content.replace(
    'logToConsole("Противогаз защищает от газа, но химикаты разъедают костюм...", "warn");',
    'logToConsole(t("log_gasmask_protects_but_corrodes"), "warn");'
)

# 36. Note locked title tab in restart/initialization
patched_content = patched_content.replace(
    'tab.innerText = `Записка ${i + 1}`;',
    'tab.innerText = t("note_title_num", i + 1);'
)

# 37. Web Audio API initialization error
patched_content = patched_content.replace(
    'console.error("Не удалось запустить Web Audio API: ", e);',
    'console.error(t("log_web_audio_error"), e);'
)

# 38. SDK initialization states
patched_content = patched_content.replace(
    'completeInitialization("РЕЖИМ: ОФФЛАЙН (ДЕМО)");',
    'completeInitialization(t("sdk_offline_demo"));'
)
patched_content = patched_content.replace(
    'completeInitialization("SDK ГОТОВ");',
    'completeInitialization(t("sdk_ready"));'
)
patched_content = patched_content.replace(
    'completeInitialization("РЕЖИМ: ДЕМО");',
    'completeInitialization(t("sdk_demo"));'
)
patched_content = patched_content.replace(
    'completeInitialization("РЕЖИМ: ОФФЛАЙН");',
    'completeInitialization(t("sdk_offline"));'
)

# 39. Transition descent overlay floor text
patched_content = patched_content.replace(
    'overlayText.innerText = `ЭТАЖ ${state.floor}`;',
    'overlayText.innerText = t("transition_floor_num", state.floor);'
)

# 40. Battery count suffix
patched_content = patched_content.replace(
    '${state.batteries} шт',
    '${t("battery_qty", state.batteries)}'
)

# 41. Apartment entry messages
old_apt_entries = """        if (door.roomType === 'armory') {
            logToConsole(`Вы вошли в ${door.name}. На стене висит знак Ликвидаторов. Под ногами рассыпаны гильзы.`, "sys");
        } else if (door.roomType === 'contaminated') {
            logToConsole(`Вы вошли в ${door.name}. Воздух здесь едкий и желтоватый. Счетчик Гейгера тихо потрескивает! (Фильтр тратится быстрее)`, "danger");
        } else if (door.roomType === 'nest') {
            logToConsole(`Вы вошли в ${door.name}. В углу копошится склизкая биомасса. Старайтесь не шуметь!`, "warn");
        } else {
            logToConsole(`Вы вошли в квартиру. Вокруг обычная серая обстановка советской квартиры-хрущевки.`, "sys");
        }"""

new_apt_entries = """        if (door.roomType === 'armory') {
            logToConsole(t("log_enter_apt_clean", getLocalizedDoorName(door)), "sys");
        } else if (door.roomType === 'contaminated') {
            logToConsole(t("log_enter_apt_gas", getLocalizedDoorName(door)), "danger");
        } else if (door.roomType === 'nest') {
            logToConsole(t("log_enter_apt_slime", getLocalizedDoorName(door)), "warn");
        } else {
            logToConsole(t("log_enter_apt_default"), "sys");
        }"""
patched_content = patched_content.replace(old_apt_entries, new_apt_entries)

# 42. Ghost whispers
old_ghost_whispers = """                const creepyLogs = [
                    "Призрак шепчет: 'Здесь нет выхода... только бесконечные этажи...'",
                    "Призрак шепчет: 'Они видят тебя... они всегда видят...'",
                    "Призрак шепчет: 'Остановись... прими Самосбор...'",
                    "Призрак шепчет: 'Ликвидатор 1324... твоя смена окончена...'"
                ];"""

new_ghost_whispers = """                const creepyLogs = [
                    t("log_ghost_whisper_1"),
                    t("log_ghost_whisper_2"),
                    t("log_ghost_whisper_3"),
                    t("log_ghost_whisper_4")
                ];"""
patched_content = patched_content.replace(old_ghost_whispers, new_ghost_whispers)

# 43. Ghost dissolve
patched_content = patched_content.replace(
    'logToConsole("Призрак закричал от боли и растаял в луче света вашего фонаря!", "sys");',
    'logToConsole(t("log_ghost_dissolve"), "sys");'
)

# 44. Loot items generation hardcoded label strings (kitchen & normal)
old_kitchen_loot = """        if (isKitchen) {
            if (r < 0.30) item = {type: 'junk', label: 'Мусор', icon: ''};
            else if (r < 0.60) item = {type: 'water', count: 25, label: 'Фляга воды (+25%)', icon: ''};
            else if (r < 0.80) item = {type: 'bandage', count: 1, label: 'Бинт', icon: ''};
            else item = {type: 'filter', count: 25, label: 'Фильтр (+25%)', icon: ''};
        } else {
            if (r < 0.12) item = {type: 'junk', label: 'Мусор', icon: ''};
            else if (r < 0.28) {
                const cnt = roomType === 'armory' ? 12 : 6;
                item = {type: 'ammo', count: cnt, label: 'Патроны (+' + cnt + ' шт.)', icon: ''};
            }
            else if (r < 0.42) item = {type: 'bandage', count: 1, label: 'Бинт', icon: ''};
            else if (r < 0.56) item = {type: 'water', count: 30, label: 'Фляга воды (+30%)', icon: ''};
            else if (r < 0.68) item = {type: 'battery', count: 1, label: 'Батарейка', icon: ''};
            else if (r < 0.78) item = {type: 'filter', count: 30, label: 'Фильтр (+30%)', icon: ''};
            else if (r < 0.88) item = {type: 'note', label: 'Записка', icon: ''};
            else if (r < 0.95 && !state.hasHackerTool) item = {type: 'hacker_tool', label: 'Дешифратор гермозатворов', icon: ''};
            else item = {type: 'bandage', count: 1, label: 'Бинт', icon: ''};
        }"""

new_kitchen_loot = """        if (isKitchen) {
            if (r < 0.30) item = {type: 'junk', label: 'Junk', icon: ''};
            else if (r < 0.60) item = {type: 'water', count: 25, label: 'Water', icon: ''};
            else if (r < 0.80) item = {type: 'bandage', count: 1, label: 'Bandage', icon: ''};
            else item = {type: 'filter', count: 25, label: 'Filter', icon: ''};
        } else {
            if (r < 0.12) item = {type: 'junk', label: 'Junk', icon: ''};
            else if (r < 0.28) {
                const cnt = roomType === 'armory' ? 12 : 6;
                item = {type: 'ammo', count: cnt, label: 'Ammo', icon: ''};
            }
            else if (r < 0.42) item = {type: 'bandage', count: 1, label: 'Bandage', icon: ''};
            else if (r < 0.56) item = {type: 'water', count: 30, label: 'Water', icon: ''};
            else if (r < 0.68) item = {type: 'battery', count: 1, label: 'Battery', icon: ''};
            else if (r < 0.78) item = {type: 'filter', count: 30, label: 'Filter', icon: ''};
            else if (r < 0.88) item = {type: 'note', label: 'Note', icon: ''};
            else if (r < 0.95 && !state.hasHackerTool) item = {type: 'hacker_tool', label: 'Decrypter', icon: ''};
            else item = {type: 'bandage', count: 1, label: 'Bandage', icon: ''};
        }"""
patched_content = patched_content.replace(old_kitchen_loot, new_kitchen_loot)

patched_content = patched_content.replace(
    "door.lootItems.unshift({type: 'hacker_tool', label: 'Дешифратор гермозатворов', icon: ''});",
    "door.lootItems.unshift({type: 'hacker_tool', label: 'Decrypter', icon: ''});"
)

# 45. Door generation default name strings
patched_content = patched_content.replace(
    'door.name = `Переход ${sec}-${secNum}`;',
    'door.name = `Transition ${sec}-${secNum}`;'
)
patched_content = patched_content.replace(
    'door.name = `Секция ${Math.floor(Math.random() * 90 + 10)}`;',
    'door.name = `Section ${Math.floor(Math.random() * 90 + 10)}`;'
)


# Save patched app.js
with open('app.js', 'w', encoding='utf-8') as f:
    f.write(patched_content)

print("\nSuccessfully patched all app.js file code and translations!")
