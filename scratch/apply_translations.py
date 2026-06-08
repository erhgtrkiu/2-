import re
import sys

# Set encoding for console output
sys.stdout.reconfigure(encoding='utf-8')

print("Starting translations application script...")

# Load dictionaries for languages to inject
RU_KEYS = """
        "loot_title": "НАЙДЕННЫЕ ПРЕДМЕТЫ",
        "loot_title_kitchen": "КУХНЯ: НАЙДЕННЫЕ ПРЕДМЕТЫ",
        "loot_empty": "Пусто. Ничего полезного не найдено.",
        "loot_take": "Забрать",
        "loot_junk": "Хлам",
        "loot_take_all": "Забрать всё",
        "loot_close": "Закрыть",
        "loot_item_junk": "Мусор",
        "loot_item_water": "Фляга воды (+{0}%)",
        "loot_item_bandage": "Бинт",
        "loot_item_filter": "Фильтр (+{0}%)",
        "loot_item_ammo": "Патроны (+{0} шт.)",
        "loot_item_battery": "Батарейка",
        "loot_item_note": "Записка",
        "loot_item_hacker_tool": "Дешифратор гермозатворов",
        "room_bedroom_searched": "Спальня обыскана",
        "room_bedroom_search": "Обыскать спальню",
        "room_kitchen_searched": "Кухня обыскана",
        "room_kitchen_search": "Обыскать кухню",
        "room_already_searched": "Уже обыскано",
        "door_apartment_2room": "Квартира {0} (2-комнатная)",
        "log_no_bandages": "У вас нет бинтов.",
        "log_healthy": "Вы абсолютно здоровы, бинт не нужен.",
        "log_bandage_used": "Вы туго перевязали раны бинтом (+35% здоровья).",
        "log_stairs_monster_threat": "[УГРОЗА] ИЗ ТЕМНОТЫ ЛЕСТНИЧНОЙ ШАХТЫ НА ВАС КИДАЕТСЯ МНОГОНОГАЯ ТВАРЬ!",
        "log_stairs_monster_shoot_time": "У вас есть 4 секунды, чтобы выстрелить из пистолета и спугнуть её!",
        "log_kick_hit": "УДАР! Вы пнули тварь! Она отлетела назад и взвизгнула!",
        "log_kick_kill": "Вы забили тварь ногами до смерти!",
        "log_kick_air": "Вы пнули воздух.",
        "log_no_ammo": "Сухой щелчок бойка... Патронов нет!",
        "log_shoot": "Грохот выстрела раскатился по бетонному колодцу этажа!",
        "log_shoot_kill": "Точный выстрел разорвал тварь! По коридору разлетелись брызги слизи.",
        "log_shoot_hit": "Пуля пробила хитиновый панцирь твари! Она яростно завизжала.",
        "log_stairs_monster_scared": "Тварь издала пронзительный визг и скрылась в вентиляционном канале.",
        "log_shoot_empty": "Вы выстрелили впустую в бетонные перекрытия.",
        "log_gate_closed_descending": "Шлюз герметично захлопнулся сзади. Грохот гидравлики уносит вас вниз.",
        "log_descent_complete": "Спуск завершен. Вы вышли на этаже {0}. Дверь заблокирована сзади.",
        "log_door_tightened": "Вы закрутили ручной прижим гермодвери изнутри. Теперь комната герметична.",
        "log_door_untightened": "Затвор двери открыт. Комната больше не защищает от внешней среды.",
        "log_exited_to_hallway": "Вы вышли обратно в бетонный коридор сектора.",
        "log_approach_door_to_lock": "Подойдите ближе к гермодвери коридора, чтобы запереть или отпереть её.",
        "log_start_shift_floor": "Начало новой смены ликвидации. Спуск с 1324 этажа...",
        "log_hack_cancelled": "Взлом прерван игроком.",
        "log_approach_furniture": "Подойдите ближе к мебели.",
        "log_ending_freeze_wait": "Вы закрыли глаза, расслабились и решили остаться на месте...",
        "log_air_hazard": "Вы вдыхаете зараженный воздух! Срочно наденьте противогаз (клавиша T)!",
        "log_gas_leak_suffocate": "Вы задыхаетесь в коридоре с утечкой газа! Наденьте противогаз (клавиша T)!",
        "log_filter_clogged": "Фильтр противогаза полностью забился! Маска бесполезна!",
        "log_samosbor_active_start": "[!!!] САМОСБОР НАЧАЛСЯ! ТОКСИЧНЫЙ ТУМАН ЗАПОЛНЯЕТ СЕКТОРЫ!",
        "log_samosbor_toxic_lungs": "Токсичный туман разъедает ваши легкие!",
        "log_gasmask_suit_corrode": "Противогаз защищает от газа, но химикаты разъедают костюм...",
        "log_gas_seeping_door": "Газ проникает под дверь! Вы не заблокировали гермозатвор!",
        "log_door_holding_rumble": "Гермозатвор держит. Вы слышите грохот за дверью.",
        "log_no_hacker_tool": "У вас нет взломщика гермодверей! Обыщите квартиры, чтобы найти его.",
        "log_hacker_battery_empty": "Батарея взломщика разряжена! Найдите батарейки в квартирах.",
        "log_hacker_final_floor_error": "Взломщик: Ошибка доступа. Затвор заблокирован центральной системой ГИГАХРУЩА. Это устройство здесь бесполезно!",
        "go_note_not_found": "[✗] ЗАПИСКА {0} (НЕ НАЙДЕНА)",
        "go_note_missing_desc": "Вы упустили этот фрагмент истории на этажах Хрущевки. Обыскивайте комнаты, чтобы найти её.",
        "hack_sig_aligned": "СИГНАЛ: ВЫРАВНИВАНИЕ (КЛИКНИТЕ СОЕДИНЕНИЕ)",
        "hack_sig_weak": "СИГНАЛ: СЛАБЫЙ (ШУМ)",
        "hack_sig_interference": "СИГНАЛ: ПОМЕХИ",
        "hack_sig_mismatch": "СИГНАЛ: РАССОГЛАСОВАНИЕ",
        "log_ach_unlocked": "ДОСТИЖЕНИЕ ПОЛУЧЕНО: \\"{0}\\"!",
        "ach_secret_title": "Секретное достижение",
        "ach_secret_hint": "Пройдите игру, чтобы открыть подробности",
        "ach_status_unlocked": "ПОЛУЧЕНО",
        "ach_status_locked": "ЗАБЛОКИРОВАНО",
        "log_drink_full": "Вы не хотите пить.",
        "log_bottle_empty": "Ваша фляга пуста! Найдите воду в жилых комнатах.",
        "log_drink_quenched": "Вы утолили жажду полностью.",
        "log_approach_gate": "Подойдите ближе к гермозатвору.",
        "note_tab_locked": "Записка {0}",
        "btn_bandage": "Бинт: {0}",
        "btn_bag_format": "Сумка (Записки: {0}/10)",
        "log_prefix_warn": "[ВНИМАНИЕ]",
        "log_prefix_danger": "[ОПАСНОСТЬ]",
        "log_prefix_loot": "[НАХОДКА]",
        "log_prefix_sys": "[СИС]"
"""

EN_KEYS = """
        "loot_title": "FOUND ITEMS",
        "loot_title_kitchen": "KITCHEN: FOUND ITEMS",
        "loot_empty": "Empty. Nothing useful found.",
        "loot_take": "Take",
        "loot_junk": "Junk",
        "loot_take_all": "Take All",
        "loot_close": "Close",
        "loot_item_junk": "Junk",
        "loot_item_water": "Water flask (+{0}%)",
        "loot_item_bandage": "Bandage",
        "loot_item_filter": "Filter (+{0}%)",
        "loot_item_ammo": "Ammo (+{0} pcs.)",
        "loot_item_battery": "Battery",
        "loot_item_note": "Note",
        "loot_item_hacker_tool": "Gate decrypter",
        "room_bedroom_searched": "Bedroom searched",
        "room_bedroom_search": "Search bedroom",
        "room_kitchen_searched": "Kitchen searched",
        "room_kitchen_search": "Search kitchen",
        "room_already_searched": "Already searched",
        "door_apartment_2room": "Apartment {0} (2-room)",
        "log_no_bandages": "You don't have bandages.",
        "log_healthy": "You are perfectly healthy, bandage not needed.",
        "log_bandage_used": "You tightly wrapped wounds with a bandage (+35% health).",
        "log_stairs_monster_threat": "[THREAT] A MULTI-LEGGED BEAST LUNGES AT YOU FROM THE DARKNESS OF THE STAIRWELL!",
        "log_stairs_monster_shoot_time": "You have 4 seconds to fire the pistol and scare it off!",
        "log_kick_hit": "KICK! You kicked the beast! It flew back and shrieked!",
        "log_kick_kill": "You kicked the beast to death!",
        "log_kick_air": "You kicked the air.",
        "log_no_ammo": "Dry click of the striker... Out of ammo!",
        "log_shoot": "The roar of the gunshot rolled through the concrete stairwell!",
        "log_shoot_kill": "A precise shot tore the beast apart! Slime splattered across the hallway.",
        "log_shoot_hit": "The bullet pierced the beast's chitinous armor! It screamed furiously.",
        "log_stairs_monster_scared": "The beast emitted a piercing shriek and vanished into the ventilation duct.",
        "log_shoot_empty": "You shot in vain into the concrete ceilings.",
        "log_gate_closed_descending": "The hatch slammed hermetically shut behind. The rumble of hydraulics carries you down.",
        "log_descent_complete": "Descent complete. You stepped out on floor {0}. The door is locked behind.",
        "log_door_tightened": "You tightened the manual blast door clamp from inside. The room is now airtight.",
        "log_door_untightened": "The door latch is open. The room no longer protects against the external environment.",
        "log_exited_to_hallway": "You walked back out into the concrete corridor of the sector.",
        "log_approach_door_to_lock": "Get closer to the corridor blast door to lock or unlock it.",
        "log_start_shift_floor": "Beginning of a new liquidation shift. Descent from the 1324th floor...",
        "log_hack_cancelled": "Hacking cancelled by player.",
        "log_approach_furniture": "Get closer to the furniture.",
        "log_ending_freeze_wait": "You closed your eyes, relaxed, and decided to stay in place...",
        "log_air_hazard": "You are inhaling contaminated air! Put on your gas mask immediately (T key)!",
        "log_gas_leak_suffocate": "You are suffocating in a corridor with a gas leak! Put on your gas mask (T key)!",
        "log_filter_clogged": "The gas mask filter is completely clogged! The mask is useless!",
        "log_samosbor_active_start": "[!!!] SAMOSBOR HAS BEGUN! TOXIC FOG IS FILLING THE SECTORS!",
        "log_samosbor_toxic_lungs": "Toxic fog corrodes your lungs!",
        "log_gasmask_suit_corrode": "The gas mask protects against gas, but chemicals corrode the suit...",
        "log_gas_seeping_door": "Gas seeps under the door! You did not lock the blast door!",
        "log_door_holding_rumble": "The blast door holds. You hear a rumble behind the door.",
        "log_no_hacker_tool": "You do not have a blast door decrypter! Search apartments to find it.",
        "log_hacker_battery_empty": "Decrypter battery is empty! Find batteries in apartments.",
        "log_hacker_final_floor_error": "Decrypter: Access error. Gate is locked by the GIGA-KHRUSHCHEVKA central system. This device is useless here!",
        "go_note_not_found": "[✗] NOTE {0} (NOT FOUND)",
        "go_note_missing_desc": "You missed this piece of history on the floors of the Khrushchovya. Search rooms to find it.",
        "hack_sig_aligned": "SIGNAL: ALIGNED (CLICK CONNECT)",
        "hack_sig_weak": "SIGNAL: WEAK (NOISE)",
        "hack_sig_interference": "SIGNAL: INTERFERENCE",
        "hack_sig_mismatch": "SIGNAL: MISMATCH",
        "log_ach_unlocked": "ACHIEVEMENT UNLOCKED: \\"{0}\\"!",
        "ach_secret_title": "Secret Achievement",
        "ach_secret_hint": "Complete the game to unlock details",
        "ach_status_unlocked": "UNLOCKED",
        "ach_status_locked": "LOCKED",
        "log_drink_full": "You are not thirsty.",
        "log_bottle_empty": "Your bottle is empty! Find water in rooms.",
        "log_drink_quenched": "You have fully quenched your thirst.",
        "log_approach_gate": "Approach closer to the blast gate.",
        "note_tab_locked": "Note {0}",
        "btn_bandage": "Bandage: {0}",
        "btn_bag_format": "Bag (Notes: {0}/10)",
        "log_prefix_warn": "[WARNING]",
        "log_prefix_danger": "[DANGER]",
        "log_prefix_loot": "[FIND]",
        "log_prefix_sys": "[SYS]"
"""

ZH_KEYS = """
        "loot_title": "发现物品",
        "loot_title_kitchen": "厨房: 发现物品",
        "loot_empty": "空。未发现有用物品。",
        "loot_take": "收取",
        "loot_junk": "垃圾",
        "loot_take_all": "全部收取",
        "loot_close": "关闭",
        "loot_item_junk": "垃圾",
        "loot_item_water": "水壶 (+{0}%)",
        "loot_item_bandage": "绷带",
        "loot_item_filter": "滤毒罐 (+{0}%)",
        "loot_item_ammo": "弹药 (+{0} 发)",
        "loot_item_battery": "电池",
        "loot_item_note": "便签",
        "loot_item_hacker_tool": "闸门破解器",
        "room_bedroom_searched": "卧室已搜寻",
        "room_bedroom_search": "搜寻卧室",
        "room_kitchen_searched": "厨房已搜寻",
        "room_kitchen_search": "搜寻厨房",
        "room_already_searched": "已搜寻过",
        "door_apartment_2room": "公寓 {0} (双室)",
        "log_no_bandages": "你没有绷带。",
        "log_healthy": "你非常健康，不需要绷带。",
        "log_bandage_used": "你用绷带包扎了伤口 (+35% 生命值)。",
        "log_stairs_monster_threat": "[威胁] 一只多足巨兽从暗无天日的楼梯井朝你扑来！",
        "log_stairs_monster_shoot_time": "你有 4 秒钟时间开枪惊吓它！",
        "log_kick_hit": "踢击！你踢中了怪物！它向后飞去并发出尖叫！",
        "log_kick_kill": "你用脚把怪物踩死了！",
        "log_kick_air": "你踢空了。",
        "log_no_ammo": "击针空响... 没有弹药！",
        "log_shoot": "枪声在楼层混凝土井道中回荡！",
        "log_shoot_kill": "精准的一枪将怪物击碎！粘液溅满了走廊。",
        "log_shoot_hit": "子弹击穿了怪物的几丁质外壳！它愤怒地嘶鸣。",
        "log_stairs_monster_scared": "怪物发出一声刺耳的尖叫，消失在通风管道中。",
        "log_shoot_empty": "你对着混凝土天花板放了空枪。",
        "log_gate_closed_descending": "身后的气密闸门轰然关闭。液压传动的轰鸣声带你下降。",
        "log_descent_complete": "下降完成。你来到了第 {0} 层。身后的门已被锁死。",
        "log_door_tightened": "你从内部拧紧了手动气密门夹。房间现在气密了。",
        "log_door_untightened": "门栓已打开。该房间不再能防御外部环境。",
        "log_exited_to_hallway": "你走回到了分区的混凝土走廊。",
        "log_approach_door_to_lock": "靠近通道密封防爆门以进行锁定或解锁。",
        "log_start_shift_floor": "开始新的清理值班。从 1324 层降落...",
        "log_hack_cancelled": "玩家取消了破解。",
        "log_approach_furniture": "靠近家具。",
        "log_ending_freeze_wait": "你闭上眼睛，放松下来，决定留在原地...",
        "log_air_hazard": "你正在吸入被污染的空气！请迅速戴上防毒面具 (T 键)！",
        "log_gas_leak_suffocate": "你在有瓦斯泄露的走廊中窒息！戴上防毒面具 (T 键)！",
        "log_filter_clogged": "防毒面具滤毒罐已完全堵塞！面具失效了！",
        "log_samosbor_active_start": "[!!!] 萨摩斯堡已开始！剧毒雾气正在充满分区！",
        "log_samosbor_toxic_lungs": "剧毒雾气正在腐蚀你的肺部！",
        "log_gasmask_suit_corrode": "防毒面具可以阻挡毒气，但化学物质正在腐蚀防护服...",
        "log_gas_seeping_door": "毒气从门下渗入！你没有锁好防爆门！",
        "log_door_holding_rumble": "密封防爆门顶住了。你听到门外传来隆隆声。",
        "log_no_hacker_tool": "你没有闸门破解器！去公寓搜寻以找到它。",
        "log_hacker_battery_empty": "破解器电池已耗尽！在公寓中寻找电池。",
        "log_hacker_final_floor_error": "破解器: 访问错误。闸门已被巨型赫鲁晓夫楼中央系统锁死。此设备在此处无用！",
        "go_note_not_found": "[✗] 便签 {0} (未发现)",
        "go_note_missing_desc": "你在赫鲁晓夫楼的楼层中错过了这段历史。搜寻房间来找到它。",
        "hack_sig_aligned": "信号: 对齐 (点击连接)",
        "hack_sig_weak": "信号: 微弱 (噪声)",
        "hack_sig_interference": "信号: 干扰",
        "hack_sig_mismatch": "信号: 不匹配",
        "log_ach_unlocked": "解锁成就: \\"{0}\\"!",
        "ach_secret_title": "秘密成就",
        "ach_secret_hint": "通关游戏以解锁详情",
        "ach_status_unlocked": "已解锁",
        "ach_status_locked": "未解锁",
        "log_drink_full": "你不想喝水。",
        "log_bottle_empty": "你的水壶空了！去房间里找水。",
        "log_drink_quenched": "你完全解渴了。",
        "log_approach_gate": "靠近闸门。",
        "note_tab_locked": "便签 {0}",
        "btn_bandage": "绷带: {0}",
        "btn_bag_format": "背包 (便签: {0}/10)",
        "log_prefix_warn": "[注意]",
        "log_prefix_danger": "[危险]",
        "log_prefix_loot": "[发现]",
        "log_prefix_sys": "[系统]"
"""

DE_KEYS = """
        "loot_title": "GEFUNDENE GEGENSTÄNDE",
        "loot_title_kitchen": "KÜCHE: GEFUNDENE GEGENSTÄNDE",
        "loot_empty": "Leer. Nichts Nützliches gefunden.",
        "loot_take": "Nehmen",
        "loot_junk": "Müll",
        "loot_take_all": "Alles nehmen",
        "loot_close": "Schließen",
        "loot_item_junk": "Müll",
        "loot_item_water": "Wasserflasche (+{0}%)",
        "loot_item_bandage": "Bandage",
        "loot_item_filter": "Filter (+{0}%)",
        "loot_item_ammo": "Munition (+{0} Stk.)",
        "loot_item_battery": "Batterie",
        "loot_item_note": "Notiz",
        "loot_item_hacker_tool": "Schutzschott-Decoder",
        "room_bedroom_searched": "Schlafzimmer durchsucht",
        "room_bedroom_search": "Schlafzimmer durchsuchen",
        "room_kitchen_searched": "Küche durchsucht",
        "room_kitchen_search": "Küche durchsuchen",
        "room_already_searched": "Bereits durchsucht",
        "door_apartment_2room": "Wohnung {0} (2-Zimmer)",
        "log_no_bandages": "Du hast keine Bandagen.",
        "log_healthy": "Du bist kerngesund, Bandage wird nicht benötigt.",
        "log_bandage_used": "Sie haben Wunden fest mit einer Bandage verbunden (+35% Gesundheit).",
        "log_stairs_monster_threat": "[BEDROHUNG] EIN MEHRBEINIGES BIEST STÜRZT SICH AUS DER DUNKELHEIT DES TREPPENHAUSES AUF SIE!",
        "log_stairs_monster_shoot_time": "Sie haben 4 Sekunden Zeit, um mit der Pistole zu schießen und es zu vertreiben!",
        "log_kick_hit": "TRITT! Sie haben das Biest getreten! Es flog zurück und kreischte!",
        "log_kick_kill": "Sie haben das Biest zu Tode getreten!",
        "log_kick_air": "Sie haben in die Luft getreten.",
        "log_no_ammo": "Trockenes Klicken des Schlagbolzens... Keine Munition!",
        "log_shoot": "Das Dröhnen des Schusses hallte durch das Betontreppenhaus!",
        "log_shoot_kill": "Ein präziser Schuss riss das Biest in Stücke! Schleimspritzer verteilten sich im Flur.",
        "log_shoot_hit": "Die Kugel durchdrang den Chitinpanzer des Biests! Es schrie wütend.",
        "log_stairs_monster_scared": "Das Biest stieß einen gellenden Schrei aus und verschwand im Lüftungsschacht.",
        "log_shoot_empty": "Sie haben vergeblich in die Betondecken geschossen.",
        "log_gate_closed_descending": "Die Schleuse schloss sich hinter Ihnen hermetisch. Das Grollen der Hydraulik trägt Sie nach unten.",
        "log_descent_complete": "Abstieg abgeschlossen. Sie haben Etage {0} betreten. Die Tür hinter Ihnen ist verriegelt.",
        "log_door_tightened": "Sie haben die manuelle Panzertürklammer von innen festgezogen. Der Raum ist jetzt luftdicht.",
        "log_door_untightened": "Die Türklinke ist offen. Der Raum schützt nicht mehr vor der äußeren Umgebung.",
        "log_exited_to_hallway": "Sie sind zurück in den Betonflur des Sektors gegangen.",
        "log_approach_door_to_lock": "Nähern Sie sich der Panzertür des Flurs, um sie zu verriegeln oder zu entriegeln.",
        "log_start_shift_floor": "Beginn einer neuen Liquidationsschicht. Abstieg aus der 1324. Etage...",
        "log_hack_cancelled": "Hacken vom Spieler abgebrochen.",
        "log_approach_furniture": "Nähern Sie sich den Möbeln.",
        "log_ending_freeze_wait": "Sie schlossen die Augen, entspannten sich und beschlossen, an Ort und Stelle zu bleiben...",
        "log_air_hazard": "Sie atmen kontaminierte Luft ein! Gasmaske sofort aufsetzen (T-Taste)!",
        "log_gas_leak_suffocate": "Sie ersticken in einem Flur mit Gasleck! Gasmaske aufsetzen (T-Taste)!",
        "log_filter_clogged": "Der Gasmaskenfilter ist komplett verstopft! Die Maske ist nutzlos!",
        "log_samosbor_active_start": "[!!!] SAMOSBOR HAT BEGONNEN! GIFTIGER NEBEL FÜLLT DIE SEKTOREN!",
        "log_samosbor_toxic_lungs": "Giftiger Nebel zerfrisst Ihre Lunge!",
        "log_gasmask_suit_corrode": "Die Gasmaske schützt vor Gas, aber Chemikalien zerfressen den Anzug...",
        "log_gas_seeping_door": "Gas dringt unter der Tür durch! Sie haben das hermetische Tor nicht verriegelt!",
        "log_door_holding_rumble": "Das hermetische Tor hält. Sie hören ein Grollen hinter der Tür.",
        "log_no_hacker_tool": "Sie haben keinen hermetischen Tor-Decoder! Durchsuchen Sie die Wohnungen, um ihn zu finden.",
        "log_hacker_battery_empty": "Decoder-Batterie ist leer! Suchen Sie Batterien in den Wohnungen.",
        "log_hacker_final_floor_error": "Decoder: Zugriffsfehler. Das Tor ist durch das Zentralsystem der GIGA-CHRUSCHTSCHOWKA verriegelt. Dieses Gerät ist hier nutzlos!",
        "go_note_not_found": "[✗] NOTIZ {0} (NICHT GEFUNDEN)",
        "go_note_missing_desc": "Sie haben dieses Stück Geschichte in den Etagen der Chruschtschowka verpasst. Durchsuchen Sie die Zimmer, um es zu finden.",
        "hack_sig_aligned": "SIGNAL: AUSGERICHTET (VERBINDUNG KLICKEN)",
        "hack_sig_weak": "SIGNAL: SCHWACH (RAUSCHEN)",
        "hack_sig_interference": "SIGNAL: STÖRUNG",
        "hack_sig_mismatch": "SIGNAL: FEHLANPASSUNG",
        "log_ach_unlocked": "ERFOLG FREIGESCHALTET: \\"{0}\\"!",
        "ach_secret_title": "Geheimer Erfolg",
        "ach_secret_hint": "Beende das Spiel, um Details freizuschalten",
        "ach_status_unlocked": "FREIGESCHALTET",
        "ach_status_locked": "GESPERRT",
        "log_drink_full": "Du hast keinen Durst.",
        "log_bottle_empty": "Deine Flasche ist leer! Finde Wasser in den Zimmern.",
        "log_drink_quenched": "Du hast deinen Durst vollständig gelöscht.",
        "log_approach_gate": "Nähern Sie sich dem hermetischen Tor.",
        "note_tab_locked": "Notiz {0}",
        "btn_bandage": "Bandage: {0}",
        "btn_bag_format": "Tasche (Notizen: {0}/10)",
        "log_prefix_warn": "[WARNUNG]",
        "log_prefix_danger": "[GEFAHR]",
        "log_prefix_loot": "[FUND]",
        "log_prefix_sys": "[SYS]"
"""

IT_KEYS = """
        "loot_title": "OGGETTI TROVATI",
        "loot_title_kitchen": "CUCINA: OGGETTI TROVATI",
        "loot_empty": "Vuoto. Nessun oggetto utile trovato.",
        "loot_take": "Prendi",
        "loot_junk": "Rifiuto",
        "loot_take_all": "Prendi tutto",
        "loot_close": "Chiudi",
        "loot_item_junk": "Rifiuto",
        "loot_item_water": "Fiaschetta d'acqua (+{0}%)",
        "loot_item_bandage": "Benda",
        "loot_item_filter": "Filtro (+{0}%)",
        "loot_item_ammo": "Munizioni (+{0} pz)",
        "loot_item_battery": "Batteria",
        "loot_item_note": "Nota",
        "loot_item_hacker_tool": "Decrittatore porte",
        "room_bedroom_searched": "Camera da letto cercata",
        "room_bedroom_search": "Cerca in camera da letto",
        "room_kitchen_searched": "Cucina cercata",
        "room_kitchen_search": "Cerca in cucina",
        "room_already_searched": "Già cercato",
        "door_apartment_2room": "Appartamento {0} (2 stanze)",
        "log_no_bandages": "Non hai bende.",
        "log_healthy": "Sei perfettamente sano, la benda non è necessaria.",
        "log_bandage_used": "Hai fasciato strettamente le ferite con una benda (+35% salute).",
        "log_stairs_monster_threat": "[MINACCIA] UNA BESTIA CON MOLTE ZAMPE SI LANCIA SU DI TE DALL'OSCURITÀ DEL VANO SCALE!",
        "log_stairs_monster_shoot_time": "Hai 4 secondi per sparare con la pistola e spaventarla!",
        "log_kick_hit": "CALCIO! Hai calciato la bestia! È volata indietro e ha strillato!",
        "log_kick_kill": "Hai preso a calci la bestia fino a ucciderla!",
        "log_kick_air": "Hai calciato l'aria.",
        "log_no_ammo": "Clic a vuoto del percussore... Munizioni esaurite!",
        "log_shoot": "Il rombo dello sparo è rimbombato nel pozzo di cemento del piano!",
        "log_shoot_kill": "Uno sparo preciso ha fatto a pezzi la bestia! La melma si è sparsa per il corridoio.",
        "log_shoot_hit": "Il proiettile ha perforato la corazza chitinosa della bestia! Ha strillato furiosamente.",
        "log_stairs_monster_scared": "La bestia ha emesso uno strido acuto ed è svanita nel condotto di ventilazione.",
        "log_shoot_empty": "Hai sparato invano contro i soffitti di cemento.",
        "log_gate_closed_descending": "Il portello si è chiuso ermeticamente alle spalle. Il rombo dell'idraulica ti porta giù.",
        "log_descent_complete": "Discesa completata. Sei uscito al piano {0}. La porta è bloccata alle spalle.",
        "log_door_tightened": "Hai stretto la morsa manuale della porta blindata dall'interno. La stanza ora è ermetica.",
        "log_door_untightened": "La chiusura della porta è aperta. La stanza non protegge più dall'ambiente esterno.",
        "log_exited_to_hallway": "Sei tornato nel corridoio di cemento del settore.",
        "log_approach_door_to_lock": "Avvicinati alla porta blindata del corridoio per bloccarla o sbloccarla.",
        "log_start_shift_floor": "Inizio di un nuovo turno di liquidazione. Discesa dal 1324° piano...",
        "log_hack_cancelled": "Hacking annullato dal giocatore.",
        "log_approach_furniture": "Avvicinati ai mobili.",
        "log_ending_freeze_wait": "Hai chiuso gli occhi, ti sei rilassato e hai deciso di rimanere sul posto...",
        "log_air_hazard": "Stai inalando aria contaminata! Indossa immediatamente la maschera (tasto T)!",
        "log_gas_leak_suffocate": "Stai soffocando in un corridoio con una fuga di gas! Indossa la maschera (tasto T)!",
        "log_filter_clogged": "Il filtro della maschera antigas è completamente intasato! La maschera è inutile!",
        "log_samosbor_active_start": "[!!!] IL SAMOSBOR È COMINCIATO! LA NEBBIA TOSSICA STA RIEMPIENDO I SETTORI!",
        "log_samosbor_toxic_lungs": "La nebbia tossica ti corrode i polmoni!",
        "log_gasmask_suit_corrode": "La maschera antigas protegge dal gas, ma le sostanze chimiche corrodono la tuta...",
        "log_gas_seeping_door": "Il gas filtra sotto la porta! Non hai bloccato la porta ermetica!",
        "log_door_holding_rumble": "La porta ermetica tiene. Senti un rombo dietro la porta.",
        "log_no_hacker_tool": "Non hai un decrittatore per porte ermetiche! Cerca negli appartamenti per trovarlo.",
        "log_hacker_battery_empty": "La batteria del decrittatore è scarica! Trova le batterie negli appartamenti.",
        "log_hacker_final_floor_error": "Decrittatore: Errore di accesso. La porta è bloccata dal sistema centrale della GIGA-KHRUSHCHEVKA. Questo dispositivo è inutile qui!",
        "go_note_not_found": "[✗] NOTA {0} (NON TROVATA)",
        "go_note_missing_desc": "Hai perso questo frammento di storia sui piani della Khrushchevka. Cerca nelle stanze per trovarlo.",
        "hack_sig_aligned": "SEGNALE: ALLINEATO (CLICCA CONNETTI)",
        "hack_sig_weak": "SEGNALE: DEBOLE (RUMORE)",
        "hack_sig_interference": "SEGNALE: INTERFERENZA",
        "hack_sig_mismatch": "SEGNALE: DISALLINEAMENTO",
        "log_ach_unlocked": "OBIETTIVO SBLOCCATO: \\"{0}\\"!",
        "ach_secret_title": "Obiettivo Segreto",
        "ach_secret_hint": "Completa il gioco per sbloccare i dettagli",
        "ach_status_unlocked": "SBLOCCATO",
        "ach_status_locked": "BLOCCATO",
        "log_drink_full": "Non hai sete.",
        "log_bottle_empty": "La tua fiaschetta è vuota! Trova acqua nelle stanze.",
        "log_drink_quenched": "Hai dissetato completamente la tua sete.",
        "log_approach_gate": "Avvicinati alla porta ermetica.",
        "note_tab_locked": "Nota {0}",
        "btn_bandage": "Benda: {0}",
        "btn_bag_format": "Borsa (Note: {0}/10)",
        "log_prefix_warn": "[ATTENZIONE]",
        "log_prefix_danger": "[PERICOLO]",
        "log_prefix_loot": "[BOTTINO]",
        "log_prefix_sys": "[SIS]"
"""

ES_KEYS = """
        "loot_title": "OBJETOS ENCONTRADOS",
        "loot_title_kitchen": "COCINA: OBJETOS ENCONTRADOS",
        "loot_empty": "Vacío. No se encontró nada útil.",
        "loot_take": "Tomar",
        "loot_junk": "Basura",
        "loot_take_all": "Tomar todo",
        "loot_close": "Cerrar",
        "loot_item_junk": "Basura",
        "loot_item_water": "Frasco de agua (+{0}%)",
        "loot_item_bandage": "Vendaje",
        "loot_item_filter": "Filtro (+{0}%)",
        "loot_item_ammo": "Munición (+{0} uds.)",
        "loot_item_battery": "Batería",
        "loot_item_note": "Nota",
        "loot_item_hacker_tool": "Descifrador de compuertas",
        "room_bedroom_searched": "Dormitorio buscado",
        "room_bedroom_search": "Buscar en el dormitorio",
        "room_kitchen_searched": "Cocina buscada",
        "room_kitchen_search": "Buscar en la cocina",
        "room_already_searched": "Ya buscado",
        "door_apartment_2room": "Apartamento {0} (2 habitaciones)",
        "log_no_bandages": "No tienes vendajes.",
        "log_healthy": "Estás perfectamente sano, no necesitas vendaje.",
        "log_bandage_used": "Te vendaste firmemente las heridas con un vendaje (+35% de salud).",
        "log_stairs_monster_threat": "[AMENAZA] ¡UNA BESTIA MULTIPATA SE LANZA SOBRE TI DESDE LA OSCURIDAD DEL HUECO DE LA ESCALERA!",
        "log_stairs_monster_shoot_time": "¡Tienes 4 segundos para disparar la pistola y asustarla!",
        "log_kick_hit": "¡PATADA! ¡Pateaste a la bestia! ¡Salió volando hacia atrás y chilló!",
        "log_kick_kill": "¡Pateaste a la bestia hasta matarla!",
        "log_kick_air": "Pateaste el aire.",
        "log_no_ammo": "Click seco del percutor... ¡Sin munición!",
        "log_shoot": "¡El rugido del disparo resonó por el pozo de concreto del piso!",
        "log_shoot_kill": "¡Un disparo preciso destrozó a la bestia! Salpicaduras de limo se esparcieron por el pasillo.",
        "log_shoot_hit": "¡La bala atravesó el caparazón quitinoso de la bestia! Chilló con furia.",
        "log_stairs_monster_scared": "La bestia emitió un chillido agudo y desapareció en el conducto de ventilación.",
        "log_shoot_empty": "Disparaste en vano contra los techos de concreto.",
        "log_gate_closed_descending": "La escotilla se cerró herméticamente detrás. El estruendo de la hidráulica te lleva hacia abajo.",
        "log_descent_complete": "Descenso completo. Saliste al piso {0}. La puerta está cerrada detrás.",
        "log_door_tightened": "Apretaste la abrazadera manual de la puerta blindada desde el interior. La habitación ahora es hermética.",
        "log_door_untightened": "El pestillo de la puerta está abierto. La habitación ya no protege contra el ambiente externo.",
        "log_exited_to_hallway": "Volviste al pasillo de concreto del sector.",
        "log_approach_door_to_lock": "Acerca de la puerta blindada del pasillo para cerrarla o abrirla.",
        "log_start_shift_floor": "Comienzo de un nuevo turno de liquidación. Descenso desde el piso 1324...",
        "log_hack_cancelled": "Hackeo cancelado por el jugador.",
        "log_approach_furniture": "Acércate a los muebles.",
        "log_ending_freeze_wait": "Cerraste los ojos, te relajaste y decidiste quedarte en tu lugar...",
        "log_air_hazard": "¡Estás inhalando aire contaminado! ¡Ponte la máscara de gas inmediatamente (tecla T)!",
        "log_gas_leak_suffocate": "¡Te asfixias en un pasillo con una fuga de gas! Ponte la máscara de gas (tecla T)!",
        "log_filter_clogged": "¡El filtro de la máscara de gas está completamente obstruido! La máscara es inútil!",
        "log_samosbor_active_start": "[!!!] ¡EL SAMOSBOR HA COMENZADO! ¡LA NIEBLA TÓXICA ESTÁ LLENANDO LOS SECTORES!",
        "log_samosbor_toxic_lungs": "¡La niebla tóxica te corroe los pulmones!",
        "log_gasmask_suit_corrode": "La máscara de gas protege contra el gas, pero los químicos corroen el traje...",
        "log_gas_seeping_door": "¡El gas se filtra por debajo de la puerta! ¡No cerraste la compuerta hermética!",
        "log_door_holding_rumble": "La compuerta hermética resiste. Escuchas un estruendo detrás de la puerta.",
        "log_no_hacker_tool": "¡No tienes un descifrador de compuertas! Busca en los apartamentos para encontrarlo.",
        "log_hacker_battery_empty": "¡La batería del descifrador está vacía! Encuentra baterías en los apartamentos.",
        "log_hacker_final_floor_error": "Descifrador: Error de acceso. La compuerta está cerrada por el sistema central de la GIGA-KHRUSHCHEVKA. ¡Este dispositivo es inútil aquí!",
        "go_note_not_found": "[✗] NOTA {0} (NO ENCONTRADA)",
        "go_note_missing_desc": "Te perdiste esta parte de la historia en los pisos de la Khrushchevka. Busca en las habitaciones para encontrarla.",
        "hack_sig_aligned": "SEÑAL: ALINEADA (CLIC EN CONECTAR)",
        "hack_sig_weak": "SEÑAL: DÉBIL (RUIDO)",
        "hack_sig_interference": "SEÑAL: INTERFERENCIA",
        "hack_sig_mismatch": "SEÑAL: DESAJUSTE",
        "log_ach_unlocked": "¡LOGRO DESBLOQUEADO: \\"{0}\\"!",
        "ach_secret_title": "Logro Secreto",
        "ach_secret_hint": "Completa el juego para desbloquear detalles",
        "ach_status_unlocked": "DESBLOQUEADO",
        "ach_status_locked": "BLOQUEADO",
        "log_drink_full": "No tienes sed.",
        "log_bottle_empty": "¡Tu frasco está vacío! Encuentra agua en las habitaciones.",
        "log_drink_quenched": "Has saciado tu sed por completo.",
        "log_approach_gate": "Acércate a la compuerta hermética.",
        "note_tab_locked": "Nota {0}",
        "btn_bandage": "Vendaje: {0}",
        "btn_bag_format": "Bolsa (Notas: {0}/10)",
        "log_prefix_warn": "[ATENCIÓN]",
        "log_prefix_danger": "[PELIGRO]",
        "log_prefix_loot": "[HALLAZGO]",
        "log_prefix_sys": "[SIS]"
"""

# Read app.js
with open('app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Helper function to insert keys right after the target log_sis_warn_3 key
def inject_keys(content, target_key, new_keys_str):
    pattern = re.escape(target_key) + r'\s*:\s*".*?"'
    match = re.search(pattern, content)
    if not match:
        print(f"Warning: could not find target key {target_key} in content!")
        return content
    
    # We want to replace matching string with itself + comma + the new keys string
    full_match = match.group(0)
    replacement = full_match + ",\n" + new_keys_str.strip()
    # Replace only the first occurrence after our search pos if we iterate
    # But since we have unique text per language block, we can replace exactly the matched substring in sequence
    # Let's replace the first occurrence of this exact match
    return content.replace(full_match, replacement, 1)

print("Injecting localization keys into LANGUAGES object...")
# Inject RU keys
content = inject_keys(content, '"log_sis_warn_3"', RU_KEYS)
# After replacing the first one (ru), we can replace the next occurrences in order.
# Since we replace each exactly once (using replace with count=1), we can just call it in sequence!
content = inject_keys(content, '"log_sis_warn_3"', EN_KEYS)
content = inject_keys(content, '"log_sis_warn_3"', ZH_KEYS)
content = inject_keys(content, '"log_sis_warn_3"', DE_KEYS)
content = inject_keys(content, '"log_sis_warn_3"', IT_KEYS)
content = inject_keys(content, '"log_sis_warn_3"', ES_KEYS)

# Let's define other logic replacements
print("Replacing hardcoded strings and emojis...")

# 1. showLootUI and getLocalizedLootItemLabel
# We will insert getLocalizedLootItemLabel right before showLootUI function declaration
get_localized_label_fn = """
function getLocalizedLootItemLabel(item) {
    if (!item) return "";
    switch (item.type) {
        case 'junk':
            return t('loot_item_junk');
        case 'water':
            return t('loot_item_water', item.count);
        case 'bandage':
            return t('loot_item_bandage');
        case 'filter':
            return t('loot_item_filter', item.count);
        case 'ammo':
            return t('loot_item_ammo', item.count);
        case 'battery':
            return t('loot_item_battery');
        case 'note':
            return t('loot_item_note');
        case 'hacker_tool':
            return t('loot_item_hacker_tool');
        default:
            return item.label || item.type || "";
    }
}
"""

content = content.replace("function showLootUI(items, doorIdx, containerKey) {", get_localized_label_fn + "\nfunction showLootUI(items, doorIdx, containerKey) {")

# 2. showLootUI title localization
content = content.replace("""    if (containerKey === 'kitchenLootItems') {
        title.innerText = 'КУХНЯ: НАЙДЕННЫЕ ПРЕДМЕТЫ';
    } else {
        title.innerText = 'НАЙДЕННЫЕ ПРЕДМЕТЫ';
    }""", """    if (containerKey === 'kitchenLootItems') {
        title.innerText = t('loot_title_kitchen');
    } else {
        title.innerText = t('loot_title');
    }""")

# 3. showLootUI empty list & items list
content = content.replace("""    if (!items || items.length === 0) {
        html = '<p style="color:#7f8c9d;padding:10px;">Пусто. Ничего полезного не найдено.</p>';
    } else {
        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            var btnHtml = '';
            if (item.type !== 'junk') {
                btnHtml = '<button onclick="takeLootItem(' + i + ')" style="background:rgba(0,200,100,0.15);border:1px solid rgba(0,200,100,0.4);color:#00ff66;padding:4px 14px;border-radius:3px;cursor:pointer;font-family:inherit;font-weight:bold;">Забрать</button>';
            } else {
                btnHtml = '<span style="color:#555;font-size:0.8rem">Хлам</span>';
            }
            html += '<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 10px;margin:4px 0;background:rgba(255,255,255,0.04);border-radius:3px;border-left:3px solid #ffcc00;">';
            html += '<span>' + (item.icon || '') + ' ' + item.label + '</span>' + btnHtml;
            html += '</div>';
        }
    }""", """    if (!items || items.length === 0) {
        html = '<p style="color:#7f8c9d;padding:10px;">' + t('loot_empty') + '</p>';
    } else {
        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            var btnHtml = '';
            if (item.type !== 'junk') {
                btnHtml = '<button onclick="takeLootItem(' + i + ')" style="background:rgba(0,200,100,0.15);border:1px solid rgba(0,200,100,0.4);color:#00ff66;padding:4px 14px;border-radius:3px;cursor:pointer;font-family:inherit;font-weight:bold;">' + t('loot_take') + '</button>';
            } else {
                btnHtml = '<span style="color:#555;font-size:0.8rem">' + t('loot_junk') + '</span>';
            }
            const label = getLocalizedLootItemLabel(item);
            html += '<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 10px;margin:4px 0;background:rgba(255,255,255,0.04);border-radius:3px;border-left:3px solid #ffcc00;">';
            html += '<span>' + label + '</span>' + btnHtml;
            html += '</div>';
        }
    }""")

# 4. showLootUI take all & close buttons
content = content.replace("""    html += '<button onclick="takeAllLoot()" style="flex:1;padding:8px;background:rgba(255,204,0,0.1);border:1px solid #ffcc00;color:#ffcc00;cursor:pointer;font-family:inherit;font-weight:bold;border-radius:3px;">Забрать всё</button>';
    html += '<button onclick="closeLootUI()" style="flex:1;padding:8px;background:rgba(255,51,51,0.1);border:1px solid #ff3333;color:#ff3333;cursor:pointer;font-family:inherit;font-weight:bold;border-radius:3px;">Закрыть</button>';""", """    html += '<button onclick="takeAllLoot()" style="flex:1;padding:8px;background:rgba(255,204,0,0.1);border:1px solid #ffcc00;color:#ffcc00;cursor:pointer;font-family:inherit;font-weight:bold;border-radius:3px;">' + t('loot_take_all') + '</button>';
    html += '<button onclick="closeLootUI()" style="flex:1;padding:8px;background:rgba(255,51,51,0.1);border:1px solid #ff3333;color:#ff3333;cursor:pointer;font-family:inherit;font-weight:bold;border-radius:3px;">' + t('loot_close') + '</button>';""")

# 5. getLocalizedDoorName
# Replace the whole function body to use localization keys
old_getLocalizedDoorName = """function getLocalizedDoorName(door) {
    if (!door) return "";
    if (door.type === 'apartment' || door.type === 'monster') {
        const num = door.number || 101;
        if (door.roomType === 'armory') {
            return `Пост Ликвидаторов №${num}`;
        } else if (door.roomType === 'contaminated') {
            return `Квартира ${num} (РАДИАЦИЯ)`;
        } else if (door.roomType === 'nest') {
            return `Техническая секция ${num} (ГНЕЗДО)`;
        } else if (door.roomType === 'bedroom_kitchen') {
            return `Квартира ${num} (2-комнатная)`;
        } else if (door.roomType === 'warehouse') {
            return t('room_warehouse');
        } else if (door.roomType === 'archive') {
            return t('room_archive');
        } else if (door.roomType === 'compressor') {
            return t('room_compressor');
        } else if (door.roomType === 'control') {
            return t('room_control');
        } else if (door.roomType === 'ventilation') {
            return t('room_ventilation');
        } else {
            return `Квартира ${num}`;
        }
    } else if (door.type === 'transition') {
        return `Переход ${door.sector || 'А'}-${door.sectorNum || 1}`;
    } else if (door.type === 'empty') {
        const idx = door.id !== undefined ? (door.id + 1) : 1;
        return `Дверь ${idx}`;
    }
    return door.name || "";
}"""

new_getLocalizedDoorName = """function getLocalizedDoorName(door) {
    if (!door) return "";
    if (door.type === 'apartment' || door.type === 'monster') {
        const num = door.number || 101;
        if (door.roomType === 'armory') {
            return t('door_armory', num);
        } else if (door.roomType === 'contaminated') {
            return t('door_contaminated', num);
        } else if (door.roomType === 'nest') {
            return t('door_nest', num);
        } else if (door.roomType === 'bedroom_kitchen') {
            return t('door_apartment_2room', num);
        } else if (door.roomType === 'warehouse') {
            return t('room_warehouse');
        } else if (door.roomType === 'archive') {
            return t('room_archive');
        } else if (door.roomType === 'compressor') {
            return t('room_compressor');
        } else if (door.roomType === 'control') {
            return t('room_control');
        } else if (door.roomType === 'ventilation') {
            return t('room_ventilation');
        } else {
            return t('door_apartment', num);
        }
    } else if (door.type === 'transition') {
        return t('door_transition', door.sector || 'A', door.sectorNum || 1);
    } else if (door.type === 'empty') {
        const idx = door.id !== undefined ? (door.id + 1) : 1;
        return t('door_empty', idx);
    }
    return door.name || "";
}"""

content = content.replace(old_getLocalizedDoorName, new_getLocalizedDoorName)

# 6. updateRoomButtons
content = content.replace("""    if (door.roomType === 'bedroom_kitchen') {
        searchBtn.innerText = door.searched ? 'Спальня обыскана' : 'Обыскать спальню';
        kitchenBtn.style.display = '';
        kitchenBtn.innerText = door.kitchenSearched ? 'Кухня обыскана' : 'Обыскать кухню';""", """    if (door.roomType === 'bedroom_kitchen') {
        searchBtn.innerText = door.searched ? t('room_bedroom_searched') : t('room_bedroom_search');
        kitchenBtn.style.display = '';
        kitchenBtn.innerText = door.kitchenSearched ? t('room_kitchen_searched') : t('room_kitchen_search');""")

content = content.replace("""    } else {
        kitchenBtn.style.display = 'none';
        searchBtn.innerText = door.searched ? 'Уже обыскано' : 'Обыскать мебель';""", """    } else {
        kitchenBtn.style.display = 'none';
        searchBtn.innerText = door.searched ? t('room_already_searched') : t('btn_search_room');""")

# 7. applyLootItem logs localization
content = content.replace("logToConsole('[НАХОДКА] Патроны (+' + (item.count || 6) + ' шт.)', 'loot');", "logToConsole(t('loot_item_ammo', item.count || 6), 'loot');")
content = content.replace("logToConsole('[НАХОДКА] Бинт (+' + (item.count || 1) + ')', 'loot');", "logToConsole(t('loot_item_bandage') + ' (+' + (item.count || 1) + ')', 'loot');")
content = content.replace("logToConsole('[НАХОДКА] Фляга воды (+' + (item.count || 30) + '%)', 'loot');", "logToConsole(t('loot_item_water', item.count || 30), 'loot');")
content = content.replace("logToConsole('[НАХОДКА] Батарейка (+1)', 'loot');", "logToConsole(t('loot_item_battery') + ' (+1)', 'loot');")
content = content.replace("logToConsole('[НАХОДКА] Фильтр (+' + (item.count || 30) + '%)', 'loot');", "logToConsole(t('loot_item_filter', item.count || 30), 'loot');")
content = content.replace("logToConsole('[НАХОДКА] Записка: \"' + LORE_NOTES[nid].title + '\"!', 'loot');", "logToConsole(t('log_loot_note', LORE_NOTES[nid].title), 'loot');")
content = content.replace("logToConsole('[НАХОДКА] ДЕШИФРАТОР ГЕРМОЗАТВОРОВ!', 'loot');", "logToConsole(t('log_loot_hacker'), 'loot');")

# 8. Room and doorway logs
content = content.replace('logToConsole("Подойдите ближе к гермодвери коридора, чтобы запереть или отпереть её.", "warn");', 'logToConsole(t("log_approach_door_to_lock"), "warn");')
content = content.replace('logToConsole("Вы закрутили ручной прижим гермодвери изнутри. Теперь комната герметична.", "action");', 'logToConsole(t("log_door_tightened"), "action");')
content = content.replace('logToConsole("Затвор двери открыт. Комната больше не защищает от внешней среды.", "warn");', 'logToConsole(t("log_door_untightened"), "warn");')
content = content.replace('logToConsole("Вы вышли обратно в бетонный коридор сектора.", "action");', 'logToConsole(t("log_exited_to_hallway"), "action");')
content = content.replace('logToConsole(`Вы спустились на этаж ${state.floor}.`, "sys");', 'logToConsole(t("log_descend_floor", state.floor), "sys");')
content = content.replace('logToConsole(`Шлюз герметично захлопнулся сзади. Грохот гидравлики уносит вас вниз.`, "sys");', 'logToConsole(t("log_gate_closed_descending"), "sys");')
content = content.replace('logToConsole(`Спуск завершен. Вы вышли на этаже ${state.floor}. Дверь заблокирована сзади.`, "sys");', 'logToConsole(t("log_descent_complete", state.floor), "sys");')

# 9. Controls and equipment logs
content = content.replace('logToConsole("Надет противогаз. Обзор ограничен, слышно ваше тяжелое дыхание.", "action");', 'logToConsole(t("log_gasmask_equip"), "action");')
content = content.replace('logToConsole("Противогаз снят.", "action");', 'logToConsole(t("log_gasmask_unequip"), "action");')
content = content.replace('logToConsole("Вы не хотите пить.", "warn");', 'logToConsole(t("log_drink_full"), "warn");')
content = content.replace('logToConsole("Ваша фляга пуста! Найдите воду в жилых комнатах.", "warn");', 'logToConsole(t("log_bottle_empty"), "warn");')
content = content.replace('logToConsole("Вы утолили жажду полностью.", "warn");', 'logToConsole(t("log_drink_quenched"), "warn");')
content = content.replace('logToConsole(`Сделан глоток воды. В бутылке осталось: ${Math.round(state.bottleWater)}% содержимого.`, "action");', 'logToConsole(t("log_drink_sip", Math.round(state.bottleWater)), "action");')
content = content.replace('logToConsole("У вас нет бинтов.", "warn");', 'logToConsole(t("log_no_bandages"), "warn");')
content = content.replace('logToConsole("Вы абсолютно здоровы, бинт не нужен.", "warn");', 'logToConsole(t("log_healthy"), "warn");')
content = content.replace('logToConsole("Вы туго перевязали раны бинтом (+35% здоровья).", "action");', 'logToConsole(t("log_bandage_used"), "action");')

# 10. Stairs monster threat logs
content = content.replace('logToConsole("[УГРОЗА] ИЗ ТЕМНОТЫ ЛЕСТНИЧНОЙ ШАХТЫ НА ВАС КИДАЕТСЯ МНОГОНОГАЯ ТВАРЬ!", "danger");', 'logToConsole(t("log_stairs_monster_threat"), "danger");')
content = content.replace('logToConsole("У вас есть 4 секунды, чтобы выстрелить из пистолета и спугнуть её!", "danger");', 'logToConsole(t("log_stairs_monster_shoot_time"), "danger");')

# 11. Combat logs
content = content.replace('logToConsole("УДАР! Вы пнули тварь! Она отлетела назад и взвизгнула!", "warn");', 'logToConsole(t("log_kick_hit"), "warn");')
content = content.replace('logToConsole("Вы забили тварь ногами до смерти!", "loot");', 'logToConsole(t("log_kick_kill"), "loot");')
content = content.replace('logToConsole("Вы пнули воздух.", "sys");', 'logToConsole(t("log_kick_air"), "sys");')
content = content.replace('logToConsole("Сухой щелчок бойка... Патронов нет!", "danger");', 'logToConsole(t("log_no_ammo"), "danger");')
content = content.replace('logToConsole("Грохот выстрела раскатился по бетонному колодцу этажа!", "action");', 'logToConsole(t("log_shoot"), "action");')
content = content.replace('logToConsole("Точный выстрел разорвал тварь! По коридору разлетелись брызги слизи.", "loot");', 'logToConsole(t("log_shoot_kill"), "loot");')
content = content.replace('logToConsole("Пуля пробила хитиновый панцирь твари! Она яростно завизжала.", "warn");', 'logToConsole(t("log_shoot_hit"), "warn");')
content = content.replace('logToConsole("Тварь издала пронзительный визг и скрылась в вентиляционном канале.", "sys");', 'logToConsole(t("log_stairs_monster_scared"), "sys");')
content = content.replace('logToConsole("Вы выстрелили впустую в бетонные перекрытия.", "warn");', 'logToConsole(t("log_shoot_empty"), "warn");')

# 12. Active samosbor event logs
content = content.replace('logToConsole(isContaminated ? "Вы вдыхаете зараженный воздух! Срочно наденьте противогаз (клавиша T)!" : "Вы задыхаетесь в коридоре с утечкой газа! Наденьте противогаз (клавиша T)!", "danger");', 'logToConsole(isContaminated ? t("log_air_hazard") : t("log_gas_leak_suffocate"), "danger");')
content = content.replace('logToConsole("Фильтр противогаза полностью забился! Маска бесполезна!", "danger");', 'logToConsole(t("log_filter_clogged"), "danger");')
content = content.replace('logToConsole("[!] ВНИМАНИЕ: Датчики зафиксировали приближение волны Самосбора!", "danger");', 'logToConsole(t("log_samosbor_warn_1"), "danger");')
content = content.replace('logToConsole("[!] До активной фазы: ~20 секунд. Найдите укрытие!", "danger");', 'logToConsole(t("log_samosbor_warn_2"), "danger");')
content = content.replace('logToConsole("[!!!] САМОСБОР НАЧАЛСЯ! ТОКСИЧНЫЙ ТУМАН ЗАПОЛНЯЕТ СЕКТОРЫ!", "danger");', 'logToConsole(t("log_samosbor_active_start"), "danger");')
content = content.replace('logToConsole("Токсичный туман разъедает ваши легкие!", "danger");', 'logToConsole(t("log_samosbor_toxic_lungs"), "danger");')
content = content.replace('logToConsole("Противогаз защищает от газа, но химикаты разъевают костюм...", "warn");', 'logToConsole(t("log_gasmask_suit_corrode"), "warn");')
content = content.replace('logToConsole("Газ проникает под дверь! Вы не заблокировали гермозатвор!", "danger");', 'logToConsole(t("log_gas_seeping_door"), "danger");')
content = content.replace('logToConsole("Гермозатвор держит. Вы слышите грохот за дверью.", "sys");', 'logToConsole(t("log_door_holding_rumble"), "sys");')
content = content.replace('logToConsole("Датчики показывают нормализацию среды. Самосбор завершился.", "sys");', 'logToConsole(t("log_samosbor_end"), "sys");')

# 13. Shift startup and console/UI logs
content = content.replace('logToConsole("Начало новой смены ликвидации. Спуск с 1324 этажа...", "sys");', 'logToConsole(t("log_start_shift_floor"), "sys");')
content = content.replace('logToConsole("Аудиосистема шлема ликвидатора инициализирована.", "sys");', 'logToConsole(t("log_sound_init"), "sys");')
content = content.replace('logToConsole("Настройки управления сохранены.", "sys");', 'logToConsole(t("log_save_controls"), "sys");')
content = content.replace('logToConsole("Взлом прерван игроком.", "warn");', 'logToConsole(t("log_hack_cancelled"), "warn");')
content = content.replace('logToConsole("Подойдите ближе к мебели.", "warn");', 'logToConsole(t("log_approach_furniture"), "warn");')
content = content.replace('logToConsole("Вы закрыли глаза, расслабились и решили остаться на месте...", "danger");', 'logToConsole(t("log_ending_freeze_wait"), "danger");')

# 14. Hacker & Gate logs
content = content.replace('logToConsole("СИС: ДОСТУП ЗАБЛОКИРОВАН.", "danger");', 'logToConsole(t("log_hack_blocked"), "danger");')
content = content.replace('logToConsole("Подойдите ближе к гермозатвору.", "warn");', 'logToConsole(t("log_approach_gate"), "warn");')
content = content.replace('logToConsole("У меня нет хакера", "warn");', 'logToConsole(t("hacker_warn"), "warn");')
content = content.replace('logToConsole("СИС: Что вы делаете? Вы на задании, спуститесь на 1 этаж", "warn");', 'logToConsole(t("log_sis_warn_1"), "warn");')
content = content.replace('logToConsole("СИС: Иван Лорим, перестаньте пытатся взламать дверь", "warn");', 'logToConsole(t("log_sis_warn_2"), "warn");')
content = content.replace('logToConsole("СИС: Последнее предупреждение", "warn");', 'logToConsole(t("log_sis_warn_3"), "warn");')
content = content.replace('logToConsole("[!] ВНИМАНИЕ: Датчики зафиксировали приближение волны Самосбора!", "danger");', 'logToConsole(t("log_samosbor_warn_1"), "danger");')
content = content.replace('logToConsole("[!] До активной фазы: ~20 секунд. Найдите укрытие!", "danger");', 'logToConsole(t("log_samosbor_warn_2"), "danger");')
content = content.replace('logToConsole("Взломщик: Ошибка доступа. Затвор заблокирован центральной системой ГИГАХРУЩА. Это устройство здесь бесполезно!", "danger");', 'logToConsole(t("log_hacker_final_floor_error"), "danger");')
content = content.replace('logToConsole("Вы собрали все записки, но не прочитали их... Вы не смогли осознать истину.", "danger");', 'logToConsole(t("log_hack_note_samosbor"), "danger");')
content = content.replace('logToConsole("У вас нет взломщика гермодверей! Обыщите квартиры, чтобы найти его.", "warn");', 'logToConsole(t("log_no_hacker_tool"), "warn");')
content = content.replace('logToConsole("Батарея взломщика разряжена! Найдите батарейки в квартирах.", "warn");', 'logToConsole(t("log_hacker_battery_empty"), "warn");')
content = content.replace("logToConsole(`Затвор дешифрован! Механизмы пришли в движение: затвор ${sdState.opened ? 'открывается' : 'закрывается'}...`, \"action\");", "logToConsole(t('log_hack_gate', sdState.opened ? t('log_hack_gate_open') : t('log_hack_gate_close')), 'action');")
content = content.replace("logToConsole(`Дешифратор: Канал ${activeHackChannel} зафиксирован!`, \"loot\");", "logToConsole(t('log_hack_bypass_ok', activeHackChannel), 'loot');")
content = content.replace('logToConsole("Дешифратор: Сбой связи! Ошибка согласования фазы сигнала.", "danger");', 'logToConsole(t("log_hack_bypass_err"), "danger");')

# 15. Achievements modal UI and unlocks
content = content.replace('logToConsole(`🏆 ДОСТИЖЕНИЕ ПОЛУЧЕНО: "${ach.title}"!`, "loot");', 'logToConsole(t("log_ach_unlocked", ach.title), "loot");')
content = content.replace('const displayTitle = isSecretLocked ? "Секретное достижение" : ach.title;', 'const displayTitle = isSecretLocked ? t("ach_secret_title") : ach.title;')
content = content.replace('const displayDesc = isSecretLocked ? "🔒 Пройдите игру, чтобы открыть подробности" : ach.description;', 'const displayDesc = isSecretLocked ? t("ach_secret_hint") : ach.description;')
content = content.replace("${ach.unlocked ? '🏆' : '🔒'}", "${ach.unlocked ? '[✓]' : '[ ]'}")
content = content.replace("${ach.unlocked ? 'ПОЛУЧЕНО' : 'ЗАБЛОКИРОВАНО'}", "${ach.unlocked ? t('ach_status_unlocked') : t('ach_status_locked')}")

# 16. Log Console Prefix Translation
old_log_prefix = """    let prefix = '';
    switch (type) {
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

new_log_prefix = """    let prefix = '';
    switch (type) {
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

content = content.replace(old_log_prefix, new_log_prefix)

# 17. HUD update button texts
content = content.replace('btnLockRoom.innerText = "Отпереть дверь";', "btnLockRoom.innerText = t('btn_unlock_room');")
content = content.replace('btnLockRoom.innerText = "Запереть дверь";', "btnLockRoom.innerText = t('btn_lock_room');")
content = content.replace("""        btnMask.innerHTML = state.maskOn
            ? 'Снять противогаз'
            : 'Надеть противогаз';""", """        btnMask.innerText = state.maskOn
            ? t('btn_mask_remove')
            : t('btn_mask');""")
content = content.replace('btnBandage.innerHTML = `Бинт: ${state.bandages || 0}`;', "btnBandage.innerText = t('btn_bandage', state.bandages || 0);")

# Update bag button text in updateHUD
content = content.replace("""    if (hudStamina) hudStamina.innerText = Math.round(state.stamina) + '%';
    if (bagNotes) bagNotes.innerText = state.notesCount;""", """    if (hudStamina) hudStamina.innerText = Math.round(state.stamina) + '%';
    if (bagNotes) bagNotes.innerText = state.notesCount;
    const btnBag = document.getElementById('btn-bag');
    if (btnBag) {
        btnBag.innerHTML = t('btn_bag_format', state.notesCount);
    }""")

# 18. updateHackSliderTuner strength meter labels
content = content.replace('strengthLabel.innerText = "СИГНАЛ: ВЫРАВНИВАНИЕ (КЛИКНИТЕ СОЕДИНЕНИЕ)";', 'strengthLabel.innerText = t("hack_sig_aligned");')
content = content.replace('strengthLabel.innerText = "СИГНАЛ: СЛАБЫЙ (ШУМ)";', 'strengthLabel.innerText = t("hack_sig_weak");')
content = content.replace('strengthLabel.innerText = "СИГНАЛ: ПОМЕХИ";', 'strengthLabel.innerText = t("hack_sig_interference");')
content = content.replace('strengthLabel.innerText = "СИГНАЛ: РАССОГЛАСОВАНИЕ";', 'strengthLabel.innerText = t("hack_sig_mismatch");')

# 19. triggerGameOver text and title translations
old_trigger_gameover_switch = """    switch (reason) {
        case "dehydration":
            title.innerText = "ЛИКВИДИРОВАН";
            title.style.color = "#ff3333";
            text = `<p>Ваш организм не выдержал чудовищного обезвоживания.</p>
                    <p>Вы упали на холодные бетонные ступени лестничного марша ${state.floor} этажа.</p>
                    <p>Никто не придет на помощь. Ваше тело останется здесь, пока очередной Самосбор не растворит его в бурую слизь.</p>`;
            break;
            
        case "stairs_monster":
            title.innerText = "РАСТЕРЗАН";
            title.style.color = "#ff3333";
            text = `<p>Вы не успели среагировать.</p>
                    <p>Тварь обрушилась на вас сверху, ломая кости грудной клетки.</p>
                    <p>Острые жвалы пробили визор противогаза. Последнее, что вы слышали — чавканье биомассы, пожирающей вашу плоть.</p>`;
            break;
            
        case "opened_monster":
            title.innerText = "ОБНУЛЕН";
            title.style.color = "#ff3333";
            text = `<p>Вы открыли дверь без предварительной проверки.</p>
                    <p>Хищная тварь Самосбора устроила гнезdo прямо за порогом.</p>
                    <p>Как только затворы разошлись, многорукая биомасса втащила вас внутрь темного помещения. Вы даже не успели закричать.</p>`;
            break;
            
        case "samosbor":
            title.innerText = "РАСТВОРЕН";
            title.style.color = "#ff3333";
            text = `<p>Вы остались в коридоре во время активной фазы Самосбора.</p>
                    <p>Токсичный туман разъел резиновые прокладки шлема и кожу в считанные секунды.</p>
                    <p>Ваше сознание угасло, пока ваши ткани плавились, стекая в вентиляционные решетки.</p>`;
            break;
            
        case "samosbor_gas":
            title.innerText = "ЗАДОХНУЛСЯ";
            title.style.color = "#ff3333";
            text = `<p>Вы спрятались в комнате, но пренебрегли средствами защиты.</p>
                    <p>Токсичный газ Самосбора просочился под гермодверь.</p>
                    <p>Без противогаза ваши легкие наполнились едкими парами, вызвав мгновенный спазм и уduшье.</p>`;
            break;
            
        case "ending_1":
            unlockAchievement("awakened");
            title.innerText = "ПРОБУЖДЕНИЕ";
            title.style.color = "#00ff66";
            badgeText = "Истинная концовка";
            badgeClass = "badge-green";
            text = `<p>Собрав все записки, вы поняли истинную природу Гигахрущевки.</p>
                    <p>Когда туман Самосбора хлынул в коридор, вы не побежали прятаться. Вы замерли на месте, раскинув руки, и закрыли глаза.</p>
                    <p>Мир вокруг задрожал, бетонные стены начали осыпаться пикселями. Фиолетовый туман обнял вас...</p>
                    <p>...И вдруг вы сделали резкий вдох. Свежий, теплый воздух наполнил легкие.</p>
                    <p>Вы открыли глаза. Вы лежали на мягкой постели. В окно светило ослепительное, настоящее СОЛНЦЕ, а за окном шелестели зеленые листья деревьев. Это был сон. Долгий кошмар, из которого можно было выбраться только перестав бояться.</p>`;
            break;"""

# Let's verify and match the slightly different string spacing or unicode characters in raw code if any
# Wait, let's use exact match but let's copy the code from app.js correctly.
# Let's inspect triggerGameOver old text from app.js in file viewer to be sure we match it exactly.
# In showLootUI, we had:
#   reason dehydration, stairs_monster, opened_monster, samosbor, samosbor_gas, ending_1
# Let's see: we can replace using a simplified regex or exact content replacement.
# Let's check triggerGameOver block from lines 7016 to 7068 of app.js.
# Let's print triggerGameOver content in our python script using string find/replace of the whole switch statement.
# Let's write the new switch:
new_trigger_gameover_switch = """    switch (reason) {
        case "dehydration":
            title.innerText = t('go_dehydration_title');
            title.style.color = "#ff3333";
            text = t('go_dehydration_desc', state.floor);
            break;
            
        case "stairs_monster":
            title.innerText = t('go_stairs_monster_title');
            title.style.color = "#ff3333";
            text = t('go_stairs_monster_desc');
            break;
            
        case "opened_monster":
            title.innerText = t('go_opened_monster_title');
            title.style.color = "#ff3333";
            text = t('go_opened_monster_desc');
            break;
            
        case "samosbor":
            title.innerText = t('go_samosbor_title');
            title.style.color = "#ff3333";
            text = t('go_samosbor_desc');
            break;
            
        case "samosbor_gas":
            title.innerText = t('go_samosbor_gas_title');
            title.style.color = "#ff3333";
            text = t('go_samosbor_gas_desc');
            break;
            
        case "ending_1":
            unlockAchievement("awakened");
            title.innerText = t('go_ending1_title');
            title.style.color = "#00ff66";
            badgeText = t('go_badge_ending1');
            badgeClass = "badge-green";
            text = t('go_ending1_desc');
            break;"""

# Let's find exactly the text between switch (reason) { and case "ending_2":
start_idx = content.find('switch (reason) {')
end_idx = content.find('case "ending_2":')
if start_idx != -1 and end_idx != -1:
    old_switch_part = content[start_idx:end_idx]
    # Replace the case dehydration block up to ending_1
    content = content[:start_idx] + "switch (reason) {\n" + new_trigger_gameover_switch + "\n        " + content[end_idx:]
    print("triggerGameOver switch successfully localized!")
else:
    print("Warning: could not locate triggerGameOver switch!")

# Replace gameover missing note list localization
content = content.replace("""                if (collected) {
                    const safeContent = note.content.replace(/\\\\n/g, '\\n');
                    noteDiv.innerHTML = `
                        <div class="gameover-note-title">[✓] ${note.title}</div>
                        <div class="gameover-note-content" style="white-space:pre-line;">${safeContent}</div>
                    `;
                } else {
                    noteDiv.innerHTML = `
                        <div class="gameover-note-title">[✗] ЗАПИСКА ${index + 1} (НЕ НАЙДЕНА)</div>
                        <div class="gameover-note-content" style="font-style: italic; color: #888;">Вы упустили этот фрагмент истории на этажах Хрущевки. Обыскивайте комнаты, чтобы найти её.</div>
                    `;
                }""", """                if (collected) {
                    const safeContent = note.content.replace(/\\\\n/g, '\\n');
                    noteDiv.innerHTML = `
                        <div class="gameover-note-title">[✓] ${note.title}</div>
                        <div class="gameover-note-content" style="white-space:pre-line;">${safeContent}</div>
                    `;
                } else {
                    noteDiv.innerHTML = `
                        <div class="gameover-note-title">${t('go_note_not_found', index + 1)}</div>
                        <div class="gameover-note-content" style="font-style: italic; color: #888;">${t('go_note_missing_desc')}</div>
                    `;
                }""")

# 20. Update applyLanguage definition
old_applyLanguage = """function applyLanguage(lang) {
    if (typeof LANGUAGES === 'undefined' || !LANGUAGES[lang]) return;
    const t = LANGUAGES[lang];
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (t[key]) {
            if (el.tagName === 'INPUT' && (el.type === 'button' || el.type === 'submit')) {
                el.value = t[key];
            } else if (key.includes('_html')) {
                el.innerHTML = t[key];
            } else {
                el.innerText = t[key];
            }
        }
    });
}"""

new_applyLanguage = """function applyLanguage(lang) {
    if (typeof LANGUAGES === 'undefined' || !LANGUAGES[lang]) return;
    const t_dict = LANGUAGES[lang];
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (t_dict[key]) {
            if (el.tagName === 'INPUT' && (el.type === 'button' || el.type === 'submit')) {
                el.value = t_dict[key];
            } else if (key.includes('_html')) {
                el.innerHTML = t_dict[key];
            } else {
                el.innerText = t_dict[key];
            }
        }
    });
    // Dynamically update note tab labels depending on locked status
    for (let nid = 0; nid < 10; nid++) {
        const tab = document.getElementById(`note-tab-${nid}`);
        if (tab) {
            if (tab.classList.contains('btn-note-locked')) {
                tab.innerText = t('note_tab_locked', nid + 1);
            } else {
                tab.innerText = LORE_NOTES[nid].title;
            }
        }
    }
}"""

content = content.replace(old_applyLanguage, new_applyLanguage)

# 21. Update sensitivity bindings at the end of the file
old_sens_bindings = """    // Sensitivity (Event Delegation for reliability)
    const sensSlider = document.getElementById('sens-slider');
    if (sensSlider) {
        sensSlider.value = typeof mouseSensMultiplier !== 'undefined' ? mouseSensMultiplier : (parseFloat(localStorage.getItem('samosbor_sensitivity')) || 1.0);
    }
    document.addEventListener('input', (e) => {
        if (e.target && e.target.id === 'sens-slider') {
            if (typeof mouseSensMultiplier !== 'undefined') mouseSensMultiplier = parseFloat(e.target.value);
            localStorage.setItem('samosbor_sensitivity', e.target.value);
        }
    });
    document.addEventListener('change', (e) => {
        if (e.target && e.target.id === 'sens-slider') {
            if (typeof mouseSensMultiplier !== 'undefined') mouseSensMultiplier = parseFloat(e.target.value);
            localStorage.setItem('samosbor_sensitivity', e.target.value);
        }
    });"""

new_sens_bindings = """    // Sensitivity (Event Delegation for reliability)
    const sensSlider = document.getElementById('settings-sensitivity-slider');
    const sensVal = document.getElementById('settings-sensitivity-value');
    if (sensSlider) {
        const savedSens = parseFloat(localStorage.getItem('samosbor_sensitivity')) || 1.0;
        sensSlider.value = savedSens;
        if (typeof mouseSensMultiplier !== 'undefined') mouseSensMultiplier = savedSens;
        if (sensVal) sensVal.innerText = savedSens.toFixed(1);
    }
    document.addEventListener('input', (e) => {
        if (e.target && e.target.id === 'settings-sensitivity-slider') {
            const val = parseFloat(e.target.value);
            if (typeof mouseSensMultiplier !== 'undefined') mouseSensMultiplier = val;
            localStorage.setItem('samosbor_sensitivity', val);
            if (sensVal) sensVal.innerText = val.toFixed(1);
        }
    });
    document.addEventListener('change', (e) => {
        if (e.target && e.target.id === 'settings-sensitivity-slider') {
            const val = parseFloat(e.target.value);
            if (typeof mouseSensMultiplier !== 'undefined') mouseSensMultiplier = val;
            localStorage.setItem('samosbor_sensitivity', val);
            if (sensVal) sensVal.innerText = val.toFixed(1);
        }
    });"""

content = content.replace(old_sens_bindings, new_sens_bindings)

# 22. Remove emojis from item templates in generateRoomLootItems
content = content.replace("icon: '🗑️'", "icon: ''")
content = content.replace("icon: '💧'", "icon: ''")
content = content.replace("icon: '🩹'", "icon: ''")
content = content.replace("icon: '💨'", "icon: ''")
content = content.replace("icon: '💥'", "icon: ''")
content = content.replace("icon: '🔋'", "icon: ''")
content = content.replace("icon: '📜'", "icon: ''")
content = content.replace("icon: '🔓'", "icon: ''")

# Write app.js back
with open('app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished applying translations and bindings successfully!")
