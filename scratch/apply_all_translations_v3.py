import sys
import os
import re
import shutil
import json

sys.stdout.reconfigure(encoding='utf-8')

print("Starting complete translation application script (V3)...")

# 1. Restore app.js from backup if it exists
backup_path = 'scratch/app_backup_before_clean.js'
if os.path.exists(backup_path):
    shutil.copy2(backup_path, 'app.js')
    print("Restored app.js from scratch/app_backup_before_clean.js")
else:
    print("No backup found, patching app.js directly")

# 2. Load base LANGUAGES from build_translations.py
sys.path.append('scratch')
from build_translations import LANGUAGES

# 3. Read key multi-line strings from apply_translations.py and apply_translations_round2.py
namespace1 = {}
with open('scratch/apply_translations.py', 'r', encoding='utf-8') as f:
    exec(f.read(), namespace1)

namespace2 = {}
with open('scratch/apply_translations_round2.py', 'r', encoding='utf-8') as f:
    exec(f.read(), namespace2)

def parse_keys_str(keys_str):
    res = {}
    pattern = r'"([a-zA-Z0-9_]+)"\s*:\s*"((?:[^"\\]|\\.)*)"'
    for k, v in re.findall(pattern, keys_str):
        v_clean = v.replace('\\"', '"')
        res[k] = v_clean
    return res

# Custom keys to add
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
        "focus_btn_default": "Взаимодействовать"
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
        "focus_btn_default": "Interact"
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
        "focus_corpse_title": "清理人员尸体",
        "focus_corpse_desc": "身穿制服的已故清理人员。搜寻小袋 (R 键)。",
        "focus_corpse_btn": "搜寻尸体",
        "focus_spawn_door_title": "分区密封闸门",
        "focus_spawn_door_desc": "分区外侧气密舱。沉重的钢材。按 B 进行解密。",
        "focus_spawn_door_btn": "尝试破解",
        "focus_stairs_door_title": "楼梯井密封闸门",
        "focus_stairs_door_desc_locked": "被巨型赫鲁晓夫楼中央系统锁死。",
        "focus_stairs_door_btn_try": "尝试破解",
        "focus_stairs_door_desc_open": "闸门已开。去往楼梯의 通道已畅通。",
        "focus_stairs_door_btn_close": "关闭闸门",
        "focus_stairs_door_desc_closed": "沉重的密封闸门已锁！按 B 进行破解。",
        "focus_stairs_door_btn_hack": "破解闸门",
        "focus_door_desc_open": "门已开。你可以进入内部 (通过 WASD 行走)。",
        "focus_door_btn_close": "关闭门",
        "focus_door_desc_closed": "密封门已关。请靠近。",
        "focus_door_btn_open": "打开门",
        "focus_object_none": "未选择对象",
        "focus_object_desc": "靠近门或可交互对象",
        "focus_btn_default": "交互"
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
        "focus_btn_default": "Interagieren"
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
        "focus_btn_default": "Interagisci"
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
        "focus_btn_default": "Interactuar"
    }
}

# 4. Merge all keys into LANGUAGES
for lang in ["ru", "en", "zh", "de", "it", "es"]:
    keys_str_1 = namespace1[f"{lang.upper()}_KEYS"]
    keys_str_2 = namespace2[f"{lang.upper()}_KEYS"]
    
    dict1 = parse_keys_str(keys_str_1)
    dict2 = parse_keys_str(keys_str_2)
    custom_dict = CUSTOM_KEYS[lang]
    
    # Merge them into build_translations' LANGUAGES
    LANGUAGES[lang].update(dict1)
    LANGUAGES[lang].update(dict2)
    LANGUAGES[lang].update(custom_dict)
    
    print(f"Language '{lang}' has now {len(LANGUAGES[lang])} total keys.")

# 5. Read app.js content
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

# 16. bagBatteries formatting (just in case, but it's fine)

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
log_to_console_prefix_old = """    let prefix = '';
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
# Let's replace the entire function body since we have its exact code
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

# 31. update applyLanguage to initialize and update state.language
apply_lang_old = """function applyLanguage(lang) {
    if (typeof LANGUAGES === 'undefined' || !LANGUAGES[lang]) return;
    const t_dict = LANGUAGES[lang];"""

apply_lang_new = """function applyLanguage(lang) {
    if (typeof LANGUAGES === 'undefined' || !LANGUAGES[lang]) return;
    if (typeof state !== 'undefined') {
        state.language = lang;
    }
    const t_dict = LANGUAGES[lang];"""
patched_content = patched_content.replace(apply_lang_old, apply_lang_new)

# Save patched app.js
with open('app.js', 'w', encoding='utf-8') as f:
    f.write(patched_content)

print("\nSuccessfully patched all app.js file code and translations!")
