/**
 * САМОСБОР: ЛИКВИДАТОР 1324 - 3D FPS Игровой движок
 */

// --- НАСТРОЙКИ ИГРЫ ---
const START_FLOOR = 1324;
const END_FLOOR = 1;
const MAX_HEALTH = 100;
const MAX_WATER = 100;
const MAX_AMMO = 24;
const MAX_FILTER = 100;

// Глобальные переменные света
let doorLights = {};
let playerFlashlight = null;
let warningBeacons = [];
let warningLights = [];

// --- РАЗНООБРАЗИЕ ГЕЙМПЛЕЯ: НОВЫЕ ПЕРЕМЕННЫЕ ---
let hallwayCrawlerMesh = null;
let crawlerHealth = 2;
let deadLiquidatorMesh = null;
let deadLiquidatorSearched = false;
let ghostMesh = null;
let activeHackChannel = 'A';
let targetFrequencies = { A: 0, B: 0, C: 0 };
let hackSuccessCallback = null;
let hackActive = false;
let lastBuiltFloor = null;

function getLocalizedDoorName(door) {
    if (!door) return "";
    if (door.type === 'apartment') {
        const num = door.number || 101;
        if (door.roomType === 'armory') {
            return `Пост Ликвидаторов №${num}`;
        } else if (door.roomType === 'contaminated') {
            return `Квартира ${num} (РАДИАЦИЯ)`;
        } else if (door.roomType === 'nest') {
            return `Техническая секция ${num} (ГНЕЗДО)`;
        } else {
            return `Квартира ${num}`;
        }
    } else if (door.type === 'transition') {
        return `Переход ${door.sector || 'А'}-${door.sectorNum || 1}`;
    } else if (door.type === 'monster') {
        const keys = ['room_warehouse', 'room_archive', 'room_compressor', 'room_control', 'room_ventilation'];
        const key = keys[door.monsterRoomIndex] || 'room_warehouse';
        return t(key);
    } else if (door.type === 'empty') {
        const idx = door.id !== undefined ? (door.id + 1) : 1;
        return `Дверь ${idx}`;
    }
    return door.name || "";
}

const LANGUAGES = {
    "ru": {
        "menu_title": "С А М О С Б О Р",
        "menu_subtitle": "ЛИКВИДАТОР: ЭТАЖ 1324 [3D FPS]",
        "menu_creator": "СОЗДАТЕЛЬ ИГРЫ: @sw1therland",
        "init_interface": "> ИНИЦИАЛИЗАЦИЯ ИНТЕРФЕЙСА ЛИКВИДАТОРА...",
        "network_ok": "> ПОДКЛЮЧЕНИЕ К СЕТИ ГИГАХРУЩЕВКИ... ОК.",
        "equipment_info": "> СНАРЯЖЕНИЕ: ПИСТОЛЕТ (24), ПРОТИВОГАЗ, ВОДА, СУМКА.",
        "mission_info": "> ЗАДАЧА: СПУСТИТЬСЯ НА 1-Й ЭТАЖ И ВЫЖИТЬ.",
        "loading_sdk": "Загрузка SDK...",
        "btn_start": "НАЧАТЬ СМЕНУ",
        "btn_settings": "НАСТРОЙКИ",
        "btn_achievements": "ДОСТИЖЕНИЯ",
        "btn_about": "ОБ ИГРЕ",
        "hud_floor": "ЭТАЖ:",
        "hud_health": "ЖИЗНЬ:",
        "hud_water": "ВОДА:",
        "hud_ammo": "ПАТРОНЫ:",
        "hud_filter": "ФИЛЬТР:",
        "hud_stamina": "БЕГ:",
        "fps_instructions": "WASD - Ходить | Shift - Бег | Space - Пинок | Мышь - Обзор | ЛКМ - Выстрел | R - Дверь | F - Фонарик | E - Слушать | T - Противогаз | Q - Вода | G - Сумка | Z - Обыск | B - Взломщик",
        "mobile_flashlight": "Фонарик",
        "mobile_listen": "Слушать",
        "mobile_door": "Дверь",
        "mobile_fire": "Огонь",
        "listening_title": "СЛУШАЮ...",
        "listening_subtext": "Шумы бетонной шахты",
        "descent_transition_title": "ПЕРЕХОД НА НИЖНИЙ ЭТАЖ...",
        "btn_mask": "Надеть противогаз",
        "btn_mask_remove": "Снять противогаз",
        "btn_drink": "Сделать глоток воды",
        "btn_descend_default": "Идите на лестницу в конце коридора",
        "focus_title": "ФОКУС ОБЪЕКТА",
        "focus_object_none": "ОБЪЕКТ НЕ ВЫБРАН",
        "focus_object_desc": "Подойдите к двери или объекту взаимодействия",
        "btn_listen": "Слушать",
        "btn_open_door": "Открыть",
        "room_actions_title": "ДЕЙСТВИЯ",
        "btn_search_room": "Обыскать мебель",
        "btn_lock_room": "Запереть дверь",
        "btn_unlock_room": "Отпереть дверь",
        "btn_exit_room": "Выйти в коридор",
        "transition_actions_title": "ТЕХНИЧЕСКИЙ ШЛЮЗ",
        "btn_enter_transition": "Перейти на другой сектор",
        "btn_cancel_transition": "Вернуться в коридор",
        "notes_title": "СУМКА: НАЙДЕННЫЕ ЗАПИСКИ",
        "notes_inventory_title": "ИНВЕНТАРЬ",
        "bag_hacker_label": "ВЗЛОМЩИК",
        "bag_batteries_label": "БАТАРЕЙКИ",
        "notes_list_title": "ЗАПИСКИ",
        "select_note_prompt": "Выберите записку в списке слева для чтения.",
        "gameover_notes_collected": "СОБРАННЫЕ ЗАПИСКИ ИЗ ГИГАХРУЩА:",
        "credits_header": "ТИТРЫ // CREDITS",
        "credits_author_label": "АВТОР И РАЗРАБОТЧИК:",
        "credits_tech": "Технологии: HTML5, Three.js, Web Audio API<br>Специально для вселенной Самосбора",
        "btn_restart": "НАЧАТЬ ЗАНОВО",
        "pause_title": "ПАУЗА",
        "btn_resume": "ПРОДОЛЖИТЬ СМЕНУ",
        "btn_exit": "ВЫЙТИ В МЕНЮ",
        "settings_title": "НАСТРОЙКИ",
        "section_language": "ВЫБОР ЯЗЫКА // LANGUAGE",
        "section_controls": "УПРАВЛЕНИЕ // CONTROLS",
        "label_rebind_desc": "Кликните по действию, затем нажмите новую клавишу на клавиатуре.",
        "btn_reset": "СБРОСИТЬ",
        "btn_save": "СОХРАНИТЬ",
        "about_title": "ОБ ИГРЕ",
        "achievements_title": "ДОСТИЖЕНИЯ",
        "achievements_subtitle": "СПИСОК ДОСТИЖЕНИЙ ЛИКВИДАТОРА",
        "hack_title": "ДЕШИФРАТОР ГЕРМОЗАТВОРА // БАЙПАС",
        "hack_sys": "СИСТЕМА: ГРУППА-Б",
        "hack_bat": "АККУМУЛЯТОР: ОК",
        "hack_chan_a_label": "КАНАЛ А",
        "hack_chan_b_label": "КАНАЛ Б",
        "hack_chan_c_label": "КАНАЛ В",
        "hack_search": "ПОИСК ЧАСТОТЫ:",
        "btn_hack_submit": "СОЕДИНЕНИЕ",
        "btn_hack_cancel": "ОТМЕНА",
        "achievement_popup_header": "Достижение получено!",
        "ending_wakeup_title": "ПРОБУЖДЕНИЕ",
        "btn_true_ending_restart": "НАЧАТЬ СМЕНУ ЗАНОВО",
        "act_move_forward": "Движение вперед",
        "act_move_backward": "Движение назад",
        "act_move_left": "Движение влево",
        "act_move_right": "Движение вправо",
        "act_sprint": "Бег (Ускорение)",
        "act_interact": "Взаимодействие / Дверь",
        "act_flashlight": "Фонарик Вкл/Выкл",
        "act_listen": "Слушать у гермодвери",
        "act_gasmask": "Надеть/снять противогаз",
        "act_water": "Сделать глоток воды",
        "act_bag": "Открыть сумку (Записки)",
        "act_search": "Обыскать комнату",
        "act_hackertool": "Применить взломщик",
        "act_pause": "Пауза (Меню)",
        "door_apartment": "Квартира {0}",
        "door_armory": "Пост Ликвидаторов №{0}",
        "door_contaminated": "Квартира {0} (РАДИАЦИЯ)",
        "door_nest": "Техническая секция {0} (ГНЕЗДО)",
        "door_transition": "Переход {0}-{1}",
        "door_empty": "Дверь {0}",
        "room_warehouse": "Склад",
        "room_archive": "Архив",
        "room_compressor": "Компрессорная",
        "room_control": "Щитовая",
        "room_ventilation": "Венткамера",
        "ach_butcher_title": "Мясник гигахруща",
        "ach_butcher_desc": "Напугайте или уничтожьте 50 тварей",
        "ach_hacker_title": "Хакер-самоучка",
        "ach_hacker_desc": "Взломайте 100 гермозатворов",
        "ach_spendthrift_title": "Транжира",
        "ach_spendthrift_desc": "Потратьте все патроны до 1000 этажа",
        "ach_survivor_title": "Выживший",
        "ach_survivor_desc": "Спуститесь ниже 1000 этажа",
        "ach_drinker_title": "Водохлёб",
        "ach_drinker_desc": "Сделайте 50 глотков очищенной воды",
        "ach_deceived_title": "Обманутый",
        "ach_deceived_desc": "Пройти на тупиковую концовку",
        "ach_awakened_title": "Пробуждённый и свободный",
        "ach_awakened_desc": "Пройти на истинную концовку",
        "ach_secret_desc": "[СЕКРЕТНОЕ ДОСТИЖЕНИЕ]",
        "about_content_html": "\n            <h3 class=\"glow-red\" style=\"margin-bottom: 5px; font-weight: bold;\">САМОСБОР: ЛИКВИДАТОР 1324</h3>\n            <p style=\"margin-top: 0; margin-bottom: 15px; color: var(--glow-green); font-weight: bold; font-family: var(--font-mono); font-size: 0.9rem;\">РАЗРАБОТЧИК ИГРЫ: @sw1therland</p>\n            <p>Вы — Ликвидатор тяжелого сектора Гигахрущевки. Ваша смена началась на 1324-м этаже. Цель проста — спуститься на 1-й этаж и выжить.</p>\n            <p style=\"margin-top: 10px;\">Во время спуска вы столкнетесь с Самосбором — смертельным явлением. Услышав сирену, немедленно найдите свободную квартиру, закройте гермодверь и наденьте противогаз.</p>\n            <p style=\"margin-top: 10px;\">Следите за уровнем воды и фильтром противогаза. Обыскивайте серванты и столы в квартирах, чтобы найти припасы, записки, взломщик гермодверей и батарейки.</p>\n            <p style=\"margin-top: 15px; color: var(--glow-amber); font-weight: bold;\">Управление:</p>\n            <ul style=\"margin-left: 20px; margin-top: 5px; display: flex; flex-direction: column; gap: 4px;\">\n                <li><b>WASD</b> — Движение</li>\n                <li><b>Shift</b> — Бег (быстро расходует выносливость)</li>\n                <li><b>Space (Пробел)</b> — Пинок (оттолкнуть бегущую тварь в коридоре)</li>\n                <li><b>Мышь</b> — Обзор (кликните по экрану для захвата указателя)</li>\n                <li><b>ЛКМ</b> — Выстрел (пугает монстра на лестничной площадке)</li>\n                <li><b>R</b> — Закрыть/открыть гермодверь</li>\n                <li><b>F</b> — Фонарик</li>\n                <li><b>E</b> — Прислушаться к звукам за дверью</li>\n                <li><b>T</b> — Надеть/снять противогаз</li>\n                <li><b>Q</b> — Сделать глоток воды</li>\n                <li><b>G / Сумка</b> — Проверить записки и инвентарь</li>\n                <li><b>Z</b> — Обыскать мебель (стол/сервант)</li>\n                <li><b>B</b> — Использовать взломщик на лестничных воротах</li>\n                <li><b>Esc / P</b> — Пауза</li>\n            </ul>\n        ",
        "ending_wakeup_desc": "Вы сделали глубокий вдох. Воздух чистый, теплый и пахнет свежей травой.<br><br>Очертания неба, зеленого дерева и шелестящих листьев сквозь полузакрытые веки обретают теплоту.<br><br>Кошмар Гигахрущевки завершен. Вы наконец-то проснулись.",
        "ending_wakeup_stats": "<div style=\"font-weight: bold; font-size: 0.95rem; color: #111111; margin-bottom: 5px; text-align: center; letter-spacing: 1px;\">ИСТИННАЯ КОРНЕВАЯ КОНЦОВКА</div>Записок собрано и прочитано: 10 / 10<br>Спустились до пробуждения на: <span id=\"true-ending-floors-descended\" style=\"font-weight: bold; color: #6b0a0a;\">{0}</span> этажей",
        "ending_wakeup_author": "<strong>Автор игры:</strong> @sw1therland<br><span style=\"font-size: 0.72rem; color: #666666;\">Спасибо за прохождение! Вы вырвались из Самостроя.</span>",
        "go_dehydration_title": "ЛИКВИДИРОВАН",
        "go_dehydration_desc": "<p>Ваш организм не выдержал чудовищного обезвоживания.</p><p>Вы упали на холодные бетонные ступени лестничного марша {0} этажа.</p><p>Никто не придет на помощь. Ваше тело останется здесь, пока очередной Самосбор не растворит его в бурую слизь.</p>",
        "go_stairs_monster_title": "РАСТЕРЗАН",
        "go_stairs_monster_desc": "<p>Вы не успели среагировать.</p><p>Тварь обрушилась на вас сверху, ломая кости грудной клетки.</p><p>Острые жвалы пробили визор противогаза. Последнее, что вы слышали — чавканье биомассы, пожирающей вашу плоть.</p>",
        "go_opened_monster_title": "ОБНУЛЕН",
        "go_opened_monster_desc": "<p>Вы открыли дверь без предварительной проверки.</p><p>Хищная тварь Самосбора устроила гнездо прямо за порогом.</p><p>Как только затворы разошлись, многорукая биомасса втащила вас внутрь темного помещения. Вы даже не успели закричать.</p>",
        "go_samosbor_title": "РАСТВОРЕН",
        "go_samosbor_desc": "<p>Вы остались в коридоре во время активной фазы Самосбора.</p><p>Токсичный туман разъел резиновые прокладки шлема и кожу в считанные секунды.</p><p>Ваше сознание угасло, пока ваши ткани плавились, стекая в вентиляционные решетки.</p>",
        "go_samosbor_gas_title": "ЗАДОХНУЛСЯ",
        "go_samosbor_gas_desc": "<p>Вы спрятались в комнате, но пренебрегли средствами защиты.</p><p>Токсичный газ Самосбора просочился под гермодверь.</p><p>Без противогаза ваши легкие наполнились едкими парами, вызвав мгновенный спазм и удушье.</p>",
        "go_ending1_title": "ПРОБУЖДЕНИЕ",
        "go_ending1_desc": "<p>Собрав все записки, вы поняли истинную природу Гигахрущевки.</p><p>Когда туман Самосбора хлынул в коридор, вы не побежали прятаться. Вы замерли на месте, раскинув руки, и закрыли глаза.</p><p>Мир вокруг задрожал, бетонные стены начали осыпаться пикселями. Фиолетовый туман обнял вас...</p><p>...И вдруг вы сделали резкий вдох. Свежий, теплый воздух наполнил легкие.</p><p>Вы открыли глаза. Вы лежали на мягкой постели. В окно светило ослепительное, настоящее СОЛНЦЕ, а за окном шелестели зеленые листья деревьев. Это был сон. Долгий кошмар, из которого можно было выбраться только перестав бояться.</p>",
        "go_ending2_title": "БЕЗВЫХОДНОСТЬ",
        "go_ending2_desc": "<p>Вы преодолели долгий путь и спустились на первый этаж.</p><p>Но прохода наружу нет. Тяжелые шлюзы герметично заварены многовековыми слоями ржавчины.</p><p>Сзади с грохотом захлопнулась дверь лестничного марша. Механизмы заклинило. Задвижки не двигаются.</p><p>В этот момент сирены взвыли на максимальной громкости. Начался мощнейший Самосбор. Укрытий нет. Двери заблокированы. Вы заперты в бетонном мешке первого этажа один на один со смертельным туманом. Это конец пути.</p>",
        "go_badge_death": "Смерть",
        "go_badge_ending1": "Истинная концовка",
        "go_badge_ending2": "Тупиковая концовка",
        "log_creep_1": "Вы услышали далёкий скрежет в бетонных стенах...",
        "log_creep_2": "Сквозняк донёс запах гнилой капусты и сырого мяса.",
        "log_creep_3": "Лампы на мгновение мигнули. Давление в шлеме стабильно.",
        "log_creep_4": "Где-то глубоко внизу раздался приглушённый металлический удар.",
        "log_creep_5": "Счётчик Гейгера тихо потрескивает. Фоновое излучение в норме.",
        "log_gh_scary": "Призрак высасывает энергию вашего фонарика!",
        "log_water_low": "Внимание! Критический уровень обезвоживания!",
        "log_descend_floor": "Спустились на этаж {0}.",
        "log_descend_warn": "Технический этаж заблокирован гермозатвором. Требуется взлом.",
        "log_ascend_floor": "Поднялись на этаж {0}.",
        "log_room_clean": "Вы вошли в {0}. Воздух чист. Источники опасности не обнаружены.",
        "log_room_hazard": "Вы вошли в {0}. Воздух заражен радиацией! Наденьте противогаз! (клавиша T)",
        "log_room_nest": "Вы вошли в {0}. Слизь на стенах шевелится. Вы ощущаете чье-то присутствие! (будьте готовы)",
        "log_room_hallway": "Вы вышли в коридор. Вентиляция гонит холодный воздух Гигахрущевки.",
        "log_lock_search_warn": "Нельзя обыскивать мебель во время Самосбора, это слишком опасно!",
        "log_lock_door": "Вы закрыли гермодверь квартиры.",
        "log_unlock_door": "Вы открыли гермодверь квартиры.",
        "log_door_listen": "Вы прислушались к звукам за дверью {0}...",
        "log_door_listen_clean": "Тишина. Кажется, там безопасно.",
        "log_door_listen_hazard": "Слышны тяжелые шаги и шорох слизи. Там тварь!",
        "log_door_listen_transition": "Слышен далекий гул трансформаторов технического шлюза.",
        "log_hack_bypass_ok": "Байпас: Канал {0} дешифрован!",
        "log_hack_bypass_err": "Байпас: сбой синхронизации фазы сигнала.",
        "log_hack_gate": "Гермозатвор! Ворота пошли на: {0}...",
        "log_hack_gate_open": "открывание",
        "log_hack_gate_close": "закрывание",
        "log_hack_hacker_err": "Дешифратор: сбой. Цепь заблокирована центральной системой гигахруща. Использование невозможно!",
        "log_hack_note_samosbor": "Вы собрали все записки, но не прочитали их... вы не смогли осознать истину.",
        "log_hack_tool_hot": "Дешифратор перегрелся! Подождите, чтобы остыл.",
        "log_hack_tool_empty": "Дешифратор разряжен! Замените батарейку.",
        "log_loot_corpse": "[✔] Вы обыскали тело, броня (+8) и фильтр (+40%) восстановлены.",
        "log_loot_note": "[✔] Найдена записка: \"{0}\"!",
        "log_loot_hacker": "[✔] Вы нашли дешифратор гермозатворов!",
        "log_loot_battery": "[✔] Вы нашли батарейку (+1 шт., всего: {0}).",
        "log_loot_synthesizer": "Вы нашли пищевой синтезатор (+50% воды).",
        "log_loot_ammo": "[✔] Вы нашли патроны (+{0} шт.).",
        "log_loot_filter": "Вы нашли новый фильтр (+50% заряда).",
        "log_loot_empty": "Вы обыскали мебель, но ничего полезного не нашли.",
        "log_gasmask_equip": "Противогаз надет. Дыхание ограничено, визор запотевает.",
        "log_gasmask_unequip": "Противогаз снят.",
        "log_gasmask_no": "У вас нет противогаза!",
        "log_gasmask_empty": "Фильтр пуст! Воздух отравлен!",
        "log_drink_sip": "Сделан глоток. В бутылке осталось: {0}% содержимого.",
        "log_siren_start": "[!] Взвыла сирена Самосбора!",
        "log_siren_desc": "У вас есть 4 секунды, чтобы укрыться в комнате и закрыть гермодверь!",
        "log_monster_shoot_scare": "Вы испугали тварь выстрелом! Она отступила вглубь шахты!",
        "log_monster_shoot_dead": "Вы уничтожили тварь выстрелом!",
        "log_monster_kick": "Вы пнули тварь!",
        "log_monster_kick_dmg": "Тварь укусила вас за ногу! Получен урон!",
        "log_crawler_run": "Вы услышали быстрый скрежет когтей на этаже!",
        "log_crawler_warn": "Тварь бежит на вас! Нажмите ПРОБЕЛ, чтобы оттолкнуть её!",
        "log_crawler_safe": "Шум утих. Тварь скрылась в вентиляции.",
        "log_air_hazard": "Вы вдыхаете ядовитые испарения! Срочно наденьте противогаз (клавиша T)!",
        "log_air_empty_warn": "Фильтр пуст! Маска не защищает!",
        "log_air_samosbor_phase": "[!] Самосбор перешел в активную фазу: ~20 секунд. Не выходите!",
        "log_air_samosbor_melt": "[!!!] Стены плавятся! Самосбор заполняет коридоры!",
        "log_air_samosbor_melt_dmg": "Кислотный туман разъедает ваш шлем!",
        "log_air_filter_melt": "Фильтр нейтрализует газы, но химикаты разъедают уплотнители...",
        "log_air_filter_empty_melt": "Фильтр пуст! Вы задыхаетесь в токсичной жиже!",
        "log_air_filter_norm": "Фильтр нейтрализует газы. Вы в безопасности.",
        "log_samosbor_end": "Сирены утихли. Самосбор закончился. Опасность миновала.",
        "log_game_start": "Смена началась. Спуститесь на 1-й этаж...",
        "log_sound_init": "Аудиосистема инициализирована.",
        "log_save_controls": "Настройки управления сохранены.",
        "log_dev_command": "Dev-команда выполнена.",
        "note_0_title": "Грязный листок бумаги (Этаж ~1200)",
        "note_1_title": "Рапорт командира группы (Этаж ~1100)",
        "note_2_title": "Памятка ГО и ЧС (Этаж ~1000)",
        "note_3_title": "Дневник ребенка (Этаж ~900)",
        "note_4_title": "Странная обгоревшая страница",
        "note_5_title": "Записка без подписи",
        "note_6_title": "Агитационная листовка (Этаж ~800)",
        "note_7_title": "Истерзанный клочок бумаги",
        "note_8_title": "Кровавый клочок блокнота (Этаж ~700)",
        "note_9_title": "Последнее признание Ликвидатора",
        "note_0_content": "Блок 1290. Семнадцатый день после блокировки сектора. \\n\\nВентиляция гудит как бешеная, оттуда постоянно пахнет сырым, гниющим мясом и химикатами. Сосед снизу вчера пропал. Его жена говорит, что слышала скрежет за гермодверью посреди ночи, будто кто-то когтями пытался подковырнуть стальной уплотнитель. \\n\\nВода в кранах уже неделю идет бурая. Кажется, фильтры на водозаборе забились останками. Ликвидаторы не приходят. Нам говорят сидеть по квартирам. Где же чертово солнце? Существует ли оно вообще, или бетон - это всё, что есть в этом мире?",
        "note_1_content": "РАПОРТ. Ликвидатор мл. сержант Соболев. Группа «Бета-6». \\n\\nНам приказали зачистить блок 1105 после локального прорыва самосбора. Всё шло по инструкции, заливали коридор реагентами. Но в торцевом коридоре мы наткнулись на квартиру №42. Гермодверь была заблокирована изнутри. Оттуда кричали дети, умоляли открыть. \\n\\nНо датчики показывали критический уровень заражения за дверью. Самосборная слизь уже пробивалась через стыки. Приказ штаба был однозначным: консервация блока. Мы заварили дверь автогеном снаружи. Дети кричали еще минут десять, пока мы работали. Я до сих пор слышу этот звук, когда закрываю глаза. Прости нас, Хрущ.",
        "note_2_content": "ПАМЯТКА ЖИЛЬЦУ ГИГАХРУЩЕВКИ ПРИ НАЧАЛЕ САМОСБОРА: \\n\\n1. При первых звуках сирены немедленно прекратите любые перемещения по лестничным маршам.\\n2. Войдите в ближайшее жилое помещение или шлюзовую зону.\\n3. Герметично закройте гермодверь. Затяните вентили ручного прижима до упора.\\n4. Наденьте средства индивидуальной защиты (противогаз ГП-9 или аналог).\\n5. Не приближайтесь к вентиляционным шахтам и дверным проемам.\\n6. Игнорируйте любые звуки, голоса родственников или коллег, доносящиеся снаружи во время активной фазы.\\n7. Ожидайте прибытия Ликвидаторов для проведения дезинфекции.",
        "note_3_content": "12 марта. \\n\\nМама забрала мои цветные карандаши, потому что я нарисовал небо. Я помню его! Оно было такое... синее-синее, и сверху висел огромный теплый круг, который светил и грел. Мама заплакала, порвала рисунок и ударила меня по рукам. Она сказала, что небо - это опасный бред сумасшедших, и если кто-то из Комитета услышит мои сказки, нас всех отправят на нижние технические этажи в переработку на концентрат. \\n\\nОна говорит, что кроме Хрущевки ничего нет. Только бетон вверх, вниз и во все стороны. Но я знаю, что она врет. Папа ушел искать выход полгода назад и не вернулся. Я найду его.",
        "note_4_content": "В полутьме стоит скрипучая железная койка с серым казенным одеялом. На тумбочке — погнутый алюминиевый чайник с отбитым носиком. На стене криво висит засиженный мухами плакат Комитета с Ликвидатором №1, а в углу непрерывно капает старый ржавый вентиль... \\n\\n[Вы холодеете от ужаса. Это точное описание вашей жилой ячейки 412 в секторе 13-А!]\\n\\nОткуда автор этой записки знает, как выглядит моя комната? Кто принес её сюда?",
        "note_5_content": "ТЫ ДОЛЖЕН ПРОСНУТЬСЯ.\\n\\nТы сейчас находишься на {0} этаже. Но это ложь. Это не реально. Невозможно спускаться бесконечно в бетонном колодце без еды и отдыха. Ты спишь. Твой противогаз давно пуст. Твои легкие сгорели в парах Самосбора, но твой угасающий мозг судорожно цепляется за иллюзию спуска.\\n\\nТы спишь, Ликвидатор. Ты должен проснуться. Должен. Проснись.",
        "note_6_content": "ГРАЖДАНЕ ГИГАХРУЩЕВКИ! \\n\\nКомитет Общественного Спасения напоминает: \\n- Вся бесконечная структура Хрущевки — единственный оплот человечества. \\n- За пределами бетонных стен царит первородный хаос и пустота.\\n- Труд ликвидатора — священен. Отдавая жизнь за герметизацию прорывов, ликвидатор обретает вечный покой в сердцах выживших.\\n- Любые слухи о «выходе» наружу — это диверсия агентов хаоса, направленная на подрыв дисциплины. \\n\\nСОХРАНЯЙТЕ БДИТЕЛЬНОСТЬ! ДОКЛАДЫВАЙТЕ О ПОДОЗРИТЕЛЬНОЙ АКТИВНОСТИ В БЛИЖАЙШИЙ ПОСТ ЛИКВИДАТОРОВ.",
        "note_7_content": "ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ ПРОСНИСЬ",
        "note_8_content": "Если ты читаешь это... беги... \\n\\nЯ пробил шахту кабельного коллектора на 700 этаже. Комитет врет нам веками! Нет никакого хаоса снаружи. Стены Хруща — это лишь оболочка. Я видел... Я видел небо! Оно действительно синее, и там пахнет травой, а не хлоркой и горелой плотью. \\n\\nНо они следят за нами. Самосбор — это не природное бедствие. Они запускают его сами через вентиляцию каждый раз, когда население этажа начинает догадываться о правде. Это зачистка! \\nЕсли начнется Самосбор, не прячься. Стой на месте в коридоре. Прими его. Нас травят газом, вызывающим галлюцинации и сон, но это единственный способ сорвать датчики слежения и... [залито старой темной кровью]",
        "note_9_content": "Если вы нашли это, значит, я уже стал частью Хрущевки. \\n\\nЯ был Ликвидатором тридцать лет. Я заваривал двери, сжигал тварей и верил Комитету. Но выхода нет. Первый этаж — это миф. Самосбор — это не туман. Это дыхание великого спящего организма. Мы все находимся внутри гигантского живого существа, которое медленно переваривает нас. Единственный способ выбраться — перестать сопротивляться сну и открыть глаза. Но мне страшно. Да простит меня Хрущ.",
        "btn_bag": "Сумка",
        "label_notes_prefix": "Записки",
        "btn_descend_ending": "Застыть на месте и ждать",
        "focus_liquidator_body": "ТЕЛО ЛИКВИДАТОРА",
        "focus_liquidator_desc": "Погибший ликвидатор в форме. Обыскать подсумки (клавиша R).",
        "focus_search_body": "Обыскать тело",
        "focus_stair_gate": "ГЕРМОЗАТВОР ЛЕСТНИЦЫ",
        "focus_locked_by_system": "Заблокировано центральной системой ГИГАХРУЩА.",
        "focus_try_hack": "Попробовать взломать",
        "focus_gate_open_desc": "Затвор открыт. Проход на лестницу свободен.",
        "focus_close_gate": "Закрыть затвор",
        "focus_gate_locked_desc": "Массивный гермозатвор заперт! Нажмите B для взлома.",
        "focus_hack_gate": "Взломать затвор",
        "focus_door_open_desc": "Дверь открыта. Вы можете зайти внутрь (пройдите WASD).",
        "btn_close_door": "Закрыть дверь",
        "focus_door_closed_desc": "Гермодверь закрыта. Подойдите вплотную.",
        "btn_open_door_action": "Открыть дверь",
        "btn_interact_action": "Взаимодействие",
        "yes": "ЕСТЬ",
        "no": "НЕТ",
        "pcs": "шт",
        "btn_rebind_waiting": "Нажмите клавишу..."
    },
    "en": {
        "menu_title": "S A M O S B O R",
        "menu_subtitle": "LIQUIDATOR: FLOOR 1324 [3D FPS]",
        "menu_creator": "GAME CREATOR: @sw1therland",
        "init_interface": "> INITIALIZING LIQUIDATOR INTERFACE...",
        "network_ok": "> CONNECTING TO GIGA-KHRUSHCHEVKA NETWORK... OK.",
        "equipment_info": "> EQUIPMENT: PISTOL (24), GAS MASK, WATER, BAG.",
        "mission_info": "> MISSION: DESCEND TO FLOOR 1 AND SURVIVE.",
        "loading_sdk": "Loading SDK...",
        "btn_start": "START SHIFT",
        "btn_settings": "SETTINGS",
        "btn_achievements": "ACHIEVEMENTS",
        "btn_about": "ABOUT GAME",
        "hud_floor": "FLOOR:",
        "hud_health": "HEALTH:",
        "hud_water": "WATER:",
        "hud_ammo": "AMMO:",
        "hud_filter": "FILTER:",
        "hud_stamina": "STAMINA:",
        "fps_instructions": "WASD - Move | Shift - Sprint | Space - Kick | Mouse - Look | LMB - Shoot | R - Door | F - Flashlight | E - Listen | T - Gas Mask | Q - Water | G - Bag | Z - Search | B - Hacker",
        "mobile_flashlight": "Flashlight",
        "mobile_listen": "Listen",
        "mobile_door": "Door",
        "mobile_fire": "Fire",
        "listening_title": "LISTENING...",
        "listening_subtext": "Noises of the concrete shaft",
        "descent_transition_title": "DESCENDING TO LOWER FLOOR...",
        "btn_mask": "Equip Gas Mask",
        "btn_mask_remove": "Remove Gas Mask",
        "btn_drink": "Take a Sip of Water",
        "btn_descend_default": "Go to the stairs at the end of the hallway",
        "focus_title": "OBJECT FOCUS",
        "focus_object_none": "NO OBJECT TARGETED",
        "focus_object_desc": "Approach a door or interactive object",
        "btn_listen": "Listen",
        "btn_open_door": "Open",
        "room_actions_title": "ACTIONS",
        "btn_search_room": "Search furniture",
        "btn_lock_room": "Lock door",
        "btn_unlock_room": "Unlock door",
        "btn_exit_room": "Exit to hallway",
        "transition_actions_title": "TECHNICAL SHAFT",
        "btn_enter_transition": "Transit to another sector",
        "btn_cancel_transition": "Return to hallway",
        "notes_title": "BAG: FOUND NOTES",
        "notes_inventory_title": "INVENTORY",
        "bag_hacker_label": "HACKER TOOL",
        "bag_batteries_label": "BATTERIES",
        "notes_list_title": "NOTES",
        "select_note_prompt": "Select a note from the list on the left to read.",
        "gameover_notes_collected": "COLLECTED NOTES FROM GIGA-KHRUSHCHEVKA:",
        "credits_header": "CREDITS",
        "credits_author_label": "AUTHOR & DEVELOPER:",
        "credits_tech": "Technologies: HTML5, Three.js, Web Audio API<br>Specially for the Samosbor universe",
        "btn_restart": "START OVER",
        "pause_title": "PAUSE",
        "btn_resume": "RESUME SHIFT",
        "btn_exit": "EXIT TO MENU",
        "settings_title": "SETTINGS",
        "section_language": "SELECT LANGUAGE",
        "section_controls": "CONTROLS",
        "label_rebind_desc": "Click on an action, then press a new key on your keyboard.",
        "btn_reset": "RESET",
        "btn_save": "SAVE",
        "about_title": "ABOUT THE GAME",
        "achievements_title": "ACHIEVEMENTS",
        "achievements_subtitle": "LIQUIDATOR ACHIEVEMENTS LIST",
        "hack_title": "HERMETIC GATE DECRYPTER // BYPASS",
        "hack_sys": "SYSTEM: GROUP-B",
        "hack_bat": "BATTERY: OK",
        "hack_chan_a_label": "CHANNEL A",
        "hack_chan_b_label": "CHANNEL B",
        "hack_chan_c_label": "CHANNEL C",
        "hack_search": "FREQUENCY SEARCH:",
        "btn_hack_submit": "CONNECT",
        "btn_hack_cancel": "CANCEL",
        "achievement_popup_header": "Achievement Unlocked!",
        "ending_wakeup_title": "AWAKENING",
        "btn_true_ending_restart": "START SHIFT ANEW",
        "act_move_forward": "Move Forward",
        "act_move_backward": "Move Backward",
        "act_move_left": "Move Left",
        "act_move_right": "Move Right",
        "act_sprint": "Sprint (Accelerate)",
        "act_interact": "Interact / Door",
        "act_flashlight": "Flashlight On/Off",
        "act_listen": "Listen at Hermetic Door",
        "act_gasmask": "Put On/Off Gas Mask",
        "act_water": "Take a Sip of Water",
        "act_bag": "Open Bag (Notes)",
        "act_search": "Search Room",
        "act_hackertool": "Apply Hacker Tool",
        "act_pause": "Pause (Menu)",
        "door_apartment": "Apartment {0}",
        "door_armory": "Liquidator Post No.{0}",
        "door_contaminated": "Apartment {0} (RADIATION)",
        "door_nest": "Technical Section {0} (NEST)",
        "door_transition": "Transit {0}-{1}",
        "door_empty": "Door {0}",
        "room_warehouse": "Warehouse",
        "room_archive": "Archive",
        "room_compressor": "Compressor Room",
        "room_control": "Control Room",
        "room_ventilation": "Ventilation Chamber",
        "ach_butcher_title": "Gigahrush Butcher",
        "ach_butcher_desc": "Scare or destroy 50 monsters",
        "ach_hacker_title": "Self-Taught Hacker",
        "ach_hacker_desc": "Hack 100 hermetic gates",
        "ach_spendthrift_title": "Spendthrift",
        "ach_spendthrift_desc": "Spend all ammo before floor 1000",
        "ach_survivor_title": "Survivor",
        "ach_survivor_desc": "Descend below floor 1000",
        "ach_drinker_title": "Water Drinker",
        "ach_drinker_desc": "Take 50 sips of purified water",
        "ach_deceived_title": "Deceived",
        "ach_deceived_desc": "Reach the dead-end ending",
        "ach_awakened_title": "Awakened and Free",
        "ach_awakened_desc": "Reach the true ending",
        "ach_secret_desc": "[SECRET ACHIEVEMENT]",
        "about_content_html": "\n            <h3 class=\"glow-red\" style=\"margin-bottom: 5px; font-weight: bold;\">SAMOSBOR: LIQUIDATOR 1324</h3>\n            <p style=\"margin-top: 0; margin-bottom: 15px; color: var(--glow-green); font-weight: bold; font-family: var(--font-mono); font-size: 0.9rem;\">GAME CREATOR: @sw1therland</p>\n            <p>You are a Liquidator in a heavy sector of the Giga-Khrushchevka. Your shift has started on the 1324th floor. The goal is simple — descend to the 1st floor and survive.</p>\n            <p style=\"margin-top: 10px;\">During your descent, you will encounter Samosbor — a deadly phenomenon. Upon hearing the siren, immediately find a vacant apartment, close the hermetic door, and put on your gas mask.</p>\n            <p style=\"margin-top: 10px;\">Watch your water level and gas mask filter. Search sideboards and desks in apartments to find supplies, lore notes, a hermetic gate decrypter, and batteries.</p>\n            <p style=\"margin-top: 15px; color: var(--glow-amber); font-weight: bold;\">Controls:</p>\n            <ul style=\"margin-left: 20px; margin-top: 5px; display: flex; flex-direction: column; gap: 4px;\">\n                <li><b>WASD</b> — Move</li>\n                <li><b>Shift</b> — Sprint (drains stamina quickly)</li>\n                <li><b>Space</b> — Kick (repel running monster in the hallway)</li>\n                <li><b>Mouse</b> — Look (click screen to lock pointer)</li>\n                <li><b>LMB</b> — Shoot (scares the monster on the staircase)</li>\n                <li><b>R</b> — Close/open hermetic door</li>\n                <li><b>F</b> — Flashlight</li>\n                <li><b>E</b> — Listen to sounds behind the door</li>\n                <li><b>T</b> — Put on/take off gas mask</li>\n                <li><b>Q</b> — Take a sip of water</li>\n                <li><b>G / Bag</b> — Check notes and inventory</li>\n                <li><b>Z</b> — Search furniture (table/sideboard)</li>\n                <li><b>B</b> — Use hacker tool on staircase gates</li>\n                <li><b>Esc / P</b> — Pause</li>\n            </ul>\n        ",
        "ending_wakeup_desc": "You took a deep breath. The air is clean, warm, and smells of fresh grass.<br><br>The outlines of the sky, a green tree, and rustling leaves through half-closed eyelids gain warmth.<br><br>The nightmare of Giga-Khrushchevka is over. You have finally woken up.",
        "ending_wakeup_stats": "<div style=\"font-weight: bold; font-size: 0.95rem; color: #111111; margin-bottom: 5px; text-align: center; letter-spacing: 1px;\">TRUE ROOT ENDING</div>Notes collected and read: 10 / 10<br>Descended before awakening by: <span id=\"true-ending-floors-descended\" style=\"font-weight: bold; color: #6b0a0a;\">{0}</span> floors",
        "ending_wakeup_author": "<strong>Game Author:</strong> @sw1therland<br><span style=\"font-size: 0.72rem; color: #666666;\">Thank you for playing! You broke out of the Samostroy.</span>",
        "go_dehydration_title": "LIQUIDATED",
        "go_dehydration_desc": "<p>Your body could not withstand the terrible dehydration.</p><p>You collapsed onto the cold concrete steps of the staircase on floor {0}.</p><p>No one is coming to help. Your body will remain here until the next Samosbor dissolves it into brown slime.</p>",
        "go_stairs_monster_title": "TORN APART",
        "go_stairs_monster_desc": "<p>You didn't react in time.</p><p>The beast fell upon you from above, crushing your chest bones.</p><p>Sharp mandibles pierced through the visor of your gas mask. The last thing you heard was the squelch of biomass devouring your flesh.</p>",
        "go_opened_monster_title": "ELIMINATED",
        "go_opened_monster_desc": "<p>You opened the door without checking first.</p><p>A predatory Samosbor beast had set up its nest right past the threshold.</p><p>As soon as the bolts slid back, the multi-limbed biomass dragged you inside the dark room. You didn't even have time to scream.</p>",
        "go_samosbor_title": "DISSOLVED",
        "go_samosbor_desc": "<p>You remained in the corridor during the active phase of Samosbor.</p><p>The toxic fog ate away the rubber seals of your helmet and your skin in seconds.</p><p>Your consciousness faded as your tissues melted, flowing into the ventilation grates.</p>",
        "go_samosbor_gas_title": "SUFFOCATED",
        "go_samosbor_gas_desc": "<p>You hid in the room, but neglected protective equipment.</p><p>The Samosbor toxic gas seeped under the hermetic door.</p><p>Without a gas mask, your lungs filled with acidic vapors, causing immediate spasm and suffocation.</p>",
        "go_ending1_title": "AWAKENING",
        "go_ending1_desc": "<p>Having collected all the notes, you understood the true nature of Giga-Khrushchevka.</p><p>When the Samosbor fog rushed into the corridor, you did not run to hide. You froze in place, spreading your arms, and closed your eyes.</p><p>The world around shook, concrete walls began to crumble into pixels. The purple fog embraced you...</p><p>...And suddenly you took a sharp breath. Fresh, warm air filled your lungs.</p><p>You opened your eyes. You were lying on a soft bed. A bright, real SUN was shining through the window, and green leaves of trees were rustling outside. It was a dream. A long nightmare from which one could escape only by ceasing to fear.</p>",
        "go_ending2_title": "HOPELESSNESS",
        "go_ending2_desc": "<p>You overcame a long path and descended to the first floor.</p><p>But there is no passage outside. The heavy lock gates are hermetically welded with centuries of rust.</p><p>Behind you, the door to the staircase slammed shut with a crash. The mechanisms jammed. The latches won't move.</p><p>At this moment, the sirens wailed at maximum volume. A massive Samosbor began. There are no shelters. The doors are blocked. You are trapped in a concrete bag of the first floor, one-on-one with the deadly fog. This is the end of the line.</p>",
        "go_badge_death": "Death",
        "go_badge_ending1": "True ending",
        "go_badge_ending2": "Dead-end ending",
        "log_creep_1": "You heard a distant scraping inside the concrete walls...",
        "log_creep_2": "A draft carried the smell of rotten cabbage and raw meat.",
        "log_creep_3": "The lamps flickered for a moment. Helmet pressure stable.",
        "log_creep_4": "Somewhere deep below, a muffled metallic impact echoed.",
        "log_creep_5": "The Geiger counter clicks quietly. Background radiation normal.",
        "log_gh_scary": "The ghost is draining your flashlight's energy!",
        "log_water_low": "Warning! Critical dehydration level!",
        "log_descend_floor": "Descended to floor {0}.",
        "log_descend_warn": "Technical floor is blocked by hermetic gate. Hacking required.",
        "log_ascend_floor": "Ascended to floor {0}.",
        "log_room_clean": "You entered {0}. Air is clean. No threats detected.",
        "log_room_hazard": "You entered {0}. Air is radioactive! Put on your gas mask! (T key)",
        "log_room_nest": "You entered {0}. Slime on the walls is moving. You feel someone's presence! (Be ready!)",
        "log_room_hallway": "You exited to the hallway. Ventilation drives the cold air of Giga-Khrushchevka.",
        "log_lock_search_warn": "Cannot search furniture during Samosbor, it's too dangerous!",
        "log_lock_door": "You closed the apartment's hermetic door.",
        "log_unlock_door": "You opened the apartment's hermetic door.",
        "log_door_listen": "You listened behind the door of {0}...",
        "log_door_listen_clean": "Silence. It seems safe inside.",
        "log_door_listen_hazard": "Heavy footsteps and slithering slime noises can be heard. There is a beast!",
        "log_door_listen_transition": "A distant hum of the technical gate transformers can be heard.",
        "log_hack_bypass_ok": "Bypass: Channel {0} decrypter synchronized!",
        "log_hack_bypass_err": "Bypass: signal phase sync failed.",
        "log_hack_gate": "Hermetic Gate! The doors are going to: {0}...",
        "log_hack_gate_open": "open",
        "log_hack_gate_close": "close",
        "log_hack_hacker_err": "Decrypter: Failure. Circuit blocked by central system. Impossible to use!",
        "log_hack_note_samosbor": "You collected all notes but did not read them... you could not realize the truth.",
        "log_hack_tool_hot": "Decrypter is overheated! Wait for it to cool down.",
        "log_hack_tool_empty": "Decrypter battery is empty! Replace the battery.",
        "log_loot_corpse": "[✔] You searched the body, armor (+8) and filter (+40%) restored.",
        "log_loot_note": "[✔] Found note: \"{0}\"!",
        "log_loot_hacker": "[✔] You found a hermetic gate decrypter!",
        "log_loot_battery": "[✔] You found a battery (+1 pc., total: {0}).",
        "log_loot_synthesizer": "You found a food synthesizer (+50% water).",
        "log_loot_ammo": "[✔] You found ammo (+{0} pcs.).",
        "log_loot_filter": "You found a new filter (+50% charge).",
        "log_loot_empty": "You searched the furniture but found nothing useful.",
        "log_gasmask_equip": "Gas mask put on. Breathing restricted, visor fogging up.",
        "log_gasmask_unequip": "Gas mask removed.",
        "log_gasmask_no": "You don't have a gas mask!",
        "log_gasmask_empty": "Filter is empty! Air is poisoned!",
        "log_drink_sip": "Sip taken. Bottle water: {0}% remaining.",
        "log_siren_start": "[!] Samosbor siren wailed!",
        "log_siren_desc": "You have 4 seconds to shelter in a room and close the door!",
        "log_monster_shoot_scare": "You scared the beast with a gunshot! It retreated deep into the shaft!",
        "log_monster_shoot_dead": "You destroyed the beast with a gunshot!",
        "log_monster_kick": "You kicked the beast!",
        "log_monster_kick_dmg": "The beast bit your leg! Damage taken!",
        "log_crawler_run": "You heard rapid scratching of claws on the floor!",
        "log_crawler_warn": "A beast is running at you! Press SPACE to kick and repel it!",
        "log_crawler_safe": "Noise faded. The beast retreated into the vents.",
        "log_air_hazard": "You are inhaling toxic fumes! Put on your gas mask immediately (T key)!",
        "log_air_empty_warn": "Filter is empty! Mask does not protect!",
        "log_air_samosbor_phase": "[!] Samosbor has entered active phase: ~20 seconds. Do not go out!",
        "log_air_samosbor_melt": "[!!!] Walls are melting! Samosbor fills the corridors!",
        "log_air_samosbor_melt_dmg": "Acidic fog is corroding your helmet!",
        "log_air_filter_melt": "Filter neutralizes gases, but chemicals corrode the seals...",
        "log_air_filter_empty_melt": "Filter is empty! You are suffocating in toxic sludge!",
        "log_air_filter_norm": "Filter neutralizes gases. You are safe.",
        "log_samosbor_end": "Sirens went quiet. Samosbor ended. The danger has passed.",
        "log_game_start": "Shift started. Descend to the 1st floor...",
        "log_sound_init": "Audio system initialized.",
        "log_save_controls": "Control settings saved.",
        "log_dev_command": "Dev command executed.",
        "note_0_title": "Dirty scrap of paper (Floor ~1200)",
        "note_1_title": "Command Report (Floor ~1100)",
        "note_2_title": "Civil Defense Memo (Floor ~1000)",
        "note_3_title": "A Child's Diary (Floor ~900)",
        "note_4_title": "Strange Burnt Page",
        "note_5_title": "Unsigned Note",
        "note_6_title": "Agitation Leaflet (Floor ~800)",
        "note_7_title": "Tattered Scrap of Paper",
        "note_8_title": "Bloody Scrap of Notebook (Floor ~700)",
        "note_9_title": "Liquidator's Last Confession",
        "note_0_content": "Block 1290. Seventeenth day after block lockdown. \\n\\nThe ventilation hums like crazy, smelling constantly of raw, rotting meat and chemicals. The neighbor downstairs disappeared yesterday. His wife says she heard scraping behind the hermetic door in the middle of the night, as if someone was clawing at the steel seal. \\n\\nTap water has been brown for a week now. Seems like the intake filters are clogged with remains. The Liquidators aren't coming. We are told to stay in our apartments. Where is the damn sun? Does it even exist, or is concrete all there is to this world?",
        "note_1_content": "REPORT. Liquidator Junior Sergeant Sobolev. Group \"Beta-6\". \\n\\nWe were ordered to clean block 1105 after a local Samosbor breach. Everything went by the book, pouring reagents down the corridor. But in the end corridor we stumbled upon apartment #42. The hermetic door was locked from the inside. Children were screaming from in there, begging us to open it. \\n\\nBut the sensors showed a critical level of contamination behind the door. Samosbor slime was already breaking through the joints. The headquarters order was explicit: seal the block. We welded the door shut with blowtorches from the outside. The children screamed for another ten minutes while we worked. I still hear that sound when I close my eyes. Forgive us, Khrush.",
        "note_2_content": "MEMO FOR GIGA-KHRUSHCHEVKA RESIDENTS UPON SAMOSBOR INITIATION: \\n\\n1. At the first sound of the siren, immediately stop any movement along the staircases.\\n2. Enter the nearest living quarters or lock zone.\\n3. Close the hermetic door tightly. Tighten the manual clamping valves all the way.\\n4. Put on personal protective equipment (GP-9 gas mask or equivalent).\\n5. Do not approach ventilation shafts or doorways.\\n6. Ignore any sounds, voices of relatives or colleagues coming from outside during the active phase.\\n7. Await the arrival of Liquidators for disinfection procedures.",
        "note_3_content": "March 12. \\n\\nMom took away my colored pencils because I drew the sky. I remember it! It was so... blue, and a huge warm circle hung above, shining and heating. Mom started crying, tore up the drawing, and slapped my hands. She said the sky is a dangerous delusion of madmen, and if anyone from the Committee hears my stories, we will all be sent to the lower technical floors to be processed into food concentrate. \\n\\nShe says there is nothing besides Khrushchevka. Only concrete up, down, and in all directions. But I know she's lying. Dad went to look for a way out six months ago and didn't return. I will find him.",
        "note_4_content": "In the dim light stands a squeaky iron bunk bed with a gray institutional blanket. On the bedside table — a bent aluminum teapot with a chipped spout. On the wall hangs a fly-blown Committee poster with Liquidator #1, and in the corner an old rusty valve drips continuously... \\n\\n[You go cold with horror. This is an exact description of your living cell 412 in sector 13-A!]\\n\\nHow does the author of this note know what my room looks like? Who brought it here?",
        "note_5_content": "YOU MUST WAKE UP.\\n\\nYou are currently on floor {0}. But this is a lie. This is not real. It is impossible to descend indefinitely in a concrete well without food or rest. You are sleeping. Your gas mask has been empty for a long time. Your lungs burned in Samosbor fumes, but your dying brain feverishly clings to the illusion of descent.\\n\\nYou are sleeping, Liquidator. You must wake up. You must. Wake up.",
        "note_6_content": "CITIZENS OF GIGA-KHRUSHCHEVKA! \\n\\nThe Committee of Public Salvation reminds you: \\n- The infinite structure of Khrushchevka is the only stronghold of humanity. \\n- Outside the concrete walls reigns primeval chaos and emptiness.\\n- The work of a liquidator is sacred. By giving their life to seal breaches, a liquidator finds eternal peace in the hearts of survivors.\\n- Any rumors of an \"exit\" outside are sabotage by agents of chaos aimed at undermining discipline. \\n\\nPRESERVE VIGILANCE! REPORT SUSPICIOUS ACTIVITY TO THE NEAREST LIQUIDATOR POST.",
        "note_7_content": "WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP",
        "note_8_content": "If you read this... run... \\n\\nI broke through the shaft of the cable collector on floor 700. The Committee has been lying to us for centuries! There is no chaos outside. The walls of Khrush are just a shell. I saw... I saw the sky! It really is blue, and it smells of grass out there, not chlorine and burnt flesh. \\n\\nBut they are watching us. Samosbor is not a natural disaster. They release it themselves through the ventilation every time the population of a floor begins to guess the truth. It's a purge! \\nIf Samosbor starts, don't hide. Stand in place in the hallway. Embrace it. They poison us with gas that causes hallucinations and sleep, but it's the only way to disrupt the tracking sensors and... [stained with old dark blood]",
        "note_9_content": "If you find this, it means I have already become part of Khrushchevka. \\n\\nI was a Liquidator for thirty years. I welded doors, burned beasts, and believed the Committee. But there is no way out. The first floor is a myth. Samosbor is not fog. It is the breath of a great sleeping organism. We are all inside a giant living creature that slowly digests us. The only way to get out is to stop resisting sleep and open your eyes. But I'm scared. May Khrush forgive me.",
        "btn_bag": "Bag",
        "label_notes_prefix": "Notes",
        "btn_descend_ending": "Freeze in place and wait",
        "focus_liquidator_body": "LIQUIDATOR BODY",
        "focus_liquidator_desc": "A dead liquidator in uniform. Search pouches (Key R).",
        "focus_search_body": "Search body",
        "focus_stair_gate": "STAIRCASE HERMETIC GATE",
        "focus_locked_by_system": "Locked by the GIGA-KHRUSHCHEVKA central system.",
        "focus_try_hack": "Try to hack",
        "focus_gate_open_desc": "Gate is open. Passage to the staircase is free.",
        "focus_close_gate": "Close gate",
        "focus_gate_locked_desc": "Massive hermetic gate is locked! Press B to hack.",
        "focus_hack_gate": "Hack gate",
        "focus_door_open_desc": "Door is open. You can walk inside (move with WASD).",
        "btn_close_door": "Close door",
        "focus_door_closed_desc": "Hermetic door is closed. Approach closely.",
        "btn_open_door_action": "Open door",
        "btn_interact_action": "Interact",
        "yes": "YES",
        "no": "NO",
        "pcs": "pcs",
        "btn_rebind_waiting": "Press a key..."
    },
    "zh": {
        "menu_title": "萨 摩 斯 堡 (Samosbor)",
        "menu_subtitle": "清理员: 1324层 [3D FPS]",
        "menu_creator": "游戏创作者: @sw1therland",
        "init_interface": "> 初始化清理员界面...",
        "network_ok": "> 连接到巨型赫鲁晓夫楼网络... 成功。",
        "equipment_info": "> 装备: 手枪 (24), 防毒面具, 水, 背包。",
        "mission_info": "> 任务: 降落到 1 层并生存。",
        "loading_sdk": "加载 SDK...",
        "btn_start": "开始值班",
        "btn_settings": "设置",
        "btn_achievements": "成就",
        "btn_about": "关于游戏",
        "hud_floor": "楼层:",
        "hud_health": "生命值:",
        "hud_water": "水分:",
        "hud_ammo": "弹药:",
        "hud_filter": "滤毒罐:",
        "hud_stamina": "体力:",
        "fps_instructions": "WASD - 移动 | Shift - 冲刺 | Space - 踢击 | 鼠标 - 视角 | 左键 - 射击 | R - 门 | F - 手电筒 | E - 听门 | T - 防毒面具 | Q - 喝水 | G - 背包 | Z - 搜索 | B - 破解器",
        "mobile_flashlight": "手电筒",
        "mobile_listen": "倾听",
        "mobile_door": "门",
        "mobile_fire": "射击",
        "listening_title": "倾听中...",
        "listening_subtext": "混凝土井的噪音",
        "descent_transition_title": "下降到下一层...",
        "btn_mask": "戴上防毒面具",
        "btn_mask_remove": "摘下防毒面具",
        "btn_drink": "喝一口水",
        "btn_descend_default": "前往走廊尽头的楼梯",
        "focus_title": "目标焦点",
        "focus_object_none": "未选中目标",
        "focus_object_desc": "靠近一扇门或交互目标",
        "btn_listen": "听门",
        "btn_open_door": "打开",
        "room_actions_title": "操作",
        "btn_search_room": "搜寻家具",
        "btn_lock_room": "锁门",
        "btn_unlock_room": "解锁开门",
        "btn_exit_room": "回到走廊",
        "transition_actions_title": "技术闸门",
        "btn_enter_transition": "穿梭到另一个分区",
        "btn_cancel_transition": "返回走廊",
        "notes_title": "背包: 收集的便签",
        "notes_inventory_title": "物品栏",
        "bag_hacker_label": "破解器",
        "bag_batteries_label": "电池",
        "notes_list_title": "便签",
        "select_note_prompt": "从左侧列表中选择要阅读的便签。",
        "gameover_notes_collected": "收集的巨型赫鲁晓夫楼便签:",
        "credits_header": "开发团队 // CREDITS",
        "credits_author_label": "作者与开发人员:",
        "credits_tech": "技术: HTML5, Three.js, Web Audio API<br>特别致敬萨摩斯堡 (Samosbor) 宇宙",
        "btn_restart": "重新开始",
        "pause_title": "暂停",
        "btn_resume": "继续值班",
        "btn_exit": "退出到主菜单",
        "settings_title": "设置",
        "section_language": "选择语言",
        "section_controls": "键位控制",
        "label_rebind_desc": "点击某个动作，然后按下键盘上的新按键。",
        "btn_reset": "重置",
        "btn_save": "保存",
        "about_title": "关于游戏",
        "achievements_title": "成就",
        "achievements_subtitle": "清理员成就列表",
        "hack_title": "密封闸门解密器 // 绕过旁路",
        "hack_sys": "系统: B组",
        "hack_bat": "电池: 正常",
        "hack_chan_a_label": "通道 A",
        "hack_chan_b_label": "通道 B",
        "hack_chan_c_label": "通道 C",
        "hack_search": "搜寻频率:",
        "btn_hack_submit": "连接",
        "btn_hack_cancel": "取消",
        "achievement_popup_header": "解锁成就！",
        "ending_wakeup_title": "觉醒",
        "btn_true_ending_restart": "重新开启新值班",
        "act_move_forward": "向前移动",
        "act_move_backward": "向后移动",
        "act_move_left": "向左移动",
        "act_move_right": "向右移动",
        "act_sprint": "冲刺加速",
        "act_interact": "交互 / 关门",
        "act_flashlight": "手电筒开关",
        "act_listen": "倾听闸门后声响",
        "act_gasmask": "戴上/摘下防毒面具",
        "act_water": "喝一口水",
        "act_bag": "打开背包 (便签)",
        "act_search": "搜寻房间",
        "act_hackertool": "使用黑客破解工具",
        "act_pause": "暂停游戏 (菜单)",
        "door_apartment": "公寓 {0}",
        "door_armory": "清理员哨所 No.{0}",
        "door_contaminated": "公寓 {0} (辐射)",
        "door_nest": "技术分区 {0} (巢穴)",
        "door_transition": "通道 {0}-{1}",
        "door_empty": "防爆门 {0}",
        "room_warehouse": "仓库",
        "room_archive": "档案室",
        "room_compressor": "压缩机房",
        "room_control": "配电室",
        "room_ventilation": "通风机房",
        "ach_butcher_title": "巨型赫鲁晓夫楼屠夫",
        "ach_butcher_desc": "吓跑或消灭 50 只怪物",
        "ach_hacker_title": "自学成才的黑客",
        "ach_hacker_desc": "破解 100 次密封闸门",
        "ach_spendthrift_title": "败家子",
        "ach_spendthrift_desc": "在下降到 1000 层前用光所有子弹",
        "ach_survivor_title": "幸存者",
        "ach_survivor_desc": "下降到 1000 层以下",
        "ach_drinker_title": "饮水狂人",
        "ach_drinker_desc": "喝 50 口净化水",
        "ach_deceived_title": "被蒙蔽者",
        "ach_deceived_desc": "达成死胡同结局",
        "ach_awakened_title": "觉醒与自由",
        "ach_awakened_desc": "达成真结局",
        "ach_secret_desc": "[秘密成就]",
        "about_content_html": "\n            <h3 class=\"glow-red\" style=\"margin-bottom: 5px; font-weight: bold;\">萨摩斯堡: 清理员 1324</h3>\n            <p style=\"margin-top: 0; margin-bottom: 15px; color: var(--glow-green); font-weight: bold; font-family: var(--font-mono); font-size: 0.9rem;\">游戏创作者: @sw1therland</p>\n            <p>你是一名在巨型赫鲁晓夫楼重污染区服役的清理员。你的值班从 1324 层开始。你的目标很简单 —— 降落到 1 层并生存下来。</p>\n            <p style=\"margin-top: 10px;\">在下降的过程中，你将遭遇“萨摩斯堡”（Samosbor）—— 一种致命的未知生态灾难。当你听到警报器响起时，请立即寻找空置公寓，紧锁密封门，并戴上防毒面具。</p>\n            <p style=\"margin-top: 10px;\">注意你的饮水量和防毒面具滤毒罐。在公寓搜寻抽屉和餐柜，寻找物资、背景便签、闸门破解器和电池。</p>\n            <p style=\"margin-top: 15px; color: var(--glow-amber); font-weight: bold;\">操作指南:</p>\n            <ul style=\"margin-left: 20px; margin-top: 5px; display: flex; flex-direction: column; gap: 4px;\">\n                <li><b>WASD</b> — 移动</li>\n                <li><b>Shift</b> — 冲刺 (快速消耗体力)</li>\n                <li><b>Space (空格)</b> — 踢击 (在走廊中击退奔袭而来的怪物)</li>\n                <li><b>鼠标</b> — 移动视角 (点击屏幕锁定鼠标)</li>\n                <li><b>鼠标左键</b> — 开火 (可惊退楼梯间守口的怪物)</li>\n                <li><b>R</b> — 开启/关闭防爆门</li>\n                <li><b>F</b> — 手电筒开关</li>\n                <li><b>E</b> — 听取门后动静</li>\n                <li><b>T</b> — 佩戴/脱下防毒面具</li>\n                <li><b>Q</b> — 喝一口水</li>\n                <li><b>G / 背包</b> — 检查收集便签与行囊物品</li>\n                <li><b>Z</b> — 搜寻室内家具 (桌子/碗柜)</li>\n                <li><b>B</b> — 对楼梯网栅闸门使用破解器</li>\n                <li><b>Esc / P</b> — 暂停</li>\n            </ul>\n        ",
        "ending_wakeup_desc": "你深吸了一口气。空气如此纯净、温暖，散发着青草的芳香。<br><br>透过半开的眼睑，天空的轮廓、翠绿的大树和沙沙作响的叶子渐渐明晰，带着丝丝暖意。<br><br>巨型赫鲁晓夫楼的梦魇已经结束。你终于醒来了。",
        "ending_wakeup_stats": "<div style=\"font-weight: bold; font-size: 0.95rem; color: #111111; margin-bottom: 5px; text-align: center; letter-spacing: 1px;\">真结局 (根源觉醒)</div>已收集并阅读便签: 10 / 10<br>觉醒前已下降了: <span id=\"true-ending-floors-descended\" style=\"font-weight: bold; color: #6b0a0a;\">{0}</span> 层",
        "ending_wakeup_author": "<strong>游戏作者:</strong> @sw1therland<br><span style=\"font-size: 0.72rem; color: #666666;\">感谢游玩！你已成功逃离了“自我构筑”。</span>",
        "go_dehydration_title": "已被清除",
        "go_dehydration_desc": "<p>你的身体无法承受极度的脱水。</p><p>你倒在了第 {0} 层冷冰冰的混凝土楼梯阶梯上。</p><p>没有人会来救援。你的尸体将一直留在这里，直到下一次“萨摩斯堡”将它溶解为褐色的粘液。</p>",
        "go_stairs_monster_title": "被撕碎",
        "go_stairs_monster_desc": "<p>你没能及时做出反应。</p><p>怪物从上方扑向你，折断了你的肋骨与胸廓。</p><p>锋利的口器刺穿了防毒面具的镜片。你听到的最后一个声音是血肉被怪物咀嚼撕裂的沙沙声。</p>",
        "go_opened_monster_title": "已被清除",
        "go_opened_monster_desc": "<p>你没有事先听门动静就贸然开了门。</p><p>一只潜伏的萨摩斯堡怪物已经在门槛后面筑了巢。</p><p>闸门拉开的瞬间，多肢的异形生物将你拖进了黑暗的房间。你甚至连惨叫都来不及发出。</p>",
        "go_samosbor_title": "已被溶解",
        "go_samosbor_desc": "<p>在“萨摩斯堡”大爆发的活跃期里，你留在了走廊中。</p><p>剧毒的雾气在数秒内就腐蚀了头盔的橡胶垫圈和你的皮肤。</p><p>你的意识逐渐消散，而你的肉体则融化了，顺着通风隔栅流走。</p>",
        "go_samosbor_gas_title": "窒息而亡",
        "go_samosbor_gas_desc": "<p>你躲在房间里，但忽视了防护装备的防护状态。</p><p>萨摩斯堡的剧毒气体从密封门的缝隙中渗了进来。</p><p>在没有佩戴防毒面具的情况下，你的肺部吸满了酸性毒气，导致瞬间痉挛并窒息。</p>",
        "go_ending1_title": "觉醒 / 醒来",
        "go_ending1_desc": "<p>收集完所有便签后，你终于明白了巨型赫鲁晓夫楼的真正本质。</p><p>当萨摩斯堡毒雾涌进走廊时，你没有去躲藏。你静静地站在原地，张开双臂，闭上了眼睛。</p><p>周围的世界开始颤抖，混凝土墙壁像像素一样崩塌。紫色的迷雾拥抱了你...</p><p>...突然，你猛地吸了一口气。清新、温暖的空气涌进了肺部。</p><p>你睁开了眼睛。你躺在一张柔软的床上。灿烂的、真正的太阳正照在窗前，窗外是树木绿叶沙沙的响声。这只是一场梦。一场只要你不再恐惧就能逃离的漫长噩梦。</p>",
        "go_ending2_title": "无路可逃",
        "go_ending2_desc": "<p>你克服了漫长的旅程，终于降落到了第一层。</p><p>但是这里根本没有通往外界的通道。沉重的气密钢闸门早被数个世纪累积的铁锈焊死。</p><p>在你身后，通往楼梯间的门轰然关闭。锁死机构卡住，插销无法挪动半分。</p><p>就在这时，警报器开到了最大音量。“萨摩斯堡”大爆发开始了。没有任何避难所，所有门都被锁死。你被困在了一层这个混凝土棺材里，不得不和致死毒雾独处。这就是旅途的终点。</p>",
        "go_badge_death": "牺牲",
        "go_badge_ending1": "真结局",
        "go_badge_ending2": "死胡同结局",
        "log_creep_1": "你听到混凝土墙壁深处传来微弱的刮擦声...",
        "log_creep_2": "微风带来一股烂卷心菜和生肉的气味。",
        "log_creep_3": "灯光闪烁了一下。头盔气压稳定。",
        "log_creep_4": "下方深处传来一声沉闷的金属撞击声。",
        "log_creep_5": "盖革计数器轻微作响。背景辐射在正常范围内。",
        "log_gh_scary": "幽灵正在吸走你手电筒的电量！",
        "log_water_low": "警告！饮水度处于极其危险的低值！",
        "log_descend_floor": "降落到 {0} 层。",
        "log_descend_warn": "技术楼层被密封门卡锁。需要使用破解工具。",
        "log_ascend_floor": "上升到 {0} 层。",
        "log_room_clean": "你进入了 {0}。空气清新，没有发现威胁。",
        "log_room_hazard": "你进入了 {0}。空气被辐射污染！请立刻戴上防毒面具 (T 键)！",
        "log_room_nest": "你进入了 {0}。墙上的粘液在蠕动，你感觉到有异形潜伏！(做好准备)",
        "log_room_hallway": "你回到了走廊。强力通风系统吹来巨型赫鲁晓夫楼的阴冷空气。",
        "log_lock_search_warn": "萨摩斯堡爆发时无法搜寻家具，太危险了！",
        "log_lock_door": "你关上并锁住了公寓的密封防爆门。",
        "log_unlock_door": "你解锁并开启了公寓的密封防爆门。",
        "log_door_listen": "你贴在门前听取 {0} 后面的动静...",
        "log_door_listen_clean": "一片死寂，里面似乎很安全。",
        "log_door_listen_hazard": "听到了沉重的脚步声和粘液滑行声。门后有怪物！",
        "log_door_listen_transition": "能听到技术闸门变压器的远方嗡嗡声。",
        "log_hack_bypass_ok": "旁路绕过: 通道 {0} 解密成功！",
        "log_hack_bypass_err": "旁路绕过: 信号相位同步失败。",
        "log_hack_gate": "气密防爆闸门！钢闸门正在进行: {0}...",
        "log_hack_gate_open": "开启",
        "log_hack_gate_close": "关闭",
        "log_hack_hacker_err": "破解器: 故障。电路被赫鲁晓夫楼中心系统锁死，无法使用！",
        "log_hack_note_samosbor": "你收集了全部的便签，但没有进行阅读...你未能感知到巨塔的真相。",
        "log_hack_tool_hot": "破解器过热！请等待其冷却。",
        "log_hack_tool_empty": "破解器电池已耗尽！请更换电池。",
        "log_loot_corpse": "[✔] 你搜寻了同伴尸体，护甲 (+8) 和滤毒罐电量 (+40%) 已恢复。",
        "log_loot_note": "[✔] 收集到便签: \"{0}\"！",
        "log_loot_hacker": "[✔] 你找到了密封门黑客破解工具！",
        "log_loot_battery": "[✔] 你找到了备用电池 (+1 节，目前共有: {0} 节)。",
        "log_loot_synthesizer": "你发现了一台食品合成器 (+50% 水分)。",
        "log_loot_ammo": "[✔] 你找到了备用弹药 (+{0} 发)。",
        "log_loot_filter": "你找到了新滤毒罐 (+50% 电量)。",
        "log_loot_empty": "你翻找了抽屉家具，但什么有用的都没找到。",
        "log_gasmask_equip": "防毒面具已戴上。呼吸受限，视窗开始起雾。",
        "log_gasmask_unequip": "防毒面具已取下。",
        "log_gasmask_no": "你没有防毒面具！",
        "log_gasmask_empty": "滤毒罐已空！空气中含有剧毒！",
        "log_drink_sip": "喝了一口水。水壶中还剩 {0}% 的水分。",
        "log_siren_start": "[!] 萨摩斯堡警报响起！",
        "log_siren_desc": "你有 4 秒钟的时间寻找房间躲避并锁好防爆门！",
        "log_monster_shoot_scare": "你开枪惊吓了怪物！它退缩回了井道深处！",
        "log_monster_shoot_dead": "你开枪消灭了异形怪物！",
        "log_monster_kick": "你踢了怪物一脚！",
        "log_monster_kick_dmg": "怪物咬了你的腿！受到了伤害！",
        "log_crawler_run": "你听到地上传来爪子踩踏的急促爬行声！",
        "log_crawler_warn": "怪物正向你扑来！按下空格键踢开它！",
        "log_crawler_safe": "噪音消失了。怪物从通风道溜走了。",
        "log_air_hazard": "你正在吸入毒气！请迅速戴上防毒面具 (T 键)！",
        "log_air_empty_warn": "滤毒罐已空！防毒面具已失去防护效果！",
        "log_air_samosbor_phase": "[!] 萨摩斯堡大爆发已进入活跃期: 约 20 秒。千万不要出门！",
        "log_air_samosbor_melt": "[!!!] 墙壁正在溶解！毒雾充斥着走廊！",
        "log_air_samosbor_melt_dmg": "酸性毒雾正在腐蚀你的面具盔体！",
        "log_air_filter_melt": "滤毒罐在中和毒气，但强酸物质正在腐蚀头盔密封圈...",
        "log_air_filter_empty_melt": "滤毒罐已空！你在剧毒粘液中窒息受损！",
        "log_air_filter_norm": "滤毒罐正在运作，你目前安全。",
        "log_samosbor_end": "警报器安静了下来。萨摩斯堡大爆发结束了。危险已经过去。",
        "log_game_start": "值班开始。请向 1 层降落...",
        "log_sound_init": "音频系统初始化成功。",
        "log_save_controls": "键位控制设置已保存。",
        "log_dev_command": "Dev 命令已执行。",
        "note_0_title": "脏兮兮的纸片 (约1200层)",
        "note_1_title": "小队指挥官报告 (约1100层)",
        "note_2_title": "民防安全备忘录 (约1000层)",
        "note_3_title": "孩子的日记 (约900层)",
        "note_4_title": "烧焦的残页",
        "note_5_title": "无署名的便签",
        "note_6_title": "宣传传单 (约800层)",
        "note_7_title": "扯碎的纸屑",
        "note_8_title": "带血的本子残页 (约700层)",
        "note_9_title": "清理员临终忏悔",
        "note_0_content": "1290分区。分区封锁后的第十七天。\\n\\n通风管道像疯了一样嗡嗡作响，里面不断飘出腐烂生肉和化学药剂的恶臭。楼下的邻居昨天失踪了。他妻子说，半夜里听到密封防撬门后面有磨牙刮擦声，好像有什么东西想用爪子撬开钢制密封条。\\n\\n自来水已经发褐一个星期了。供水网的过滤器大概被尸骸堵住了。清理员没来。我们被告知待在各自的公寓里。该死的太阳在哪？它真的存在吗，还是说这个世界只有混凝土？",
        "note_1_content": "报告。清理员下士 索博列夫。小队“贝塔-6”。\\n\\n在发生局部萨摩斯堡泄露后，我们接到命令清除1105分区。一切都按照规程进行，我们往走廊里倾倒化学试剂。但在走廊尽头，我们撞上了42号公寓。气密防爆门从里面锁死了。里面有孩子在尖叫，哭喊着哀求我们开门。\\n\\n但传感器显示门后是致命级污染。“萨摩斯堡”粘液已经开始往密封夹缝外溢。总部的命令很明确：封锁并焊死整个分区。我们用喷灯在外面把防爆门彻底焊死了。我们在焊接工作时，里面的孩子大概又哭嚎了十分钟。当我闭上眼睛，我依然能听到那声音。原谅我们吧，赫鲁晓夫楼。",
        "note_2_content": "致赫鲁晓夫巨塔居民 —— 萨摩斯堡爆发时防范备忘录：\\n\\n1. 警报声响起时，请立即停止在楼梯间的任何移动。\\n2. 尽快进入最近的居民住宅或闸阀封锁舱。\\n3. 紧锁密封门。将手动气密手轮顺时针拧到最紧。\\n4. 佩戴个人呼吸防护设备 (GP-9 型面具或同类兼容产品)。\\n5. 远离通风井道及门廊开口。\\n6. 灾难爆发活跃期，请无视门外传来的任何异响、包括亲属或战友的呼救声。\\n7. 在住宅内静候清理小队抵达进行洗消灭活作业。",
        "note_3_content": "3月12日。\\n\\n妈妈没收了我的彩色铅笔，因为我画了天空。我记得它的样子！它是那样的... 湛蓝湛蓝，上面挂着一个又圆又暖的大球，会发光还会发热。妈妈看着画哭了出来，把画撕碎，狠狠地拍打我的手。她对我说天空是疯子的胡话，要是被委员会的人听见我讲天空，我们全家都会被发配到下层底舱里、做成合成淀粉营养罐头。\\n\\n她说除了赫鲁晓夫大楼以外，什么都没有。头顶、脚下，往任何方向走都只有水泥。但我知道她在骗人。爸爸六个月前去找出口，就再也没有回来。我会找到他的。",
        "note_4_content": "昏暗的微光下摆着一张咯吱作响的铁架床，上面铺着灰色的公用毛毯。床头柜上放着一个瘪了口的铝茶壶。墙上歪歪斜斜地贴着一张布满苍蝇迹的委员会海报，海报上印着“一号清理员”，屋角的一个生锈的老阀门在不停滴水...\\n\\n[你浑身因恐惧而感到冰冷。这恰恰正是你在 13-A 分区 412 号宿舍房间里的布置！]\\n\\n写下这张便签的人是怎么知道我的房间摆设的？是谁把它带到这里的？",
        "note_5_content": "你必须醒过来。\\n\\n你现在在第 {0} 层。但这是个谎言，这里不是真实的。人不可能在没有食物和睡眠的情况下，在这混凝土深井里永无止境地降落。你在梦境之中。你的面具滤毒罐早就用光了。你的双肺已被萨摩斯堡的强酸雾气灼焦熔化，但你逐渐窒息脑缺氧的脑干依然在死死抱紧降落的幻想。\\n\\n你睡着了，清理员。你必须醒过来。必须要。醒来吧。",
        "note_6_content": "致赫鲁晓夫大楼全体市民！\\n\\n社会救助委员会在此提醒各位：\\n- 巨型赫鲁晓夫楼的无尽水泥建筑结构是人类文明的唯一避风港。\\n- 墙外没有出路，只有原始虚无与混乱灾异。\\n- 清理员的工作是神圣的。为了阻止灾难泄露而牺牲自己，清理员将在生者心中获得不朽与永宁。\\n- 任何关于外界有“出口”的言论都是混乱势力意图动摇纪律的破坏宣传。\\n\\n保持警惕！向最近的清理哨岗举报可疑行为。",
        "note_7_content": "快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来 快醒来",
        "note_8_content": "如果你能读到这行字... 跑...\\n\\n我在 700 层打穿了电缆管道竖井。委员会向我们撒了几个世纪的谎！外面根本就没有什么虚空混乱。巨塔的钢筋混凝土只是一层外壳。我看到了... 我看到了真正的天空！它真的是蓝色的，外面闻起来是青草的芬芳，绝不是什么漂白粉和烧焦血肉的臭气。\\n\\n但他们在监视我们。萨摩斯堡根本不是什么自然生态现象。每当某层的居民开始察觉到真相时，他们就会通过通风系统主动释放毒气。这是一场大清洗！\\n如果萨摩斯堡警报响起，别去躲藏。就站在走廊中央。接纳它。他们用致幻气体让我们沉睡，但只有这样才能干扰他们的跟踪传感器，然后... [被大片暗红色血迹糊住了]",
        "note_9_content": "如果你找到这个，说明我已经成了赫鲁晓夫巨塔的一部分。\\n\\n我当了三十年清理员。我焊死过防爆门，烧死过异形怪物，坚信委员会说的每一句话。但外面根本没有路。一层只是个虚构的传说。萨摩斯堡也不是毒雾，它其实是那个沉睡中的庞大有机巨兽在呼吸。我们全都在这头巨大怪物的肠道里，正被它慢慢消化。逃离的唯一方法就是停止在睡梦中挣扎、睁开双眼。但我感到好害怕。愿大楼宽恕我。",
        "btn_bag": "背包",
        "label_notes_prefix": "笔记",
        "btn_descend_ending": "伫立原地等待",
        "focus_liquidator_body": "清理人员尸体",
        "focus_liquidator_desc": "一名身穿制服的死去的清理人员。搜寻袋子（R键）。",
        "focus_search_body": "搜寻尸体",
        "focus_stair_gate": "楼梯气密闸门",
        "focus_locked_by_system": "被巨型赫鲁晓夫楼中央系统锁定。",
        "focus_try_hack": "尝试黑入",
        "focus_gate_open_desc": "闸门已开。前往楼梯的通道已畅通。",
        "focus_close_gate": "关闭闸门",
        "focus_gate_locked_desc": "沉重的气密闸门已锁！按B键黑入。",
        "focus_hack_gate": "黑入闸门",
        "focus_door_open_desc": "门已开。你可以走进去（使用WASD移动）。",
        "btn_close_door": "关门",
        "focus_door_closed_desc": "气密门已关闭。走近一些。",
        "btn_open_door_action": "开门",
        "btn_interact_action": "交互",
        "yes": "有",
        "no": "无",
        "pcs": "个",
        "btn_rebind_waiting": "按下按键..."
    },
    "de": {
        "menu_title": "S A M O S B O R",
        "menu_subtitle": "LIQUIDATOR: ETAGE 1324 [3D FPS]",
        "menu_creator": "SPIELENTWICKLER: @sw1therland",
        "init_interface": "> INITIATION DER LIQUIDATOR-SCHNITTSTELLE...",
        "network_ok": "> VERBINDUNG ZUM GIGA-CHRUSCHTSCHOWKA-NETZWERK... OK.",
        "equipment_info": "> AUSRÜSTUNG: PISTOLE (24), GASMASKE, WASSER, TASCHE.",
        "mission_info": "> ZIEL: AUF DIE 1. ETAGE ABSTEIGEN UND ÜBERLEBEN.",
        "loading_sdk": "Lade SDK...",
        "btn_start": "SCHICHT BEGINNEN",
        "btn_settings": "EINSTELLUNGEN",
        "btn_achievements": "ERFOLGE",
        "btn_about": "ÜBER DAS SPIEL",
        "hud_floor": "ETAGE:",
        "hud_health": "LEBEN:",
        "hud_water": "WASSER:",
        "hud_ammo": "MUNITION:",
        "hud_filter": "FILTER:",
        "hud_stamina": "AUSDAUER:",
        "fps_instructions": "WASD - Bewegen | Shift - Sprinten | Space - Tritt | Maus - Umschauen | LMB - Schießen | R - Tür | F - Taschenlampe | E - Lauschen | T - Gasmaske | Q - Wasser | G - Tasche | Z - Suchen | B - Hacken",
        "mobile_flashlight": "Licht",
        "mobile_listen": "Lauschen",
        "mobile_door": "Tür",
        "mobile_fire": "Schießen",
        "listening_title": "LAUSCHE...",
        "listening_subtext": "Geräusche des Betonschachts",
        "descent_transition_title": "ABSTIEG ZUR UNTEREN ETAGE...",
        "btn_mask": "Gasmaske aufsetzen",
        "btn_mask_remove": "Gasmaske abnehmen",
        "btn_drink": "Einen Schluck trinken",
        "btn_descend_default": "Gehen Sie zur Treppe am Ende des Flurs",
        "focus_title": "OBJEKTFOKUS",
        "focus_object_none": "KEIN OBJEKT GEWÄHLT",
        "focus_object_desc": "Nähern Sie sich einer Tür oder einem Interaktionspunkt",
        "btn_listen": "Lauschen",
        "btn_open_door": "Öffnen",
        "room_actions_title": "AKTIONEN",
        "btn_search_room": "Möbel durchsuchen",
        "btn_lock_room": "Tür verriegeln",
        "btn_unlock_room": "Tür entriegeln",
        "btn_exit_room": "In den Flur gehen",
        "transition_actions_title": "TECHNISCHE SCHLEUSE",
        "btn_enter_transition": "In anderen Sektor wechseln",
        "btn_cancel_transition": "In den Flur zurückkehren",
        "notes_title": "TASCHE: GEFUNDENE NOTIZEN",
        "notes_inventory_title": "INVENTAR",
        "bag_hacker_label": "DECODER",
        "bag_batteries_label": "BATTERIEN",
        "notes_list_title": "NOTIZEN",
        "select_note_prompt": "Wählen Sie eine Notiz aus der Liste links zum Lesen.",
        "gameover_notes_collected": "GEWELTE NOTIZEN AUS GIGA-CHRUSCHTSCHOWKA:",
        "credits_header": "ABSPANN // CREDITS",
        "credits_author_label": "AUTOR & ENTWICKLER:",
        "credits_tech": "Technologien: HTML5, Three.js, Web Audio API<br>Speziell für das Samosbor-Universum",
        "btn_restart": "NEUSTART",
        "pause_title": "PAUSE",
        "btn_resume": "SCHICHT FORTSETZEN",
        "btn_exit": "HAUPTMENÜ",
        "settings_title": "EINSTELLUNGEN",
        "section_language": "SPRACHE WÄHLEN // SELECT LANGUAGE",
        "section_controls": "STEUERUNG // CONTROLS",
        "label_rebind_desc": "Klicken Sie auf eine Aktion, und drücken Sie dann eine neue Taste auf der Tastatur.",
        "btn_reset": "ZURÜCKSETZEN",
        "btn_save": "SPEICHERN",
        "about_title": "ÜBER DAS SPIEL",
        "achievements_title": "ERFOLGE",
        "achievements_subtitle": "ERFOLGSLISTE DES LIQUIDATORS",
        "hack_title": "GERMETISCHES TOR DECODER // BYPASS",
        "hack_sys": "SYSTEM: GRUPE-B",
        "hack_bat": "BATTERIE: OK",
        "hack_chan_a_label": "KANAL A",
        "hack_chan_b_label": "KANAL B",
        "hack_chan_c_label": "KANAL C",
        "hack_search": "FREQUENZSUCHE:",
        "btn_hack_submit": "VERBINDEN",
        "btn_hack_cancel": "ABBRECHEN",
        "achievement_popup_header": "Erfolg freigeschaltet!",
        "ending_wakeup_title": "ERWACHEN",
        "btn_true_ending_restart": "NEUE SCHICHT STARTEN",
        "act_move_forward": "Bewegen vorwärts",
        "act_move_backward": "Bewegen rückwärts",
        "act_move_left": "Bewegen links",
        "act_move_right": "Bewegen rechts",
        "act_sprint": "Sprinten (Beschleunigen)",
        "act_interact": "Interagieren / Tür",
        "act_flashlight": "Taschenlampe Ein/Aus",
        "act_listen": "Lauschen an der Panzertür",
        "act_gasmask": "Gasmaske aufsetzen/abnehmen",
        "act_water": "Einen Schluck trinken",
        "act_bag": "Tasche öffnen (Notizen)",
        "act_search": "Raum durchsuchen",
        "act_hackertool": "Decoder verwenden",
        "act_pause": "Pause (Menü)",
        "door_apartment": "Wohnung {0}",
        "door_armory": "Liquidatorenposten Nr. {0}",
        "door_contaminated": "Wohnung {0} (STRAHLUNG)",
        "door_nest": "Technische Sektion {0} (NEST)",
        "door_transition": "Übergang {0}-{1}",
        "door_empty": "Tür {0}",
        "room_warehouse": "Lager",
        "room_archive": "Archiv",
        "room_compressor": "Kompreßorraum",
        "room_control": "Schalttafelraum",
        "room_ventilation": "Lüftungskammer",
        "ach_butcher_title": "Metzger der Chruschtschowka",
        "ach_butcher_desc": "Erschrecken oder eliminieren Sie 50 Monster",
        "ach_hacker_title": "Autodidaktischer Hacker",
        "ach_hacker_desc": "Hacken Sie 100 hermetische Tore",
        "ach_spendthrift_title": "Verschwender",
        "ach_spendthrift_desc": "Verbrauchen Sie alle Munition vor Etage 1000",
        "ach_survivor_title": "Überlebender",
        "ach_survivor_desc": "Steigen Sie unter Etage 1000 ab",
        "ach_drinker_title": "Säufer",
        "ach_drinker_desc": "Trinken Sie 50 Schlucke Wasser",
        "ach_deceived_title": "Betrogener",
        "ach_deceived_desc": "Erreichen Sie das Sackgassen-Ende",
        "ach_awakened_title": "Erwacht und frei",
        "ach_awakened_desc": "Erreichen Sie das wahre Ende",
        "ach_secret_desc": "[GEHEIMER ERFOLG]",
        "about_content_html": "\n            <h3 class=\"glow-red\" style=\"margin-bottom: 5px; font-weight: bold;\">SAMOSBOR: LIQUIDATOR 1324</h3>\n            <p style=\"margin-top: 0; margin-bottom: 15px; color: var(--glow-green); font-weight: bold; font-family: var(--font-mono); font-size: 0.9rem;\">SPIELENTWICKLER: @sw1therland</p>\n            <p>Sie sind ein Liquidator im schweren Sektor der Giga-Chruschtschowka. Ihre Schicht hat auf der 1324. Etage begonnen. Das Ziel ist einfach — steigen Sie zur 1. Etage ab und überleben Sie.</p>\n            <p style=\"margin-top: 10px;\">Während Ihres Abstiegs stoßen Sie auf Samosbor — ein tödliches Phänomen. Wenn Sie die Sirene hören, suchen Sie sofort eine freie Wohnung auf, schließen Sie die Panzertür und setzen Sie Ihre Gasmaske auf.</p>\n            <p style=\"margin-top: 10px;\">Achten Sie auf Ihren Wasserstand und den Filter der Gasmaske. Durchsuchen Sie Sideboards und Tische in Wohnungen, um Vorräte, Notizen, einen Decoder und Batterien zu finden.</p>\n            <p style=\"margin-top: 15px; color: var(--glow-amber); font-weight: bold;\">Steuerung:</p>\n            <ul style=\"margin-left: 20px; margin-top: 5px; display: flex; flex-direction: column; gap: 4px;\">\n                <li><b>WASD</b> — Bewegung</li>\n                <li><b>Shift</b> — Sprinten (verbraucht schnell Ausdauer)</li>\n                <li><b>Space (Leertaste)</b> — Tritt (um das rennende Monster im Flur wegzustoßen)</li>\n                <li><b>Maus</b> — Umschauen (klicken, um den Zeiger zu sperren)</li>\n                <li><b>LMB</b> — Schuss (erschreckt das Monster auf dem Treppenabsatz)</li>\n                <li><b>R</b> — Panzertür öffnen/schließen</li>\n                <li><b>F</b> — Taschenlampe</li>\n                <li><b>E</b> — Auf Geräusche hinter der Tür lauschen</li>\n                <li><b>T</b> — Gasmaske aufsetzen/abnehmen</li>\n                <li><b>Q</b> — Einen Schluck Wasser trinken</li>\n                <li><b>G / Tasche</b> — Inventar und Notizen prüfen</li>\n                <li><b>Z</b> — Möbel durchsuchen (Tisch/Schrank)</li>\n                <li><b>B</b> — Decoder an Treppentoren verwenden</li>\n                <li><b>Esc / P</b> — Pause</li>\n            </ul>\n        ",
        "ending_wakeup_desc": "Sie haben tief eingeatmet. Die Luft ist rein, warm und duftet nach frischem Gras.<br><br>Die Umrisse des Himmels, eines grünen Baumes und raschelnder Blätter durch halb geschlossene Lider gewinnen an Wärme.<br><br>Der Albtraum der Giga-Chruschtschowka ist vorbei. Sie sind endlich aufgewacht.",
        "ending_wakeup_stats": "<div style=\"font-weight: bold; font-size: 0.95rem; color: #111111; margin-bottom: 5px; text-align: center; letter-spacing: 1px;\">WAHRES ENDE</div>Notizen gesammelt und gelesen: 10 / 10<br>Vor dem Erwachen abgestiegen um: <span id=\"true-ending-floors-descended\" style=\"font-weight: bold; color: #6b0a0a;\">{0}</span> Etagen",
        "ending_wakeup_author": "<strong>Autor des Spiels:</strong> @sw1therland<br><span style=\"font-size: 0.72rem; color: #666666;\">Danke fürs Spielen! Sie sind dem Samostroy entkommen.</span>",
        "go_dehydration_title": "LIQUIDIERT",
        "go_dehydration_desc": "<p>Ihr Körper konnte der schrecklichen Dehydrierung nicht standhalten.</p><p>Sie brachen auf den kalten Betonstufen des Treppenhauses auf Etage {0} zusammen.</p><p>Niemand wird kommen, um zu helfen. Ihr Körper wird hier bleiben, bis der nächste Samosbor ihn in braunen Schleim auflöst.</p>",
        "go_stairs_monster_title": "ZERISSEN",
        "go_stairs_monster_desc": "<p>Sie haben nicht rechtzeitig reagiert.</p><p>Das Biest stürzte von oben auf Sie herab und brach Ihre Rippen.</p><p>Scharfe Kiefer durchbohrten das Visier Ihrer Gasmaske. Das Letzte, was Sie hörten, war das Schmatzen der Biomasse, die Ihr Fleisch fraß.</p>",
        "go_opened_monster_title": "ELIMINIERT",
        "go_opened_monster_desc": "<p>Sie haben die Tür geöffnet, ohne vorher zu lauschen.</p><p>Ein rauberisches Samosbor-Biest hatte sein Nest direkt hinter der Schwelle gebaut.</p><p>Sobald die Riegel zurückgingen, zog die vielgliedrige Biomasse Sie in den dunklen Raum. Sie hatten nicht einmal Zeit zu schreien.</p>",
        "go_samosbor_title": "AUFGELÖST",
        "go_samosbor_desc": "<p>Sie blieben während der aktiven Phase von Samosbor im Flur.</p><p>Der giftige Nebel zerfraß die Gummidichtungen Ihres Helms und Ihre Haut in Sekundenschnelle.</p><p>Ihr Bewusstsein schwand, während Ihr Gewebe schmolz und in die Lüftungsgitter floss.</p>",
        "go_samosbor_gas_title": "ERSTICKT",
        "go_samosbor_gas_desc": "<p>Sie haben sich im Zimmer versteckt, aber die Schutzausrüstung vernachlässigt.</p><p>Das giftige Samosbor-Gas drang unter der Panzertür durch.</p><p>Ohne Gasmaske füllte sich Ihre Lunge mit ätzenden Dämpfen, was zu sofortigem Krampf und Erstickung führte.</p>",
        "go_ending1_title": "ERWACHEN",
        "go_ending1_desc": "<p>Nachdem Sie alle Notizen gesammelt hatten, verstanden Sie die wahre Natur der Giga-Chruschtschowka.</p><p>Als der Samosbor-Nebel in den Flur strömte, liefen Sie nicht weg, um sich zu verstecken. Sie blieben auf der Stelle stehen, breiteten die Arme aus und schlossen die Augen.</p><p>Die Welt um Sie herum bebte, Betonwände begannen in Pixeln zu zerfallen. Der violette Nebel umarmte Sie...</p><p>...Und plötzlich machten Sie einen tiefen Atemzug. Frische, warme Luft füllte Ihre Lunge.</p><p>Sie öffneten die Augen. Sie lagen auf einem weichen Bett. Die echte SONNE schien hell durch das Fenster, und grüne Blätter raschelten draußen. Es war ein Traum. Ein langer Albtraum, dem man nur entkommen konnte, indem man aufhörte, sich zu fürchten.</p>",
        "go_ending2_title": "AUSWEGLOSIGKEIT",
        "go_ending2_desc": "<p>Sie haben einen langen Weg zurückgelegt und sind im ersten Stock angekommen.</p><p>Doch draußen gibt es keinen Durchgang. Die schweren Schleusentore sind durch jahrhundertelangen Rost hermetisch verschweißt.</p><p>Hinter Ihnen schlug die Tür zum Treppenhaus mit einem Krachen zu. Die Mechanismen sind blockiert. Die Riegel lassen sich nicht bewegen.</p><p>In diesem Moment heulten die Sirenen mit maximaler Lautstärke. Ein gewaltiger Samosbor begann. Es gibt keine Zuflucht. Die Türen sind versperrt. Sie sind in einem Betonsack der ersten Etage gefangen, allein mit dem tödlichen Nebel. Dies ist das Ende des Weges.</p>",
        "go_badge_death": "Tod",
        "go_badge_ending1": "Wahres Ende",
        "go_badge_ending2": "Sackgassen-Ende",
        "log_creep_1": "Sie hörten ein fernes Scharren in den Betonwänden...",
        "log_creep_2": "Ein Luftzug trug den Geruch von verrottetem Kohl und rohem Fleisch herbei.",
        "log_creep_3": "Die Lampen flackerten für einen Moment. Helmdruck stabil.",
        "log_creep_4": "Irgendwo tief unten hallte ein gedämpfter metallischer Aufprall wider.",
        "log_creep_5": "Der Geigerzähler knackt leise. Hintergrundstrahlung im Normbereich.",
        "log_gh_scary": "Der Geist entzieht Ihrer Taschenlampe die Energie!",
        "log_water_low": "Warnung! Kritischer Dehydrierungsgrad!",
        "log_descend_floor": "Auf Etage {0} abgestiegen.",
        "log_descend_warn": "Technische Etage ist durch hermetisches Tor blockiert. Hacken erforderlich.",
        "log_ascend_floor": "Auf Etage {0} aufgestiegen.",
        "log_room_clean": "Sie haben {0} betreten. Die Luft ist rein. Keine Bedrohungen erkannt.",
        "log_room_hazard": "Sie haben {0} betreten. Die Luft ist radioaktiv! Gasmaske aufsetzen! (T-Taste)",
        "log_room_nest": "Sie haben {0} betreten. Der Schleim an den Wänden bewegt sich. Sie spüren eine Präsenz! (Seien Sie bereit)",
        "log_room_hallway": "Sie sind in den Flur zurückgekehrt. Die Belüftung treibt die kalte Luft der Chruschtschowka an.",
        "log_lock_search_warn": "Während des Samosbors dürfen keine Möbel durchsucht werden, das ist zu gefährlich!",
        "log_lock_door": "Sie haben die Panzertür der Wohnung geschlossen.",
        "log_unlock_door": "Sie haben die Panzertür der Wohnung geöffnet.",
        "log_door_listen": "Sie lauschen an der Tür von {0}...",
        "log_door_listen_clean": "Stille. Es scheint sicher zu sein.",
        "log_door_listen_hazard": "Schwere Schritte und das Schlittern von Schleim sind zu hören. Da ist ein Biest!",
        "log_door_listen_transition": "Ein fernes Summen der Transformatoren der Schleuse ist zu hören.",
        "log_hack_bypass_ok": "Bypass: Kanal {0} erfolgreich dechiffriert!",
        "log_hack_bypass_err": "Bypass: Signalphasen-Synchronisationsfehler.",
        "log_hack_gate": "Hermetisches Tor! Die Tore bewegen sich in Richtung: {0}...",
        "log_hack_gate_open": "Öffnung",
        "log_hack_gate_close": "Schließung",
        "log_hack_hacker_err": "Decoder: Fehler. Schaltkreis durch Zentralsystem blockiert. Verwendung unmöglich!",
        "log_hack_note_samosbor": "Sie haben alle Notizen gesammelt, aber nicht gelesen... Sie konnten die Wahrheit nicht erkennen.",
        "log_hack_tool_hot": "Decoder ist überhitzt! Warten Sie, bis er abgekühlt ist.",
        "log_hack_tool_empty": "Decoder-Batterie ist leer! Ersetzen Sie die Batterie.",
        "log_loot_corpse": "[✔] Sie haben die Leiche durchsucht, Rüstung (+8) und Filter (+40%) wiederhergestellt.",
        "log_loot_note": "[✔] Notiz gefunden: \"{0}\"!",
        "log_loot_hacker": "[✔] Sie haben einen Decoder gefunden!",
        "log_loot_battery": "[✔] Sie haben eine Batterie gefunden (+1 Stk., insgesamt: {0}).",
        "log_loot_synthesizer": "Sie haben einen Lebensmittelsynthesizer gefunden (+50% Wasser).",
        "log_loot_ammo": "[✔] Sie haben Munition gefunden (+{0} Stk.).",
        "log_loot_filter": "Sie haben einen neuen Filter gefunden (+50% Ladung).",
        "log_loot_empty": "Sie haben die Möbel durchsucht, aber nichts Nützliches gefunden.",
        "log_gasmask_equip": "Gasmaske aufgesetzt. Atmung eingeschränkt, Visier beschlägt.",
        "log_gasmask_unequip": "Gasmaske abgenommen.",
        "log_gasmask_no": "Sie haben keine Gasmaske!",
        "log_gasmask_empty": "Filter ist leer! Luft ist vergiftet!",
        "log_drink_sip": "Schluck genommen. Flaschenwasser: {0}% verbleibend.",
        "log_siren_start": "[!] Samosbor-Sirene heult!",
        "log_siren_desc": "Sie haben 4 Sekunden Zeit, um sich in einem Raum in Sicherheit zu bringen und die Tür zu schließen!",
        "log_monster_shoot_scare": "Sie haben das Biest mit einem Schuss erschreckt! Es hat sich tief in den Schacht zurückgezogen!",
        "log_monster_shoot_dead": "Sie haben das Biest mit einem Schuss vernichtet!",
        "log_monster_kick": "Sie haben das Biest getreten!",
        "log_monster_kick_dmg": "Das Biest hat Sie ins Bein gebissen! Schaden erlitten!",
        "log_crawler_run": "Sie hörten ein schnelles Kratzen von Krallen auf dem Boden!",
        "log_crawler_warn": "Ein Biest rennt auf Sie zu! Drücken Sie die LEERTASTE, um es wegzustoßen!",
        "log_crawler_safe": "Geräusch verblasst. Das Biest ist in die Lüftung geflohen.",
        "log_air_hazard": "Sie atmen giftige Dämpfe ein! Gasmaske sofort aufsetzen (T-Taste)!",
        "log_air_empty_warn": "Filter ist leer! Maske schützt nicht!",
        "log_air_samosbor_phase": "[!] Samosbor ist in die aktive Phase eingetreten: ~20 Sekunden. Gehen Sie nicht hinaus!",
        "log_air_samosbor_melt": "[!!!] Die Wände schmelzen! Samosbor füllt die Korridore!",
        "log_air_samosbor_melt_dmg": "Saurer Nebel zerfrisst Ihren Helm!",
        "log_air_filter_melt": "Filter neutralisiert Gase, aber Chemikalien zerfressen die Dichtungen...",
        "log_air_filter_empty_melt": "Filter ist leer! Sie ersticken in giftigem Schlamm!",
        "log_air_filter_norm": "Filter neutralisiert Gase. Sie sind in Sicherheit.",
        "log_samosbor_end": "Sirenen verstummt. Samosbor beendet. Die Gefahr ist vorüber.",
        "log_game_start": "Schicht begonnen. Steigen Sie zur 1. Etage ab...",
        "log_sound_init": "Audiosystem initialisiert.",
        "log_save_controls": "Steuerungseinstellungen gespeichert.",
        "log_dev_command": "Dev-Befehl ausgeführt.",
        "note_0_title": "Ein schmutziger Zettel (Etage ~1200)",
        "note_1_title": "Rapport des Truppführers (Etage ~1100)",
        "note_2_title": "Zivilschutzmerkblatt (Etage ~1000)",
        "note_3_title": "Tagebuch eines Kindes (Etage ~900)",
        "note_4_title": "Seltsame verbrannte Seite",
        "note_5_title": "Unsignierte Notiz",
        "note_6_title": "Agitationsflugblatt (Etage ~800)",
        "note_7_title": "Zerrissener Papierschnipsel",
        "note_8_title": "Blutiger Zettel aus einem Notizbuch (Etage ~700)",
        "note_9_title": "Letztes Geständnis eines Liquidators",
        "note_0_content": "Block 1290. Siebzehnter Tag nach der Blockierung des Sektors. \\n\\nDie Belüftung summt wie verrückt, von dort riecht es ständig nach rohem, verrottendem Fleisch und Chemikalien. Der Nachbar von unten ist gestern verschwunden. Seine Frau sagt, sie habe mitten in der Nacht ein Scharren hinter der Panzertür gehört, als ob jemand versucht hätte, die Stahldichtung mit den Krallen aufzuhebeln. \\n\\nDas Leitungswasser ist seit einer Woche braun. Es scheint, als wären die Filter verstopft. Keine Liquidatoren kommen. Man sagt uns, wir sollen in den Wohnungen bleiben. Wo ist die verdammte Sonne? Existiert sie überhaupt, oder ist Beton alles, was es auf dieser Welt gibt?",
        "note_1_content": "RAPORT. Liquidator Unteroffizier Sobolew. Gruppe \"Beta-6\". \\n\\nWir erhielten den Befehl, Block 1105 nach einem lokalen Samosbor-Durchbruch zu säubern. Alles verlief nach Vorschrift, wir gossen Reagenzien in den Flur. Doch im Endkorridor stießen wir auf Wohnung #42. Die Panzertür war von innen verriegelt. Kinder schrien von dort drinnen und flehten uns an, zu öffnen. \\n\\nDoch die Sensoren zeigten eine kritische Kontamination hinter der Tür. Samosbor-Schleim drang bereits durch die Fugen. Der Befehl des Hauptquartiers war eindeutig: Versiegelung des Blocks. Wir haben die Tür von außen mit Schweißbrennern verschweißt. Die Kinder schrien noch etwa zehn Minuten lang, während wir arbeiteten. Ich höre diesen Ton immer noch, wenn ich die Augen schließe. Vergib uns, Chruschtschowka.",
        "note_2_content": "MERKBLATT FÜR BEWOHNER DER GIGA-CHRUSCHTSCHOWKA BEI BEGINN EINES SAMOSBORS: \\n\\n1. Stellen Sie beim ersten Ertönen der Sirene sofort jegliche Bewegung in den Treppenhäusern ein.\\n2. Betreten Sie die nächste Wohnung oder Schleusenzone.\\n3. Schließen Sie die Panzertür fest. Ziehen Sie die manuellen Spannventile bis zum Anschlag an.\\n4. Setzen Sie persönliche Schutzausrüstung auf (GP-9 Gasmaske oder Ähnliches).\\n5. Nähern Sie sich nicht Lüftungsschächten oder Türöffnungen.\\n6. Ignorieren Sie während der aktiven Phase alle Geräusche, Stimmen von Verwandten oder Kollegen von draußen.\\n7. Warten Sie auf das Eintreffen der Liquidatoren zur Desinfektion.",
        "note_3_content": "12. März. \\n\\nMama hat mir meine Buntstifte weggenommen, weil ich den Himmel gezeichnet habe. Ich erinnere mich an ihn! Er war so... blau, und oben hing ein riesiger warmer Kreis, der schien und wärmte. Mama weinte, zerriss die Zeichnung und schlug mir auf die Hände. Sie sagte, der Himmel sei ein gefährlicher Wahn von Verrückten, und wenn jemand vom Komitee meine Geschichten hört, werden wir alle in die unteren technischen Etagen geschickt, um zu Lebensmittelkonzentrat verarbeitet zu werden. \\n\\nSie sagt, außer Chruschtschowka gibt es nichts. Nur Beton nach oben, unten und in alle Richtungen. Aber ich weiß, dass sie lügt. Papa ging vor einem halben Jahr weg, um einen Ausweg zu suchen, und kam nicht zurück. Ich werde ihn finden.",
        "note_4_content": "Im Dämmerlicht steht ein quietschendes Eisenbett mit einer grauen Decke. Auf dem Nachttisch — ein verbogener Aluminiumkessel mit abgebrochener Tülle. An der Wand hängt schief ein fliegenübersätes Komitee-Plakat mit Liquidator #1, und in der Ecke tropft ununterbrochen ein altes rostiges Ventil... \\n\\n[Sie werden kalt vor Entsetzen. Dies ist eine genaue Beschreibung Ihrer Wohnzelle 412 im Sektor 13-A!]\\n\\nWoher weiß der Autor dieser Notiz, wie mein Zimmer aussieht? Wer hat sie hierher gebracht?",
        "note_5_content": "DU MUSST ERWACHEN.\\n\\nDu befindest dich derzeit auf Etage {0}. Aber das ist eine Lüge. Das ist nicht real. Es ist unmöglich, endlos in einem Betonschacht ohne Nahrung oder Ruhe abzusteigen. Du schläfst. Deine Gasmaske ist seit langem leer. Deine Lunge verbrannte in Samosbor-Dämpfen, aber dein sterbendes Gehirn klammert sich fieberhaft an die Illusion des Abstiegs.\\n\\nDu schläfst, Liquidator. Du musst erwachen. Du musst. Wach auf.",
        "note_6_content": "BÜRGER DER GIGA-CHRUSCHTSCHOWKA! \\n\\nDas Komitee für öffentliche Rettung erinnert Sie: \\n- Die unendliche Struktur der Chruschtschowka ist die einzige Hochburg der Menschheit. \\n- Außerhalb der Betonmauern herrscht Urchaos und Leere.\\n- Die Arbeit eines Liquidators ist heilig. Indem er sein Leben für die Versiegelung von Rissen gibt, findet ein Liquidator ewigen Frieden in den Herzen der Überlebenden.\\n- Alle Gerüchte über einen \"Ausgang\" nach draußen sind Sabotage durch Agenten des Chaos, um die Disziplin zu untergraben. \\n\\nHALTEN SIE DIE WACHSAMKEIT AUFRECHT! MELDEN SIE VERDÄCHTIGE AKTIVITÄTEN DEM NÄCHSTEN POSTEN DER LIQUIDATOREN.",
        "note_7_content": "WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF WACH AUF",
        "note_8_content": "Wenn du das liest... lauf... \\n\\nIch habe den Schacht des Kabelkollektors auf Etage 700 durchbrochen. Das Komitee belügt uns seit Jahrhunderten! Draußen gibt es kein Chaos. Die Mauern der Chruschtschowka sind nur eine Hülle. Ich habe... ich habe den Himmel gesehen! Er ist wirklich blau, und es riecht dort nach Gras, nicht nach Chlor und verbranntem Fleisch. \\n\\nAber sie beobachten uns. Samosbor ist keine Naturkatastrophe. Sie lassen ihn selbst durch die Belüftung frei, jedes Mal, wenn die Bevölkerung einer Etage beginnt, die Wahrheit zu ahnen. Es ist eine Säuberung! \\nWenn der Samosbor beginnt, versteck dich nicht. Bleib im Flur stehen. Nimm ihn an. Sie vergiften uns mit Gas, das Halluzinationen und Schlaf verursacht, aber es ist der einzige Weg, die Tracking-Sensoren zu stören und... [mit altem, dunklem Blut befleckt]",
        "note_9_content": "Wenn du dies findest, bedeutet das, dass ich bereits Teil der Chruschtschowka geworden bin. \\n\\nIch war dreißig Jahre lang Liquidator. Ich schweißte Türen zu, verbrannte Bestien und glaubte dem Komitee. Aber es gibt keinen Ausweg. Die erste Etage ist ein Mythos. Samosbor ist kein Nebel. Es ist der Atem eines großen, schlafenden Organismus. Wir befinden uns alle im Inneren eines riesigen Lebewesens, das uns langsam verdaut. Der einzige Weg, herauszukommen, besteht darin, sich nicht mehr gegen den Schlaf zu wehren und die Augen zu öffnen. Aber ich habe Angst. Möge die Chruschtschowka mir vergeben.",
        "btn_bag": "Tasche",
        "label_notes_prefix": "Notizen",
        "btn_descend_ending": "Auf der Stelle erstarren und warten",
        "focus_liquidator_body": "LIQUIDATORENLEICHE",
        "focus_liquidator_desc": "Ein toter Liquidator in Uniform. Taschen durchsuchen (Taste R).",
        "focus_search_body": "Leiche durchsuchen",
        "focus_stair_gate": "TREPPENHAUS-HERMETIKTOR",
        "focus_locked_by_system": "Gesperrt durch das Zentralsystem der GIGA-CHRUSCHTSCHOWKA.",
        "focus_try_hack": "Hacken versuchen",
        "focus_gate_open_desc": "Tor ist offen. Durchgang zum Treppenhaus ist frei.",
        "focus_close_gate": "Tor schließen",
        "focus_gate_locked_desc": "Massives Hermetiktor verriegelt! Drücken Sie B zum Hacken.",
        "focus_hack_gate": "Tor hacken",
        "focus_door_open_desc": "Tür ist offen. Sie können hineingehen (mit WASD bewegen).",
        "btn_close_door": "Tür schließen",
        "focus_door_closed_desc": "Hermetische Tür ist geschlossen. Gehen Sie näher heran.",
        "btn_open_door_action": "Tür öffnen",
        "btn_interact_action": "Interagieren",
        "yes": "JA",
        "no": "NEIN",
        "pcs": "Stk",
        "btn_rebind_waiting": "Taste drücken..."
    },
    "it": {
        "menu_title": "S A M O S B O R",
        "menu_subtitle": "LIQUIDATORE: PIANO 1324 [3D FPS]",
        "menu_creator": "CREATORE DEL GIOCO: @sw1therland",
        "init_interface": "> INIZIALIZZAZIONE INTERFACCIA LIQUIDATORE...",
        "network_ok": "> CONNESSIONE ALLA RETE GIGA-KHRUSHCHEVKA... OK.",
        "equipment_info": "> EQUIPAGGIAMENTO: PISTOLA (24), MASCHERA ANTIGAS, ACQUA, BORSA.",
        "mission_info": "> MISSIONE: SCENDI AL 1° PIANO E SOPRAVVIVI.",
        "loading_sdk": "Caricamento SDK...",
        "btn_start": "INIZIA TURNO",
        "btn_settings": "IMPOSTAZIONI",
        "btn_achievements": "OBIETTIVI",
        "btn_about": "INFO GIOCO",
        "hud_floor": "PIANO:",
        "hud_health": "SALUTE:",
        "hud_water": "ACQUA:",
        "hud_ammo": "MUNIZIONI:",
        "hud_filter": "FILTRO:",
        "hud_stamina": "RESISTENZA:",
        "fps_instructions": "WASD - Muovi | Shift - Scatto | Space - Calcio | Mouse - Guarda | LMB - Spara | R - Porta | F - Torcia | E - Ascolta | T - Maschera antigas | Q - Acqua | G - Borsa | Z - Cerca | B - Hacker",
        "mobile_flashlight": "Torcia",
        "mobile_listen": "Ascolta",
        "mobile_door": "Porta",
        "mobile_fire": "Fuoco",
        "listening_title": "ASCOLTO...",
        "listening_subtext": "Rumori del pozzo di cemento",
        "descent_transition_title": "DISCESA AL PIANO INFERIORE...",
        "btn_mask": "Indossa maschera antigas",
        "btn_mask_remove": "Togli maschera antigas",
        "btn_drink": "Bevi un sorso d'acqua",
        "btn_descend_default": "Vai alle scale in fondo al corridoio",
        "focus_title": "FOCUS OGGETTO",
        "focus_object_none": "NESSUN OGGETTO SELEZIONATO",
        "focus_object_desc": "Avvicinati a una porta o a un oggetto interattivo",
        "btn_listen": "Ascolta",
        "btn_open_door": "Apri",
        "room_actions_title": "AZIONI",
        "btn_search_room": "Cerca nei mobili",
        "btn_lock_room": "Blocca porta",
        "btn_unlock_room": "Sblocca porta",
        "btn_exit_room": "Esci nel corridoio",
        "transition_actions_title": "CHIASSO TECNICO",
        "btn_enter_transition": "Passa a un altro settore",
        "btn_cancel_transition": "Ritorna al corridoio",
        "notes_title": "BORSA: NOTE TROVATE",
        "notes_inventory_title": "INVENTARIO",
        "bag_hacker_label": "STRUMENTO HACKER",
        "bag_batteries_label": "BATTERIE",
        "notes_list_title": "NOTE",
        "select_note_prompt": "Seleziona una nota dall'elenco a sinistra per leggerla.",
        "gameover_notes_collected": "NOTE RACCOLTE DALLA GIGA-KHRUSHCHEVKA:",
        "credits_header": "RICONOSCIMENTI // CREDITS",
        "credits_author_label": "AUTORE E SVILUPPATORE:",
        "credits_tech": "Tecnologie: HTML5, Three.js, Web Audio API<br>Specificamente per l'universo Samosbor",
        "btn_restart": "RICOMINCIA",
        "pause_title": "PAUSA",
        "btn_resume": "RIPRENDI TURNO",
        "btn_exit": "ESCI AL MENU",
        "settings_title": "IMPOSTAZIONI",
        "section_language": "SELEZIONA LINGUA // SELECT LANGUAGE",
        "section_controls": "CONTROLLI // CONTROLLI",
        "label_rebind_desc": "Fai clic su un'azione, quindi premi un nuovo tasto sulla tastiera.",
        "btn_reset": "RIPRISTINA",
        "btn_save": "SALVA",
        "about_title": "INFO GIOCO",
        "achievements_title": "OBIETTIVI",
        "achievements_subtitle": "ELENCO OBIETTIVI LIQUIDATORE",
        "hack_title": "DECRIPTATORE PORTA ERMETICA // BYPASS",
        "hack_sys": "SISTEMA: GRUPPO-B",
        "hack_bat": "BATTERIA: OK",
        "hack_chan_a_label": "CANALE A",
        "hack_chan_b_label": "CANALE B",
        "hack_chan_c_label": "CANALE C",
        "hack_search": "RICERCA FREQUENZA:",
        "btn_hack_submit": "CONNETTI",
        "btn_hack_cancel": "ANNULLA",
        "achievement_popup_header": "Obiettivo sbloccato!",
        "ending_wakeup_title": "RISVEGLIO",
        "btn_true_ending_restart": "INIZIA NUOVO TURNO",
        "act_move_forward": "Muovi Avanti",
        "act_move_backward": "Muovi Indietro",
        "act_move_left": "Muovi Sinistra",
        "act_move_right": "Muovi Destra",
        "act_sprint": "Scatto (Accelera)",
        "act_interact": "Interagisci / Porta",
        "act_flashlight": "Torcia Accendi/Spegni",
        "act_listen": "Ascolta alla porta ermetica",
        "act_gasmask": "Indossa/togli maschera antigas",
        "act_water": "Bevi un sorso d'acqua",
        "act_bag": "Apri Borsa (Note)",
        "act_search": "Cerca in Stanza",
        "act_hackertool": "Usa Strumento Hacker",
        "act_pause": "Pausa (Menu)",
        "door_apartment": "Appartamento {0}",
        "door_armory": "Postazione Liquidatori N.{0}",
        "door_contaminated": "Appartamento {0} (RADIAZIONI)",
        "door_nest": "Sezione Tecnica {0} (NIDO)",
        "door_transition": "Transito {0}-{1}",
        "door_empty": "Porta {0}",
        "room_warehouse": "Magazzino",
        "room_archive": "Archivio",
        "room_compressor": "Sala compressori",
        "room_control": "Quadro elettrico",
        "room_ventilation": "Camera di ventilazione",
        "ach_butcher_title": "Macellaio di Gigahrush",
        "ach_butcher_desc": "Spaventa o distruggi 50 mostri",
        "ach_hacker_title": "Hacker Autodidatta",
        "ach_hacker_desc": "Decripta 100 porte ermetiche",
        "ach_spendthrift_title": "Sciupone",
        "ach_spendthrift_desc": "Spendi tutte le munizioni prima del piano 1000",
        "ach_survivor_title": "Sopravvissuto",
        "ach_survivor_desc": "Scendi sotto il piano 1000",
        "ach_drinker_title": "Idratato",
        "ach_drinker_desc": "Bevi 50 sorsi d'acqua purificata",
        "ach_deceived_title": "Ingannato",
        "ach_deceived_desc": "Raggiungi il finale senza via d'uscita",
        "ach_awakened_title": "Risvegliato e Libero",
        "ach_awakened_desc": "Raggiungi il finale vero",
        "ach_secret_desc": "[OBIETTIVO SEGRETO]",
        "about_content_html": "\n            <h3 class=\"glow-red\" style=\"margin-bottom: 5px; font-weight: bold;\">SAMOSBOR: LIQUIDATORE 1324</h3>\n            <p style=\"margin-top: 0; margin-bottom: 15px; color: var(--glow-green); font-weight: bold; font-family: var(--font-mono); font-size: 0.9rem;\">CREATORE GIOCO: @sw1therland</p>\n            <p>Sei un Liquidatore del settore pesante della Giga-Khrushchevka. Il tuo turno è iniziato al piano 1324. L'obiettivo è semplice: scendere al 1° piano e sopravvivere.</p>\n            <p style=\"margin-top: 10px;\">Durante la discesa, incontrerai il Samosbor, un fenomeno mortale. Quando senti la sirena, trova immediatamente un appartamento vuoto, chiudi la porta ermetica e indossa la maschera antigas.</p>\n            <p style=\"margin-top: 10px;\">Monitora il livello dell'acqua e il filtro della maschera antigas. Cerca nelle credenze e nei tavoli degli appartamenti per trovare provviste, note informative, un decriptatore per porte e batterie.</p>\n            <p style=\"margin-top: 15px; color: var(--glow-amber); font-weight: bold;\">Controlli:</p>\n            <ul style=\"margin-left: 20px; margin-top: 5px; display: flex; flex-direction: column; gap: 4px;\">\n                <li><b>WASD</b> — Movimento</li>\n                <li><b>Shift</b> — Scatto (consuma rapidamente la resistenza)</li>\n                <li><b>Space (Spazio)</b> — Calcio (per respingere i mostri che corrono nel corridoio)</li>\n                <li><b>Mouse</b> — Visuale (fai clic sullo schermo per bloccare il cursore)</li>\n                <li><b>LMB</b> — Sparo (spaventa il mostro sul pianerottolo delle scale)</li>\n                <li><b>R</b> — Apri/chiudi porta ermetica</li>\n                <li><b>F</b> — Torcia</li>\n                <li><b>E</b> — Ascolta rumori dietro la porta</li>\n                <li><b>T</b> — Indossa/togli maschera antigas</li>\n                <li><b>Q</b> — Bevi un sorso d'acqua</li>\n                <li><b>G / Borsa</b> — Controlla note e inventario</li>\n                <li><b>Z</b> — Cerca nei mobili (tavolo/credenza)</li>\n                <li><b>B</b> — Usa il decriptatore sulla grata delle scale</li>\n                <li><b>Esc / P</b> — Pausa</li>\n            </ul>\n        ",
        "ending_wakeup_desc": "Hai fatto un respiro profondo. L'aria è pulita, calda e profuma di erba fresca.<br><br>I contorni del cielo, di un albero verde e del fruscio delle foglie attraverso le palpebre semichiuse acquistano calore.<br><br>L'incubo della Giga-Khrushchevka è finito. Finalmente ti sei svegliato.",
        "ending_wakeup_stats": "<div style=\"font-weight: bold; font-size: 0.95rem; color: #111111; margin-bottom: 5px; text-align: center; letter-spacing: 1px;\">FINALE VERO</div>Note raccolte e lette: 10 / 10<br>Sceso prima del risveglio di: <span id=\"true-ending-floors-descended\" style=\"font-weight: bold; color: #6b0a0a;\">{0}</span> piani",
        "ending_wakeup_author": "<strong>Autore del gioco:</strong> @sw1therland<br><span style=\"font-size: 0.72rem; color: #666666;\">Grazie per aver giocato! Sei fuggito dal Samostroy.</span>",
        "go_dehydration_title": "LIQUIDATO",
        "go_dehydration_desc": "<p>Il tuo corpo non ha resistito alla terribile disidratazione.</p><p>Sei crollato sui freddi gradini di cemento del vano scale al piano {0}.</p><p>Nessuno verrà in soccorso. Il tuo corpo rimarrà qui finché il prossimo Samosbor non lo dissolverà in melma marrone.</p>",
        "go_stairs_monster_title": "SBRANATO",
        "go_stairs_monster_desc": "<p>Non hai reagito in tempo.</p><p>La bestia ti è piombata addosso dall'alto, spezzandoti le costole.</p><p>Mandibole affilate hanno perforato la visiera della maschera antigas. L'ultima cosa che hai sentito è stato il rumore della biomassa che divorava la tua carne.</p>",
        "go_opened_monster_title": "ELIMINATO",
        "go_opened_monster_desc": "<p>Hai aperto la porta senza prima ascoltare.</p><p>Una bestia predatrice del Samosbor aveva fatto il nido proprio oltre la soglia.</p><p>Non appena i bulloni si sono aperti, la biomassa multi-arto ti ha trascinato all'interno della stanza buia. Non hai avuto nemmeno il tempo di urlare.</p>",
        "go_samosbor_title": "DISSOLTO",
        "go_samosbor_desc": "<p>Sei rimasto nel corridoio durante la fase attiva del Samosbor.</p><p>La nebbia tossica ha corroso le guarnizioni di gomma del casco e la tua pelle in pochi secondi.</p><p>La tua coscienza è svanita mentre i tuoi tessuti si scioglievano, scorrendo nelle griglie di ventilazione.</p>",
        "go_samosbor_gas_title": "ASFISSIATO",
        "go_samosbor_gas_desc": "<p>Ti sei nascosto nella stanza, ma hai trascurato i dispositivi di protezione.</p><p>Il gas tossico del Samosbor è filtrato sotto la porta ermetica.</p><p>Senza maschera antigas, i tuoi polmoni si sono riempiti di vapori acidi, causando spasmi immediati e soffocamento.</p>",
        "go_ending1_title": "RISVEGLIO",
        "go_ending1_desc": "<p>Dopo aver raccolto tutte le note, hai compreso la vera natura della Giga-Khrushchevka.</p><p>Quando la nebbia del Samosbor si è riversata nel corridoio, non sei corso a nasconderti. Ti sei bloccato sul posto, allargando le braccia, e hai chiuso gli occhi.</p><p>Il mondo intorno è tremato, i muri di cemento hanno iniziato a sgretolarsi in pixel. La nebbia viola ti ha abbracciato...</p><p>...E all'improvviso hai fatto un respiro profondo. Aria fresca e calda ti ha riempito i polmoni.</p><p>Hai aperto gli occhi. Eri sdraiato su un letto morbido. Un SOLE luminoso e vero risplendeva attraverso la finestra, e foglie verdi frusciavano fuori. Era un sogno. Un lungo incubo da cui potevi sfuggire solo smettendo di avere paura.</p>",
        "go_ending2_title": "SENZA VIA D'USCITA",
        "go_ending2_desc": "<p>Hai superato un lungo cammino e sei sceso al primo piano.</p><p>Ma non c'è passaggio per l'esterno. Le pesanti porte della chiusa sono saldate ermeticamente da secoli di ruggine.</p><p>Dietro di te, la porta del vano scale si è chiusa con un fragore. I meccanismi sono bloccati. I chiavistelli non si muovono.</p><p>In questo momento, le sirene hanno iniziato a ululare al massimo volume. Un massiccio Samosbor ha avuto inizio. Non ci sono rifugi. Le porte sono bloccate. Sei intrappolato in un sacco di cemento al primo piano, faccia a faccia con la nebbia mortale. Questa è la fine del percorso.</p>",
        "go_badge_death": "Morte",
        "go_badge_ending1": "Finale vero",
        "go_badge_ending2": "Senza via d'uscita",
        "log_creep_1": "Hai sentito un lontano graffio all'interno delle pareti di cemento...",
        "log_creep_2": "Una corrente d'aria ha portato l'odore di cavolo marcio e carne cruda.",
        "log_creep_3": "Le luci hanno tremolato per un momento. Pressione casco stabile.",
        "log_creep_4": "Da qualche parte in profondità, è riecheggiato un impatto metallico soffocato.",
        "log_creep_5": "Il contatore Geiger fa clic silenziosamente. Radiazione di fondo nella norma.",
        "log_gh_scary": "Il fantasma sta prosciugando l'energia della tua torcia!",
        "log_water_low": "Attenzione! Livello di disidratazione critico!",
        "log_descend_floor": "Sceso al piano {0}.",
        "log_descend_warn": "Il piano tecnico è bloccato da una porta ermetica. Richiesto l'hacking.",
        "log_ascend_floor": "Salito al piano {0}.",
        "log_room_clean": "Sei entrato in {0}. L'aria è pulita. Nessuna minaccia rilevata.",
        "log_room_hazard": "Sei entrato in {0}. L'aria è radioattiva! Indossa la maschera! (tasto T)",
        "log_room_nest": "Sei entrato in {0}. La melma sulle pareti si muove. Senti una presenza! (Preparati!)",
        "log_room_hallway": "Sei uscito nel corridoio. La ventilazione spinge l'aria fredda della Khrushchevka.",
        "log_lock_search_warn": "Impossibile cercare nei mobili durante il Samosbor, è troppo pericoloso!",
        "log_lock_door": "Hai chiuso la porta ermetica dell'appartamento.",
        "log_unlock_door": "Hai aperto la porta ermetica dell'appartamento.",
        "log_door_listen": "Hai ascoltato dietro la porta di {0}...",
        "log_door_listen_clean": "Silenzio. Sembra sicuro all'interno.",
        "log_door_listen_hazard": "Si sentono passi pesanti e melma che striscia. C'è una bestia!",
        "log_door_listen_transition": "Si sente il lontano ronzio dei trasformatori del chiasso tecnico.",
        "log_hack_bypass_ok": "Bypass: Canale {0} decrittato con successo!",
        "log_hack_bypass_err": "Bypass: errore di sincronizzazione di fase del segnale.",
        "log_hack_gate": "Porta Ermetica! Le porte si muovono verso: {0}...",
        "log_hack_gate_open": "apertura",
        "log_hack_gate_close": "chiusura",
        "log_hack_hacker_err": "Decrittatore: Guasto. Circuito bloccato dal sistema centrale. Impossibile da usare!",
        "log_hack_note_samosbor": "Hai raccolto tutte le note ma non le hai lette... non hai potuto comprendere la verità.",
        "log_hack_tool_hot": "Il decrittatore è surriscaldato! Attendere che si raffreddi.",
        "log_hack_tool_empty": "La batteria del decrittatore è scarica! Sostituire la batteria.",
        "log_loot_corpse": "[✔] Hai perquisito il corpo, armatura (+8) e filtro (+40%) ripristinati.",
        "log_loot_note": "[✔] Nota trovata: \"{0}\"!",
        "log_loot_hacker": "[✔] Hai trovato un decrittatore per porte ermetiche!",
        "log_loot_battery": "[✔] Hai trovato una batteria (+1 pz, totale: {0}).",
        "log_loot_synthesizer": "Hai trovato un sintetizzatore di cibo (+50% acqua).",
        "log_loot_ammo": "[✔] Hai trovato munizioni (+{0} pz).",
        "log_loot_filter": "Hai trovato un nuovo filtro (+50% carica).",
        "log_loot_empty": "Hai cercato nei mobili ma non hai trovato nulla di utile.",
        "log_gasmask_equip": "Maschera antigas indossata. Respirazione limitata, la visiera si appanna.",
        "log_gasmask_unequip": "Maschera antigas rimossa.",
        "log_gasmask_no": "Non hai una maschera antigas!",
        "log_gasmask_empty": "Il filtro è scarico! L'aria è avvelenata!",
        "log_drink_sip": "Sorso preso. Acqua bottiglia: {0}% rimanente.",
        "log_siren_start": "[!] La sirena del Samosbor ha iniziato a ululare!",
        "log_siren_desc": "Hai 4 secondi per ripararti in una stanza e chiudere la porta!",
        "log_monster_shoot_scare": "Hai spaventato la bestia con un colpo di pistola! Si è ritirata nel pozzo!",
        "log_monster_shoot_dead": "Hai distrutto la bestia con un colpo di pistola!",
        "log_monster_kick": "Hai calciato la bestia!",
        "log_monster_kick_dmg": "La bestia ti ha morso la gamba! Danno subito!",
        "log_crawler_run": "Hai sentito un rapido graffiare di artigli sul pavimento!",
        "log_crawler_warn": "Una bestia corre verso di te! Premi SPAZIO per calciarla via!",
        "log_crawler_safe": "Il rumore è svanito. La bestia è fuggita nelle prese d'aria.",
        "log_air_hazard": "Stai inalando fumi tossici! Indossa immediatamente la maschera (tasto T)!",
        "log_air_empty_warn": "Il filtro è scarico! La maschera non ti protegge!",
        "log_air_samosbor_phase": "[!] Samosbor entrato nella fase attiva: ~20 secondi. Non uscire!",
        "log_air_samosbor_melt": "[!!!] Le pareti si sciolgono! Il Samosbor riempie i corridoi!",
        "log_air_samosbor_melt_dmg": "La nebbia acida corrode il tuo casco!",
        "log_air_filter_melt": "Il filtro neutralizza i gas, ma i prodotti chimici corrodono le guarnizioni...",
        "log_air_filter_empty_melt": "Il filtro è vuoto! Stai soffocando nel fango tossico!",
        "log_air_filter_norm": "Il filtro neutralizza i gas. Sei al sicuro.",
        "log_samosbor_end": "Le sirene si sono zittite. Il Samosbor è finito. Il pericolo è passato.",
        "log_game_start": "Turno iniziato. Scendi al 1° piano...",
        "log_sound_init": "Sistema audio inizializzato.",
        "log_save_controls": "Impostazioni di controllo salvate.",
        "log_dev_command": "Comando dev eseguito.",
        "note_0_title": "Foglietto sporco (Piano ~1200)",
        "note_1_title": "Rapporto del comandante (Piano ~1100)",
        "note_2_title": "Memo della Protezione Civile (Piano ~1000)",
        "note_3_title": "Diario di un bambino (Piano ~900)",
        "note_4_title": "Pagina bruciata misteriosa",
        "note_5_title": "Nota non firmata",
        "note_6_title": "Volantino propagandistico (Piano ~800)",
        "note_7_title": "Pezzo di carta lacerato",
        "note_8_title": "Pezzo di quaderno insanguinato (Piano ~700)",
        "note_9_title": "Ultima confessione di un Liquidatore",
        "note_0_content": "Blocco 1290. Diciassettesimo giorno dopo il blocco del settore. \\n\\nLa ventilazione sibila come impazzita, emana costantemente un odore di carne cruda e in decomposizione mescolata a sostanze chimiche. Il vicino di sotto è scomparso ieri. La moglie dice di aver sentito dei graffi dietro la porta ermetica a metà notte, come se qualcuno cercasse di scardinare la guarnizione in acciaio con gli artigli. \\n\\nL'acqua del rubinetto è marrone da una settimana. Sembra che i filtri della presa d'acqua siano ostruiti da resti organici. I Liquidatori non arrivano. Ci dicono di stare barricati in appartamento. Dov'è il maledetto sole? Esiste davvero o il cemento è tutto ciò che esiste in questo mondo?",
        "note_1_content": "RAPPORTO. Liquidatore sergente Sobolev. Gruppo \"Beta-6\". \\n\\nCi è stato ordinato di bonificare il blocco 1105 dopo una fuga locale di Samosbor. Tutto è andato secondo le regole, gettando reagenti nel corridoio. Ma nel corridoio finale ci siamo imbattuti nell'appartamento #42. La porta ermetica era bloccata dall'interno. Dei bambini gridavano da lì dentro, pregandoci di aprire. \\n\\nMa i sensori mostravano una contaminazione critica dietro la porta. La melma del Samosbor stava già filtrando attraverso i giunti. L'ordine del comando era esplicito: sigillare il blocco. Abbiamo saldato la porta dall'esterno con le fiamme ossidriche. I bambini hanno gridato per altri dieci minuti mentre lavoravamo. Sento ancora quel suono quando chiudo gli occhi. Perdonaci, Khrush.",
        "note_2_content": "MEMO PER I RESIDENTI DI GIGA-KHRUSHCHEVKA ALL'INIZIO DEL SAMOSBOR: \\n\\n1. Al primo suono della sirena, interrompi immediatamente ogni movimento lungo le scale.\\n2. Entra nell'appartamento o zona di chiusa più vicina.\\n3. Chiudi ermeticamente la porta ermetica. Stringi a fondo le valvole manuali di serraggio.\\n4. Indossa i dispositivi di protezione individuale (maschera antigas GP-9 o equivalente).\\n5. Non avvicinarti ai condotti di ventilazione o alle aperture delle porte.\\n6. Ignora qualsiasi suono, voce di parenti o colleghi proveniente dall'esterno durante la fase attiva.\\n7. Attendi l'arrivo dei Liquidatori per le procedure di disinfezione.",
        "note_3_content": "12 marzo. \\n\\nMamma mi ha tolto i pastelli colorati perché ho disegnato il cielo. Io lo ricordo! Era così... blu, e sopra c'era un grande cerchio caldo che splendeva e riscaldava. Mamma ha iniziato a piangere, ha strappato il disegno e mi ha colpito le mani. Ha detto che il cielo è una pericolosa allucinazione da matti, e che se qualcuno del Comitato sente le mie storie, verremo tutti mandati ai piani tecnici inferiori per essere trasformati in concentrato di cibo. \\n\\nDice che non c'è nulla oltre alla Khrushchevka. Solo cemento in alto, in basso e in ogni direzione. Ma so che mente. Papà è andato a cercare una via d'uscita sei mesi fa e non è tornato. Lo troverò.",
        "note_4_content": "Nella penombra c'è una branda di ferro cigolante con una coperta grigia dell'istituto. Sul comodino — una teiera di alluminio piegata con il beccuccio scheggiato. Sulla parete è appeso storto un manifesto del Comitato coperto di mosche con il Liquidatore #1, e nell'angolo una vecchia valvola arrugginita gocciola continuamente... \\n\\n[Ti si gela il sangue dal terrore. Questa è l'esatta descrizione della tua cella abitativa 412 nel settore 13-A!]\\n\\nCome fa l'autore di questa nota a sapere che aspetto ha la mia stanza? Chi l'ha portata qui?",
        "note_5_content": "DEVI SVEGLIARTI.\\n\\nTi trovi attualmente al piano {0}. Ma questa è una bugia. Non è reale. È impossibile scendere all'infinito in un pozzo di cemento senza cibo né riposo. Stai dormendo. La tua maschera antigas è vuota da tempo. I tuoi polmoni sono bruciati nei fumi del Samosbor, ma il tuo cervello morente si aggrappa febbrilmente all'illusione della discesa.\\n\\nStai dormendo, Liquidatore. Devi svegliarti. Devi. Svegliati.",
        "note_6_content": "CITTADINI DI GIGA-KHRUSHCHEVKA! \\n\\nIl Comitato di Salute Pubblica vi ricorda: \\n- La struttura infinita della Khrushchevka è l'unica roccaforte dell'umanità. \\n- Fuori dalle mura di cemento regna il caos primordiale e il vuoto.\\n- Il lavoro del liquidatore è sacro. Dando la vita per sigillare le falle, un liquidatore trova la pace eterna nei cuori dei superstiti.\\n- Qualsiasi voce di una \"uscita\" all'esterno è un sabotaggio da parte di agenti del caos volti a minare la disciplina. \\n\\nMANTENETE LA VIGILANZA! SEGNALATE ATTIVITÀ SOSPETTE AL POSTO DI LIQUIDATORI PIÙ VICINO.",
        "note_7_content": "SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI SVEGLIATI",
        "note_8_content": "Se leggi questo... scappa... \\n\\nHo perforato il condotto del collettore di cavi al piano 700. Il Comitato ci mente da secoli! Non c'è alcun caos là fuori. Le pareti del Khrush sono solo un guscio. Ho visto... ho visto il cielo! È davvero blu, e là fuori profuma di erba, non di cloro e carne bruciata. \\n\\nMa ci tengono d'occhio. Il Samosbor non è un disastro naturale. Lo rilasciano loro stessi attraverso la ventilazione ogni volta che la popolazione di un piano inizia a indovinare la verità. È una purga! \\nSe inizia il Samosbor, non nasconderti. Resta fermo nel corridoio. Accoglilo. Ci avvelenano con un gas che provoca allucinazioni e sonno, ma è l'unico modo per disturbare i sensori di tracciamento e... [macchiato di vecchio sangue scuro]",
        "note_9_content": "Se trovi questo, significa che sono già diventato parte della Khrushchevka. \\n\\nSono stato un Liquidatore per trent'anni. Ho saldato porte, bruciato bestie e creduto al Comitato. Ma non c'è via d'uscita. Il primo piano è un mito. Il Samosbor non è nebbia. È il respiro di un grande organismo dormiente. Siamo tutti all'interno di una gigantesca creatura vivente che ci digerisce lentamente. L'unico modo per uscire è smettere di resistere al sonno e aprire gli occhi. Ma ho paura. Che il Khrush mi perdoni.",
        "btn_bag": "Borsa",
        "label_notes_prefix": "Note",
        "btn_descend_ending": "Congelati sul posto e aspetta",
        "focus_liquidator_body": "CORPO DEL LIQUIDATOR",
        "focus_liquidator_desc": "Un liquidatore morto in uniforme. Cerca nelle tasche (tasto R).",
        "focus_search_body": "Cerca corpo",
        "focus_stair_gate": "CANCELLO ERMETICO DELLE SCALE",
        "focus_locked_by_system": "Bloccato dal sistema centrale della GIGA-KHRUSHCHEVKA.",
        "focus_try_hack": "Prova ad hackerare",
        "focus_gate_open_desc": "Il cancello è aperto. Il passaggio alle scale è libero.",
        "focus_close_gate": "Chiudi cancello",
        "focus_gate_locked_desc": "Il massiccio cancello ermetico è bloccato! Premi B per hackerare.",
        "focus_hack_gate": "Hackera cancello",
        "focus_door_open_desc": "La porta è aperta. Puoi entrare (muoviti con WASD).",
        "btn_close_door": "Chiudi porta",
        "focus_door_closed_desc": "La porta ermetica è chiusa. Avvicinati.",
        "btn_open_door_action": "Apri porta",
        "btn_interact_action": "Interagisci",
        "yes": "SÌ",
        "no": "NO",
        "pcs": "pz",
        "btn_rebind_waiting": "Premi un tasto..."
    },
    "es": {
        "menu_title": "S A M O S B O R",
        "menu_subtitle": "LIQUIDADOR: PISO 1324 [3D FPS]",
        "menu_creator": "CREADOR DEL JUEGO: @sw1therland",
        "init_interface": "> INICIALIZANDO INTERFAZ DE LIQUIDADOR...",
        "network_ok": "> CONECTANDO A LA RED GIGA-KHRUSHCHEVKA... OK.",
        "equipment_info": "> EQUIPAMIENTO: PISTOLA (24), MÁSCARA DE GAS, AGUA, BOLSA.",
        "mission_info": "> MISIÓN: DESCENDER AL 1.ER PISO Y SOBREVIVIR.",
        "loading_sdk": "Cargando SDK...",
        "btn_start": "INICIAR TURNO",
        "btn_settings": "CONFIGURACIÓN",
        "btn_achievements": "LOGROS",
        "btn_about": "ACERCA DE",
        "hud_floor": "PISO:",
        "hud_health": "SALUD:",
        "hud_water": "AGUA:",
        "hud_ammo": "MUNICIÓN:",
        "hud_filter": "FILTRO:",
        "hud_stamina": "RESISTENCIA:",
        "fps_instructions": "WASD - Mover | Shift - Sprint | Space - Patada | Ratón - Mirar | LMB - Disparar | R - Puerta | F - Linterna | E - Escuchar | T - Máscara de gas | Q - Agua | G - Bolsa | Z - Buscar | B - Hacker",
        "mobile_flashlight": "Linterna",
        "mobile_listen": "Escuchar",
        "mobile_door": "Puerta",
        "mobile_fire": "Fuego",
        "listening_title": "ESCUCHANDO...",
        "listening_subtext": "Ruidos del pozo de concreto",
        "descent_transition_title": "DESCENDIENDO AL PISO INFERIOR...",
        "btn_mask": "Ponerse máscara de gas",
        "btn_mask_remove": "Quitarse máscara de gas",
        "btn_drink": "Dar un sorbo de agua",
        "btn_descend_default": "Ve a las escaleras al final del pasillo",
        "focus_title": "ENFOQUE DE OBJETO",
        "focus_object_none": "OBJETO NO SELECCIONADO",
        "focus_object_desc": "Acércate a una puerta u objeto interactivo",
        "btn_listen": "Escuchar",
        "btn_open_door": "Abrir",
        "room_actions_title": "ACCIONES",
        "btn_search_room": "Buscar en los muebles",
        "btn_lock_room": "Cerrar puerta",
        "btn_unlock_room": "Abrir puerta",
        "btn_exit_room": "Salir al pasillo",
        "transition_actions_title": "COMPUERTA TÉCNICA",
        "btn_enter_transition": "Pasar a otro sector",
        "btn_cancel_transition": "Volver al pasillo",
        "notes_title": "BOLSA: NOTAS ENCONTRADAS",
        "notes_inventory_title": "INVENTARIO",
        "bag_hacker_label": "DISPOSITIVO DE HACKEO",
        "bag_batteries_label": "BATERÍAS",
        "notes_list_title": "NOTAS",
        "select_note_prompt": "Selecciona una nota de la lista de la izquierda para leerla.",
        "gameover_notes_collected": "NOTAS RECOGIDAS DE LA GIGA-KHRUSHCHEVKA:",
        "credits_header": "CRÉDITOS",
        "credits_author_label": "AUTOR Y DESARROLLADOR:",
        "credits_tech": "Tecnologías: HTML5, Three.js, Web Audio API<br>Especialmente para el universo Samosbor",
        "btn_restart": "REINICIAR",
        "pause_title": "PAUSA",
        "btn_resume": "REANUDAR TURNO",
        "btn_exit": "SALIR AL MENÚ",
        "settings_title": "CONFIGURACIÓN",
        "section_language": "SELECCIONAR IDIOMA // SELECT LANGUAGE",
        "section_controls": "CONTROLES // CONTROLES",
        "label_rebind_desc": "Haz clic en una acción, luego presiona una nueva tecla en el teclado.",
        "btn_reset": "RESTABLECER",
        "btn_save": "GUARDAR",
        "about_title": "ACERCA DEL GIOCO",
        "achievements_title": "LOGROS",
        "achievements_subtitle": "LISTA DE LOGROS DEL LIQUIDADOR",
        "hack_title": "DESCRIFRADOR DE COMPUERTA HERMÉTICA // DERIVACIÓN",
        "hack_sys": "SISTEMA: GRUPO-B",
        "hack_bat": "BATERÍA: OK",
        "hack_chan_a_label": "CANAL A",
        "hack_chan_b_label": "CANAL B",
        "hack_chan_c_label": "CANAL C",
        "hack_search": "BÚSQUEDA DE FRECUENCIA:",
        "btn_hack_submit": "CONECTAR",
        "btn_hack_cancel": "CANCELAR",
        "achievement_popup_header": "¡Logro desbloqueado!",
        "ending_wakeup_title": "DESPERTAR",
        "btn_true_ending_restart": "INICIAR NUEVO TURNO",
        "act_move_forward": "Mover Adelante",
        "act_move_backward": "Mover Atrás",
        "act_move_left": "Mover Izquierda",
        "act_move_right": "Mover Derecha",
        "act_sprint": "Sprint (Acelerar)",
        "act_interact": "Interactuar / Puerta",
        "act_flashlight": "Linterna Encender/Apagar",
        "act_listen": "Escuchar en la compuerta",
        "act_gasmask": "Ponerse/quitarse máscara de gas",
        "act_water": "Dar un sorbo de agua",
        "act_bag": "Abrir Bolsa (Notas)",
        "act_search": "Buscar en Habitación",
        "act_hackertool": "Usar Herramienta Hacker",
        "act_pause": "Pausa (Menú)",
        "door_apartment": "Apartamento {0}",
        "door_armory": "Puesto de Liquidadores N.º{0}",
        "door_contaminated": "Apartamento {0} (RADIACIÓN)",
        "door_nest": "Sección Técnica {0} (NIDO)",
        "door_transition": "Tránsito {0}-{1}",
        "door_empty": "Puerta {0}",
        "room_warehouse": "Almacén",
        "room_archive": "Archivo",
        "room_compressor": "Sala de compresores",
        "room_control": "Sala de control",
        "room_ventilation": "Cámara de ventilación",
        "ach_butcher_title": "Carnicero de Gigahrush",
        "ach_butcher_desc": "Asusta o destruye 50 monstruos",
        "ach_hacker_title": "Hacker Autodidacta",
        "ach_hacker_desc": "Hackea 100 compuertas herméticas",
        "ach_spendthrift_title": "Derrochador",
        "ach_spendthrift_desc": "Gasta toda la munición antes del piso 1000",
        "ach_survivor_title": "Superviviente",
        "ach_survivor_desc": "Desciende por debajo del piso 1000",
        "ach_drinker_title": "Bebedor de Agua",
        "ach_drinker_desc": "Da 50 sorbos de agua purificada",
        "ach_deceived_title": "Engañado",
        "ach_deceived_desc": "Consigue el final sin salida",
        "ach_awakened_title": "Despierto y Libre",
        "ach_awakened_desc": "Consigue el final verdadero",
        "ach_secret_desc": "[LOGRO SECRETO]",
        "about_content_html": "\n            <h3 class=\"glow-red\" style=\"margin-bottom: 5px; font-weight: bold;\">SAMOSBOR: LIQUIDADOR 1324</h3>\n            <p style=\"margin-top: 0; margin-bottom: 15px; color: var(--glow-green); font-weight: bold; font-family: var(--font-mono); font-size: 0.9rem;\">CREADOR DEL JUEGO: @sw1therland</p>\n            <p>Eres un Liquidador del sector pesado de la Giga-Khrushchevka. Tu turno comenzó en el piso 1324. El objetivo es simple: descender al 1.er piso y sobrevivir.</p>\n            <p style=\"margin-top: 10px;\">Durante el descenso, te enfrentarás al Samosbor, un fenómeno mortal. Al escuchar la sirena, busca inmediatamente un apartamento vacío, cierra la compuerta hermética y ponte la máscara de gas.</p>\n            <p style=\"margin-top: 10px;\">Vigila el nivel de agua y el filtro de la máscara. Busca en alacenas y mesas de los apartamentos para encontrar suministros, notas, un descifrador de compuertas y baterías.</p>\n            <p style=\"margin-top: 15px; color: var(--glow-amber); font-weight: bold;\">Controles:</p>\n            <ul style=\"margin-left: 20px; margin-top: 5px; display: flex; flex-direction: column; gap: 4px;\">\n                <li><b>WASD</b> — Movimiento</li>\n                <li><b>Shift</b> — Sprint (agota la resistencia rápidamente)</li>\n                <li><b>Space (Espacio)</b> — Patada (repele al monstruo corredor en el pasillo)</li>\n                <li><b>Ratón</b> — Vista (haz clic en la pantalla para bloquear el puntero)</li>\n                <li><b>LMB</b> — Disparo (asusta al monstruo en el rellano de las escaleras)</li>\n                <li><b>R</b> — Cerrar/abrir compuerta hermética</li>\n                <li><b>F</b> — Linterna</li>\n                <li><b>E</b> — Escuchar ruidos detrás de la puerta</li>\n                <li><b>T</b> — Ponerse/quitarse la máscara de gas</li>\n                <li><b>Q</b> — Dar un sorbo de agua</li>\n                <li><b>G / Bolsa</b> — Comprobar notas e inventario</li>\n                <li><b>Z</b> — Buscar en muebles (mesa/alacena)</li>\n                <li><b>B</b> — Usar el descifrador en la verja de las escaleras</li>\n                <li><b>Esc / P</b> — Pausa</li>\n            </ul>\n        ",
        "ending_wakeup_desc": "Hiciste una respiración profunda. El aire está limpio, cálido y huele a hierba fresca.<br><br>Los contornos del cielo, un árbol verde y el susurro de las hojas a través de los párpados semicerrados adquieren calidez.<br><br>La pesadilla de la Giga-Khrushchevka ha terminado. Por fin te has despertado.",
        "ending_wakeup_stats": "<div style=\"font-weight: bold; font-size: 0.95rem; color: #111111; margin-bottom: 5px; text-align: center; letter-spacing: 1px;\">FINAL VERDADERO</div>Notas recogidas y leídas: 10 / 10<br>Descendiste antes de despertar: <span id=\"true-ending-floors-descended\" style=\"font-weight: bold; color: #6b0a0a;\">{0}</span> pisos",
        "ending_wakeup_author": "<strong>Autor del juego:</strong> @sw1therland<br><span style=\"font-size: 0.72rem; color: #666666;\">¡Gracias por jugar! Escapaste del Samostroy.</span>",
        "go_dehydration_title": "LIQUIDADO",
        "go_dehydration_desc": "<p>Tu cuerpo no pudo soportar la terrible deshidratación.</p><p>Te desplomaste sobre los fríos escalones de cemento del hueco de la escalera en el piso {0}.</p><p>Nadie vendrá a ayudarte. Tu cuerpo permanecerá aquí hasta que el próximo Samosbor lo disuelva en limo marrón.</p>",
        "go_stairs_monster_title": "DESPEDAZADO",
        "go_stairs_monster_desc": "<p>No reaccionaste a tiempo.</p><p>La bestia cayó sobre ti desde arriba, rompiéndote las costillas del pecho.</p><p>Mandíbulas afiladas perforaron el visor de tu máscara de gas. Lo último que escuchaste fue el chasquido de la biomasa devorando tu carne.</p>",
        "go_opened_monster_title": "ELIMINADO",
        "go_opened_monster_desc": "<p>Abriste la puerta sin escuchar primero.</p><p>Una bestia depredadora del Samosbor había hecho su nido justo al cruzar el umbral.</p><p>Tan pronto como los pernos se abrieron, la biomasa multi-extremidad te arrastró al interior de la habitación oscura. Ni siquiera tuviste tiempo de gritar.</p>",
        "go_samosbor_title": "DISUELTO",
        "go_samosbor_desc": "<p>Te quedaste en el pasillo durante la fase activa del Samosbor.</p><p>La niebla tóxica corroyó las juntas de goma de tu casco y tu piel en segundos.</p><p>Tu conocimiento se desvaneció mientras tus tejidos se derretían, fluyendo hacia las rejillas de ventilación.</p>",
        "go_samosbor_gas_title": "ASFIXIADO",
        "go_samosbor_gas_desc": "<p>Te escondiste en la habitación, pero descuidaste el equipo de protección.</p><p>El gas tóxico del Samosbor se filtró debajo de la compuerta hermética.</p><p>Sin máscara de gas, tus pulmones se llenaron de vapores ácidos, provocando espasmos inmediatos y asfixia.</p>",
        "go_ending1_title": "DESPERTAR",
        "go_ending1_desc": "<p>Habiendo recogido todas las notas, comprendiste la verdadera naturaleza de la Giga-Khrushchevka.</p><p>Cuando la niebla del Samosbor irrumpió en el pasillo, no corriste a esconderte. Te congelaste en el lugar, abriendo los brazos, y cerraste los ojos.</p><p>El mundo alrededor tembló, los muros de cemento comenzaron a desmoronarse en píxeles. La niebla púrpura te abrazó...</p><p>...Y de repente diste un fuerte respiro. Aire fresco y cálido llenó tus pulmones.</p><p>Abriste los ojos. Estabas acostado en una cama blanda. Un SOL brillante y real brillaba a través de la ventana, y hojas verdes susurraban afuera. Era un sueño. Una larga pesadilla de la que solo podías escapar dejando de tener miedo.</p>",
        "go_ending2_title": "SIN SALIDA",
        "go_ending2_desc": "<p>Superaste un largo camino y descendiste al primer piso.</p><p>Pero no hay paso al exterior. Las pesadas compuertas de la esclusa están herméticamente soldadas por siglos de óxido.</p><p>Detrás de ti, la puerta del hueco de la escalera se cerró con un estruendo. Los mecanismos se atascaron. Los pestillos no se mueven.</p><p>En este momento, las sirenas comenzaron a aullar al máximo volumen. Un Samosbor masivo comenzó. No hay refugios. Las puertas están bloqueadas. Estás atrapado en un saco de hormigón en el primer piso, cara a cara con la niebla mortal. Este es el final del camino.</p>",
        "go_badge_death": "Muerte",
        "go_badge_ending1": "Final verdadero",
        "go_badge_ending2": "Final sin salida",
        "log_creep_1": "¡Oíste un raspado lejano dentro de las paredes de cemento!",
        "log_creep_2": "Una corriente de aire trajo el olor de col podrida y carne cruda.",
        "log_creep_3": "Las luces parpadearon por un momento. Presión del casco estable.",
        "log_creep_4": "En algún lugar profundo de abajo, resonó un impacto metálico amortiguado.",
        "log_creep_5": "El contador Geiger hace clic silenciosamente. Radiación de fondo normal.",
        "log_gh_scary": "¡El fantasma está drenando la energía de tu linterna!",
        "log_water_low": "¡Advertencia! ¡Nivel de deshidratación crítico!",
        "log_descend_floor": "Descendiste al piso {0}.",
        "log_descend_warn": "El piso técnico está bloqueado por compuerta hermética. Se requiere pirateo.",
        "log_ascend_floor": "Ascendiste al piso {0}.",
        "log_room_clean": "Entraste en {0}. El aire está limpio. No se detectaron amenazas.",
        "log_room_hazard": "Entraste en {0}. ¡El aire es radiactivo! ¡Ponte la máscara! (tecla T)",
        "log_room_nest": "Entraste en {0}. El limo en las paredes se mueve. ¡Sientes una presencia! (¡Prepárate!)",
        "log_room_hallway": "Saliste al pasillo. La ventilación impulsa el aire frío de la Khrushchevka.",
        "log_lock_search_warn": "¡No se pueden buscar muebles durante el Samosbor, es demasiado peligroso!",
        "log_lock_door": "Cerraste la compuerta hermética del apartamento.",
        "log_unlock_door": "Abriste la compuerta hermética del apartamento.",
        "log_door_listen": "Escuchaste detrás de la puerta de {0}...",
        "log_door_listen_clean": "Silencio. Parece seguro adentro.",
        "log_door_listen_hazard": "Se escuchan pasos pesados y limo deslizándose. ¡Hay una bestia!",
        "log_door_listen_transition": "Se escucha el rumiar lejano de los transformadores de la compuerta técnica.",
        "log_hack_bypass_ok": "Bypass: ¡Canal {0} descifrado con éxito!",
        "log_hack_bypass_err": "Bypass: error de sincronización de fase de señal.",
        "log_hack_gate": "¡Compuerta Hermética! Las compuertas van hacia: {0}...",
        "log_hack_gate_open": "apertura",
        "log_hack_gate_close": "cierre",
        "log_hack_hacker_err": "Descifrador: Fallo. Circuito bloqueado por el sistema central. ¡Imposible de usar!",
        "log_hack_note_samosbor": "Recogiste todas las notas pero no las leíste... no pudiste comprender la verdad.",
        "log_hack_tool_hot": "¡El descifrador está sobrecalentado! Espera a que se enfríe.",
        "log_hack_tool_empty": "¡La batería del descifrador está vacía! Reemplaza la batería.",
        "log_loot_corpse": "[✔] Buscaste en el cuerpo, armadura (+8) y filtro (+40%) restablecidos.",
        "log_loot_note": "[✔] Nota encontrada: \"{0}\"!",
        "log_loot_hacker": "[✔] ¡Encontraste un descifrador de compuertas!",
        "log_loot_battery": "[✔] Encontraste una batería (+1 ud., total: {0}).",
        "log_loot_synthesizer": "Encontraste un sintetizador de alimentos (+50% de agua).",
        "log_loot_ammo": "[✔] Encontraste munición (+{0} uds.).",
        "log_loot_filter": "Encontraste un nuevo filtro (+50% de carga).",
        "log_loot_empty": "Buscaste en los muebles pero no encontraste nada útil.",
        "log_gasmask_equip": "Máscara de gas puesta. Respiración limitada, el visor se empaña.",
        "log_gasmask_unequip": "Máscara de gas quitada.",
        "log_gasmask_no": "¡No tienes máscara de gas!",
        "log_gasmask_empty": "¡El filtro está vacío! ¡El aire está envenenado!",
        "log_drink_sip": "Sorbo tomado. Agua botella: {0}% restante.",
        "log_siren_start": "[!] ¡La sirena del Samosbor comenzó a sonar!",
        "log_siren_desc": "¡Tienes 4 segundos para refugiarte en una habitación y cerrar la puerta!",
        "log_monster_shoot_scare": "¡Asustaste a la bestia con un disparo! ¡Se retiró al fondo del pozo!",
        "log_monster_shoot_dead": "¡Destruiste a la bestia con un disparo!",
        "log_monster_kick": "¡Pateaste a la bestia!",
        "log_monster_kick_dmg": "¡La bestia te mordió la pierna! ¡Daño recibido!",
        "log_crawler_run": "¡Escuchaste un rápido rascar de garras en el suelo!",
        "log_crawler_warn": "¡Una bestia corre hacia ti! ¡Presiona ESPACIO para patearla y repelerla!",
        "log_crawler_safe": "El ruido se desvaneció. La bestia huyó a las rejillas de ventilación.",
        "log_air_hazard": "¡Estás inhalando gases tóxicos! ¡Ponte la máscara de gas inmediatamente (tecla T)!",
        "log_air_empty_warn": "¡El filtro está vacío! ¡La máscara no te protege!",
        "log_air_samosbor_phase": "[!] El Samosbor entró en fase activa: ~20 segundos. ¡No salgas!",
        "log_air_samosbor_melt": "[!!!] ¡Las paredes se derriten! ¡El Samosbor llena los pasillos!",
        "log_air_samosbor_melt_dmg": "¡La niebla ácida corroe tu casco!",
        "log_air_filter_melt": "El filtro neutraliza gases, pero los químicos corroen los sellos...",
        "log_air_filter_empty_melt": "¡El filtro está vacío! ¡Te asfixias en el lodo tóxico!",
        "log_air_filter_norm": "El filtro neutraliza los gases. Estás a salvo.",
        "log_samosbor_end": "Las sirenas se callaron. Terminó el Samosbor. Pasó el peligro.",
        "log_game_start": "Comenzó el turno. Desciende al 1.er piso...",
        "log_sound_init": "Sistema de audio inicializado.",
        "log_save_controls": "Configuración de controles guardada.",
        "log_dev_command": "Comando dev ejecutado.",
        "note_0_title": "Papel mugriento (Piso ~1200)",
        "note_1_title": "Informe del comandante (Piso ~1100)",
        "note_2_title": "Memo de Protección Civil (Piso ~1000)",
        "note_3_title": "Diario de un niño (Piso ~900)",
        "note_4_title": "Página quemada misteriosa",
        "note_5_title": "Nota sin firma",
        "note_6_title": "Folleto de agitación (Piso ~800)",
        "note_7_title": "Trozo de papel destrozado",
        "note_8_title": "Papel de libreta ensangrentado (Piso ~700)",
        "note_9_title": "Última confesión de un Liquidador",
        "note_0_content": "Bloque 1290. Decimoséptimo día después del cierre del sector. \\n\\nLa ventilación zumba como loca, huele constantemente a carne cruda en descomposición y a químicos. El vecino de abajo desapareció ayer. Su esposa dice que oyó raspaduras detrás de la compuerta hermética en mitad de la noche, como si alguien intentara levantar el sello de acero con garras. \\n\\nEl agua del grifo lleva una semana saliendo marrón. Parece que los filtros de toma de agua están obstruidos con restos. Los Liquidadores no vienen. Nos dicen que nos quedemos en los apartamentos. ¿Dónde está el maldito sol? ¿Existe siquiera, o el hormigón es todo lo que hay en este mundo?",
        "note_1_content": "INFORME. Liquidador Sargento Sobolev. Grupo \"Beta-6\". \\n\\nSe nos ordenó limpiar el bloque 1105 después de una fuga local de Samosbor. Todo fue de acuerdo con las reglas, vertiendo reactivos en el pasillo. Pero en el pasillo final nos encontramos con el apartamento #42. La compuerta hermética estaba bloqueada desde el interior. Los niños gritaban desde allí dentro, rogándonos que abriéramos. \\n\\nPero los sensores mostraron una contaminación crítica detrás de la puerta. El limo del Samosbor ya se estaba filtrando por las juntas. La orden del mando fue explícita: sellar el bloque. Soldamos la puerta desde el exterior con sopletes. Los niños gritaron durante otros diez minutos mientras trabajábamos. Todavía escucho ese sonido cuando cierro los ojos. Perdónanos, Khrush.",
        "note_2_content": "MEMORÁNDUM PARA RESIDENTES DE GIGA-KHRUSHCHEVKA AL COMIENZO DEL SAMOSBOR: \\n\\n1. Al primer sonido de la sirena, detenga inmediatamente todo movimiento por las escaleras.\\n2. Ingrese a la vivienda o zona de esclusa más cercana.\\n3. Cierre herméticamente la compuerta hermética. Apriete a fondo las válvulas manuales de sujeción.\\n4. Póngase el equipo de protección personal (máscara de gas GP-9 o equivalente).\\n5. No se acerque a los conductos de ventilación ni a las aberturas de las puertas.\\n6. Ignore cualquier sonido, voces de familiares o colegas que provengan del exterior durante la fase activa.\\n7. Espere la llegada de los Liquidadores para los procedimientos de desinfección.",
        "note_3_content": "12 de marzo. \\n\\nMamá me quitó los lápices de colores porque dibujé el cielo. ¡Yo lo recuerdo! Era tan... azul, y arriba colgaba un gran círculo cálido que brillaba y calentaba. Mamá comenzó a llorar, rompió el dibujo y me golpeó en las manos. Dijo que el cielo es una peligrosa ilusión de locos, y que si alguien del Comité escucha mis historias, seremos enviados a los pisos técnicos inferiores para ser procesados en concentrado de alimentos. \\n\\nDice que no hay nada más que la Khrushchevka. Solo concreto hacia arriba, hacia abajo y en todas las direcciones. Pero sé que miente. Papá fue a buscar una salida hace seis meses y no regresó. Lo encontraré.",
        "note_4_content": "En la penumbra hay una litera de hierro chirriante con una manta gris de la institución. En la mesita de noche — una tetera de aluminio doblada con el pico astillado. En la pared cuelga torcido un cartel del Comité cubierto de moscas con el Liquidador #1, y en la esquina una vieja válvula oxidada gotea continuamente... \\n\\n[Te quedas frío de terror. ¡Esta es la descripción exacta de tu celda de vivienda 412 en el sector 13-A!]\\n\\n¿Cómo sabe el autor de esta nota cómo es mi habitación? ¿Quién la trajo aquí?",
        "note_5_content": "DEBES DESPERTAR.\\n\\nTe encuentras actualmente en el piso {0}. Pero esto es una mentira. No es real. Es imposible descender indefinidamente en un pozo de concreto sin comida ni descanso. Estás durmiendo. Tu máscara de gas está vacía desde hace mucho tiempo. Tus pulmones se quemaron con los humos del Samosbor, pero tu cerebro moribundo se aferra febrilmente a la ilusión del descenso.\\n\\nEstás durmiendo, Liquidador. Debes despertar. Debes. Despierta.",
        "note_6_content": "¡CIUDADANOS DE GIGA-KHRUSHCHEVKA! \\n\\nEl Comité de Salvación Pública le recuerda: \\n- La estructura infinita de la Khrushchevka es el único baluarte de la humanidad. \\n- Fuera de los muros de concreto reina el caos primigenio y el vacío.\\n- El trabajo de un liquidador es sagrado. Al dar su vida para sellar brechas, un liquidador encuentra la paz eterna en los corazones de los supervivientes.\\n- Cualquier rumor de una \"salida\" al exterior es un sabotaje de los agentes del caos para socavar la disciplina. \\n\\n¡MANTENGA LA VIGILANCIA! INFORME DE ACTIVIDADES SOSPECHOSAS AL PUESTO DE LIQUIDADORES MÁS CERCANO.",
        "note_7_content": "DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA DESPIERTA",
        "note_8_content": "Si lees esto... corre... \\n\\nPerforé el hueco del colector de cables en el piso 700. ¡El Comité nos ha estado mintiendo durante siglos! No hay caos afuera. Las paredes de Khrush son solo una carcasa. ¡Vi... vi el cielo! Realmente es azul, y huele a hierba allí afuera, no a cloro y carne quemada. \\n\\nPero nos vigilan. El Samosbor no es un desastre natural. Ellos mismos lo liberan a través de la ventilación cada vez que la población de un piso comienza a adivinar la verdad. ¡Es una purga! \\nSi comienza el Samosbor, no te escondas. Quédate quieto en el pasillo. Acógelo. Nos envenenan con gas que causa alucinaciones y sueño, pero es la única forma de perturbar los sensores de seguimiento y... [manchado de sangre oscura vieja]",
        "note_9_content": "Si encuentras esto, significa que ya me he convertido en parte de la Khrushchevka. \\n\\nFui Liquidador durante treinta años. Soldé puertas, quemé bestias y creí en el Comité. Pero no hay salida. El primer piso es un mito. El Samosbor no es niebla. Es la respiración de un gran organismo durmiente. Todos estamos dentro de una criatura viviente gigante que nos digiere lentamente. La única forma de salir es dejar de resistirse al sueño y abrir los ojos. Pero tengo miedo. Que el Khrush me perdone.",
        "btn_bag": "Bolsa",
        "label_notes_prefix": "Notas",
        "btn_descend_ending": "Congelarse en el lugar y esperar",
        "focus_liquidator_body": "CUERPO DE LIQUIDADOR",
        "focus_liquidator_desc": "Un liquidador muerto con uniforme. Registrar bolsillos (tecla R).",
        "focus_search_body": "Registrar cuerpo",
        "focus_stair_gate": "COMPUERTA HERMÉTICA DE ESCALERA",
        "focus_locked_by_system": "Bloqueado por el sistema central de la GIGA-KHRUSHCHEVKA.",
        "focus_try_hack": "Intentar hackear",
        "focus_gate_open_desc": "La compuerta está abierta. El paso a la escalera está libre.",
        "focus_close_gate": "Cerrar compuerta",
        "focus_gate_locked_desc": "¡La compuerta hermética masiva está cerrada! Pulsa B para hackear.",
        "focus_hack_gate": "Hackear compuerta",
        "focus_door_open_desc": "La puerta está abierta. Puedes entrar (muévete con WASD).",
        "btn_close_door": "Cerrar puerta",
        "focus_door_closed_desc": "La puerta hermética está cerrada. Acércate.",
        "btn_open_door_action": "Abrir puerta",
        "btn_interact_action": "Interactuar",
        "yes": "SÌ",
        "no": "NO",
        "pcs": "uds",
        "btn_rebind_waiting": "Pulsa una tecla..."
    }
};

function t(key, ...args) {
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

const LORE_NOTES = Array.from({ length: 10 }, (_, id) => ({
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
    gigahrush_butcher: {
        id: "gigahrush_butcher",
        get title() { return t('ach_butcher_title'); },
        get description() { return t('ach_butcher_desc'); },
        target: 50,
        unlocked: false,
        progress: 0
    },
    self_taught_hacker: {
        id: "self_taught_hacker",
        get title() { return t('ach_hacker_title'); },
        get description() { return t('ach_hacker_desc'); },
        target: 100,
        unlocked: false,
        progress: 0
    },
    spendthrift: {
        id: "spendthrift",
        get title() { return t('ach_spendthrift_title'); },
        get description() { return t('ach_spendthrift_desc'); },
        target: 1,
        unlocked: false,
        progress: 0
    },
    survivor: {
        id: "survivor",
        get title() { return t('ach_survivor_title'); },
        get description() { return t('ach_survivor_desc'); },
        target: 1,
        unlocked: false,
        progress: 0
    },
    water_drinker: {
        id: "water_drinker",
        get title() { return t('ach_drinker_title'); },
        get description() { return t('ach_drinker_desc'); },
        target: 50,
        unlocked: false,
        progress: 0
    },
    deceived: {
        id: "deceived",
        get title() { return t('ach_deceived_title'); },
        get description() { 
            const isUnlocked = ACHIEVEMENTS.deceived ? ACHIEVEMENTS.deceived.unlocked : false;
            return isUnlocked ? t('ach_deceived_desc') : t('ach_secret_desc');
        },
        target: 1,
        unlocked: false,
        progress: 0,
        secret: true
    },
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
    }
};

function loadAchievements() {
    const saved = localStorage.getItem('samosbor_achievements');
    if (saved) {
        try {
            const parsed = JSON.parse(saved);
            for (let id in ACHIEVEMENTS) {
                if (parsed[id]) {
                    ACHIEVEMENTS[id].unlocked = !!parsed[id].unlocked;
                    ACHIEVEMENTS[id].progress = parseInt(parsed[id].progress) || 0;
                }
            }
        } catch(e) {
            console.error("Failed to load achievements", e);
        }
    }
}

function saveAchievements() {
    try {
        const data = {};
        for (let id in ACHIEVEMENTS) {
            data[id] = {
                unlocked: ACHIEVEMENTS[id].unlocked,
                progress: ACHIEVEMENTS[id].progress
            };
        }
        localStorage.setItem('samosbor_achievements', JSON.stringify(data));
    } catch(e) {
        console.error("Failed to save achievements", e);
    }
}

function progressAchievement(id, amount = 1) {
    const ach = ACHIEVEMENTS[id];
    if (!ach || ach.unlocked) return;
    
    ach.progress = Math.min(ach.target, ach.progress + amount);
    saveAchievements();
    updateAchievementsModalUI();
    
    if (ach.progress >= ach.target) {
        unlockAchievement(id);
    }
}

function unlockAchievement(id) {
    const ach = ACHIEVEMENTS[id];
    if (!ach || ach.unlocked) return;
    
    ach.unlocked = true;
    ach.progress = ach.target;
    saveAchievements();
    updateAchievementsModalUI();
    
    // Play chime sound
    playAchievementUnlockSound();
    
    // Display visual Steam-style popup
    const popup = document.getElementById('achievement-popup');
    const titleEl = document.getElementById('achievement-popup-title');
    if (popup && titleEl) {
        titleEl.innerText = ach.title;
        popup.classList.remove('achievement-popup-hidden');
        popup.classList.add('achievement-popup-visible');
        
        if (window._achievementPopupTimeout) {
            clearTimeout(window._achievementPopupTimeout);
        }
        window._achievementPopupTimeout = setTimeout(() => {
            popup.classList.remove('achievement-popup-visible');
            popup.classList.add('achievement-popup-hidden');
        }, 4000);
    }
    
    logToConsole(`🏆 ДОСТИЖЕНИЕ ПОЛУЧЕНО: "${ach.title}"!`, "loot");
}

function playAchievementUnlockSound() {
    initAudio();
    if (!audioCtx) return;
    try {
        const now = audioCtx.currentTime;
        const osc1 = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        
        osc1.type = 'sine';
        // Retro C5-E5-G5-C6 major arpeggio chime
        osc1.frequency.setValueAtTime(523.25, now);
        osc1.frequency.setValueAtTime(659.25, now + 0.1);
        osc1.frequency.setValueAtTime(783.99, now + 0.2);
        osc1.frequency.setValueAtTime(1046.50, now + 0.3);
        
        gainNode.gain.setValueAtTime(0.001, now);
        gainNode.gain.linearRampToValueAtTime(0.18, now + 0.05);
        gainNode.gain.exponentialRampToValueAtTime(0.001, now + 0.7);
        
        osc1.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        
        osc1.start(now);
        osc1.stop(now + 0.7);
    } catch(e) {
        console.error("Audio chime error:", e);
    }
}

function updateAchievementsModalUI() {
    const container = document.getElementById('achievements-list-container');
    if (!container) return;
    
    container.innerHTML = '';
    for (let id in ACHIEVEMENTS) {
        const ach = ACHIEVEMENTS[id];
        const card = document.createElement('div');
        card.className = `achievement-card ${ach.unlocked ? 'unlocked' : 'locked'}`;
        
        const isSecretLocked = ach.secret && !ach.unlocked;
        const displayTitle = isSecretLocked ? "Секретное достижение" : ach.title;
        const displayDesc = isSecretLocked ? "🔒 Пройдите игру, чтобы открыть подробности" : ach.description;
        
        let progressHTML = '';
        if (ach.target > 1 && !isSecretLocked) {
            const pct = (ach.progress / ach.target) * 100;
            progressHTML = `
                <div class="achievement-card-progress-container">
                    <div class="achievement-card-progress-bar" style="width: ${pct}%;"></div>
                </div>
                <div class="achievement-card-progress-text">${ach.progress} / ${ach.target}</div>
            `;
        }
        
        card.innerHTML = `
            <div class="achievement-card-icon">
                ${ach.unlocked ? '🏆' : '🔒'}
            </div>
            <div class="achievement-card-info">
                <div class="achievement-card-title">${displayTitle}</div>
                <div class="achievement-card-desc">${displayDesc}</div>
                ${progressHTML}
            </div>
            <div class="achievement-card-status">
                ${ach.unlocked ? 'ПОЛУЧЕНО' : 'ЗАБЛОКИРОВАНО'}
            </div>
        `;
        container.appendChild(card);
    }
}

function openAchievementsModal() {
    updateAchievementsModalUI();
    const modal = document.getElementById('achievements-modal');
    if (modal) modal.classList.remove('modal-hidden');
}

function closeAchievementsModal() {
    const modal = document.getElementById('achievements-modal');
    if (modal) modal.classList.add('modal-hidden');
}

// --- ГЛОБАЛЬНОЕ СОСТОЯНИЕ ИГРЫ ---
let state = {
    floor: START_FLOOR,
    spawnFloor: START_FLOOR,
    health: MAX_HEALTH,
    water: MAX_WATER,
    ammo: MAX_AMMO,
    filter: MAX_FILTER,
    maskOn: false,
    notesCollected: [false, false, false, false, false, false, false, false, false, false],
    notesRead: [false, false, false, false, false, false, false, false, false, false],
    notesCount: 0,
    
    // Статусы Самосбора
    samosborStatus: 'normal', 
    samosborTimeLeft: 100, 
    samosborCountdown: 20, 
    samosborActiveDuration: 30, 
    
    // Двери на этаже (теперь 6 дверей)
    floorsData: {},
    get doors() {
        if (!this.floorsData) {
            this.floorsData = {};
        }
        if (!this.floorsData[this.floor]) {
            getOrGenerateFloorDoors(this.floor);
        }
        return this.floorsData[this.floor].doors;
    },
    set doors(val) {
        if (!this.floorsData) {
            this.floorsData = {};
        }
        this.floorsData[this.floor] = { doors: val };
    },
    focusedDoorIndex: null, // Дверь в перекрестии прицела
    focusedStairsDoor: false, // Гермозатвор на лестнице в перекрестии
    
    // Местоположение игрока
    location: 'hallway', // 'hallway', 'room', 'transition'
    samosborSafe: false, 
    searchProgress: 0,
    isSearching: false,
    
    // Лестничный монстр
    stairsMonsterActive: false,
    stairsMonsterTimeLeft: 0,
    
    audioInit: false,
    bottleWater: 100,
    
    // Новые механики взлома и бега
    stamina: 100,
    hasHackerTool: false,
    batteries: 0,
    stairsDoors: {},
    keyBindings: {},
    language: 'ru',
    floorEvent: null
};

// --- ФИЗИКА И ПОЛОЖЕНИЕ ИГРОКА (3D FPS) ---
let playerPos = new THREE.Vector3(0, 0, 0);
let playerYaw = 0; // Вращение по горизонтали
let playerPitch = 0; // Вращение по вертикали
let keys = {}; // Зажатые клавиши

// --- НАСТРОЙКИ КЛАВИАТУРЫ И УПРАВЛЕНИЯ ---
const DEFAULT_KEY_BINDINGS = {
    'MoveForward': 'KeyW',
    'MoveBackward': 'KeyS',
    'MoveLeft': 'KeyA',
    'MoveRight': 'KeyD',
    'Sprint': 'ShiftLeft',
    'Interact': 'KeyR',
    'Flashlight': 'KeyF',
    'Listen': 'KeyE',
    'GasMask': 'KeyT',
    'Water': 'KeyQ',
    'Bag': 'KeyG',
    'Search': 'KeyZ',
    'HackerTool': 'KeyB',
    'Pause': 'Escape'
};

const ACTION_LABELS = {
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
};

function loadKeyBindings() {
    try {
        const saved = localStorage.getItem('samosbor_keybindings');
        if (saved) {
            state.keyBindings = JSON.parse(saved);
            for (let k in DEFAULT_KEY_BINDINGS) {
                if (!state.keyBindings[k]) {
                    state.keyBindings[k] = DEFAULT_KEY_BINDINGS[k];
                }
            }
            return;
        }
    } catch (e) {
        console.warn("Failed to load keybindings:", e);
    }
    state.keyBindings = Object.assign({}, DEFAULT_KEY_BINDINGS);
}

function saveKeyBindings() {
    try {
        localStorage.setItem('samosbor_keybindings', JSON.stringify(state.keyBindings));
    } catch (e) {
        console.error("Failed to save keybindings:", e);
    }
}

// --- УПРАВЛЕНИЕ ЛЕСТНИЧНЫМИ ДВЕРЯМИ ---
function getOrGenerateStairsDoor(floorNum) {
    if (!state.stairsDoors) {
        state.stairsDoors = {};
    }
    if (state.stairsDoors[floorNum] !== undefined) {
        return state.stairsDoors[floorNum];
    }
    if (floorNum === START_FLOOR) {
        state.stairsDoors[floorNum] = { opened: true };
    } else if (floorNum === 1) {
        state.stairsDoors[floorNum] = { opened: false };
    } else if (floorNum === 1320) {
        // Guaranteed locked to force player to loot apartments on floor 1320 for hacker tool
        state.stairsDoors[floorNum] = { opened: false };
    } else {
        // Если у игрока ещё нет взломщика гермодверей, затворы не могут быть закрытыми
        if (!state.hasHackerTool) {
            state.stairsDoors[floorNum] = { opened: true };
        } else {
            // 40% chance of being closed (needs hacker tool)
            state.stairsDoors[floorNum] = { opened: Math.random() >= 0.4 };
        }
    }
    return state.stairsDoors[floorNum];
}
let pointerLocked = false;
let footstepTimeAccumulator = 0; // Накопитель времени для звуков шагов
const playerSpeed = 4.0;
const sensitivity = 0.0025;

// Мобильное управление движением (флаги виртуального D-pad)
let mvUp = false, mvDown = false, mvLeft = false, mvRight = false;
let touchStartX = 0, touchStartY = 0;

// --- ТРЁХМЕРНАЯ ГРАФИКА (THREE.JS ENGINE) ---
let renderer, scene, camera, raycaster;
let floorMesh, ceilingMesh, leftWallMesh, rightWallMesh, backWallMesh, frontWallMesh;
let doorPivots = []; // Створки дверей в 3D
let ceilingPipes = [];
let ceilingLights = [];
let warningBeacon, warningLight;
let roomMeshes = [];
let transitionMeshes = [];
let stairsMonsterMesh = null;
let staircaseMeshes = [];
let proceduralTextures = {};

// Координаты дверей на этаже: 3 слева (X = -3), 3 справа (X = 3)
const DOOR_LAYOUT = [
    { x: -3.0, z: -10, rot: Math.PI / 2 },
    { x: -3.0, z: -22, rot: Math.PI / 2 },
    { x: -3.0, z: -34, rot: Math.PI / 2 },
    { x: 3.0, z: -10, rot: -Math.PI / 2 },
    { x: 3.0, z: -22, rot: -Math.PI / 2 },
    { x: 3.0, z: -34, rot: -Math.PI / 2 }
];

function init3D() {
    const holder = document.getElementById('canvas-holder');
    if (!holder) return;
    
    holder.innerHTML = '';
    
    // 1. WebGL рендерер
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
    renderer.setSize(holder.clientWidth, holder.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    holder.appendChild(renderer.domElement);
    
    // 2. Сцена и камера
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x060709);
    scene.fog = new THREE.FogExp2(0x060709, 0.06);
    
    camera = new THREE.PerspectiveCamera(65, holder.clientWidth / holder.clientHeight, 0.1, 100);
    camera.rotation.order = 'YXZ'; // Важно для FPS вращения!
    
    raycaster = new THREE.Raycaster();
    
    // 3. Создаем текстуры
    generateProceduralTextures();
    
    // 4. Строим сцену
    build3DScene();
    
    // Добавляем фонарик игрока (включен по умолчанию)
    playerFlashlight = new THREE.SpotLight(0xffffee, 2.5, 25, Math.PI / 3.5, 0.6, 1);
    playerFlashlight.position.set(0, 0, 0);
    playerFlashlight.target.position.set(0, 0, -1);
    playerFlashlight.castShadow = true;
    playerFlashlight.shadow.mapSize.width = 512;
    playerFlashlight.shadow.mapSize.height = 512;
    playerFlashlight.shadow.bias = -0.001;
    camera.add(playerFlashlight);
    camera.add(playerFlashlight.target);
    
    // Procedural First-Person Pistol Model
    const pistolGroup = new THREE.Group();
    pistolGroup.name = "pistol";
    const pistolMetal = new THREE.MeshStandardMaterial({ color: 0x22252a, roughness: 0.5, metalness: 0.8 });
    const pistolGrip = new THREE.MeshStandardMaterial({ color: 0x111215, roughness: 0.8 });
    const laserSightMat = new THREE.MeshBasicMaterial({ color: 0xff0000 });
    
    // Slide/Barrel
    const slideGeo = new THREE.BoxGeometry(0.04, 0.05, 0.22);
    const slide = new THREE.Mesh(slideGeo, pistolMetal);
    pistolGroup.add(slide);
    
    // Grip
    const gripGeo = new THREE.BoxGeometry(0.035, 0.11, 0.045);
    const grip = new THREE.Mesh(gripGeo, pistolGrip);
    grip.position.set(0, -0.065, 0.045);
    grip.rotation.x = 0.25;
    pistolGroup.add(grip);
    
    // Trigger guard
    const guardGeo = new THREE.BoxGeometry(0.015, 0.03, 0.05);
    const guard = new THREE.Mesh(guardGeo, pistolMetal);
    guard.position.set(0, -0.035, -0.02);
    pistolGroup.add(guard);

    // Laser module
    const laserGeo = new THREE.CylinderGeometry(0.007, 0.007, 0.07, 8);
    const laser = new THREE.Mesh(laserGeo, pistolMetal);
    laser.rotation.x = Math.PI / 2;
    laser.position.set(0, -0.022, -0.05);
    pistolGroup.add(laser);

    const lensGeo = new THREE.CylinderGeometry(0.004, 0.004, 0.002, 8);
    const lens = new THREE.Mesh(lensGeo, laserSightMat);
    lens.rotation.x = Math.PI / 2;
    lens.position.set(0, -0.022, -0.086);
    pistolGroup.add(lens);
    
    pistolGroup.position.set(0.18, -0.16, -0.32);
    pistolGroup.rotation.y = -Math.PI / 20;
    pistolGroup.rotation.x = Math.PI / 80;
    camera.add(pistolGroup);
    
    scene.add(camera);
    
    // 5. Запуск цикла
    animate3D();
}

function generateProceduralTextures() {
    const createNoiseTexture = (baseColor, noiseColor, scale = 1, isConcrete = false) => {
        const canvas = document.createElement('canvas');
        canvas.width = 256;
        canvas.height = 256;
        const ctx = canvas.getContext('2d');
        
        ctx.fillStyle = baseColor;
        ctx.fillRect(0, 0, 256, 256);
        
        ctx.fillStyle = noiseColor;
        for (let i = 0; i < 6000; i++) {
            const size = Math.random() * 2 + 1;
            const x = Math.random() * 256;
            const y = Math.random() * 256;
            ctx.globalAlpha = Math.random() * 0.18;
            ctx.fillRect(x, y, size, size);
        }
        
        if (isConcrete) {
            ctx.fillStyle = 'rgba(74, 52, 32, 0.15)';
            for (let i = 0; i < 18; i++) {
                ctx.beginPath();
                ctx.arc(Math.random() * 256, Math.random() * 256, Math.random() * 60 + 20, 0, Math.PI * 2);
                ctx.fill();
            }
            ctx.strokeStyle = 'rgba(10, 10, 10, 0.4)';
            ctx.lineWidth = 1;
            for (let i = 0; i < 4; i++) {
                ctx.beginPath();
                ctx.moveTo(Math.random() * 256, Math.random() * 256);
                ctx.lineTo(Math.random() * 256, Math.random() * 256);
                ctx.stroke();
            }
        }
        
        ctx.globalAlpha = 1.0;
        const tex = new THREE.CanvasTexture(canvas);
        tex.wrapS = THREE.RepeatWrapping;
        tex.wrapT = THREE.RepeatWrapping;
        tex.repeat.set(scale, scale);
        return tex;
    };
    
    const createDoorTexture = () => {
        const canvas = document.createElement('canvas');
        canvas.width = 256;
        canvas.height = 512;
        const ctx = canvas.getContext('2d');
        
        ctx.fillStyle = '#2d333b';
        ctx.fillRect(0, 0, 256, 512);
        
        ctx.fillStyle = '#5c2d13';
        for (let i = 0; i < 2000; i++) {
            ctx.globalAlpha = Math.random() * 0.2;
            ctx.fillRect(Math.random() * 256, Math.random() * 512, Math.random() * 4 + 1, Math.random() * 4 + 1);
        }
        
        ctx.strokeStyle = '#111417';
        ctx.lineWidth = 4;
        ctx.strokeRect(10, 10, 236, 492);
        ctx.strokeRect(20, 20, 216, 230);
        ctx.strokeRect(20, 262, 216, 230);
        
        // Вентиль штурвала
        ctx.strokeStyle = '#4a5463';
        ctx.lineWidth = 8;
        ctx.beginPath();
        ctx.arc(128, 256, 42, 0, Math.PI * 2);
        ctx.stroke();
        
        ctx.fillStyle = '#111316';
        ctx.beginPath();
        ctx.arc(128, 256, 16, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.fillStyle = '#4a5463';
        ctx.fillRect(124, 202, 8, 108);
        ctx.fillRect(74, 252, 108, 8);
        
        ctx.globalAlpha = 1.0;
        return new THREE.CanvasTexture(canvas);
    };

    const createWallpaperTexture = () => {
        const canvas = document.createElement('canvas');
        canvas.width = 128;
        canvas.height = 128;
        const ctx = canvas.getContext('2d');
        
        ctx.fillStyle = '#261e16';
        ctx.fillRect(0, 0, 128, 128);
        
        ctx.strokeStyle = '#181109';
        ctx.lineWidth = 2;
        for (let x = 16; x < 128; x += 32) {
            ctx.beginPath();
            ctx.moveTo(x, 0); ctx.lineTo(x, 128);
            ctx.stroke();
        }
        ctx.globalAlpha = 0.25;
        ctx.strokeStyle = '#e6b800';
        ctx.lineWidth = 1;
        for (let y = 0; y < 128; y += 16) {
            for (let x = 0; x < 128; x += 16) {
                ctx.beginPath();
                ctx.moveTo(x, y + 8);
                ctx.lineTo(x + 8, y);
                ctx.lineTo(x + 16, y + 8);
                ctx.lineTo(x + 8, y + 16);
                ctx.closePath();
                ctx.stroke();
            }
        }
        ctx.globalAlpha = 1.0;
        const tex = new THREE.CanvasTexture(canvas);
        tex.wrapS = THREE.RepeatWrapping;
        tex.wrapT = THREE.RepeatWrapping;
        tex.repeat.set(4, 4);
        return tex;
    };
    
    const createStairsDoorTexture = () => {
        const canvas = document.createElement('canvas');
        canvas.width = 256;
        canvas.height = 512;
        const ctx = canvas.getContext('2d');
        
        ctx.fillStyle = '#1c2024';
        ctx.fillRect(0, 0, 256, 512);
        
        ctx.fillStyle = '#4a2f1b';
        for (let i = 0; i < 1500; i++) {
            ctx.globalAlpha = Math.random() * 0.15;
            ctx.fillRect(Math.random() * 256, Math.random() * 512, Math.random() * 5 + 1, Math.random() * 5 + 1);
        }
        ctx.globalAlpha = 1.0;
        
        ctx.strokeStyle = '#0e1013';
        ctx.lineWidth = 6;
        ctx.strokeRect(6, 6, 244, 500);
        ctx.beginPath();
        ctx.moveTo(6, 256);
        ctx.lineTo(250, 256);
        ctx.stroke();
        
        ctx.strokeStyle = '#2d333b';
        ctx.lineWidth = 4;
        ctx.strokeRect(16, 16, 224, 230);
        ctx.strokeRect(16, 266, 224, 230);
        
        ctx.beginPath();
        ctx.moveTo(20, 20); ctx.lineTo(236, 242);
        ctx.moveTo(236, 20); ctx.lineTo(20, 242);
        ctx.moveTo(20, 270); ctx.lineTo(236, 492);
        ctx.moveTo(236, 270); ctx.lineTo(20, 492);
        ctx.stroke();
        
        ctx.fillStyle = '#ffcc00';
        ctx.globalAlpha = 0.4;
        ctx.fillRect(6, 6, 20, 500);
        ctx.fillRect(230, 6, 20, 500);
        ctx.fillStyle = '#000000';
        for (let y = 10; y < 512; y += 30) {
            ctx.beginPath();
            ctx.moveTo(6, y);
            ctx.lineTo(26, y + 20);
            ctx.lineTo(26, y + 30);
            ctx.lineTo(6, y + 10);
            ctx.closePath();
            ctx.fill();
            
            ctx.beginPath();
            ctx.moveTo(230, y);
            ctx.lineTo(250, y + 20);
            ctx.lineTo(250, y + 30);
            ctx.lineTo(230, y + 10);
            ctx.closePath();
            ctx.fill();
        }
        ctx.globalAlpha = 1.0;
        
        return new THREE.CanvasTexture(canvas);
    };

    proceduralTextures.concrete = createNoiseTexture('#424750', '#1c1f24', 3, true);
    proceduralTextures.ceiling = createNoiseTexture('#25282e', '#090a0c', 4, false);
    proceduralTextures.rust = createNoiseTexture('#4a3325', '#160e0a', 1, false);
    proceduralTextures.door = createDoorTexture();
    proceduralTextures.wallpaper = createWallpaperTexture();
    proceduralTextures.stairsDoor = createStairsDoorTexture();

    // Procedural Normal Map generator from Canvas texture image data
    const createNormalMap = (srcCanvas, strength = 1.0) => {
        const width = srcCanvas.width;
        const height = srcCanvas.height;
        const ctxSrc = srcCanvas.getContext('2d');
        const imgData = ctxSrc.getImageData(0, 0, width, height);
        const data = imgData.data;

        const normalCanvas = document.createElement('canvas');
        normalCanvas.width = width;
        normalCanvas.height = height;
        const ctxDst = normalCanvas.getContext('2d');
        const dstData = ctxDst.createImageData(width, height);
        const dst = dstData.data;

        const getPixelIntensity = (x, y) => {
            const px = (x + width) % width;
            const py = (y + height) % height;
            const idx = (py * width + px) * 4;
            return (data[idx] + data[idx+1] + data[idx+2]) / 3;
        };

        for (let y = 0; y < height; y++) {
            for (let x = 0; x < width; x++) {
                const idx = (y * width + x) * 4;
                const hL = getPixelIntensity(x - 1, y);
                const hR = getPixelIntensity(x + 1, y);
                const hD = getPixelIntensity(x, y - 1);
                const hU = getPixelIntensity(x, y + 1);
                const dx = (hR - hL) / 255.0 * strength;
                const dy = (hU - hD) / 255.0 * strength;
                const len = Math.sqrt(dx * dx + dy * dy + 1.0);
                const nx = -dx / len;
                const ny = -dy / len;
                const nz = 1.0 / len;
                dst[idx]   = Math.floor((nx * 0.5 + 0.5) * 255);
                dst[idx+1] = Math.floor((ny * 0.5 + 0.5) * 255);
                dst[idx+2] = Math.floor((nz * 0.5 + 0.5) * 255);
                dst[idx+3] = 255;
            }
        }
        ctxDst.putImageData(dstData, 0, 0);
        return normalCanvas;
    };

    // Generating Normal/Bump Map CanvasTextures to add realistic 3D depth under PointLights/Flashlight
    proceduralTextures.concreteNormal = new THREE.CanvasTexture(createNormalMap(proceduralTextures.concrete.image, 3.5));
    proceduralTextures.concreteNormal.wrapS = THREE.RepeatWrapping;
    proceduralTextures.concreteNormal.wrapT = THREE.RepeatWrapping;
    proceduralTextures.concreteNormal.repeat.copy(proceduralTextures.concrete.repeat);

    proceduralTextures.ceilingNormal = new THREE.CanvasTexture(createNormalMap(proceduralTextures.ceiling.image, 2.5));
    proceduralTextures.ceilingNormal.wrapS = THREE.RepeatWrapping;
    proceduralTextures.ceilingNormal.wrapT = THREE.RepeatWrapping;
    proceduralTextures.ceilingNormal.repeat.copy(proceduralTextures.ceiling.repeat);

    proceduralTextures.rustNormal = new THREE.CanvasTexture(createNormalMap(proceduralTextures.rust.image, 2.5));
    proceduralTextures.rustNormal.wrapS = THREE.RepeatWrapping;
    proceduralTextures.rustNormal.wrapT = THREE.RepeatWrapping;
    proceduralTextures.rustNormal.repeat.copy(proceduralTextures.rust.repeat);

    proceduralTextures.doorNormal = new THREE.CanvasTexture(createNormalMap(proceduralTextures.door.image, 4.0));

    proceduralTextures.wallpaperNormal = new THREE.CanvasTexture(createNormalMap(proceduralTextures.wallpaper.image, 2.5));
    proceduralTextures.wallpaperNormal.wrapS = THREE.RepeatWrapping;
    proceduralTextures.wallpaperNormal.wrapT = THREE.RepeatWrapping;
    proceduralTextures.wallpaperNormal.repeat.copy(proceduralTextures.wallpaper.repeat);
    
    proceduralTextures.stairsDoorNormal = new THREE.CanvasTexture(createNormalMap(proceduralTextures.stairsDoor.image, 4.0));
}

function disposeHierarchy(obj) {
    if (!obj) return;
    if (obj.children) {
        for (let i = obj.children.length - 1; i >= 0; i--) {
            disposeHierarchy(obj.children[i]);
        }
    }
    if (obj.geometry) {
        try { obj.geometry.dispose(); } catch(e) {}
    }
    if (obj.material) {
        if (Array.isArray(obj.material)) {
            obj.material.forEach(mat => {
                try { mat.dispose(); } catch(e) {}
            });
        } else {
            try { obj.material.dispose(); } catch(e) {}
        }
    }
}

function removeAndDispose(mesh) {
    if (!mesh) return;
    scene.remove(mesh);
    disposeHierarchy(mesh);
}

function build3DScene() {
    // Удаление старых объектов с высвобождением видеопамяти
    if (hallwayCrawlerMesh) { removeAndDispose(hallwayCrawlerMesh); hallwayCrawlerMesh = null; }
    if (deadLiquidatorMesh) { removeAndDispose(deadLiquidatorMesh); deadLiquidatorMesh = null; }
    if (ghostMesh) { removeAndDispose(ghostMesh); ghostMesh = null; }
    
    doorPivots.forEach(m => removeAndDispose(m));
    doorPivots = [];
    ceilingPipes.forEach(m => removeAndDispose(m));
    ceilingPipes = [];
    ceilingLights.forEach(m => removeAndDispose(m));
    ceilingLights = [];
    roomMeshes.forEach(m => removeAndDispose(m));
    roomMeshes = [];
    transitionMeshes.forEach(m => removeAndDispose(m));
    transitionMeshes = [];
    staircaseMeshes.forEach(m => removeAndDispose(m));
    staircaseMeshes = [];
    if (stairsMonsterMesh) { removeAndDispose(stairsMonsterMesh); stairsMonsterMesh = null; }
    
    warningBeacons = [];
    warningLights = [];
    doorLights = {};
    
    if (floorMesh) { removeAndDispose(floorMesh); floorMesh = null; }
    if (ceilingMesh) { removeAndDispose(ceilingMesh); ceilingMesh = null; }
    if (leftWallMesh) { removeAndDispose(leftWallMesh); leftWallMesh = null; }
    if (rightWallMesh) { removeAndDispose(rightWallMesh); rightWallMesh = null; }
    if (backWallMesh) { removeAndDispose(backWallMesh); backWallMesh = null; }
    if (warningBeacon) { removeAndDispose(warningBeacon); warningBeacon = null; }
    
    // Мы всегда рендерим вертикальный мир (коридоры и комнаты), так как он бесшовный
    scene.fog.color.setHex(0x060709);
    scene.fog.density = 0.06;
    
    // Генерируем текущий этаж, 2 выше и 2 ниже
    for (let i = 2; i >= -2; i--) {
        const floorNum = state.floor + i;
        const baseY = i * 5.0;
        buildFloor(floorNum, baseY);
    }
    
    // Выбор события этажа при переходе
    const isNewFloor = (state.floor !== lastBuiltFloor);
    if (isNewFloor) {
        lastBuiltFloor = state.floor;
        state.floorEvent = null;
        deadLiquidatorSearched = false;
        
        // Удаляем тварь при смене этажа
        if (hallwayCrawlerMesh) {
            scene.remove(hallwayCrawlerMesh);
            hallwayCrawlerMesh = null;
        }
        
        // Спавн ползающей твари с шансом 22% (если не спавн и не 1-й этаж)
        if (Math.random() < 0.22 && state.floor < START_FLOOR && state.floor > 1) {
            spawnHallwayCrawler(-38.0, 0.0);
        }
        
        // Случайные события с шансом 45%
        if (state.floor < START_FLOOR && state.floor > 1 && Math.random() < 0.45) {
            const evRand = Math.random();
            if (evRand < 0.25) {
                state.floorEvent = 'flicker';
                logToConsole("Свет на этом этаже нестабилен. Энергосеть перегружена.", "warn");
            } else if (evRand < 0.50) {
                state.floorEvent = 'gas_leak';
                logToConsole("ВНИМАНИЕ: Слышно шипение труб. В коридоре утечка газа Самосбора!", "danger");
            } else if (evRand < 0.75) {
                state.floorEvent = 'corpse';
                logToConsole("На полу впереди лежит неподвижное тело ликвидатора...", "sys");
            } else {
                state.floorEvent = 'ghost';
                logToConsole("Леденящий сквозняк... В глубине коридора промелькнул силуэт.", "sys");
            }
        }
    }
    
    // Единый фоновый свет
    const ambLight = new THREE.AmbientLight(0xffffff, 0.12);
    scene.add(ambLight);
    roomMeshes.push(ambLight);
    
    // Отрисовка объектов событий текущего этажа
    if (state.floorEvent === 'corpse') {
        spawnDeadLiquidatorMesh();
    } else if (state.floorEvent === 'ghost') {
        spawnGhostMesh();
    }
    
    // Если тварь активна, добавляем её обратно на сцену
    if (hallwayCrawlerMesh) {
        scene.add(hallwayCrawlerMesh);
    }
    
    // Спавн 3D Лестничного монстра (если активен)
    if (state.stairsMonsterActive) {
        spawn3DMonster();
    }
}


function createDetailedCabinet(dirX) {
    const group = new THREE.Group();
    const woodMat = new THREE.MeshStandardMaterial({ color: 0x3d2314, roughness: 0.9 });
    const glassMat = new THREE.MeshStandardMaterial({ color: 0x88ccff, transparent: true, opacity: 0.5, roughness: 0.1 });
    const handleMat = new THREE.MeshStandardMaterial({ color: 0xaaaaaa, roughness: 0.4, metalness: 0.8 });
    
    const base = new THREE.Mesh(new THREE.BoxGeometry(1.8, 1.5, 0.8), woodMat);
    base.position.y = 0.75;
    base.receiveShadow = true; // Optimized shadows
    group.add(base);
    
    const top = new THREE.Mesh(new THREE.BoxGeometry(1.7, 2.0, 0.7), woodMat);
    top.position.y = 2.5;
    top.receiveShadow = true; // Optimized shadows
    group.add(top);
    
    const glass = new THREE.Mesh(new THREE.BoxGeometry(1.5, 1.8, 0.05), glassMat);
    glass.position.set(-0.36 * dirX, 2.5, 0); 
    group.add(glass);
    
    return group;
}

function createDetailedTable() {
    const group = new THREE.Group();
    const woodMat = new THREE.MeshStandardMaterial({ color: 0x5e3a21, roughness: 0.8 });
    
    const top = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.1, 1.0), woodMat);
    top.position.y = 0.95;
    top.receiveShadow = true; // Optimized shadows
    group.add(top);
    
    const legGeo = new THREE.BoxGeometry(0.1, 0.9, 0.1);
    const positions = [
        [-0.7, -0.4], [0.7, -0.4], [-0.7, 0.4], [0.7, 0.4]
    ];
    positions.forEach(pos => {
        const leg = new THREE.Mesh(legGeo, woodMat);
        leg.position.set(pos[0], 0.45, pos[1]);
        leg.receiveShadow = true; // Optimized shadows
        group.add(leg);
    });
    
    return group;
}

function createDetailedPanel(dirX) {
    const group = new THREE.Group();
    const metalMat = new THREE.MeshStandardMaterial({ color: 0x333333, roughness: 0.7 });
    const screenMat = new THREE.MeshBasicMaterial({ color: 0x0044aa });
    const buttonRed = new THREE.MeshBasicMaterial({ color: 0xff0000 });
    const buttonGreen = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    
    const base = new THREE.Mesh(new THREE.BoxGeometry(0.6, 1.0, 1.5), metalMat);
    base.position.y = 0.5;
    base.receiveShadow = true; // Optimized shadows
    group.add(base);
    
    const deck = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.8, 1.5), metalMat);
    deck.position.set(-0.15 * dirX, 1.2, 0);
    deck.rotation.z = (Math.PI / 6) * dirX;
    deck.receiveShadow = true; // Optimized shadows
    group.add(deck);
    
    const screen = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.5, 0.8), screenMat);
    screen.position.set(-0.46 * dirX, 1.35, 0);
    screen.rotation.z = (Math.PI / 6) * dirX;
    group.add(screen);
    
    return group;
}

function addVolumetricHandle(doorMesh) {
    const handleMat = new THREE.MeshStandardMaterial({
        color: 0x484d54,
        roughness: 0.5,
        metalness: 0.85
    });

    const shaftGeo = new THREE.CylinderGeometry(0.018, 0.018, 0.06, 8);
    shaftGeo.rotateX(Math.PI / 2); // Align pointing along Z-axis
    
    const wheelGeo = new THREE.TorusGeometry(0.12, 0.012, 8, 24);
    
    const spokeHGeo = new THREE.CylinderGeometry(0.008, 0.008, 0.24, 8);
    spokeHGeo.rotateZ(Math.PI / 2); // Align pointing along X-axis
    
    const spokeVGeo = new THREE.CylinderGeometry(0.008, 0.008, 0.24, 8); // Align pointing along Y-axis

    [-1, 1].forEach((side) => {
        const shaftZ = side * (0.05 + 0.03);
        const wheelZ = side * (0.05 + 0.06 + 0.006);

        // 1. Shaft
        const shaft = new THREE.Mesh(shaftGeo, handleMat);
        shaft.position.set(0.42, 0, shaftZ);
        shaft.castShadow = true;
        shaft.receiveShadow = true;
        doorMesh.add(shaft);

        // 2. Wheel Torus
        const wheel = new THREE.Mesh(wheelGeo, handleMat);
        wheel.position.set(0.42, 0, wheelZ);
        wheel.castShadow = true;
        wheel.receiveShadow = true;
        doorMesh.add(wheel);

        // 3. Horizontal Spoke
        const spokeH = new THREE.Mesh(spokeHGeo, handleMat);
        spokeH.position.set(0.42, 0, wheelZ);
        spokeH.castShadow = true;
        spokeH.receiveShadow = true;
        doorMesh.add(spokeH);

        // 4. Vertical Spoke
        const spokeV = new THREE.Mesh(spokeVGeo, handleMat);
        spokeV.position.set(0.42, 0, wheelZ);
        spokeV.castShadow = true;
        spokeV.receiveShadow = true;
        doorMesh.add(spokeV);
    });
}

function buildFloor(floorNum, baseY) {

    const wallMat = new THREE.MeshStandardMaterial({ 
        map: proceduralTextures.concrete, 
        normalMap: proceduralTextures.concreteNormal, 
        roughness: 0.8,
        metalness: 0.05
    });
    const floorMat = new THREE.MeshStandardMaterial({ 
        map: proceduralTextures.concrete, 
        normalMap: proceduralTextures.concreteNormal, 
        roughness: 0.9
    });
    const ceilingMat = new THREE.MeshStandardMaterial({ 
        map: proceduralTextures.ceiling, 
        normalMap: proceduralTextures.ceilingNormal, 
        roughness: 0.95
    });
    
    // 1. Пол и потолок коридора (BoxGeometry для устранения засветов)
    const floorGeo = new THREE.BoxGeometry(6, 0.2, 42);
    const fMesh = new THREE.Mesh(floorGeo, floorMat);
    fMesh.position.set(0, baseY - 0.1, -21);
    fMesh.receiveShadow = true;
    scene.add(fMesh);
    roomMeshes.push(fMesh);
    
    const ceilingGeo = new THREE.BoxGeometry(6, 0.2, 42);
    const cMesh = new THREE.Mesh(ceilingGeo, ceilingMat);
    cMesh.position.set(0, baseY + 5.0 + 0.1, -21);
    cMesh.receiveShadow = true;
    scene.add(cMesh);
    roomMeshes.push(cMesh);
    
    // 2. Сегментированные толстые стены коридора
    const segments = [
        { zStart: 0, zEnd: -9.4 },
        { zStart: -10.6, zEnd: -21.4 },
        { zStart: -22.6, zEnd: -33.4 },
        { zStart: -34.6, zEnd: -42.0 }
    ];
    
    const buildWallSide = (xPos) => {
        const wallGroup = new THREE.Group();
        segments.forEach(seg => {
            const len = Math.abs(seg.zStart - seg.zEnd);
            const zCenter = (seg.zStart + seg.zEnd) / 2;
            const mesh = new THREE.Mesh(new THREE.BoxGeometry(0.2, 5.0, len), wallMat);
            mesh.position.set(0, 2.5, zCenter);
            mesh.receiveShadow = true;
            mesh.castShadow = true;
            wallGroup.add(mesh);
        });
        [-10, -22, -34].forEach(zDoor => {
            const meshTop = new THREE.Mesh(new THREE.BoxGeometry(0.2, 2.4, 1.2), wallMat);
            meshTop.position.set(0, 3.8, zDoor);
            meshTop.receiveShadow = true;
            meshTop.castShadow = true;
            wallGroup.add(meshTop);
        });
        wallGroup.position.set(xPos, baseY, 0);
        wallGroup.rotation.y = 0;
        scene.add(wallGroup);
        roomMeshes.push(wallGroup);
        return wallGroup;
    };
    
    leftWallMesh = buildWallSide(-3.1);
    rightWallMesh = buildWallSide(3.1);
    
    // Задняя стена коридора
    const backWall = new THREE.Mesh(new THREE.BoxGeometry(6, 5, 0.2), wallMat);
    backWall.position.set(0, baseY + 2.5, 0.1);
    backWall.receiveShadow = true;
    backWall.castShadow = true;
    scene.add(backWall);
    roomMeshes.push(backWall);
    
    // Перегородка с лестничным проемом на Z = -42
    const stairsHoleWallL = new THREE.Mesh(new THREE.BoxGeometry(1.5, 5, 0.2), wallMat);
    stairsHoleWallL.position.set(-2.25, baseY + 2.5, -42);
    stairsHoleWallL.receiveShadow = true;
    stairsHoleWallL.castShadow = true;
    scene.add(stairsHoleWallL);
    staircaseMeshes.push(stairsHoleWallL);
    
    const stairsHoleWallR = new THREE.Mesh(new THREE.BoxGeometry(1.5, 5, 0.2), wallMat);
    stairsHoleWallR.position.set(2.25, baseY + 2.5, -42);
    stairsHoleWallR.receiveShadow = true;
    stairsHoleWallR.castShadow = true;
    scene.add(stairsHoleWallR);
    staircaseMeshes.push(stairsHoleWallR);
    
    // 3. Физическая П-образная лестница вниз (к baseY - 5.0)
    const stepWidth = 1.5;
    const stepHeight = 0.3125;
    const stepDepth = 0.625;
    const stepsCount = 8;
    
    // Левый пролет (вниз от baseY до Y = baseY - 2.5)
    for (let i = 0; i < stepsCount; i++) {
        const stepGeo = new THREE.BoxGeometry(stepWidth, stepHeight, stepDepth);
        const step = new THREE.Mesh(stepGeo, wallMat);
        step.position.set(-0.75, baseY - stepHeight * i - stepHeight / 2, -42.0 - stepDepth * i - stepDepth / 2);
        step.receiveShadow = true;
        scene.add(step);
        staircaseMeshes.push(step);
    }
    
    // Разворотная площадка на Y = baseY - 2.5
    const landing = new THREE.Mesh(new THREE.BoxGeometry(3.0, 0.2, 2.5), wallMat);
    landing.position.set(0, baseY - 2.5 - 0.1, -48.25);
    landing.receiveShadow = true;
    landing.castShadow = true;
    scene.add(landing);
    staircaseMeshes.push(landing);
    
    // Правый пролет (вниз от Y = baseY - 2.5 до Y = baseY - 5.0)
    for (let i = 0; i < stepsCount; i++) {
        const stepGeo = new THREE.BoxGeometry(stepWidth, stepHeight, stepDepth);
        const step = new THREE.Mesh(stepGeo, wallMat);
        step.position.set(0.75, baseY - 2.5 - stepHeight * i - stepHeight / 2, -47.0 + stepDepth * i + stepDepth / 2);
        step.receiveShadow = true;
        scene.add(step);
        staircaseMeshes.push(step);
    }
    
    // Разделитель между пролетами
    const partition = new THREE.Mesh(new THREE.BoxGeometry(0.1, 3.5, 5.0), wallMat);
    partition.position.set(0, baseY - 1.25, -44.5);
    partition.receiveShadow = true;
    partition.castShadow = true;
    scene.add(partition);
    staircaseMeshes.push(partition);
    
    // Стены лестничного колодца
    const shaftL = new THREE.Mesh(new THREE.BoxGeometry(0.2, 5.0, 7.5), wallMat);
    shaftL.position.set(-1.6, baseY - 2.5, -45.75);
    shaftL.receiveShadow = true;
    shaftL.castShadow = true;
    scene.add(shaftL);
    staircaseMeshes.push(shaftL);
    
    const shaftR = new THREE.Mesh(new THREE.BoxGeometry(0.2, 5.0, 7.5), wallMat);
    shaftR.position.set(1.6, baseY - 2.5, -45.75);
    shaftR.receiveShadow = true;
    shaftR.castShadow = true;
    scene.add(shaftR);
    staircaseMeshes.push(shaftR);
    
    const shaftB = new THREE.Mesh(new THREE.BoxGeometry(3.2, 5.0, 0.2), wallMat);
    shaftB.position.set(0, baseY - 2.5, -49.6);
    shaftB.receiveShadow = true;
    shaftB.castShadow = true;
    scene.add(shaftB);
    staircaseMeshes.push(shaftB);
    
    // Stairs blast doors at Z = -47.0
    const sdState = getOrGenerateStairsDoor(floorNum);
    const sdGroup = new THREE.Group();
    sdGroup.name = `stairsDoor_${floorNum}`;
    sdGroup.position.set(0, baseY - 2.5, -47.0);
    
    const sdPanelMat = new THREE.MeshStandardMaterial({
        map: proceduralTextures.stairsDoor,
        normalMap: proceduralTextures.stairsDoorNormal,
        roughness: 0.6,
        metalness: 0.8
    });
    
    const sdLeftMesh = new THREE.Mesh(new THREE.BoxGeometry(1.5, 5.0, 0.15), sdPanelMat);
    sdLeftMesh.name = "left_panel";
    sdLeftMesh.receiveShadow = true;
    sdLeftMesh.castShadow = true;
    sdGroup.add(sdLeftMesh);
    
    const sdRightMesh = new THREE.Mesh(new THREE.BoxGeometry(1.5, 5.0, 0.15), sdPanelMat);
    sdRightMesh.name = "right_panel";
    sdRightMesh.receiveShadow = true;
    sdRightMesh.castShadow = true;
    sdGroup.add(sdRightMesh);
    
    if (sdState.opened) {
        sdLeftMesh.position.set(-2.25, 2.5, 0); // slid open
        sdRightMesh.position.set(2.25, 2.5, 0);
    } else {
        sdLeftMesh.position.set(-0.75, 2.5, 0); // closed
        sdRightMesh.position.set(0.75, 2.5, 0);
    }
    
    // Door Frame details (outlines)
    const frameMat = new THREE.MeshStandardMaterial({
        map: proceduralTextures.rust,
        normalMap: proceduralTextures.rustNormal,
        roughness: 0.5,
        metalness: 0.8
    });
    const sdFrameTop = new THREE.Mesh(new THREE.BoxGeometry(3.2, 0.3, 0.3), frameMat);
    sdFrameTop.position.set(0, 4.85, 0);
    sdGroup.add(sdFrameTop);
    
    const sdFrameL = new THREE.Mesh(new THREE.BoxGeometry(0.3, 5.0, 0.3), frameMat);
    sdFrameL.position.set(-1.65, 2.5, 0);
    sdGroup.add(sdFrameL);
    
    const sdFrameR = new THREE.Mesh(new THREE.BoxGeometry(0.3, 5.0, 0.3), frameMat);
    sdFrameR.position.set(1.65, 2.5, 0);
    sdGroup.add(sdFrameR);
    
    scene.add(sdGroup);
    staircaseMeshes.push(sdGroup);
    
    // 4. Потолочные трубы
    const pipeMat = new THREE.MeshStandardMaterial({ 
        map: proceduralTextures.rust, 
        normalMap: proceduralTextures.rustNormal, 
        metalness: 0.8, 
        roughness: 0.3 
    });
    const pipeGeo = new THREE.CylinderGeometry(0.12, 0.12, 42, 8);
    
    const pipeL = new THREE.Mesh(pipeGeo, pipeMat);
    pipeL.rotation.x = Math.PI / 2;
    pipeL.position.set(-2.2, baseY + 4.4, -21);
    scene.add(pipeL);
    ceilingPipes.push(pipeL);
    
    const pipeR = new THREE.Mesh(pipeGeo, pipeMat);
    pipeR.rotation.x = Math.PI / 2;
    pipeR.position.set(2.2, baseY + 4.4, -21);
    scene.add(pipeR);
    ceilingPipes.push(pipeR);
    
    // 5. Освещение (PointLight тени ОТКЛЮЧЕНЫ во избежание лагов)
    const lightGeo = new THREE.BoxGeometry(0.8, 0.1, 1.4);
    const lightEmissiveMat = new THREE.MeshBasicMaterial({ color: 0xccffcc });
    const zLights = [-2, -10, -22, -34, -44];
    zLights.forEach(z => {
        const lamp = new THREE.Mesh(lightGeo, lightEmissiveMat);
        lamp.position.set(0, baseY + 4.95, z);
        scene.add(lamp);
        ceilingLights.push(lamp);
        
        if (Math.abs(floorNum - state.floor) <= 1) {
            const pl = new THREE.PointLight(0xd5ffd0, 0.65, 16);
            pl.position.set(0, baseY + 4.5, z);
            pl.castShadow = false;
            scene.add(pl);
            ceilingLights.push(pl);
        }
    });
    
    // Сигнальный маяк Самосбора на Z = -38
    const beacon = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.3, 8), new THREE.MeshBasicMaterial({ color: 0x440000 }));
    beacon.position.set(0, baseY + 4.8, -38);
    scene.add(beacon);
    warningBeacons.push(beacon);
    
    if (Math.abs(floorNum - state.floor) <= 1) {
        const wl = new THREE.PointLight(0xff0000, 0, 15);
        wl.position.set(0, baseY + 4.4, -38);
        wl.castShadow = false;
        scene.add(wl);
        warningLights.push(wl);
    }
    
    // 6. Двери и интерьеры комнат
    const doorGeo = new THREE.BoxGeometry(1.2, 2.6, 0.1);
    const doorMat = new THREE.MeshStandardMaterial({ 
        map: proceduralTextures.door, 
        normalMap: proceduralTextures.doorNormal, 
        roughness: 0.5 
    });
    const roomWallMat = new THREE.MeshStandardMaterial({ 
        map: proceduralTextures.wallpaper, 
        normalMap: proceduralTextures.wallpaperNormal, 
        roughness: 0.8, 
        side: THREE.DoubleSide 
    });
    const roomFloorMat = new THREE.MeshStandardMaterial({ 
        map: proceduralTextures.concrete, 
        normalMap: proceduralTextures.concreteNormal, 
        roughness: 0.9, 
        side: THREE.DoubleSide 
    });
    const transWallMat = new THREE.MeshStandardMaterial({ 
        map: proceduralTextures.rust, 
        normalMap: proceduralTextures.rustNormal, 
        roughness: 0.7, 
        side: THREE.DoubleSide 
    });
    const roomCeilMat = new THREE.MeshStandardMaterial({ 
        map: proceduralTextures.ceiling, 
        normalMap: proceduralTextures.ceilingNormal, 
        roughness: 0.95, 
        side: THREE.DoubleSide 
    });
    
    const floorDoors = getOrGenerateFloorDoors(floorNum);
    
    DOOR_LAYOUT.forEach((layout, idx) => {
        const doorObj = floorDoors[idx];
        
        const doorPivot = new THREE.Group();
        // Размещаем петлю двери сбоку проема для правильной стыковки и анимации
        const zPivot = layout.x < 0 ? layout.z + 0.6 : layout.z - 0.6;
        doorPivot.position.set(layout.x, baseY + 1.3, zPivot);
        doorPivot.rotation.y = layout.rot;
        doorPivot.userData = { floor: floorNum, doorIndex: idx };
        
        const doorMesh = new THREE.Mesh(doorGeo, doorMat);
        doorMesh.name = `door_${idx}`;
        doorMesh.position.set(0.6, 0, 0); // Смещение от петли
        doorMesh.userData = { doorIndex: idx };
        doorMesh.castShadow = true;
        doorMesh.receiveShadow = true;
        
        // Add volumetric handles to both sides of the door
        addVolumetricHandle(doorMesh);
        
        doorPivot.add(doorMesh);
        
        if (doorObj && doorObj.opened) {
            doorPivot.rotation.y = layout.rot + Math.PI / 2;
        }
        
        scene.add(doorPivot);
        doorPivots.push(doorPivot);
        
        if (doorObj) {
            const roomGroup = new THREE.Group();
            const isLeft = layout.x < 0;
            const dirX = isLeft ? -1 : 1;
            
            if (doorObj.type === 'apartment') {
                // Сдвиг комнат глубже наружу, чтобы предотвратить пересечения со стенами коридора
                const roomCenterX = layout.x + (3.7 * dirX);
                const roomCenterZ = layout.z;
                const wallOffsetX = layout.x + (0.3 * dirX);
                const backWallX = layout.x + (7.1 * dirX);
                
                const rFloor = new THREE.Mesh(new THREE.BoxGeometry(7.0, 0.1, 7.0), roomFloorMat);
                rFloor.position.set(roomCenterX, baseY - 0.05, roomCenterZ);
                rFloor.receiveShadow = true;
                roomGroup.add(rFloor);
                
                const rCeil = new THREE.Mesh(new THREE.BoxGeometry(7.0, 0.1, 7.0), roomCeilMat);
                rCeil.position.set(roomCenterX, baseY + 5.0 + 0.05, roomCenterZ);
                rCeil.receiveShadow = true;
                roomGroup.add(rCeil);
                
                const rBackWall = new THREE.Mesh(new THREE.BoxGeometry(0.2, 5.0, 7.0), roomWallMat);
                rBackWall.position.set(backWallX, baseY + 2.5, roomCenterZ);
                rBackWall.castShadow = true;
                rBackWall.receiveShadow = true;
                roomGroup.add(rBackWall);
                
                const rSideWall1 = new THREE.Mesh(new THREE.BoxGeometry(7.0, 5.0, 0.2), roomWallMat);
                rSideWall1.position.set(roomCenterX, baseY + 2.5, roomCenterZ - 3.5 - 0.1);
                rSideWall1.castShadow = true;
                rSideWall1.receiveShadow = true;
                roomGroup.add(rSideWall1);
                
                const rSideWall2 = new THREE.Mesh(new THREE.BoxGeometry(7.0, 5.0, 0.2), roomWallMat);
                rSideWall2.position.set(roomCenterX, baseY + 2.5, roomCenterZ + 3.5 + 0.1);
                rSideWall2.castShadow = true;
                rSideWall2.receiveShadow = true;
                roomGroup.add(rSideWall2);
                
                const rFrontWall1 = new THREE.Mesh(new THREE.BoxGeometry(0.2, 5.0, 2.9), roomWallMat);
                rFrontWall1.position.set(wallOffsetX, baseY + 2.5, roomCenterZ - 2.05);
                rFrontWall1.castShadow = true;
                rFrontWall1.receiveShadow = true;
                roomGroup.add(rFrontWall1);
                
                const rFrontWall2 = new THREE.Mesh(new THREE.BoxGeometry(0.2, 5.0, 2.9), roomWallMat);
                rFrontWall2.position.set(wallOffsetX, baseY + 2.5, roomCenterZ + 2.05);
                rFrontWall2.castShadow = true;
                rFrontWall2.receiveShadow = true;
                roomGroup.add(rFrontWall2);
                
                const rFrontWallTop = new THREE.Mesh(new THREE.BoxGeometry(0.2, 2.4, 1.2), roomWallMat);
                rFrontWallTop.position.set(wallOffsetX, baseY + 3.8, roomCenterZ);
                rFrontWallTop.castShadow = true;
                rFrontWallTop.receiveShadow = true;
                roomGroup.add(rFrontWallTop);
                
                const cab = createDetailedCabinet(dirX);
                cab.position.set(layout.x + (5.5 * dirX), baseY, roomCenterZ - 2.0);
                roomGroup.add(cab);
                
                const table = createDetailedTable();
                table.position.set(roomCenterX, baseY, roomCenterZ);
                roomGroup.add(table);
                
                if (Math.abs(floorNum - state.floor) <= 1) {
                    const roomLight = new THREE.PointLight(0xffeedd, doorObj.opened ? 0.3 : 0, 8);
                    roomLight.position.set(roomCenterX, baseY + 4, roomCenterZ);
                    roomLight.castShadow = false;
                    roomGroup.add(roomLight);
                    doorLights[floorNum + '_' + idx] = roomLight;
                }
                
            } else if (doorObj.type === 'transition') {
                const roomCenterX = layout.x + (2.7 * dirX);
                const roomCenterZ = layout.z;
                const wallOffsetX = layout.x + (0.3 * dirX);
                const backWallX = layout.x + (5.1 * dirX);
                
                const rFloor = new THREE.Mesh(new THREE.BoxGeometry(5.0, 0.1, 5.0), transWallMat);
                rFloor.position.set(roomCenterX, baseY - 0.05, roomCenterZ);
                rFloor.receiveShadow = true;
                roomGroup.add(rFloor);
                
                const rCeil = new THREE.Mesh(new THREE.BoxGeometry(5.0, 0.1, 5.0), transWallMat);
                rCeil.position.set(roomCenterX, baseY + 5.0 + 0.05, roomCenterZ);
                rCeil.receiveShadow = true;
                roomGroup.add(rCeil);
                
                const rBackWall = new THREE.Mesh(new THREE.BoxGeometry(0.2, 5.0, 5.0), transWallMat);
                rBackWall.position.set(layout.x + (5.0 * dirX) + (0.1 * dirX), baseY + 2.5, roomCenterZ);
                rBackWall.castShadow = true;
                rBackWall.receiveShadow = true;
                roomGroup.add(rBackWall);
                
                const rSideWall1 = new THREE.Mesh(new THREE.BoxGeometry(5.0, 5.0, 0.2), transWallMat);
                rSideWall1.position.set(roomCenterX, baseY + 2.5, roomCenterZ - 2.5 - 0.1);
                rSideWall1.castShadow = true;
                rSideWall1.receiveShadow = true;
                roomGroup.add(rSideWall1);
                
                const rSideWall2 = new THREE.Mesh(new THREE.BoxGeometry(5.0, 5.0, 0.2), transWallMat);
                rSideWall2.position.set(roomCenterX, baseY + 2.5, roomCenterZ + 2.5 + 0.1);
                rSideWall2.castShadow = true;
                rSideWall2.receiveShadow = true;
                roomGroup.add(rSideWall2);
                
                const rFrontWall1 = new THREE.Mesh(new THREE.BoxGeometry(0.2, 5.0, 1.9), transWallMat);
                rFrontWall1.position.set(wallOffsetX, baseY + 2.5, roomCenterZ - 1.55);
                rFrontWall1.castShadow = true;
                rFrontWall1.receiveShadow = true;
                roomGroup.add(rFrontWall1);
                
                const rFrontWall2 = new THREE.Mesh(new THREE.BoxGeometry(0.2, 5.0, 1.9), transWallMat);
                rFrontWall2.position.set(wallOffsetX, baseY + 2.5, roomCenterZ + 1.55);
                rFrontWall2.castShadow = true;
                rFrontWall2.receiveShadow = true;
                roomGroup.add(rFrontWall2);
                
                const rFrontWallTop = new THREE.Mesh(new THREE.BoxGeometry(0.2, 2.4, 1.2), transWallMat);
                rFrontWallTop.position.set(wallOffsetX, baseY + 3.8, roomCenterZ);
                rFrontWallTop.castShadow = true;
                rFrontWallTop.receiveShadow = true;
                roomGroup.add(rFrontWallTop);
                
                const panel = createDetailedPanel(dirX);
                panel.position.set(layout.x + (4.5 * dirX), baseY, roomCenterZ);
                roomGroup.add(panel);
                
                if (Math.abs(floorNum - state.floor) <= 1) {
                    const transLight = new THREE.PointLight(0x00aaff, doorObj.opened ? 0.5 : 0, 6);
                    transLight.position.set(roomCenterX, baseY + 4, roomCenterZ);
                    transLight.castShadow = (floorNum === state.floor);
                    roomGroup.add(transLight);
                    doorLights[floorNum + '_' + idx] = transLight;
                }
                
            } else {
                const blankWall = new THREE.Mesh(new THREE.BoxGeometry(0.2, 5.0, 1.2), wallMat);
                blankWall.position.set(layout.x + (0.5 * dirX), baseY + 2.5, layout.z);
                blankWall.castShadow = true;
                blankWall.receiveShadow = true;
                roomGroup.add(blankWall);
            }
            
            scene.add(roomGroup);
            roomMeshes.push(roomGroup);
        }
    });
}

function spawn3DMonster() {
    if (stairsMonsterMesh) scene.remove(stairsMonsterMesh);
    
    stairsMonsterMesh = new THREE.Group();
    // Ставим монстра на верхнюю часть лестницы
    stairsMonsterMesh.position.set(-0.75, 0, -42.0);
    
    const bodyMat = new THREE.MeshBasicMaterial({ color: 0x050505 });
    const eyeMat = new THREE.MeshBasicMaterial({ color: 0xff0033 });
    
    const bodyGeo = new THREE.SphereGeometry(1.1, 16, 16);
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    stairsMonsterMesh.add(body);
    
    const limbGeo = new THREE.CylinderGeometry(0.1, 0.03, 3.0, 6);
    for (let i = 0; i < 8; i++) {
        const limb = new THREE.Mesh(limbGeo, bodyMat);
        limb.rotation.x = Math.random() * Math.PI * 2;
        limb.rotation.y = Math.random() * Math.PI * 2;
        limb.rotation.z = Math.random() * Math.PI * 2;
        limb.translateY(1.5);
        stairsMonsterMesh.add(limb);
    }
    
    const eyeGeo = new THREE.SphereGeometry(0.08, 8, 8);
    const eyePositions = [
        [0.4, 0.5, 1.0], [-0.5, 0.3, 1.0], [0.1, 0.7, 0.9],
        [-0.2, 0.6, 1.1], [0.3, 0.2, 1.1]
    ];
    
    eyePositions.forEach(pos => {
        const eye = new THREE.Mesh(eyeGeo, eyeMat);
        eye.position.set(pos[0], pos[1], pos[2]);
        stairsMonsterMesh.add(eye);
    });
    
    scene.add(stairsMonsterMesh);
}

// --- СОЗДАНИЕ И СПАВН ТВАРЕЙ И АНОМАЛИЙ ---
function createCrawlerMesh() {
    const group = new THREE.Group();
    group.name = "crawler";
    
    // Тело: темная слизистая биомасса
    const bodyMat = new THREE.MeshStandardMaterial({
        color: 0x181216,
        roughness: 0.9,
        metalness: 0.1
    });
    
    const body = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.22, 0.7), bodyMat);
    body.position.y = 0.11;
    body.receiveShadow = true;
    body.castShadow = true;
    group.add(body);
    
    // Голова
    const head = new THREE.Mesh(new THREE.SphereGeometry(0.18, 8, 8), bodyMat);
    head.position.set(0, 0.16, -0.35);
    group.add(head);
    
    // Красные светящиеся глаза
    const eyeMat = new THREE.MeshBasicMaterial({ color: 0xff0000 });
    const leftEye = new THREE.Mesh(new THREE.SphereGeometry(0.04, 4, 4), eyeMat);
    leftEye.position.set(-0.07, 0.20, -0.5);
    group.add(leftEye);
    
    const rightEye = new THREE.Mesh(new THREE.SphereGeometry(0.04, 4, 4), eyeMat);
    rightEye.position.set(0.07, 0.20, -0.5);
    group.add(rightEye);
    
    // 6 шевелящихся ножек
    for (let i = 0; i < 6; i++) {
        const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.35), bodyMat);
        const side = (i % 2 === 0) ? -1 : 1;
        const zOffset = -0.2 + Math.floor(i / 2) * 0.2;
        leg.rotation.z = side * Math.PI / 4;
        leg.rotation.y = -side * Math.PI / 8;
        leg.position.set(side * 0.3, 0.08, zOffset);
        group.add(leg);
    }
    
    return group;
}

function spawnHallwayCrawler(zPos, xPos = 0) {
    if (hallwayCrawlerMesh) {
        scene.remove(hallwayCrawlerMesh);
        hallwayCrawlerMesh = null;
    }
    
    crawlerHealth = 2;
    hallwayCrawlerMesh = createCrawlerMesh();
    hallwayCrawlerMesh.position.set(xPos, 0, zPos);
    scene.add(hallwayCrawlerMesh);
    
    logToConsole("Вы слышите жуткий, шуршащий звук когтей по бетону откуда-то впереди...", "warn");
    playScaryScreechSound();
}

function playScaryScreechSound() {
    initAudio();
    if (!audioCtx) return;
    const now = audioCtx.currentTime;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(320, now);
    osc.frequency.linearRampToValueAtTime(750, now + 0.15);
    osc.frequency.exponentialRampToValueAtTime(110, now + 0.4);
    
    gain.gain.setValueAtTime(0.08, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.45);
    
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start(now);
    osc.stop(now + 0.5);
}

function playSoundDamage() {
    initAudio();
    if (!audioCtx) return;
    const now = audioCtx.currentTime;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(160, now);
    osc.frequency.linearRampToValueAtTime(70, now + 0.25);
    
    gain.gain.setValueAtTime(0.12, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
    
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start(now);
    osc.stop(now + 0.35);
}

function playSoundSwitch() {
    initAudio();
    if (!audioCtx) return;
    const now = audioCtx.currentTime;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    
    osc.type = 'sine';
    osc.frequency.setValueAtTime(600, now);
    osc.frequency.setValueAtTime(300, now + 0.05);
    
    gain.gain.setValueAtTime(0.015, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
    
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start(now);
    osc.stop(now + 0.15);
}

function spawnDeadLiquidatorMesh() {
    if (deadLiquidatorMesh) {
        scene.remove(deadLiquidatorMesh);
        deadLiquidatorMesh = null;
    }
    
    deadLiquidatorMesh = new THREE.Group();
    deadLiquidatorMesh.name = "dead_liquidator";
    deadLiquidatorMesh.position.set(0, 0.08, -18.0);
    
    // Оранжевый защитный костюм
    const suitMat = new THREE.MeshStandardMaterial({ color: 0xd35400, roughness: 0.9 });
    const bootMat = new THREE.MeshStandardMaterial({ color: 0x111111, roughness: 0.8 });
    const metalMat = new THREE.MeshStandardMaterial({ color: 0x7f8c8d, metalness: 0.8, roughness: 0.3 });
    
    const body = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.15, 1.2), suitMat);
    body.receiveShadow = true;
    body.castShadow = true;
    deadLiquidatorMesh.add(body);
    
    // Шлем
    const helmet = new THREE.Mesh(new THREE.SphereGeometry(0.16, 8, 8), metalMat);
    helmet.position.set(0, 0.08, -0.75);
    deadLiquidatorMesh.add(helmet);
    
    // Сапоги
    const leftBoot = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.15, 0.22), bootMat);
    leftBoot.position.set(-0.16, 0, 0.7);
    deadLiquidatorMesh.add(leftBoot);
    
    const rightBoot = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.15, 0.22), bootMat);
    rightBoot.position.set(0.16, 0, 0.7);
    deadLiquidatorMesh.add(rightBoot);
    
    scene.add(deadLiquidatorMesh);
}

function spawnGhostMesh() {
    if (ghostMesh) {
        scene.remove(ghostMesh);
        ghostMesh = null;
    }
    
    ghostMesh = new THREE.Group();
    ghostMesh.name = "ghost";
    ghostMesh.position.set(0, 1.2, -28.0);
    
    const ghostMat = new THREE.MeshBasicMaterial({ 
        color: 0x88d8ff, 
        transparent: true, 
        opacity: 0.25,
        wireframe: true 
    });
    
    const head = new THREE.Mesh(new THREE.SphereGeometry(0.32, 12, 12), ghostMat);
    ghostMesh.add(head);
    
    const body = new THREE.Mesh(new THREE.ConeGeometry(0.35, 1.4, 12, 1, true), ghostMat);
    body.position.y = -0.7;
    body.rotation.x = Math.PI;
    ghostMesh.add(body);
    
    scene.add(ghostMesh);
}

// Цикл рендеринга и управления в 3D (FPS сглаживание)
let animFrameId = null;
let lastTime = performance.now();

function animate3D() {
    animFrameId = requestAnimationFrame(animate3D);
    
    // Optimization: Skip updating and rendering if the game interface is inactive
    const mainInterface = document.getElementById('main-interface');
    if (!mainInterface || mainInterface.classList.contains('screen-inactive')) {
        return;
    }
    
    const time = performance.now();
    const deltaTime = Math.min((time - lastTime) * 0.001, 0.1); // Лимит на лаг в 100мс
    lastTime = time;
    
    if (isGamePaused) {
        if (renderer && scene && camera) {
            renderer.render(scene, camera);
        }
        return;
    }
    
    // 1. ОБРАБОТКА ДВИЖЕНИЯ ИГРОКА (WASD)
    if (state.location !== 'room' || !state.isSearching) {
        handleFPSMovement(deltaTime);
    }
    
    // 2. ОБНОВЛЕНИЕ КАМЕРЫ (ПОЛОЖЕНИЕ И РОТАЦИЯ)
    camera.rotation.set(0, 0, 0);
    camera.rotation.y = playerYaw;
    camera.rotation.x = playerPitch;
    
    // Встряска камеры от Самосбора
    let shakeX = 0, shakeY = 0;
    if (state.samosborStatus === 'warning') {
        shakeX = (Math.random() - 0.5) * 0.02;
        shakeY = (Math.random() - 0.5) * 0.02;
    } else if (state.samosborStatus === 'active') {
        shakeX = (Math.random() - 0.5) * 0.06;
        shakeY = (Math.random() - 0.5) * 0.06;
    }
    
    // Камера располагается на высоте глаз (1.8 от уровня ног игрока)
    camera.position.set(playerPos.x + shakeX, playerPos.y + 1.8 + shakeY, playerPos.z);
    
    // 3. РЕЙКАСТИНГ (ПОИСК ДВЕРЕЙ В ЦЕНТРЕ ЭКРАНА)
    if (state.location === 'hallway' && !state.stairsMonsterActive) {
        performInteractionRaycast();
    }
    
    // 4. ДВИЖЕНИЕ МОНСТРА НА ЛЕСТНИЦЕ
    if (state.stairsMonsterActive && stairsMonsterMesh) {
        // Тряска чудовища
        stairsMonsterMesh.position.x += (Math.random() - 0.5) * 0.05;
        // Движение к камере игрока
        stairsMonsterMesh.position.z -= 1.8 * deltaTime;
        stairsMonsterMesh.position.y = getStepsY(stairsMonsterMesh.position.x, stairsMonsterMesh.position.y, stairsMonsterMesh.position.z);
        
        // Если монстр подошел слишком близко (к Z координате игрока) - смерть
        if (stairsMonsterMesh.position.z <= playerPos.z + 2.0) {
            triggerGameOver("stairs_monster");
        }
    }
    
    // 5. АНИМАЦИЯ АВАРИЙНОЙ ЛАМПЫ САМОСБОРА
    if (warningLights.length > 0) {
        const timeSec = time * 0.001;
        if (state.samosborStatus === 'warning') {
            const pulse = (Math.sin(timeSec * 7) + 1) * 0.5;
            warningLights.forEach(wl => {
                wl.intensity = pulse * 1.5;
                wl.color.setHex(0xffaa00);
            });
            warningBeacons.forEach(wb => {
                wb.material.color.setHex(pulse > 0.5 ? 0xffaa00 : 0x442200);
            });
        } else if (state.samosborStatus === 'active') {
            const flash = (Math.floor(timeSec * 8) % 2 === 0) ? 1 : 0;
            warningLights.forEach(wl => {
                wl.intensity = flash * 3.0;
                wl.color.setHex(0xff0000);
            });
            warningBeacons.forEach(wb => {
                wb.material.color.setHex(flash === 1 ? 0xff0000 : 0x550000);
            });
            
            scene.fog.color.setHex(0x180522);
            renderer.setClearColor(0x180522);
        } else {
            warningLights.forEach(wl => {
                wl.intensity = 0;
            });
            warningBeacons.forEach(wb => {
                wb.material.color.setHex(0x330000);
            });
            if (scene.fog.color.getHex() !== 0x060709) {
                scene.fog.color.setHex(0x060709);
                renderer.setClearColor(0x060709);
            }
        }
    }
    
    // Эффект мерцания света при событии flicker
    if (state.floorEvent === 'flicker' && !isGamePaused) {
        const time = Date.now();
        const flicker = Math.sin(time * 0.05) * Math.cos(time * 0.02);
        const lightsOff = flicker > 0.35 || (Math.random() < 0.08 && (time % 500 < 100));
        
        ceilingLights.forEach(light => {
            light.intensity = lightsOff ? 0 : 1.2;
        });
    }
    
    // Плавное парение призрака
    if (ghostMesh && !isGamePaused) {
        ghostMesh.position.y = 1.2 + Math.sin(Date.now() * 0.003) * 0.12;
    }
    
    // Движение и атака ползающей твари в коридоре
    if (hallwayCrawlerMesh && !isGamePaused) {
        const targetZ = state.location === 'hallway' ? playerPos.z : 0.0;
        const targetX = state.location === 'hallway' ? playerPos.x : 0.0;
        
        const dx = targetX - hallwayCrawlerMesh.position.x;
        const dz = targetZ - hallwayCrawlerMesh.position.z;
        const dist = Math.sqrt(dx * dx + dz * dz);
        
        if (dist > 0.5) {
            const speed = 0.04;
            hallwayCrawlerMesh.position.x += (dx / dist) * speed;
            hallwayCrawlerMesh.position.z += (dz / dist) * speed;
            
            // Анимация шевеления лапок
            const t = Date.now() * 0.015;
            hallwayCrawlerMesh.children.forEach(child => {
                if (child.geometry && child.geometry.type === "CylinderGeometry") {
                    child.rotation.x = Math.sin(t) * 0.25;
                }
            });
        }
        
        // Атака при приближении к игроку
        const distToPlayer = playerPos.distanceTo(hallwayCrawlerMesh.position);
        if (distToPlayer < 1.3) {
            logToConsole("ТВАРЬ НАПАЛА НА ВАС! Своими жвалами она прокусила вам скафандр!", "danger");
            state.health = Math.max(0, state.health - 25);
            playSoundDamage();
            scene.remove(hallwayCrawlerMesh);
            hallwayCrawlerMesh = null;
            
            if (state.health <= 0) {
                triggerGameOver("stairs_monster");
            }
            updateHUD();
        }
    }

    // Рендер кадра
    if (renderer && scene && camera) {
        renderer.render(scene, camera);
    }
}

// Управление физическим движением игрока (координатная сетка с коллизиями)
function handleFPSMovement(deltaTime) {
    if (state.stairsMonsterActive || hackActive) return; // Locked when monster attacks or hacking
    
    const prevX = playerPos.x;
    const prevZ = playerPos.z;
    
    const moveVector = new THREE.Vector3();
    
    // Get custom keybindings
    const bindFwd = state.keyBindings['MoveForward'] || 'KeyW';
    const bindBwd = state.keyBindings['MoveBackward'] || 'KeyS';
    const bindLft = state.keyBindings['MoveLeft'] || 'KeyA';
    const bindRgt = state.keyBindings['MoveRight'] || 'KeyD';
    const bindSprint = state.keyBindings['Sprint'] || 'ShiftLeft';
    
    // Считываем WASD / Стрелки клавиатуры или виртуальные кнопки D-pad
    if (keys[bindFwd] || keys['ArrowUp'] || mvUp) moveVector.z -= 1;
    if (keys[bindBwd] || keys['ArrowDown'] || mvDown) moveVector.z += 1;
    if (keys[bindLft] || keys['ArrowLeft'] || mvLeft) moveVector.x -= 1;
    if (keys[bindRgt] || keys['ArrowRight'] || mvRight) moveVector.x += 1;
    
    let currentSpeed = playerSpeed;
    let isSprinting = keys[bindSprint] || keys['ShiftLeft'] || keys['ShiftRight'];
    
    if (isSprinting && moveVector.lengthSq() > 0 && state.stamina > 0) {
        currentSpeed = 6.5;
        state.stamina = Math.max(0, state.stamina - 30 * deltaTime);
    } else {
        if (moveVector.lengthSq() > 0) {
            state.stamina = Math.min(100, state.stamina + 15 * deltaTime);
        } else {
            state.stamina = Math.min(100, state.stamina + 25 * deltaTime);
        }
    }
    
    if (moveVector.lengthSq() > 0) {
        // Переводим вектор движения относительно взгляда игрока (yaw)
        moveVector.normalize();
        moveVector.applyAxisAngle(new THREE.Vector3(0, 1, 0), playerYaw);
        
        // Умножаем на скорость
        const finalSpeed = window._customSpeed || currentSpeed;
        moveVector.multiplyScalar(finalSpeed * deltaTime);
        
        // Новые предлагаемые координаты
        const nextX = playerPos.x + moveVector.x;
        const nextZ = playerPos.z + moveVector.z;
        
        // Обработка границ и коллизий (Бесшовный мир)
        // 1. Коридор и Лестница
        if (nextZ < -42) {
            // Лестничная шахта
            let allowed = false;
            
            // Проверка границ в лестничной шахте
            if (nextZ >= -49.5) {
                if (nextZ >= -47.0) {
                    // Коридоры лестниц
                    if (playerPos.x < 0) {
                        // Левая лестница
                        if (nextX >= -1.4 && nextX <= -0.1) {
                            allowed = true;
                        }
                    } else {
                        // Правая лестница
                        if (nextX >= 0.1 && nextX <= 1.4) {
                            allowed = true;
                        }
                    }
                } else {
                    // Разворотная площадка
                    if (nextX >= -1.4 && nextX <= 1.4) {
                        allowed = true;
                    }
                }
            }
            
            if (allowed) {
                // Stairs doors collision check at Z = -47.0
                const sdState = getOrGenerateStairsDoor(state.floor);
                let finalNextZ = nextZ;
                if (!sdState.opened) {
                    if (playerPos.z >= -47.0 && nextZ < -47.0) {
                        finalNextZ = -46.95;
                    } else if (playerPos.z < -47.0 && nextZ >= -47.0) {
                        finalNextZ = -47.05;
                    }
                }
                
                playerPos.x = nextX;
                playerPos.z = finalNextZ;
                
                // Вычисляем высоту
                playerPos.y = getStepsY(playerPos.x, playerPos.y, playerPos.z);
                
                // Смена этажей по высоте Y
                if (playerPos.y < -4.7) {
                    state.floor = state.floor - 1;
                    playerPos.y += 5.0;
                    
                    if (state.floor < END_FLOOR) { // Allow floor 1
                        triggerGameOver("ending_2");
                        return;
                    }
                    
                    if (Math.random() < 0.1 && !state.stairsMonsterActive) {
                        triggerStairsMonster();
                    } else {
                        logToConsole(`Вы спустились на этаж ${state.floor}.`, "sys");
                    }
                    
                    build3DScene();
                    updateHUD();
                } else if (playerPos.y > 4.7) {
                    if (state.floor >= state.spawnFloor) {
                        // Clamp floor ascension
                        playerPos.y = 4.7;
                        logToConsole("Верхние этажи заблокированы гермозатвором. Прохода нет.", "warn");
                    } else {
                        state.floor = state.floor + 1;
                        playerPos.y -= 5.0;
                        
                        logToConsole(`Вы поднялись на этаж ${state.floor}.`, "sys");
                        
                        build3DScene();
                        updateHUD();
                    }
                }
                
                if (state.location !== 'hallway') {
                    state.location = 'hallway';
                    updateHUD();
                }
            }
        } else if (nextZ > 0.5) {
            // Задний тупик
            playerPos.z = 0.5;
        } else {
            // КОРИДОР И КОМНАТЫ (Z от 0 до -42) — AABB Collision System
            playerPos.y = 0; // На этаже
            
            // Build AABB colliders for walls and doors
            const colliders = [];
            const PR = 0.3; // Player radius
            
            // Corridor walls (left and right) — segments between doors
            // Left wall
            colliders.push({ minX: -3.2, maxX: -2.9, minZ: -9.4, maxZ: 0.0 });
            colliders.push({ minX: -3.2, maxX: -2.9, minZ: -21.4, maxZ: -10.6 });
            colliders.push({ minX: -3.2, maxX: -2.9, minZ: -33.4, maxZ: -22.6 });
            colliders.push({ minX: -3.2, maxX: -2.9, minZ: -42.0, maxZ: -34.6 });
            // Right wall
            colliders.push({ minX: 2.9, maxX: 3.2, minZ: -9.4, maxZ: 0.0 });
            colliders.push({ minX: 2.9, maxX: 3.2, minZ: -21.4, maxZ: -10.6 });
            colliders.push({ minX: 2.9, maxX: 3.2, minZ: -33.4, maxZ: -22.6 });
            colliders.push({ minX: 2.9, maxX: 3.2, minZ: -42.0, maxZ: -34.6 });
            // Back wall (spawn end)
            colliders.push({ minX: -3.2, maxX: 3.2, minZ: 0.0, maxZ: 0.3 });
            
            // Door and room colliders
            DOOR_LAYOUT.forEach((layout, idx) => {
                const doorObj = state.doors[idx];
                if (!doorObj) return;
                
                const isLeft = layout.x < 0;
                
                // Closed door or empty slot — block the doorway
                if (!doorObj.opened || doorObj.type === 'empty') {
                    if (isLeft) {
                        colliders.push({ minX: -3.2, maxX: -2.9, minZ: layout.z - 0.6, maxZ: layout.z + 0.6 });
                    } else {
                        colliders.push({ minX: 2.9, maxX: 3.2, minZ: layout.z - 0.6, maxZ: layout.z + 0.6 });
                    }
                }
                
                // Room walls (if door exists and is not empty)
                if (doorObj.type !== 'empty') {
                    const roomWidth = doorObj.type === 'apartment' ? 3.5 : (doorObj.type === 'monster' ? 4.0 : 2.5);
                    const roomDepth = doorObj.type === 'apartment' ? 7.0 : 5.0;
                    const dirX = isLeft ? -1 : 1;
                    
                    const backWallX = layout.x + roomDepth * dirX;
                    const zMin = layout.z - roomWidth;
                    const zMax = layout.z + roomWidth;
                    
                    // Back wall of room
                    colliders.push({ minX: backWallX - 0.15, maxX: backWallX + 0.15, minZ: zMin, maxZ: zMax });
                    
                    // Side walls of room
                    colliders.push({ minX: Math.min(layout.x, backWallX), maxX: Math.max(layout.x, backWallX), minZ: zMin - 0.15, maxZ: zMin + 0.15 });
                    colliders.push({ minX: Math.min(layout.x, backWallX), maxX: Math.max(layout.x, backWallX), minZ: zMax - 0.15, maxZ: zMax + 0.15 });
                    
                    // Front wall segments (around doorway)
                    const frontDoorHalf = 0.6;
                    if (isLeft) {
                        colliders.push({ minX: -3.2, maxX: -2.9, minZ: zMin, maxZ: layout.z - frontDoorHalf });
                        colliders.push({ minX: -3.2, maxX: -2.9, minZ: layout.z + frontDoorHalf, maxZ: zMax });
                    } else {
                        colliders.push({ minX: 2.9, maxX: 3.2, minZ: zMin, maxZ: layout.z - frontDoorHalf });
                        colliders.push({ minX: 2.9, maxX: 3.2, minZ: layout.z + frontDoorHalf, maxZ: zMax });
                    }
                    
                    // Furniture colliders inside rooms
                    if (doorObj.type === 'apartment') {
                        const cabX = layout.x + 5.5 * dirX;
                        const cabZ = layout.z - 2.0;
                        colliders.push({ minX: cabX - 1.0, maxX: cabX + 1.0, minZ: cabZ - 0.5, maxZ: cabZ + 0.5 });
                        
                        const tableX = layout.x + 3.7 * dirX;
                        const tableZ = layout.z;
                        colliders.push({ minX: tableX - 0.9, maxX: tableX + 0.9, minZ: tableZ - 0.6, maxZ: tableZ + 0.6 });
                    } else if (doorObj.type === 'transition') {
                        const panelX = layout.x + 4.5 * dirX;
                        colliders.push({ minX: panelX - 0.4, maxX: panelX + 0.4, minZ: layout.z - 0.8, maxZ: layout.z + 0.8 });
                    }
                }
            });
            
            // AABB vs circle collision check
            function checkAABBCollision(px, pz, radius) {
                for (const box of colliders) {
                    const closestX = Math.max(box.minX, Math.min(px, box.maxX));
                    const closestZ = Math.max(box.minZ, Math.min(pz, box.maxZ));
                    const distX = px - closestX;
                    const distZ = pz - closestZ;
                    if ((distX * distX + distZ * distZ) < (radius * radius)) {
                        return true;
                    }
                }
                return false;
            }
            
            // Try X movement independently
            if (!checkAABBCollision(nextX, playerPos.z, PR)) {
                playerPos.x = nextX;
            }
            // Try Z movement independently
            if (!checkAABBCollision(playerPos.x, nextZ, PR)) {
                playerPos.z = nextZ;
            }
            
            // Determine location (hallway vs room)
            let insideRoomIdx = -1;
            DOOR_LAYOUT.forEach((layout, idx) => {
                const doorObj = state.doors[idx];
                if (!doorObj || doorObj.type === 'empty') return;
                
                const isLeft = layout.x < 0;
                const roomWidth = doorObj.type === 'apartment' ? 3.5 : (doorObj.type === 'monster' ? 4.0 : 2.5);
                const roomDepth = doorObj.type === 'apartment' ? 7.0 : 5.0;
                const dirX = isLeft ? -1 : 1;
                const backWallX = layout.x + roomDepth * dirX;
                
                const pxInRoom = isLeft ? 
                    (playerPos.x <= layout.x && playerPos.x >= backWallX) :
                    (playerPos.x >= layout.x && playerPos.x <= backWallX);
                const pzInRoom = (playerPos.z >= layout.z - roomWidth && playerPos.z <= layout.z + roomWidth);
                
                if (pxInRoom && pzInRoom) {
                    insideRoomIdx = idx;
                }
            });
            
            if (insideRoomIdx >= 0) {
                const newLoc = state.doors[insideRoomIdx].type === 'apartment' ? 'room' : 
                               (state.doors[insideRoomIdx].type === 'transition' ? 'transition' : 'room');
                if (state.location !== newLoc || state.focusedDoorIndex !== insideRoomIdx) {
                    const oldLoc = state.location;
                    state.location = newLoc;
                    state.focusedDoorIndex = insideRoomIdx;
                    updateHUD();
                    
                    // Выводим описание атмосферы при входе в новую комнату
                    if (newLoc === 'room' && oldLoc === 'hallway') {
                        const door = state.doors[insideRoomIdx];
                        if (door.roomType === 'armory') {
                            logToConsole(`Вы вошли в ${door.name}. На стене висит знак Ликвидаторов. Под ногами рассыпаны гильзы.`, "sys");
                        } else if (door.roomType === 'contaminated') {
                            logToConsole(`Вы вошли в ${door.name}. Воздух здесь едкий и желтоватый. Счетчик Гейгера тихо потрескивает! (Фильтр тратится быстрее)`, "danger");
                        } else if (door.roomType === 'nest') {
                            logToConsole(`Вы вошли в ${door.name}. В углу копошится склизкая биомасса. Старайтесь не шуметь!`, "warn");
                        } else {
                            logToConsole(`Вы вошли в квартиру. Вокруг обычная серая обстановка советской квартиры-хрущевки.`, "sys");
                        }
                    }
                }
            } else {
                if (state.location !== 'hallway') {
                    state.location = 'hallway';
                    state.focusedDoorIndex = null;
                    updateHUD();
                }
            }
        }
        
        state.water = Math.max(0, state.water - 0.002); // Slower water consumption when moving
        
        // Footstep sound system: trigger steps at walking rate if actually moved
        const distMoved = Math.sqrt((playerPos.x - prevX) * (playerPos.x - prevX) + (playerPos.z - prevZ) * (playerPos.z - prevZ));
        if (distMoved > 0.01) {
            footstepTimeAccumulator += deltaTime;
            const finalSpd = window._customSpeed || currentSpeed;
            const stepInterval = Math.max(0.2, 1.5 / finalSpd);
            if (footstepTimeAccumulator >= stepInterval) {
                playSoundStep();
                footstepTimeAccumulator = 0;
            }
        } else {
            footstepTimeAccumulator = 0;
        }
    }
}

function getStepsY(x, y, z) {
    if (z >= -42) return 0;
    const stairsProgress = Math.max(0, Math.min(1.0, (-42.0 - z) / 5.0));
    if (z < -47) {
        if (y < 0) {
            return -2.5;
        } else {
            return 2.5;
        }
    }
    if (x < 0) {
        if (y < 1.25) {
            return -2.5 * stairsProgress;
        } else {
            return 5.0 - 2.5 * stairsProgress;
        }
    } else {
        if (y < -1.25) {
            return -5.0 + 2.5 * stairsProgress;
        } else {
            return 2.5 * stairsProgress;
        }
    }
}

let lastFocusedDoorIndex = undefined;
let lastFocusedStairsDoor = false;
let lastFocusedCorpse = false;

// Рейкаст в центр экрана для фокусировки объекта
function performInteractionRaycast(force = false) {
    // Проецируем луч прямо по центру камеры
    raycaster.setFromCamera(new THREE.Vector2(0, 0), camera);
    
    // Собираем дочерние меши из дверных пивотов для пересечения
    const meshArray = [];
    doorPivots.forEach(pivot => {
        if (pivot.userData && pivot.userData.floor === state.floor) {
            pivot.children.forEach(child => meshArray.push(child));
        }
    });
    
    // Add current stairs door meshes of the floor
    const sdGroup = scene.getObjectByName(`stairsDoor_${state.floor}`);
    if (sdGroup) {
        sdGroup.children.forEach(child => {
            if (child.name === 'left_panel' || child.name === 'right_panel') {
                meshArray.push(child);
            }
        });
    }
    
    // Добавляем части тела ликвидатора
    if (deadLiquidatorMesh && !deadLiquidatorSearched) {
        deadLiquidatorMesh.children.forEach(child => meshArray.push(child));
    }
    
    // Добавляем части призрака
    if (ghostMesh) {
        ghostMesh.children.forEach(child => {
            meshArray.push(child);
            if (child.children) {
                child.children.forEach(gc => meshArray.push(gc));
            }
        });
    }
    
    const intersects = raycaster.intersectObjects(meshArray, true);
    
    let hitDoorIdx = null;
    let hitStairsDoor = false;
    let hitCorpse = false;
    
    if (intersects.length > 0) {
        const hitObj = intersects[0].object;
        const dist = intersects[0].distance;
        
        // 1. Если это призрак и расстояние < 12.0
        if (ghostMesh && (hitObj === ghostMesh || (hitObj.parent && (hitObj.parent === ghostMesh || hitObj.parent.parent === ghostMesh)) || ghostMesh.getObjectById(hitObj.id)) && dist < 12.0) {
            if (playerFlashlight && playerFlashlight.intensity > 0) {
                logToConsole("Призрак закричал от боли и растаял в луче света вашего фонаря!", "sys");
                playScaryScreechSound();
                scene.remove(ghostMesh);
                ghostMesh = null;
            } else {
                if (!window.ghostWhispered) {
                    window.ghostWhispered = true;
                    const creepyLogs = [
                        "Призрак шепчет: 'Здесь нет выхода... только бесконечные этажи...'",
                        "Призрак шепчет: 'Они видят тебя... они всегда видят...'",
                        "Призрак шепчет: 'Остановись... прими Самосбор...'",
                        "Призрак шепчет: 'Ликвидатор 1324... твоя смена окончена...'"
                    ];
                    logToConsole(creepyLogs[Math.floor(Math.random() * creepyLogs.length)], "danger");
                    playSoundScaryWhisper();
                }
            }
        }
        
        // 2. Если это тело ликвидатора и расстояние < 3.5
        else if (deadLiquidatorMesh && (hitObj === deadLiquidatorMesh || (hitObj.parent && hitObj.parent === deadLiquidatorMesh) || deadLiquidatorMesh.getObjectById(hitObj.id)) && dist < 3.5) {
            hitCorpse = true;
        }
        
        // 3. Если это створка затвора на лестнице и расстояние < 4.0
        else if ((hitObj.name === 'left_panel' || hitObj.name === 'right_panel') && dist < 4.0) {
            hitStairsDoor = true;
        }
        
        // 4. Если это квартирная дверь и расстояние < 3.5
        else if (hitObj.name.startsWith('door_') && dist < 3.5) {
            hitDoorIdx = hitObj.userData.doorIndex;
        }
    }
    
    // Обновляем состояние
    state.focusedDoorIndex = hitDoorIdx;
    state.focusedStairsDoor = hitStairsDoor;
    state.focusedCorpse = hitCorpse;
    
    // Обновляем UI
    updateFocusedObjectUI(force);
}

// Обновление UI фокусировки объекта
function updateFocusedObjectUI(force = false) {
    if (!force && 
        state.focusedDoorIndex === lastFocusedDoorIndex && 
        state.focusedStairsDoor === lastFocusedStairsDoor && 
        state.focusedCorpse === lastFocusedCorpse) {
        return;
    }
    
    lastFocusedDoorIndex = state.focusedDoorIndex;
    lastFocusedStairsDoor = state.focusedStairsDoor;
    lastFocusedCorpse = state.focusedCorpse;
    
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
}

// Звук страшного шепота призрака
function playSoundScaryWhisper() {
    initAudio();
    if (!audioCtx) return;
    const now = audioCtx.currentTime;
    const osc1 = audioCtx.createOscillator();
    const osc2 = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    
    osc1.type = 'sine';
    osc1.frequency.setValueAtTime(80, now);
    osc1.frequency.linearRampToValueAtTime(140, now + 1.2);
    
    osc2.type = 'triangle';
    osc2.frequency.setValueAtTime(150, now);
    osc2.frequency.linearRampToValueAtTime(70, now + 1.5);
    
    gain.gain.setValueAtTime(0.04, now);
    gain.gain.linearRampToValueAtTime(0.04, now + 1.0);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 1.5);
    
    osc1.connect(gain);
    osc2.connect(gain);
    gain.connect(audioCtx.destination);
    
    osc1.start(now);
    osc1.stop(now + 1.5);
    osc2.start(now);
    osc2.stop(now + 1.5);
}

// --- МИНИ-ИГРА И ВЗЛОМ ГЕРМОЗАТВОРОВ ---
function startHackPuzzle(onSuccess) {
    hackActive = true;
    hackSuccessCallback = onSuccess;
    activeHackChannel = 'A';
    
    // Рандомизируем целевые частоты трех каналов от 15.0 до 95.0 MHz
    targetFrequencies.A = (Math.random() * 80 + 15).toFixed(1);
    targetFrequencies.B = (Math.random() * 80 + 15).toFixed(1);
    targetFrequencies.C = (Math.random() * 80 + 15).toFixed(1);
    
    document.getElementById('hack-target-a').innerText = `${targetFrequencies.A} MHz`;
    document.getElementById('hack-target-b').innerText = `${targetFrequencies.B} MHz`;
    document.getElementById('hack-target-c').innerText = `${targetFrequencies.C} MHz`;
    
    // Сбрасываем цвета кнопок каналов (красные)
    document.getElementById('hack-chan-a').style.color = '#ff3333';
    document.getElementById('hack-chan-b').style.color = '#ff3333';
    document.getElementById('hack-chan-c').style.color = '#ff3333';
    
    document.getElementById('hack-target-a').style.textDecoration = 'none';
    document.getElementById('hack-target-b').style.textDecoration = 'none';
    document.getElementById('hack-target-c').style.textDecoration = 'none';
    
    document.getElementById('hack-modal').classList.remove('modal-hidden');
    if (document.pointerLockElement) {
        document.exitPointerLock();
    }
    
    // Сбрасываем слайдер частоты
    const slider = document.getElementById('hack-tuner-slider');
    slider.value = 500;
    
    updateHackSliderTuner();
}

function updateHackSliderTuner() {
    const slider = document.getElementById('hack-tuner-slider');
    const freqVal = (parseFloat(slider.value) / 10).toFixed(1);
    document.getElementById('hack-current-freq').innerText = `${freqVal} MHz`;
    
    const targetVal = parseFloat(targetFrequencies[activeHackChannel]);
    const diff = Math.abs(parseFloat(freqVal) - targetVal);
    
    const strengthLabel = document.getElementById('hack-signal-strength');
    if (diff < 1.5) {
        strengthLabel.innerText = "СИГНАЛ: ВЫРАВНИВАНИЕ (КЛИКНИТЕ СОЕДИНЕНИЕ)";
        strengthLabel.style.color = '#00ff66';
    } else if (diff < 5.0) {
        strengthLabel.innerText = "СИГНАЛ: СЛАБЫЙ (ШУМ)";
        strengthLabel.style.color = '#ffcc00';
    } else if (diff < 12.0) {
        strengthLabel.innerText = "СИГНАЛ: ПОМЕХИ";
        strengthLabel.style.color = '#ffaa00';
    } else {
        strengthLabel.innerText = "СИГНАЛ: РАССОГЛАСОВАНИЕ";
        strengthLabel.style.color = '#ff3333';
    }
    
    playTuningBeep(diff);
}

function playTuningBeep(diff) {
    initAudio();
    if (!audioCtx) return;
    const now = audioCtx.currentTime;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    
    let pitch = 150;
    if (diff < 1.5) pitch = 880;
    else if (diff < 5.0) pitch = 440;
    else if (diff < 12.0) pitch = 260;
    
    osc.frequency.setValueAtTime(pitch, now);
    
    let volume = 0.008;
    if (diff < 1.5) volume = 0.04;
    else if (diff < 5.0) volume = 0.02;
    else if (diff < 12.0) volume = 0.015;
    
    gain.gain.setValueAtTime(volume, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
    
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start(now);
    osc.stop(now + 0.1);
}

function submitHackTuning() {
    const slider = document.getElementById('hack-tuner-slider');
    const freqVal = parseFloat(slider.value) / 10;
    const targetVal = parseFloat(targetFrequencies[activeHackChannel]);
    const diff = Math.abs(freqVal - targetVal);
    
    if (diff <= 1.5) {
        // Успешный захват канала
        const chanEl = document.getElementById(`hack-chan-${activeHackChannel.toLowerCase()}`);
        chanEl.style.color = '#00ff66';
        document.getElementById(`hack-target-${activeHackChannel.toLowerCase()}`).innerText = "LOCKED";
        
        // Звук фиксации
        initAudio();
        if (audioCtx) {
            const now = audioCtx.currentTime;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.frequency.setValueAtTime(1200, now);
            gain.gain.setValueAtTime(0.1, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start(now);
            osc.stop(now + 0.35);
        }
        
        logToConsole(`Дешифратор: Канал ${activeHackChannel} зафиксирован!`, "loot");
        
        if (activeHackChannel === 'A') {
            activeHackChannel = 'B';
        } else if (activeHackChannel === 'B') {
            activeHackChannel = 'C';
        } else {
            // Все 3 канала взломаны!
            document.getElementById('hack-modal').classList.add('modal-hidden');
            hackActive = false;
            
            if (hackSuccessCallback) {
                hackSuccessCallback();
            }
        }
    } else {
        // Звуковой сигнал об ошибке
        initAudio();
        if (audioCtx) {
            const now = audioCtx.currentTime;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(100, now);
            gain.gain.setValueAtTime(0.15, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start(now);
            osc.stop(now + 0.45);
        }
        logToConsole("Дешифратор: Сбой связи! Ошибка согласования фазы сигнала.", "danger");
    }
}

// --- ИСПОЛЬЗОВАНИЕ ВЗЛОМЩИКА ---
function useHackerTool() {
    if (!state.focusedStairsDoor && Math.abs(playerPos.z - (-47.0)) > 2.5) {
        logToConsole("Подойдите ближе к лестничному гермозатвору.", "warn");
        return;
    }
    
    initAudio();
    
    // Last Floor check
    if (state.floor === 1) {
        logToConsole("Взломщик: Ошибка доступа. Затвор заблокирован центральной системой ГИГАХРУЩА. Это устройство здесь бесполезно!", "danger");
        
        // Trigger ending sequence after 3 seconds
        disableAllControls(true);
        setTimeout(() => {
            const allNotesRead = state.notesRead && state.notesRead.every(x => x);
            if (state.notesCount === 10 && allNotesRead) {
                triggerGameOver("ending_1");
            } else {
                if (state.notesCount === 10 && !allNotesRead) {
                    logToConsole("Вы собрали все записки, но не прочитали их... Вы не смогли осознать истину.", "danger");
                }
                triggerGameOver("ending_2");
            }
        }, 3000);
        return;
    }
    
    // Check if player has hacker tool
    if (!state.hasHackerTool) {
        logToConsole("У вас нет взломщика гермодверей! Обыщите квартиры, чтобы найти его.", "warn");
        return;
    }
    
    // Check battery
    if (!window._infBatteries && state.batteries <= 0) {
        logToConsole("Батарея взломщика разряжена! Найдите батарейки в квартирах.", "warn");
        return;
    }
    
    // Запускаем взлом-дешифратор!
    startHackPuzzle(() => {
        // Успешный исход
        const sdState = getOrGenerateStairsDoor(state.floor);
        sdState.opened = !sdState.opened;
        
        // Воспроизводим звук движения двери после обхода
        setTimeout(() => {
            playSoundDoor(!sdState.opened);
        }, 300);
        
        logToConsole(`Затвор дешифрован! Механизмы пришли в движение: затвор ${sdState.opened ? 'открывается' : 'закрывается'}...`, "action");
        
        // Progress achievement
        progressAchievement('self_taught_hacker', 1);
        
        // Анимация в 3D
        const sdGroup = scene.getObjectByName(`stairsDoor_${state.floor}`);
        if (sdGroup) {
            const left = sdGroup.getObjectByName("left_panel");
            const right = sdGroup.getObjectByName("right_panel");
            if (left && right) {
                let t = 0;
                const startL = left.position.x;
                const startR = right.position.x;
                const targetL = sdState.opened ? -2.25 : -0.75;
                const targetR = sdState.opened ? 2.25 : 0.75;
                
                const anim = setInterval(() => {
                    t += 0.05;
                    if (t >= 1.0) {
                        left.position.x = targetL;
                        right.position.x = targetR;
                        clearInterval(anim);
                    } else {
                        left.position.x = startL + (targetL - startL) * t;
                        right.position.x = startR + (targetR - startR) * t;
                    }
                }, 30);
            }
        }
        
        updateFocusedObjectUI(true);
        updateHUD();
    });
    
    // Тратим батарейку на запуск
    if (!window._infBatteries) {
        state.batteries--;
    }
    updateInventoryUI();
}

function updateInventoryUI() {
    const bagHacker = document.getElementById('bag-hacker-tool');
    const bagBatteries = document.getElementById('bag-batteries');
    if (bagHacker) {
        bagHacker.innerText = state.hasHackerTool ? "ЕСТЬ" : "НЕТ";
        bagHacker.style.color = state.hasHackerTool ? "var(--glow-green)" : "var(--glow-red)";
    }
    if (bagBatteries) {
        bagBatteries.innerText = `${state.batteries} шт`;
    }
}

// --- ПАУЗА И РЕБИНД ---
let isGamePaused = false;
function togglePauseGame(pause = !isGamePaused) {
    const splash = document.getElementById('splash-screen');
    const goScreen = document.getElementById('gameover-screen');
    if (splash.classList.contains('screen-active') || goScreen.classList.contains('screen-active')) {
        return;
    }
    
    isGamePaused = pause;
    const pauseScreen = document.getElementById('pause-screen');
    if (isGamePaused) {
        pauseScreen.className = 'panel screen-active modal-backdrop';
        if (document.pointerLockElement) {
            document.exitPointerLock();
        }
        Object.keys(keys).forEach(k => keys[k] = false);
    } else {
        pauseScreen.className = 'panel screen-inactive modal-backdrop';
        const canvasHolder = document.getElementById('canvas-holder');
        if (canvasHolder && !state.isSearching) {
            canvasHolder.requestPointerLock();
        }
    }
}

let rebindingAction = null;
function populateRebindList() {
    const list = document.getElementById('rebind-list');
    if (!list) return;
    list.innerHTML = '';
    
    for (let action in state.keyBindings) {
        const keyCode = state.keyBindings[action];
        const label = ACTION_LABELS[action] || action;
        
        const row = document.createElement('div');
        row.className = 'rebind-row';
        row.innerHTML = `
            <span class="rebind-label">${label}</span>
            <button class="rebind-btn" data-action="${action}">${keyCode}</button>
        `;
        list.appendChild(row);
    }
    
    const buttons = list.querySelectorAll('.rebind-btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            if (rebindingAction) return;
            rebindingAction = btn.getAttribute('data-action');
            btn.innerText = 'Нажмите клавишу...';
            btn.classList.add('waiting');
        });
    });
}

// --- ПОДТВЕРЖДЕНИЕ ВЗАИМОДЕЙСТВИЯ (КЛИК / КЛАВИШИ) ---
function interactWithFocused() {
    if (state.focusedCorpse) {
        searchDeadLiquidator();
        return;
    }
    if (state.focusedStairsDoor) {
        useHackerTool();
        return;
    }
    if (state.location === 'hallway') {
        if (state.focusedDoorIndex !== null) {
            const door = state.doors[state.focusedDoorIndex];
            if (!door.opened) {
                openDoor();
            } else {
                closeDoor();
            }
        }
    } else if (state.location === 'room') {
        // В комнате - обыскиваем мебель по динамическим координатам
        const doorIdx = state.focusedDoorIndex;
        if (doorIdx !== null && doorIdx >= 0) {
            const layout = DOOR_LAYOUT[doorIdx];
            const dirX = layout.x < 0 ? -1 : 1;
            const cabPos = new THREE.Vector3(layout.x + (5.5 * dirX), 0, layout.z - 2.0);
            const tablePos = new THREE.Vector3(layout.x + (3.7 * dirX), 0, layout.z);
            
            if (playerPos.distanceTo(cabPos) < 3.5 || playerPos.distanceTo(tablePos) < 3.0) {
                searchRoom();
            } else {
                logToConsole("Подойдите к серванту или столу вплотную, чтобы обыскать их.", "warn");
            }
        } else {
            searchRoom();
        }
    }
}

function listenToFocused() {
    if (state.location === 'hallway' && state.focusedDoorIndex !== null) {
        listenToDoor();
    }
}


// --- ДЕЙСТВИЯ СУРВИВАЛА И ДВЕРЕЙ ---

function listenToDoor() {
    if (state.focusedDoorIndex === null || state.location !== 'hallway' || state.stairsMonsterActive) return;
    initAudio();
    
    const door = state.doors[state.focusedDoorIndex];
    const ind = document.getElementById('listening-indicator');
    const subtext = document.getElementById('listening-subtext');
    
    ind.className = '';
    disableAllControls(true);
    
    logToConsole(`Ликвидатор прислонился к двери ${door.name} и слушает...`, "action");
    
    const barNodes = document.querySelectorAll('.bar');
    let tickCount = 0;
    
    if (door.type === 'monster') {
        playSoundMonsterHiss();
        subtext.innerText = "Скрежет, глухое утробное шипение!";
        subtext.style.color = '#ff3333';
    } else if (door.type === 'transition') {
        subtext.innerText = "Свист воздуха, далекий гул вентиляции";
        subtext.style.color = '#00e5ff';
        if (audioCtx) {
            const now = audioCtx.currentTime;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(300, now);
            osc.frequency.linearRampToValueAtTime(150, now + 1.5);
            gain.gain.setValueAtTime(0.01, now);
            gain.gain.linearRampToValueAtTime(0.05, now + 0.3);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 1.4);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start(now);
            osc.stop(now + 1.5);
        }
    } else {
        subtext.innerText = "Только тяжелое эхо пустых комнат";
        subtext.style.color = '#00ff66';
    }
    
    const waveInterval = setInterval(() => {
        tickCount++;
        barNodes.forEach(bar => {
            let h = 2;
            if (door.type === 'monster') {
                h = Math.random() * 26 + 4;
            } else if (door.type === 'transition') {
                h = Math.sin(tickCount + Math.random()) * 8 + 10;
            } else {
                h = Math.random() * 4 + 2;
            }
            bar.style.height = `${h}px`;
        });
        
        if (tickCount >= 15) {
            clearInterval(waveInterval);
            ind.className = 'overlay-hidden';
            disableAllControls(false);
            updateHUD();
        }
    }, 100);
}

function openDoor() {
    if (state.focusedDoorIndex === null || state.location !== 'hallway' || state.stairsMonsterActive) return;
    initAudio();
    
    const door = state.doors[state.focusedDoorIndex];
    
    if (door.type === 'empty') {
        logToConsole("Ручка не поддается. Гермозатвор заклинен намертво ржавчиной.", "warn");
        return;
    }
    
    door.opened = true;
    
    // Включаем свет в комнате (меняем интенсивность вместо visible для избежания лагов шейдеров)
    if (doorLights && doorLights[state.floor + '_' + state.focusedDoorIndex]) {
        doorLights[state.floor + '_' + state.focusedDoorIndex].intensity = door.type === 'transition' ? 0.5 : 0.3;
    }
    
    // Анимация в 3D (открытие створки вокруг петель)
    const pivot = doorPivots.find(p => p.userData && p.userData.floor === state.floor && p.userData.doorIndex === state.focusedDoorIndex);
    if (pivot) {
        let angle = 0;
        const layout = DOOR_LAYOUT[state.focusedDoorIndex];
        const doorAnim = setInterval(() => {
            angle += 0.08;
            pivot.rotation.y = layout.rot + angle;
            if (angle >= Math.PI / 2) {
                clearInterval(doorAnim);
                pivot.rotation.y = layout.rot + Math.PI / 2;
            }
        }, 20);
    }
    
    playSoundDoor(false);
    logToConsole(`С лязгом замков дверь ${door.name} открылась наружу.`, "action");
    
    if (door.type === 'monster') {
        // Скример смерти
        disableAllControls(true);
        document.getElementById('jumpscare-overlay').className = '';
        playSoundMonsterHiss();
        
        if (audioCtx) {
            const now = audioCtx.currentTime;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(80, now);
            osc.frequency.linearRampToValueAtTime(120, now + 0.8);
            gain.gain.setValueAtTime(0.9, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.9);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start(now);
            osc.stop(now + 1.0);
        }
        
        setTimeout(() => {
            document.getElementById('jumpscare-overlay').className = 'overlay-hidden';
            triggerGameOver("opened_monster");
        }, 1200);
    }
    
    updateHUD();
    updateFocusedObjectUI(true);
}

function closeDoor() {
    if (state.focusedDoorIndex === null) return;
    const door = state.doors[state.focusedDoorIndex];
    if (!door || !door.opened) return;
    
    door.opened = false;
    playSoundDoor();
    
    // Animate door visual
    const pivot = doorPivots.find(p => p.userData.doorIndex === state.focusedDoorIndex && p.userData.floor === state.floor);
    if (pivot) {
        const layout = DOOR_LAYOUT[state.focusedDoorIndex];
        let angle = pivot.rotation.y;
        const targetAngle = layout.rot;
        const anim = setInterval(() => {
            angle -= 0.1;
            if (angle <= targetAngle) {
                pivot.rotation.y = targetAngle;
                clearInterval(anim);
            } else {
                pivot.rotation.y = angle;
            }
        }, 16);
    }
    
    // Turn off light
    const lKey = state.floor + '_' + state.focusedDoorIndex;
    if (doorLights[lKey]) {
        doorLights[lKey].intensity = 0;
    }
    
    logToConsole(`Вы заперли дверь ${door.name}.`, "sys");
    updateFocusedObjectUI(true);
}

function searchRoom() {
    if (state.location !== 'room') return;
    // Найти дверь для обыска
    let doorIdx = state.focusedDoorIndex;
    if (doorIdx === null) {
        // Ищем первую открытую квартиру
        doorIdx = state.doors.findIndex(d => d.type === 'apartment' && d.opened);
        if (doorIdx === -1) return;
    }
    const door = state.doors[doorIdx];
    if (!door || door.searched) return;
    
    initAudio();
    state.isSearching = true;
    disableAllControls(true);
    
    const roomOverlay = document.getElementById('room-overlay');
    const progressBar = document.getElementById('room-search-progress');
    const title = document.getElementById('room-title');
    const status = document.getElementById('room-status-text');
    
    title.innerText = "ОБЫСК МЕБЕЛИ";
    status.innerText = "Проверяем полки, перетряхиваем барахло...";
    roomOverlay.className = '';
    
    let progress = 0;
    
    let searchSoundInterval = setInterval(() => {
        if (!audioCtx) return;
        const now = audioCtx.currentTime;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(80 + Math.random()*45, now);
        gain.gain.setValueAtTime(0.06, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(now);
        osc.stop(now + 0.15);
    }, 180);
    
    const progressInterval = setInterval(() => {
        progress += 5;
        progressBar.style.width = `${progress}%`;
        
        if (progress >= 100) {
            clearInterval(progressInterval);
            clearInterval(searchSoundInterval);
            
            roomOverlay.className = 'overlay-hidden';
            door.searched = true;
            state.isSearching = false;
            disableAllControls(false);
            
            // Проверяем событие Гнезда Твари
            if (door.roomType === 'nest' && Math.random() < 0.50) {
                logToConsole("УЖАСНЫЙ ШОРОХ! Из шевелящейся слизи в углу на вас бросилась тварь!", "danger");
                state.health = Math.max(0, state.health - 20);
                playSoundDamage();
                if (state.health <= 0) {
                    triggerGameOver("stairs_monster");
                    return;
                }
                // Спавним тварь в коридоре перед этой дверью
                const layout = DOOR_LAYOUT[doorIdx];
                spawnHallwayCrawler(layout.z, layout.x < 0 ? -2.5 : 2.5);
            } else {
                distributeLoot(doorIdx);
            }
            updateHUD();
        }
    }, 85);
}

function searchDeadLiquidator() {
    if (!deadLiquidatorMesh || deadLiquidatorSearched) return;
    
    initAudio();
    state.isSearching = true;
    disableAllControls(true);
    
    const roomOverlay = document.getElementById('room-overlay');
    const progressBar = document.getElementById('room-search-progress');
    const title = document.getElementById('room-title');
    const status = document.getElementById('room-status-text');
    
    title.innerText = "ОБЫСК ТЕЛА ЛИКВИДАТОРА";
    status.innerText = "Осматриваем разгрузочный жилет, ищем полезное снаряжение...";
    roomOverlay.className = '';
    
    let progress = 0;
    
    let searchSoundInterval = setInterval(() => {
        if (!audioCtx) return;
        const now = audioCtx.currentTime;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(60 + Math.random()*30, now);
        gain.gain.setValueAtTime(0.05, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(now);
        osc.stop(now + 0.12);
    }, 200);
    
    const progressInterval = setInterval(() => {
        progress += 5;
        progressBar.style.width = `${progress}%`;
        
        if (progress >= 100) {
            clearInterval(progressInterval);
            clearInterval(searchSoundInterval);
            
            roomOverlay.className = 'overlay-hidden';
            deadLiquidatorSearched = true;
            state.isSearching = false;
            disableAllControls(false);
            
            // Награда за обыск тела
            state.batteries += 1;
            state.ammo = Math.min(MAX_AMMO, state.ammo + 8);
            state.filter = Math.min(MAX_FILTER, state.filter + 40);
            
            logToConsole("[НАХОДКА] Вы нашли батарейку, патроны (+8) и фильтр противогаза (+40%) на теле ликвидатора.", "loot");
            playSoundLoot();
            
            // Удаляем визуальное тело со сцены
            if (deadLiquidatorMesh) {
                scene.remove(deadLiquidatorMesh);
                deadLiquidatorMesh = null;
            }
            
            state.focusedCorpse = false;
            updateFocusedObjectUI(true);
            updateHUD();
        }
    }, 70);
}

function distributeLoot(doorIdxParam) {
    let doorIdx = doorIdxParam !== undefined ? doorIdxParam : state.focusedDoorIndex;
    if (doorIdx === null) {
        doorIdx = state.doors.findIndex(d => d.type === 'apartment' && d.opened);
    }
    const door = doorIdx !== null && doorIdx !== -1 ? state.doors[doorIdx] : null;
    if (!door) return;
    
    let loot = door.loot || 'junk';
    
    // Если в комнате записка, пытаемся выдать ее
    if (loot === 'note') {
        if (state.notesCount < LORE_NOTES.length && door.roomType !== 'armory') {
            const nextNoteId = state.notesCount;
            state.notesCollected[nextNoteId] = true;
            state.notesCount++;
            
            const tab = document.getElementById(`note-tab-${nextNoteId}`);
            if (tab) {
                tab.classList.remove('btn-note-locked');
                tab.innerText = LORE_NOTES[nextNoteId].title;
            }
            
            logToConsole(`[НАХОДКА] Найдена старая записка: "${LORE_NOTES[nextNoteId].title}"!`, "loot");
            playSoundLoot();
            openNotesModal(nextNoteId);
            return;
        } else {
            // Если все записки собраны или это оружейная, даем патроны или воду
            loot = Math.random() < 0.5 ? 'ammo' : 'water';
        }
    }
    
    // Если в комнате взломщик гермодверей
    if (loot === 'hacker_tool') {
        if (!state.hasHackerTool) {
            state.hasHackerTool = true;
            logToConsole("[НАХОДКА] Вы нашли ВЗЛОМЩИК ГЕРМОДВЕРЕЙ! Теперь вы можете открывать лестничные затворы.", "loot");
            playSoundLoot();
            updateInventoryUI();
            return;
        } else {
            // Если уже есть, даем батарейку
            loot = 'battery';
        }
    }
    
    // Распределяем предмет по категории
    if (loot === 'battery') {
        state.batteries++;
        logToConsole(`[НАХОДКА] Найдена батарейка для взломщика (+1 шт., всего: ${state.batteries}).`, "loot");
        playSoundLoot();
        updateInventoryUI();
    } else if (loot === 'water') {
        state.bottleWater = Math.min(100, state.bottleWater + 50);
        logToConsole("Найдена фляга чистой синтезированной воды (+50% запаса).", "loot");
        playSoundLoot();
    } else if (loot === 'ammo') {
        const count = door.roomType === 'armory' ? 16 : 8;
        state.ammo = Math.min(MAX_AMMO, state.ammo + count);
        logToConsole(`[НАХОДКА] Найдены пистолетные патроны (+${count} шт.).`, "loot");
        playSoundLoot();
    } else if (loot === 'filter') {
        state.filter = Math.min(MAX_FILTER, state.filter + 50);
        logToConsole("Найден новый патрон фильтра для противогаза (+50% заряда).", "loot");
        playSoundLoot();
    } else {
        logToConsole("Вы обыскали углы, но нашли лишь серую бетонную пыль.", "warn");
    }
}

function lockRoom() {
    if (state.location !== 'room') return;
    initAudio();
    
    state.samosborSafe = !state.samosborSafe;
    playSoundDoor(true);
    
    if (state.samosborSafe) {
        logToConsole("Вы закрутили ручной прижим гермодвери изнутри. Теперь комната герметична.", "action");
    } else {
        logToConsole("Затвор двери открыт. Комната больше не защищает от внешней среды.", "warn");
    }
    
    // Визуально закрываем или открываем дверь комнаты на этаже
    const door = state.doors[state.focusedDoorIndex];
    if (door) {
        door.opened = !state.samosborSafe;
    }
    
    // Animate the door visually instead of rebuilding entire scene
    const pivot = doorPivots.find(p => p.userData && p.userData.floor === state.floor && p.userData.doorIndex === state.focusedDoorIndex);
    if (pivot) {
        const layout = DOOR_LAYOUT[state.focusedDoorIndex];
        if (state.samosborSafe) {
            // Close door animation
            let angle = pivot.rotation.y;
            const targetAngle = layout.rot;
            const anim = setInterval(() => {
                angle -= 0.1;
                if (angle <= targetAngle) {
                    pivot.rotation.y = targetAngle;
                    clearInterval(anim);
                } else {
                    pivot.rotation.y = angle;
                }
            }, 16);
        } else {
            // Open door animation
            let angle = 0;
            const doorAnim = setInterval(() => {
                angle += 0.08;
                pivot.rotation.y = layout.rot + angle;
                if (angle >= Math.PI / 2) {
                    clearInterval(doorAnim);
                    pivot.rotation.y = layout.rot + Math.PI / 2;
                }
            }, 20);
        }
    }
    
    updateHUD();
}

function exitRoom() {
    if (state.location !== 'room' && state.location !== 'transition') return;
    initAudio();
    
    const exitFromIdx = state.focusedDoorIndex !== null ? state.focusedDoorIndex : 0;
    
    state.samosborSafe = false;
    state.location = 'hallway';
    
    playSoundDoor(false);
    logToConsole("Вы вышли обратно в бетонный коридор сектора.", "action");
    
    // Возвращаем игрока в коридор вплотную к той двери, из которой он вышел
    const layout = DOOR_LAYOUT[exitFromIdx];
    // Ставим игрока чуть спереди двери
    const spawnOffset = (layout.x < 0) ? 1.0 : -1.0;
    playerPos.set(layout.x + spawnOffset, 0, layout.z);
    playerYaw = (layout.x < 0) ? Math.PI/2 : -Math.PI/2; // смотрим поперек на коридор
    playerPitch = 0;
    
    // Убеждаемся, что дверь открыта при выходе
    const door = state.doors[exitFromIdx];
    if (door) {
        door.opened = true;
    }
    
    // Визуально открываем дверь в 3D при выходе
    const pivot = doorPivots.find(p => p.userData && p.userData.floor === state.floor && p.userData.doorIndex === exitFromIdx);
    if (pivot) {
        pivot.rotation.y = layout.rot + Math.PI / 2;
    }
    
    updateHUD();
}

// Физический спуск по лестнице (когда игрок дошел до низа)
function triggerFloorDescent() {
    if (state.stairsMonsterActive) return;
    initAudio();
    
    disableAllControls(true);
    
    // Спускаемся на этаж
    state.floor--;
    
    // Check survivor achievement (reaching below floor 1000)
    if (state.floor < 1000) {
        unlockAchievement('survivor');
    }
    
    // Проигрываем звук затвора и шагов
    playSoundDoor(true);
    
    // Показываем экран перехода
    const overlay = document.getElementById('descent-transition-overlay');
    const overlayText = document.getElementById('transition-floor-num');
    overlayText.innerText = `ЭТАЖ ${state.floor}`;
    overlay.className = '';
    
    setTimeout(() => {
        
        if (state.floor < END_FLOOR) {
            overlay.className = 'overlay-hidden';
            triggerGameOver("ending_2");
            return;
        }
        
        // Шанс встретить чудовище на лестнице (10%)
        if (Math.random() < 0.1) {
            overlay.className = 'overlay-hidden';
            triggerStairsMonster();
            updateHUD();
        } else {
            // Генерируем 6 дверей по шансам пользователя
            generateDoorsForFloor();
            build3DScene();
            
            // Сбросываем позицию игрока на старт нового этажа
            playerPos.set(0, 0, -1.0);
            playerYaw = 0;
            playerPitch = 0;
            
            logToConsole(`Вы спустились на этаж ${state.floor}.`, "sys");
            
            updateHUD();
            
            setTimeout(() => {
                overlay.className = 'overlay-hidden';
                disableAllControls(false);
            }, 300);
        }
    }, 1200);
}

// Генерация 6 дверей по шансам пользователя
function getOrGenerateFloorDoors(floorNum) {
    if (!state.floorsData) {
        state.floorsData = {};
    }
    if (state.floorsData[floorNum]) {
        return state.floorsData[floorNum].doors;
    }
    
    let doors = [];
    const apt0Num = Math.floor(Math.random() * 800 + 100);
    doors.push({
        id: 0,
        type: 'apartment',
        number: apt0Num,
        name: `Квартира ${apt0Num}`,
        opened: false,
        searched: false
    });
    
    const hasTransition = Math.random() < 0.3;
    const hasMonster = Math.random() < 0.6;
    
    for (let i = 1; i <= 5; i++) {
        let type = 'empty';
        if (Math.random() < 0.3) {
            type = 'apartment';
        }
        const aptNum = Math.floor(Math.random() * 800 + 100);
        doors.push({
            id: i,
            type: type,
            number: aptNum,
            name: type === 'apartment' ? `Квартира ${aptNum}` : `Дверь ${i + 1}`,
            opened: false,
            searched: false
        });
    }
    
    if (hasTransition) {
        const slots = [1, 2, 3, 4, 5].sort(() => Math.random() - 0.5);
        for (let s of slots) {
            if (doors[s].type === 'empty') {
                doors[s].type = 'transition';
                const sectors = ['А', 'Б', 'В', 'Г', 'Е'];
                const sec = sectors[Math.floor(Math.random()*sectors.length)];
                const secNum = Math.floor(Math.random()*99+1);
                doors[s].sector = sec;
                doors[s].sectorNum = secNum;
                doors[s].name = `Переход ${sec}-${secNum}`;
                break;
            }
        }
    }
    
    if (hasMonster) {
        const slots = [1, 2, 3, 4, 5].sort(() => Math.random() - 0.5);
        for (let s of slots) {
            if (doors[s].type === 'empty') {
                doors[s].type = 'monster';
                const locations = ['Склад', 'Архив', 'Компрессорная', 'Щитовая', 'Венткамера'];
                const mIdx = Math.floor(Math.random() * locations.length);
                doors[s].monsterRoomIndex = mIdx;
                doors[s].name = locations[mIdx];
                break;
            }
        }
    }
    
    doors.forEach((door, idx) => {
        if (door.type === 'apartment') {
            // Различные типы комнат для разнообразия геймплея
            const rTypeRand = Math.random();
            let rType = 'standard';
            let rNum = door.number || Math.floor(Math.random() * 800 + 100);
            let rName = `Квартира ${rNum}`;
            
            if (rTypeRand < 0.15) {
                rType = 'armory';
                rNum = Math.floor(Math.random() * 90 + 10);
                rName = `Пост Ликвидаторов №${rNum}`;
            } else if (rTypeRand < 0.30) {
                rType = 'contaminated';
                rNum = Math.floor(Math.random() * 800 + 100);
                rName = `Квартира ${rNum} (РАДИАЦИЯ)`;
            } else if (rTypeRand < 0.40) {
                rType = 'nest';
                rNum = Math.floor(Math.random() * 90 + 10);
                rName = `Техническая секция ${rNum} (ГНЕЗДО)`;
            }
            
            door.roomType = rType;
            door.number = rNum;
            door.name = rName;
            
            // Предварительный спавн вещей (loot)
            let loot = null;
            if (floorNum === 1320 && idx === 0) {
                // Взломщик гарантирован на 1320 этаже в первой комнате
                loot = 'hacker_tool';
            } else {
                const r = Math.random();
                if (r < 0.12 && !state.hasHackerTool) {
                    loot = 'hacker_tool';
                } else if (r < 0.35) {
                    loot = (rType === 'armory') ? 'ammo' : (Math.random() < 0.5 ? 'ammo' : 'water');
                } else if (r < 0.55) {
                    loot = 'battery';
                } else if (r < 0.80) {
                    loot = (rType === 'armory') ? 'ammo' : 'note';
                } else {
                    loot = 'junk';
                }
            }
            door.loot = loot;
        } else if (door.type === 'empty') {
            door.name = `Секция ${Math.floor(Math.random() * 90 + 10)}`;
        }
    });
    
    state.floorsData[floorNum] = { doors: doors };
    return doors;
}

function generateDoorsForFloor() {
    if (state.floorsData) {
        delete state.floorsData[state.floor];
    }
    getOrGenerateFloorDoors(state.floor);
}

function enterTransition() {
    if (state.location !== 'transition') return;
    initAudio();
    
    state.water = Math.max(0, state.water - 4);
    
    const skipFloors = 20 + Math.floor(Math.random() * 60);
    state.floor = Math.max(1, state.floor - skipFloors);
    
    playSoundDoor(true);
    logToConsole(`Шлюз герметично захлопнулся сзади. Грохот гидравлики уносит вас вниз.`, "sys");
    
    const holder = document.getElementById('canvas-holder');
    holder.style.transition = "opacity 0.5s ease";
    holder.style.opacity = "0.0";
    
    setTimeout(() => {
        logToConsole(`Спуск завершен. Вы вышли на этаже ${state.floor}. Дверь заблокирована сзади.`, "sys");
        
        if (state.floor < END_FLOOR) {
            triggerGameOver("ending_2");
            return;
        }
        
        state.location = 'hallway';
        state.focusedDoorIndex = null;
        generateDoorsForFloor();
        build3DScene();
        
        // Ставим игрока в начало нового коридора
        playerPos.set(0, 0, -1.0);
        playerYaw = 0;
        playerPitch = 0;
        
        updateHUD();
        holder.style.opacity = "1";
    }, 1000);
}

function toggleGasMask() {
    initAudio();
    state.maskOn = !state.maskOn;
    
    playSoundMask();
    if (state.maskOn) {
        logToConsole("Надет противогаз. Обзор ограничен, слышно ваше тяжелое дыхание.", "action");
        if (audioCtx) {
            const now = audioCtx.currentTime;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            const filter = audioCtx.createBiquadFilter();
            filter.type = 'bandpass';
            filter.frequency.value = 250;
            osc.type = 'sine';
            osc.frequency.value = 80;
            gain.gain.setValueAtTime(0.01, now);
            gain.gain.linearRampToValueAtTime(0.12, now + 0.15);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.6);
            osc.connect(filter);
            filter.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start(now);
            osc.stop(now + 0.7);
        }
    } else {
        logToConsole("Противогаз снят.", "action");
    }
    updateHUD();
}

function drinkWater() {
    initAudio();
    if (state.water >= MAX_WATER) {
        logToConsole("Вы не хотите пить.", "warn");
        return;
    }
    
    if (state.bottleWater <= 0) {
        logToConsole("Ваша фляга пуста! Найдите воду в жилых комнатах.", "warn");
        return;
    }
    
    const drinkAmount = Math.min(25, 100 - state.water);
    const actualTaken = Math.min(drinkAmount, state.bottleWater);
    
    if (actualTaken <= 0) {
        logToConsole("Вы утолили жажду полностью.", "warn");
        return;
    }
    
    state.bottleWater -= actualTaken;
    state.water += actualTaken;
    
    // Progress achievement
    progressAchievement('water_drinker', 1);
    
    playSoundDrink();
    logToConsole(`Сделан глоток воды. В бутылке осталось: ${Math.round(state.bottleWater)}% содержимого.`, "action");
    
    updateHUD();
}


// --- ЛЕСТНИЧНЫЙ МОНСТР (3D FIGHT) ---

function triggerStairsMonster() {
    state.stairsMonsterActive = true;
    state.stairsMonsterTimeLeft = 4;
    
    playSoundMonsterHiss();
    logToConsole("[УГРОЗА] ИЗ ТЕМНОТЫ ЛЕСТНИЧНОЙ ШАХТЫ НА ВАС КИДАЕТСЯ МНОГОНОГАЯ ТВАРЬ!", "danger");
    logToConsole("У вас есть 4 секунды, чтобы выстрелить из пистолета и спугнуть её!", "danger");
    
    document.getElementById('btn-descend').setAttribute('disabled', 'true');
    document.getElementById('btn-descend').classList.add('btn-disabled');
    
    disableDoors(true);
    
    // Блокируем игрока на лестничной площадке лицом к чудовищу
    playerPos.set(0, -2.5, -48.25); // на площадке
    playerYaw = 0; // смотрим вверх на лестницу
    playerPitch = 0.2;
    
    build3DScene();
}

let lastKickTime = 0;

function playKickSwooshSound() {
    initAudio();
    if (!audioCtx) return;
    try {
        const now = audioCtx.currentTime;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(150, now);
        osc.frequency.exponentialRampToValueAtTime(40, now + 0.2);
        
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.2);
        
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        
        osc.start(now);
        osc.stop(now + 0.2);
    } catch(e) {}
}

function playKickHitSound() {
    initAudio();
    if (!audioCtx) return;
    try {
        const now = audioCtx.currentTime;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(90, now);
        osc.frequency.linearRampToValueAtTime(30, now + 0.15);
        
        gain.gain.setValueAtTime(0.5, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
        
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        
        osc.start(now);
        osc.stop(now + 0.15);
        
        const osc2 = audioCtx.createOscillator();
        const gain2 = audioCtx.createGain();
        osc2.type = 'sine';
        osc2.frequency.setValueAtTime(450, now);
        osc2.frequency.exponentialRampToValueAtTime(200, now + 0.25);
        gain2.gain.setValueAtTime(0.15, now);
        gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
        
        osc2.connect(gain2);
        gain2.connect(audioCtx.destination);
        osc2.start(now);
        osc2.stop(now + 0.25);
    } catch(e) {}
}

function animateKickVisual() {
    const pistol = camera.getObjectByName("pistol");
    if (!pistol) return;
    
    let t = 0;
    const anim = setInterval(() => {
        t += 0.1;
        if (t <= 0.5) {
            pistol.position.y = -0.16 - t * 0.2;
            pistol.position.z = -0.32 - t * 0.1;
            pistol.rotation.x = t * 0.4;
        } else if (t <= 1.0) {
            const t2 = t - 0.5;
            pistol.position.y = -0.26 + t2 * 0.2;
            pistol.position.z = -0.37 + t2 * 0.1;
            pistol.rotation.x = 0.2 - t2 * 0.4;
        } else {
            clearInterval(anim);
            pistol.position.set(0.18, -0.16, -0.32);
            pistol.rotation.set(0, 0, 0);
        }
    }, 20);
}

function performPlayerKick() {
    if (isGamePaused) return;
    const now = Date.now();
    if (now - lastKickTime < 800) return;
    lastKickTime = now;
    
    playKickSwooshSound();
    animateKickVisual();
    
    if (hallwayCrawlerMesh && state.location === 'hallway') {
        const dx = hallwayCrawlerMesh.position.x - playerPos.x;
        const dz = hallwayCrawlerMesh.position.z - playerPos.z;
        const dist = Math.sqrt(dx * dx + dz * dz);
        
        if (dist < 3.5) {
            const pushDirZ = dz / (dist || 1);
            const pushDirX = dx / (dist || 1);
            
            hallwayCrawlerMesh.position.x += pushDirX * 5.0;
            hallwayCrawlerMesh.position.z += pushDirZ * 5.0;
            hallwayCrawlerMesh.position.z = Math.max(-50.0, Math.min(0.0, hallwayCrawlerMesh.position.z));
            
            crawlerHealth -= 1;
            playKickHitSound();
            logToConsole("УДАР! Вы пнули тварь! Она отлетела назад и взвизгнула!", "warn");
            
            if (crawlerHealth <= 0) {
                logToConsole("Вы забили тварь ногами до смерти!", "loot");
                scene.remove(hallwayCrawlerMesh);
                hallwayCrawlerMesh = null;
                progressAchievement('gigahrush_butcher', 1);
            }
            return;
        }
    }
    
    logToConsole("Вы пнули воздух.", "sys");
}

function shootPistol() {
    initAudio();
    if (state.ammo <= 0) {
        logToConsole("Сухой щелчок бойка... Патронов нет!", "danger");
        return;
    }
    
    state.ammo--;
    playSoundShot();
    
    // Achievement check: spendthrift (out of ammo above floor 1000)
    if (state.floor > 1000 && state.ammo === 0) {
        unlockAchievement('spendthrift');
    }
    
    // Вспышка в Three.js
    if (scene) {
        const flashLight = new THREE.PointLight(0xfff0c0, 4.0, 30);
        flashLight.position.set(camera.position.x, camera.position.y, camera.position.z - 1.0);
        scene.add(flashLight);
        setTimeout(() => scene.remove(flashLight), 60);
    }
    
    logToConsole("Грохот выстрела раскатился по бетонному колодцу этажа!", "action");
    
    // Pistol 3D Recoil and Muzzle Flash animation
    const pistol = camera.getObjectByName("pistol");
    if (pistol) {
        // Kickback and rotate up
        pistol.position.z += 0.05;
        pistol.rotation.x -= 0.12;
        
        // Spawn 3D muzzle flash cylinder/cone
        const flashGeo = new THREE.CylinderGeometry(0.01, 0.04, 0.06, 8);
        const flashMat = new THREE.MeshBasicMaterial({ color: 0xffaa44 });
        const flash = new THREE.Mesh(flashGeo, flashMat);
        flash.rotation.x = Math.PI / 2;
        flash.position.set(0, 0.01, -0.16); // tip of muzzle
        pistol.add(flash);
        setTimeout(() => pistol.remove(flash), 60);
        
        let recoilTime = 0;
        const anim = setInterval(() => {
            recoilTime += 16;
            if (recoilTime >= 150) {
                // Restore origin
                pistol.position.set(0.18, -0.16, -0.32);
                pistol.rotation.set(Math.PI / 80, -Math.PI / 20, 0);
                clearInterval(anim);
            } else {
                const t = recoilTime / 150;
                pistol.position.z = -0.32 + 0.05 * (1 - t);
                pistol.rotation.x = Math.PI / 80 - 0.12 * (1 - t);
            }
        }, 16);
    }
    
    // Проверка попадания в ползающую тварь
    if (hallwayCrawlerMesh) {
        raycaster.setFromCamera(new THREE.Vector2(0, 0), camera);
        const intersects = raycaster.intersectObjects(hallwayCrawlerMesh.children, true);
        if (intersects.length > 0) {
            crawlerHealth -= 1;
            if (crawlerHealth <= 0) {
                logToConsole("Точный выстрел разорвал тварь! По коридору разлетелись брызги слизи.", "loot");
                scene.remove(hallwayCrawlerMesh);
                hallwayCrawlerMesh = null;
                // Progress gigahrush butcher
                progressAchievement('gigahrush_butcher', 1);
            } else {
                logToConsole("Пуля пробила хитиновый панцирь твари! Она яростно завизжала.", "warn");
                playScaryScreechSound();
            }
            updateHUD();
            return;
        }
    }
    
    if (state.stairsMonsterActive) {
        state.stairsMonsterActive = false;
        logToConsole("Тварь издала пронзительный визг и скрылась в вентиляционном канале.", "sys");
        
        // Progress gigahrush butcher
        progressAchievement('gigahrush_butcher', 1);
        
        document.getElementById('btn-descend').removeAttribute('disabled');
        document.getElementById('btn-descend').classList.remove('btn-disabled');
        disableDoors(false);
        
        if (stairsMonsterMesh) {
            scene.remove(stairsMonsterMesh);
            stairsMonsterMesh = null;
        }
        
        // Генерируем 6 дверей и сбрасываем игрока в начало
        generateDoorsForFloor();
        build3DScene();
        
        playerPos.set(0, 0, -1.0);
        playerYaw = 0;
        playerPitch = 0;
    } else {
        logToConsole("Вы выстрелили впустую в бетонные перекрытия.", "warn");
    }
    
    updateHUD();
}


// --- УПРАВЛЕНИЕ ДИАЛОГАМИ И МОДАЛКАМИ ---

function openNotesModal(autoSelectId = null) {
    const modal = document.getElementById('notes-modal');
    modal.classList.remove('modal-hidden');
    
    if (autoSelectId !== null) {
        selectNoteInModal(autoSelectId);
    } else {
        document.getElementById('note-content-area').innerHTML = `<p class="select-note-prompt">Выберите найденную записку в списке слева для чтения.</p>`;
    }
}

function closeNotesModal() {
    document.getElementById('notes-modal').classList.add('modal-hidden');
    
    // Check if player has collected and read all 10 notes
    const allNotesRead = state.notesRead && state.notesRead.every(x => x);
    if (state.notesCount === 10 && allNotesRead) {
        triggerTrueWakeupEnding();
    }
}

function toggleBag() {
    const modal = document.getElementById('notes-modal');
    if (modal) {
        if (modal.classList.contains('modal-hidden')) {
            openNotesModal();
        } else {
            closeNotesModal();
        }
    }
}

function selectNoteInModal(id) {
    if (!state.notesCollected[id]) return;
    
    // Mark as read
    state.notesRead[id] = true;
    
    for (let i = 0; i < LORE_NOTES.length; i++) {
        const tab = document.getElementById(`note-tab-${i}`);
        if (tab) tab.classList.remove('btn-note-selected');
    }
    
    document.getElementById(`note-tab-${id}`).classList.add('btn-note-selected');
    
    const area = document.getElementById('note-content-area');
    const note = LORE_NOTES[id];
    
    let contentText = note.content;
    if (contentText.includes("[FLOOR]")) {
        contentText = contentText.replace("[FLOOR]", state.floor);
    }
    
    let textStyle = "white-space:pre-line;";
    if (id === 7) {
        textStyle = "white-space:pre-line; color:#ff3333; font-weight:bold; font-size:1.2rem; line-height:1.8; text-align:center; text-shadow:0 0 10px rgba(255,0,0,0.8);";
    }
    
    area.innerHTML = `
        <div class="blood-stain blood-stain-1"></div>
        <div class="blood-stain blood-stain-2"></div>
        <div class="blood-stain blood-stain-3"></div>
        <h3 style="margin-bottom:15px; color:#6b0a0a; font-weight:bold;">${note.title}</h3>
        <p style="${textStyle}">${contentText}</p>
    `;
}

let trueEndingAudioInterval = null;
let menuNatureAnimFrame = null;
let menuNatureCanvas = null;

function stopAtmosphere() {
    if (atmosphereOsc) {
        try {
            atmosphereOsc.stop();
        } catch(e) {}
        atmosphereOsc = null;
    }
    if (heartbeatInterval) {
        clearInterval(heartbeatInterval);
        heartbeatInterval = null;
    }
}

function enableMenuWakeupTheme() {
    // 1. Hide hazard stripes
    const hazardStripes = document.querySelectorAll('#splash-screen .hazard-stripe');
    hazardStripes.forEach(stripe => {
        stripe.style.display = 'none';
    });
    
    // 2. Change title glow from red to green
    const titleEl = document.querySelector('#splash-screen .title-text');
    if (titleEl) {
        titleEl.classList.remove('glow-red');
        titleEl.classList.add('glow-green');
        titleEl.style.textShadow = '0 0 15px rgba(0, 255, 102, 0.8)';
    }
    
    // 3. Change creator subtitle color
    const creatorEl = document.querySelector('#splash-screen .creator-subtitle');
    if (creatorEl) {
        creatorEl.style.color = 'var(--glow-green)';
        creatorEl.style.textShadow = '0 0 10px rgba(0, 255, 102, 0.5)';
    }
    
    // 4. Update terminal text block
    const terminalBlock = document.querySelector('#splash-screen .terminal-text-block');
    if (terminalBlock) {
        terminalBlock.style.borderColor = 'var(--glow-green)';
        terminalBlock.style.boxShadow = 'inset 0 0 8px rgba(0, 255, 102, 0.15)';
        terminalBlock.style.color = '#00ff66';
        terminalBlock.innerHTML = `
            <p class="blink-cursor">> ДЕКОМПИЛЯЦИЯ КОШМАРА... ОК.</p>
            <p>> ПОДКЛЮЧЕНИЕ К РЕАЛЬНОМУ МИРУ... ОК.</p>
            <p>> ВОЗДУХ: ЧИСТЫЙ, ТРАВА: ЗЕЛЕНАЯ, НЕБО: СИНЕЕ.</p>
            <p class="glow-green">> ЗАДАЧА: СНОВА СДЕЛАЙТЕ СВОЙ ВЫБОР И БУДЬТЕ СВОБОДНЫ.</p>
        `;
    }
    
    // 5. Add dynamic animated nature background canvas
    const splash = document.getElementById('splash-screen');
    if (!splash) return;
    
    if (!menuNatureCanvas) {
        menuNatureCanvas = document.createElement('canvas');
        menuNatureCanvas.id = 'menu-nature-canvas';
        menuNatureCanvas.style.position = 'absolute';
        menuNatureCanvas.style.top = '0';
        menuNatureCanvas.style.left = '0';
        menuNatureCanvas.style.width = '100%';
        menuNatureCanvas.style.height = '100%';
        menuNatureCanvas.style.zIndex = '1';
        menuNatureCanvas.style.pointerEvents = 'none';
        menuNatureCanvas.style.opacity = '0.55';
        menuNatureCanvas.style.filter = 'blur(10px)';
        
        splash.insertBefore(menuNatureCanvas, splash.firstChild);
        
        const children = splash.children;
        for (let i = 0; i < children.length; i++) {
            const child = children[i];
            if (child.id !== 'menu-nature-canvas') {
                child.style.position = 'relative';
                child.style.zIndex = '2';
            }
        }
        
        animateMenuNature();
    }
}

function disableMenuWakeupTheme() {
    if (menuNatureAnimFrame) {
        cancelAnimationFrame(menuNatureAnimFrame);
        menuNatureAnimFrame = null;
    }
    if (menuNatureCanvas) {
        menuNatureCanvas.remove();
        menuNatureCanvas = null;
    }
    
    // Restore hazard stripes
    const hazardStripes = document.querySelectorAll('#splash-screen .hazard-stripe');
    hazardStripes.forEach(stripe => {
        stripe.style.display = 'block';
    });
    
    // Restore title glow to red
    const titleEl = document.querySelector('#splash-screen .title-text');
    if (titleEl) {
        titleEl.classList.remove('glow-green');
        titleEl.classList.add('glow-red');
        titleEl.style.textShadow = '0 0 10px rgba(255, 51, 51, 0.6)';
    }
    
    // Restore creator subtitle color
    const creatorEl = document.querySelector('#splash-screen .creator-subtitle');
    if (creatorEl) {
        creatorEl.style.color = 'var(--glow-amber)';
        creatorEl.style.textShadow = '0 0 5px rgba(255, 204, 0, 0.4)';
    }
    
    // Restore terminal block text and styles
    const terminalBlock = document.querySelector('#splash-screen .terminal-text-block');
    if (terminalBlock) {
        terminalBlock.style.borderColor = 'var(--border-color)';
        terminalBlock.style.boxShadow = 'inset 0 0 8px rgba(0, 255, 102, 0.15)';
        terminalBlock.style.color = '#39e376';
        terminalBlock.innerHTML = `
            <p class="blink-cursor">> ИНИЦИАЛИЗАЦИЯ ИНТЕРФЕЙСА ЛИКВИДАТОРА...</p>
            <p>> ПОДКЛЮЧЕНИЕ К СЕТИ ГИГАХРУЩЕВКИ... ОК.</p>
            <p>> СНАРЯЖЕНИЕ: ПИСТОЛЕТ (24), ПРОТИВОГАЗ, ВОДА, СУМКА.</p>
            <p class="glow-green">> ЗАДАЧА: СПУСТИТЬСЯ НА 1-Й ЭТАЖ И ВЫЖИТЬ.</p>
        `;
    }
}

function animateMenuNature() {
    if (!menuNatureCanvas) return;
    const ctx = menuNatureCanvas.getContext('2d');
    
    let time = 0;
    const particles = [];
    for (let i = 0; i < 20; i++) {
        particles.push({
            x: Math.random() * 800,
            y: Math.random() * 600,
            vx: 0.2 + Math.random() * 0.5,
            vy: -0.1 - Math.random() * 0.3,
            size: 2 + Math.random() * 4,
            alpha: 0.1 + Math.random() * 0.4,
            wiggleSpeed: 0.002 + Math.random() * 0.005,
            wiggleOffset: Math.random() * 100
        });
    }
    
    function loop() {
        if (!menuNatureCanvas) return;
        const rect = menuNatureCanvas.getBoundingClientRect();
        const w = menuNatureCanvas.width = rect.width || 800;
        const h = menuNatureCanvas.height = rect.height || 600;
        
        time += 16.67;
        ctx.clearRect(0, 0, w, h);
        
        // 1. Sky Gradient
        const skyGrad = ctx.createLinearGradient(0, 0, 0, h);
        skyGrad.addColorStop(0, '#7ec0ee');
        skyGrad.addColorStop(0.6, '#e0f6ff');
        skyGrad.addColorStop(1, '#a8e4a0');
        ctx.fillStyle = skyGrad;
        ctx.fillRect(0, 0, w, h);
        
        // 2. Pulsating Sun
        const sunX = w * 0.25;
        const sunY = h * 0.25;
        const sunRadBase = Math.min(w, h) * 0.15;
        const sunRad = sunRadBase + Math.sin(time * 0.001) * (sunRadBase * 0.1);
        const sunGrad = ctx.createRadialGradient(sunX, sunY, 10, sunX, sunY, sunRad);
        sunGrad.addColorStop(0, 'rgba(255, 255, 220, 0.85)');
        sunGrad.addColorStop(1, 'rgba(255, 255, 255, 0)');
        ctx.fillStyle = sunGrad;
        ctx.fillRect(0, 0, w, h);
        
        // 3. Clouds
        const cloudSpeed = 0.015;
        const drawCloud = (cx, cy, scale) => {
            ctx.fillStyle = 'rgba(255, 255, 255, 0.65)';
            ctx.beginPath();
            ctx.arc(cx, cy, 30 * scale, 0, Math.PI * 2);
            ctx.arc(cx + 40 * scale, cy - 10 * scale, 40 * scale, 0, Math.PI * 2);
            ctx.arc(cx + 80 * scale, cy, 30 * scale, 0, Math.PI * 2);
            ctx.arc(cx + 40 * scale, cy + 15 * scale, 25 * scale, 0, Math.PI * 2);
            ctx.closePath();
            ctx.fill();
        };
        const cloud1X = ((time * cloudSpeed + 100) % (w + 200)) - 100;
        drawCloud(cloud1X, h * 0.18, 1.2);
        
        const cloud2X = (((time * cloudSpeed * 0.7) + w * 0.5) % (w + 200)) - 100;
        drawCloud(cloud2X, h * 0.3, 0.8);
        
        // 4. Grass Hill
        const hillGrad = ctx.createLinearGradient(0, h * 0.75, 0, h);
        hillGrad.addColorStop(0, '#55a630');
        hillGrad.addColorStop(1, '#2b9348');
        ctx.fillStyle = hillGrad;
        ctx.beginPath();
        const hillYOffset = Math.sin(time * 0.0005) * 5;
        ctx.ellipse(w * 0.5, h + 100 + hillYOffset, w * 0.7, h * 0.4, 0, 0, Math.PI * 2);
        ctx.fill();
        
        // 5. Tree
        const treeX = w * 0.75;
        const treeY = h * 0.85;
        const treeSway = Math.sin(time * 0.0008) * 15;
        
        ctx.fillStyle = '#6f4e37';
        ctx.beginPath();
        ctx.moveTo(treeX - 15, treeY);
        ctx.quadraticCurveTo(treeX - 10, treeY - 80, treeX - 30 + treeSway * 0.5, treeY - 180);
        ctx.lineTo(treeX - 5 + treeSway * 0.5, treeY - 180);
        ctx.quadraticCurveTo(treeX + 15, treeY - 80, treeX + 20, treeY);
        ctx.closePath();
        ctx.fill();
        
        const branchX = treeX - 18 + treeSway * 0.5;
        const branchY = treeY - 180;
        
        ctx.fillStyle = 'rgba(56, 176, 0, 0.85)';
        ctx.beginPath();
        ctx.arc(branchX - 50 + treeSway * 0.3, branchY - 20, 55, 0, Math.PI * 2);
        ctx.arc(branchX + 50 + treeSway * 0.3, branchY - 30, 60, 0, Math.PI * 2);
        ctx.arc(branchX + treeSway * 0.3, branchY - 70, 65, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.fillStyle = 'rgba(0, 114, 0, 0.85)';
        ctx.beginPath();
        ctx.arc(branchX - 30 + treeSway * 0.4, branchY + 10, 45, 0, Math.PI * 2);
        ctx.arc(branchX + 40 + treeSway * 0.4, branchY - 10, 45, 0, Math.PI * 2);
        ctx.fill();
        
        // 6. Particles
        particles.forEach(p => {
            p.x += p.vx + Math.sin(time * p.wiggleSpeed + p.wiggleOffset) * 0.4;
            p.y += p.vy;
            if (p.x > w + 20) p.x = -20;
            if (p.y < -20) {
                p.y = h + 20;
                p.x = Math.random() * w;
            }
            ctx.fillStyle = `rgba(180, 240, 150, ${p.alpha})`;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
        });
        
        menuNatureAnimFrame = requestAnimationFrame(loop);
    }
    
    if (menuNatureAnimFrame) {
        cancelAnimationFrame(menuNatureAnimFrame);
    }
    loop();
}

function drawProceduralNature() {
    const canvas = document.createElement('canvas');
    canvas.width = 800;
    canvas.height = 600;
    const ctx = canvas.getContext('2d');
    
    // Sky gradient (blue to white)
    const skyGrad = ctx.createLinearGradient(0, 0, 0, 600);
    skyGrad.addColorStop(0, '#7ec0ee'); // Sky blue
    skyGrad.addColorStop(0.6, '#e0f6ff'); // Horizon
    skyGrad.addColorStop(1, '#a8e4a0'); // Grass horizon blend
    ctx.fillStyle = skyGrad;
    ctx.fillRect(0, 0, 800, 600);
    
    // Sun glow
    const sunGrad = ctx.createRadialGradient(200, 150, 10, 200, 150, 200);
    sunGrad.addColorStop(0, 'rgba(255, 255, 220, 0.8)');
    sunGrad.addColorStop(1, 'rgba(255, 255, 255, 0)');
    ctx.fillStyle = sunGrad;
    ctx.fillRect(0, 0, 800, 600);

    // Grass meadow
    const grassGrad = ctx.createLinearGradient(0, 450, 0, 600);
    grassGrad.addColorStop(0, '#55a630');
    grassGrad.addColorStop(1, '#2b9348');
    ctx.fillStyle = grassGrad;
    ctx.beginPath();
    ctx.ellipse(400, 650, 500, 220, 0, 0, Math.PI * 2);
    ctx.fill();

    // Tree trunk
    ctx.fillStyle = '#6f4e37'; // Brown
    ctx.beginPath();
    ctx.moveTo(580, 500);
    ctx.quadraticCurveTo(570, 400, 550, 300);
    ctx.lineTo(570, 300);
    ctx.quadraticCurveTo(595, 400, 610, 500);
    ctx.closePath();
    ctx.fill();
    
    // Tree leaves (soft layered circles)
    ctx.fillStyle = '#38b000';
    ctx.beginPath();
    ctx.arc(520, 280, 65, 0, Math.PI * 2);
    ctx.arc(590, 260, 75, 0, Math.PI * 2);
    ctx.arc(560, 210, 70, 0, Math.PI * 2);
    ctx.fill();
    
    ctx.fillStyle = '#007200';
    ctx.beginPath();
    ctx.arc(500, 290, 45, 0, Math.PI * 2);
    ctx.arc(610, 270, 50, 0, Math.PI * 2);
    ctx.fill();

    const natureDiv = document.getElementById('true-ending-nature');
    if (natureDiv) {
        natureDiv.style.backgroundImage = `url(${canvas.toDataURL()})`;
    }
}

function playTrueEndingMusic() {
    initAudio();
    if (!audioCtx) return;
    try {
        const chords = [
            [261.63, 329.63, 392.00, 523.25], // C Major
            [349.23, 440.00, 523.25, 698.46], // F Major
            [392.00, 493.88, 587.33, 783.99], // G Major
            [329.63, 392.00, 493.88, 659.25]  // E Minor
        ];
        let chordIdx = 0;
        
        function playChord() {
            const now = audioCtx.currentTime;
            const currentChord = chords[chordIdx];
            chordIdx = (chordIdx + 1) % chords.length;
            
            currentChord.forEach((freq, i) => {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                
                osc.type = 'sine';
                osc.frequency.setValueAtTime(freq, now + i * 0.12);
                
                gain.gain.setValueAtTime(0.001, now);
                gain.gain.linearRampToValueAtTime(0.05, now + 1.0);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 4.8);
                
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                
                osc.start(now);
                osc.stop(now + 5.0);
            });
        }
        
        playChord();
        trueEndingAudioInterval = setInterval(playChord, 5000);
    } catch(e) {
        console.error("Audio true ending music error:", e);
    }
}

function triggerTrueWakeupEnding() {
    if (gameInterval) clearInterval(gameInterval);
    stopSoundSiren();
    disableAllControls(true);
    
    // Draw nature background procedurally
    drawProceduralNature();
    
    // 1. Show whiteout overlay
    const whiteout = document.getElementById('true-ending-whiteout');
    if (whiteout) {
        whiteout.style.opacity = '1';
    }
    
    // 2. Transition to waking up screen after whiteout (4 seconds)
    setTimeout(() => {
        const wakeupScreen = document.getElementById('true-ending-wakeup');
        const credits = document.getElementById('true-ending-credits');
        const floorsText = document.getElementById('true-ending-floors-descended');
        
        // Hide game interfaces
        document.getElementById('main-interface').className = 'screen-inactive';
        
        if (wakeupScreen) {
            wakeupScreen.classList.remove('screen-inactive');
            wakeupScreen.style.display = 'flex';
            // Force redraw/reflow
            wakeupScreen.offsetHeight;
            wakeupScreen.style.opacity = '1';
        }
        
        // Calculate floors descended
        if (floorsText) {
            floorsText.innerText = (START_FLOOR - state.floor).toString();
        }
        
        // Play light peaceful chords
        playTrueEndingMusic();
        
        // 3. Fade in credits card (after another 1.5 seconds)
        setTimeout(() => {
            if (credits) {
                credits.style.opacity = '1';
            }
            unlockAchievement("awakened");
        }, 1500);
        
    }, 4000);
}

// --- КОНЦОВКИ И GAME OVER ---

function triggerGameOver(reason) {
    if (gameInterval) clearInterval(gameInterval);
    stopSoundSiren();
    
    state.location = 'hallway';
    state.stairsMonsterActive = false;
    
    const screen = document.getElementById('gameover-screen');
    const title = document.getElementById('gameover-title');
    const story = document.getElementById('gameover-story');
    const badge = document.getElementById('ending-badge');
    
    screen.className = 'panel screen-active';
    document.getElementById('main-interface').className = 'screen-inactive';
    
    let text = "";
    let badgeText = "Смерть";
    let badgeClass = "badge-red";
    
    switch (reason) {
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
                    <p>Хищная тварь Самосбора устроила гнездо прямо за порогом.</p>
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
                    <p>Без противогаза ваши легкие наполнились едкими парами, вызвав мгновенный спазм и удушье.</p>`;
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
            break;
            
        case "ending_2":
            unlockAchievement("deceived");
            title.innerText = "БЕЗВЫХОДНОСТЬ";
            title.style.color = "#ff3333";
            badgeText = "Тупиковая концовка";
            badgeClass = "badge-red";
            text = `<p>Вы преодолели долгий путь и спустились на первый этаж.</p>
                    <p>Но прохода наружу нет. Тяжелые шлюзы герметично заварены многовековыми слоями ржавчины.</p>
                    <p>Сзади с грохотом захлопнулась дверь лестничного марша. Механизмы заклинило. Задвижки не двигаются.</p>
                    <p>В этот момент сирены взвыли на максимальной громкости. Начался мощнейший Самосбор. Укрытий нет. Двери заблокированы. Вы заперты в бетонном мешке первого этажа один на один со смертельным туманом. Это конец пути.</p>`;
            if (audioCtx) {
                playScaryMusic();
            }
            break;
    }
    
    badge.innerText = badgeText;
    badge.className = badgeClass;
    story.innerHTML = text;

    // Show collected notes at the end of the game for story endings
    const notesContainer = document.getElementById('gameover-notes-container');
    const notesList = document.getElementById('gameover-notes-list');
    const creditsContainer = document.getElementById('gameover-credits-container');
    
    if (creditsContainer) {
        if (reason === 'ending_1' || reason === 'ending_2') {
            creditsContainer.style.display = 'block';
        } else {
            creditsContainer.style.display = 'none';
        }
    }
    
    if (notesContainer && notesList) {
        if (reason === 'ending_1' || reason === 'ending_2') {
            notesContainer.style.display = 'block';
            notesList.innerHTML = '';
            
            LORE_NOTES.forEach((note, index) => {
                const collected = state.notesCollected[index];
                const noteDiv = document.createElement('div');
                noteDiv.className = `gameover-note-item ${collected ? 'collected' : 'missing'}`;
                
                if (collected) {
                    noteDiv.innerHTML = `
                        <div class="gameover-note-title">[✓] ${note.title}</div>
                        <div class="gameover-note-content">${note.content}</div>
                    `;
                } else {
                    noteDiv.innerHTML = `
                        <div class="gameover-note-title">[✗] ЗАПИСКА ${index + 1} (НЕ НАЙДЕНА)</div>
                        <div class="gameover-note-content" style="font-style: italic; color: #888;">Вы упустили этот фрагмент истории на этажах Хрущевки. Обыскивайте комнаты, чтобы найти её.</div>
                    `;
                }
                notesList.appendChild(noteDiv);
            });
        } else {
            notesContainer.style.display = 'none';
        }
    }
}


// --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ И БЛОКИРОВКИ ---

function disableAllControls(disable) {
    const buttons = [
        'btn-mask', 'btn-drink', 'btn-bag',
        'btn-listen', 'btn-open-door',
        'btn-search-room', 'btn-lock-room', 'btn-exit-room',
        'btn-enter-transition', 'btn-cancel-transition'
    ];
    
    buttons.forEach(id => {
        const btn = document.getElementById(id);
        if (!btn) return;
        
        if (disable) {
            btn.setAttribute('disabled', 'true');
            btn.classList.add('btn-disabled');
        } else {
            if (id === 'btn-listen' || id === 'btn-open-door') {
                if (state.focusedDoorIndex === null || state.location !== 'hallway') return;
            }
            if (id === 'btn-search-room' && state.focusedDoorIndex !== null) {
                const activeDoor = state.doors[state.focusedDoorIndex];
                if (activeDoor && activeDoor.searched) return;
            }
            btn.removeAttribute('disabled');
            btn.classList.remove('btn-disabled');
        }
    });
}

function disableDoors(disable) {
    // В FPS режиме двери кликаются физически, поэтому кнопки дверей в HUD теперь чисто информативные
}

// --- СИСТЕМНЫЙ ЖУРНАЛ (ЛОГ) ---

function logToConsole(message, type = "sys") {
    const feed = document.getElementById('log-feed');
    if (!feed) return;
    
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    
    const time = new Date();
    const timeStr = `${String(time.getHours()).padStart(2, '0')}:${String(time.getMinutes()).padStart(2, '0')}:${String(time.getSeconds()).padStart(2, '0')}`;
    
    let colorClass = '';
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
    }
    
    entry.innerHTML = `<span class="log-time">${timeStr}</span> <span class="${colorClass}">${prefix}</span> ${message}`;
    feed.appendChild(entry);
    feed.scrollTop = feed.scrollHeight;
    
    // Ограничиваем количество записей в логе
    while (feed.children.length > 100) {
        feed.removeChild(feed.firstChild);
    }
}


// --- ОБНОВЛЕНИЕ HUD (ИНТЕРФЕЙСА СОСТОЯНИЯ) ---

function updateHUD() {
    const hudFloor = document.getElementById('hud-floor');
    const hudHealth = document.getElementById('hud-health');
    const hudWater = document.getElementById('hud-water');
    const hudAmmo = document.getElementById('hud-ammo');
    const hudFilter = document.getElementById('hud-filter');
    const hudStamina = document.getElementById('hud-stamina');
    const bagNotes = document.getElementById('bag-notes-count');
    
    if (hudFloor) hudFloor.innerText = state.floor;
    if (hudHealth) hudHealth.innerText = Math.round(state.health) + '%';
    if (hudWater) hudWater.innerText = Math.round(state.water) + '%';
    if (hudAmmo) hudAmmo.innerText = state.ammo;
    if (hudFilter) hudFilter.innerText = Math.round(state.filter) + '%';
    if (hudStamina) hudStamina.innerText = Math.round(state.stamina) + '%';
    if (bagNotes) bagNotes.innerText = state.notesCount;
    
    // Цветовые индикаторы критических значений
    const healthContainer = document.getElementById('hud-health-container');
    const waterContainer = document.getElementById('hud-water-container');
    const ammoContainer = document.getElementById('hud-ammo-container');
    const filterContainer = document.getElementById('hud-filter-container');
    const staminaContainer = document.getElementById('hud-stamina-container');
    
    if (healthContainer) {
        healthContainer.className = 'hud-item ' + (state.health <= 30 ? 'glow-red animate-blink' : 'glow-green');
    }
    if (waterContainer) {
        waterContainer.className = 'hud-item ' + (state.water <= 20 ? 'glow-red animate-blink' : 'glow-blue');
    }
    if (ammoContainer) {
        ammoContainer.className = 'hud-item ' + (state.ammo <= 4 ? 'glow-red' : 'glow-yellow');
    }
    if (filterContainer) {
        filterContainer.className = 'hud-item ' + (state.filter <= 20 ? 'glow-red animate-blink' : 'glow-purple');
    }
    if (staminaContainer) {
        staminaContainer.className = 'hud-item ' + (state.stamina <= 20 ? 'glow-red animate-blink' : 'glow-orange');
    }
    
    // Обновляем маску противогаза визуально
    const maskOverlay = document.getElementById('gasmask-overlay');
    if (maskOverlay) {
        maskOverlay.className = state.maskOn ? '' : 'overlay-hidden';
    }
    
    // Обновляем вид панелей взаимодействия
    const roomActions = document.getElementById('room-actions-bar');
    const transActions = document.getElementById('transition-actions-bar');
    const focusedHud = document.querySelector('.focused-object-hud');
    
    if (roomActions) {
        roomActions.className = (state.location === 'room') ? '' : 'room-actions-hidden';
    }
    if (transActions) {
        transActions.className = (state.location === 'transition') ? '' : 'room-actions-hidden';
    }
    if (focusedHud) {
        focusedHud.style.display = (state.location === 'hallway') ? 'block' : 'none';
    }
    
    // Обновляем кнопку запирания двери в комнате
    const btnLockRoom = document.getElementById('btn-lock-room');
    if (btnLockRoom) {
        if (state.samosborSafe) {
            btnLockRoom.innerText = "Отпереть дверь";
            btnLockRoom.classList.remove('glow-green');
            btnLockRoom.classList.add('glow-red');
        } else {
            btnLockRoom.innerText = "Запереть дверь";
            btnLockRoom.classList.remove('glow-red');
            btnLockRoom.classList.add('glow-green');
        }
    }
    
    // Обновляем кнопку противогаза
    const btnMask = document.getElementById('btn-mask');
    if (btnMask) {
        btnMask.innerHTML = state.maskOn
            ? 'Снять противогаз'
            : 'Надеть противогаз';
    }
    
    updateInventoryUI();
}


// --- ГЛАВНЫЙ ИГРОВОЙ ЦИКЛ (TICK КАЖДУЮ СЕКУНДУ) ---

let gameInterval = null;

function startGameLoop() {
    // Очищаем предыдущий цикл, если он был
    if (gameInterval) clearInterval(gameInterval);
    
    gameInterval = setInterval(() => {
        // Пропускаем тик, если игра на паузе или завершена
        if (isGamePaused) return;
        const goScreen = document.getElementById('gameover-screen');
        if (goScreen && goScreen.classList.contains('screen-active')) return;
        
        // 1. РАСХОД ВОДЫ (ЕСТЕСТВЕННАЯ ДЕГИДРАТАЦИЯ)
        state.water = Math.max(0, state.water - 0.15); // медленнее (было 0.4)
        
        // 2. РАСХОД ФИЛЬТРА ПРОТИВОГАЗА / ЗАРАЖЕНИЕ В ЗАРАЖЕННОЙ КВАРТИРЕ И ПРИ УТЕЧКЕ
        const currentDoor = state.focusedDoorIndex !== null ? state.doors[state.focusedDoorIndex] : null;
        const isContaminated = (state.location === 'room' && currentDoor && currentDoor.roomType === 'contaminated');
        const isGasLeakHallway = (state.location === 'hallway' && state.floorEvent === 'gas_leak');
        
        if ((isContaminated || isGasLeakHallway) && !state.maskOn) {
            state.health = Math.max(0, state.health - (isContaminated ? 5 : 4));
            logToConsole(isContaminated ? "Вы вдыхаете зараженный воздух! Срочно наденьте противогаз (клавиша T)!" : "Вы задыхаетесь в коридоре с утечкой газа! Наденьте противогаз (клавиша T)!", "danger");
            playSoundDamage();
            if (state.health <= 0) {
                triggerGameOver("samosbor_gas");
                return;
            }
        }
        
        if (state.maskOn) {
            let decay = 0.6;
            if (isContaminated) decay = 1.8;
            else if (isGasLeakHallway) decay = 1.1;
            
            state.filter = Math.max(0, state.filter - decay);
            if (state.filter <= 0) {
                logToConsole("Фильтр противогаза полностью забился! Маска бесполезна!", "danger");
                state.maskOn = false;
                updateHUD();
            }
        }
        
        // 3. СМЕРТЬ ОТ ОБЕЗВОЖИВАНИЯ
        if (state.water <= 0) {
            state.health -= 2;
            if (state.health <= 0) {
                state.health = 0;
                triggerGameOver("dehydration");
                return;
            }
        }
        
        // 4. ТАЙМЕР САМОСБОРА
        if (state.samosborStatus === 'normal') {
            state.samosborTimeLeft -= 1;
            
            if (state.samosborTimeLeft <= 0) {
                // Переходим к предупреждению
                state.samosborStatus = 'warning';
                state.samosborCountdown = 20;
                logToConsole("[!] ВНИМАНИЕ: Датчики зафиксировали приближение волны Самосбора!", "danger");
                logToConsole("[!] До активной фазы: ~20 секунд. Найдите укрытие!", "danger");
                startSoundSiren();
                
                // Оверлей предупреждения
                const overlay = document.getElementById('samosbor-overlay');
                if (overlay) overlay.className = 'samosbor-warning';
            }
        } else if (state.samosborStatus === 'warning') {
            state.samosborCountdown -= 1;
            
            if (state.samosborCountdown <= 0) {
                // Активная фаза
                state.samosborStatus = 'active';
                state.samosborActiveDuration = 30;
                logToConsole("[!!!] САМОСБОР НАЧАЛСЯ! ТОКСИЧНЫЙ ТУМАН ЗАПОЛНЯЕТ СЕКТОРЫ!", "danger");
                
                const overlay = document.getElementById('samosbor-overlay');
                if (overlay) overlay.className = 'samosbor-active';
            }
        } else if (state.samosborStatus === 'active') {
            state.samosborActiveDuration -= 1;
            
            // Наносим урон, если игрок в коридоре без маски
            if (state.location === 'hallway') {
                if (!state.maskOn) {
                    state.health -= 15;
                    logToConsole("Токсичный туман разъедает ваши легкие!", "danger");
                } else {
                    state.health -= 2;
                    logToConsole("Противогаз защищает от газа, но химикаты разъедают костюм...", "warn");
                }
            } else if (state.location === 'room') {
                if (!state.samosborSafe) {
                    // Незаблокированная комната
                    if (!state.maskOn) {
                        state.health -= 8;
                        logToConsole("Газ проникает под дверь! Вы не заблокировали гермозатвор!", "danger");
                    } else {
                        state.health -= 1;
                    }
                } else {
                    // Заблокированная комната - безопасно
                    logToConsole("Гермозатвор держит. Вы слышите грохот за дверью.", "sys");
                }
            }
            
            // Проверяем смерть
            if (state.health <= 0) {
                state.health = 0;
                if (state.location === 'room' && !state.maskOn) {
                    triggerGameOver("samosbor_gas");
                } else {
                    triggerGameOver("samosbor");
                }
                return;
            }
            
            // Конец Самосбора
            if (state.samosborActiveDuration <= 0) {
                state.samosborStatus = 'normal';
                state.samosborTimeLeft = 60 + Math.floor(Math.random() * 60);
                logToConsole("Датчики показывают нормализацию среды. Самосбор завершился.", "sys");
                stopSoundSiren();
                
                const overlay = document.getElementById('samosbor-overlay');
                if (overlay) overlay.className = 'overlay-hidden';
            }
        }
        
        // 5. ТАЙМЕР МОНСТРА НА ЛЕСТНИЦЕ
        if (state.stairsMonsterActive) {
            state.stairsMonsterTimeLeft -= 1;
            if (state.stairsMonsterTimeLeft <= 0) {
                // Не успели выстрелить — смерть
                triggerGameOver("stairs_monster");
                return;
            }
        }
        
        updateHUD();
        
    }, 1000); // Каждую секунду
}


// --- ИНИЦИАЛИЗАЦИЯ И НАЗНАЧЕНИЕ СОБЫТИЙ ---

function restartGame() {
    isGamePaused = false;
    window._infBatteries = false;
    disableMenuWakeupTheme();
    if (trueEndingAudioInterval) {
        clearInterval(trueEndingAudioInterval);
        trueEndingAudioInterval = null;
    }
    stopAtmosphere();
    if (audioCtx) {
        startAtmosphere();
        startHeartbeatLoop();
    }
    loadKeyBindings();
    
    state = {
        floor: START_FLOOR,
        spawnFloor: START_FLOOR,
        health: MAX_HEALTH,
        water: MAX_WATER,
        ammo: MAX_AMMO,
        filter: MAX_FILTER,
        maskOn: false,
        notesCollected: [false, false, false, false, false, false, false, false, false, false],
        notesRead: [false, false, false, false, false, false, false, false, false, false],
        notesCount: 0,
        samosborStatus: 'normal',
        samosborTimeLeft: 90 + Math.floor(Math.random() * 30),
        samosborCountdown: 20,
        samosborActiveDuration: 30,
        floorsData: {},
        get doors() {
            if (!this.floorsData) {
                this.floorsData = {};
            }
            if (!this.floorsData[this.floor]) {
                getOrGenerateFloorDoors(this.floor);
            }
            return this.floorsData[this.floor].doors;
        },
        set doors(val) {
            if (!this.floorsData) {
                this.floorsData = {};
            }
            this.floorsData[this.floor] = { doors: val };
        },
        focusedDoorIndex: null,
        focusedStairsDoor: false,
        location: 'hallway',
        samosborSafe: false,
        searchProgress: 0,
        isSearching: false,
        stairsMonsterActive: false,
        stairsMonsterTimeLeft: 0,
        audioInit: state.audioInit,
        bottleWater: 100,
        stamina: 100,
        hasHackerTool: false,
        batteries: 0,
        stairsDoors: {},
        keyBindings: state.keyBindings,
        floorEvent: null
    };
    
    // Сброс динамических событий и монстров
    hallwayCrawlerMesh = null;
    deadLiquidatorMesh = null;
    ghostMesh = null;
    deadLiquidatorSearched = false;
    hackActive = false;
    lastBuiltFloor = null;
    
    lastFocusedDoorIndex = undefined;
    lastFocusedStairsDoor = false;
    lastFocusedCorpse = false;
    window.ghostWhispered = false;
    
    // Запуск FPS положения ликвидатора
    playerPos.set(0, 0, -1.0); // Стоим в начале коридора
    playerYaw = 0; // Смотрим строго прямо по коридору
    playerPitch = 0;
    
    for (let i = 0; i < LORE_NOTES.length; i++) {
        const tab = document.getElementById(`note-tab-${i}`);
        if (tab) {
            tab.className = 'btn-note-item btn-note-locked';
            tab.innerText = `Записка ${i + 1}`;
        }
    }
    
    const feed = document.getElementById('log-feed');
    if (feed) feed.innerHTML = '';
    
    document.getElementById('gasmask-overlay').className = 'overlay-hidden';
    document.getElementById('samosbor-overlay').className = 'overlay-hidden';
    document.getElementById('jumpscare-overlay').className = 'overlay-hidden';
    document.getElementById('listening-indicator').className = 'overlay-hidden';
    document.getElementById('room-overlay').className = 'overlay-hidden';
    
    const container = document.getElementById('game-container');
    container.className = '';
    
    document.getElementById('gameover-screen').className = 'panel screen-inactive';
    document.getElementById('splash-screen').className = 'panel screen-inactive';
    document.getElementById('main-interface').className = '';
    
    logToConsole("Начало новой смены ликвидации. Спуск с 1324 этажа...", "sys");
    
    // Генерируем 6 дверей по шансам пользователя
    generateDoorsForFloor();
    
    // Инициализация 3D
    init3D();
    
    updateHUD();
    startGameLoop();
}

// --- АУДИОДВИЖОК (WEB AUDIO API SYNTHESIZER) ---
let audioCtx = null;
let bgmSource = null;
let isAudioInit = false;

let atmosphereOsc = null;
let atmosphereGain = null;
let alarmInterval = null;
let heartbeatInterval = null;

function initAudio() {
    if (state.audioInit) return;
    try {
        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        audioCtx = new AudioContextClass();
        state.audioInit = true;
        
        const inMenu = document.getElementById('splash-screen').classList.contains('screen-active');
        if (ACHIEVEMENTS.awakened && ACHIEVEMENTS.awakened.unlocked && inMenu) {
            playTrueEndingMusic();
        } else {
            startAtmosphere();
            startHeartbeatLoop();
        }
        logToConsole("Аудиосистема шлема ликвидатора инициализирована.", "sys");
    } catch (e) {
        console.error("Не удалось запустить Web Audio API: ", e);
    }
}

function startAtmosphere() {
    if (!audioCtx) return;
    try {
        atmosphereOsc = audioCtx.createOscillator();
        atmosphereGain = audioCtx.createGain();
        const filter = audioCtx.createBiquadFilter();
        
        atmosphereOsc.type = 'sawtooth';
        atmosphereOsc.frequency.value = 55; // Низкая нота Ля (A1)
        
        filter.type = 'lowpass';
        filter.frequency.value = 80;
        
        atmosphereGain.gain.value = 0.05;
        
        atmosphereOsc.connect(filter);
        filter.connect(atmosphereGain);
        atmosphereGain.connect(audioCtx.destination);
        
        atmosphereOsc.start();
    } catch (e) {
        console.error("Failed to start atmosphere sound:", e);
    }
}

function startHeartbeatLoop() {
    if (!audioCtx) return;
    heartbeatInterval = setInterval(() => {
        // Удары сердца: двойной тук
        playThump(60, 0.15);
        setTimeout(() => {
            playThump(55, 0.15);
        }, 250);
    }, 1200);
}

function playThump(freq, duration) {
    if (!audioCtx) return;
    try {
        const now = audioCtx.currentTime;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, now);
        osc.frequency.exponentialRampToValueAtTime(10, now + duration);
        
        gain.gain.setValueAtTime(0.18, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + duration);
        
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        
        osc.start(now);
        osc.stop(now + duration);
    } catch (e) {}
}

function playSoundMonsterHiss() {
    if (!audioCtx) return;
    try {
        const now = audioCtx.currentTime;
        const bufferSize = audioCtx.sampleRate * 1.5;
        const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            data[i] = Math.random() * 2 - 1;
        }
        const noise = audioCtx.createBufferSource();
        noise.buffer = buffer;
        
        const filter = audioCtx.createBiquadFilter();
        filter.type = 'bandpass';
        filter.frequency.setValueAtTime(1000, now);
        filter.frequency.exponentialRampToValueAtTime(120, now + 1.5);
        
        const gain = audioCtx.createGain();
        gain.gain.setValueAtTime(0.15, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 1.5);
        
        noise.connect(filter);
        filter.connect(gain);
        gain.connect(audioCtx.destination);
        
        noise.start(now);
        noise.stop(now + 1.5);
    } catch (e) {}
}

function playSoundDoor(isSlam = false) {
    if (!audioCtx) return;
    try {
        const now = audioCtx.currentTime;
        const duration = isSlam ? 0.6 : 1.2;
        
        // Шум трения гермозатвора
        const bufferSize = audioCtx.sampleRate * duration;
        const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            data[i] = Math.random() * 2 - 1;
        }
        const noise = audioCtx.createBufferSource();
        noise.buffer = buffer;
        
        const filter = audioCtx.createBiquadFilter();
        filter.type = 'bandpass';
        filter.frequency.setValueAtTime(isSlam ? 180 : 320, now);
        filter.Q.value = 2.0;
        
        const gain = audioCtx.createGain();
        gain.gain.setValueAtTime(isSlam ? 0.22 : 0.08, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + duration);
        
        noise.connect(filter);
        filter.connect(gain);
        gain.connect(audioCtx.destination);
        
        noise.start(now);
        noise.stop(now + duration);
        
        if (isSlam) {
            // Низкий удар при закрытии гермодвери
            const osc = audioCtx.createOscillator();
            const oscGain = audioCtx.createGain();

            osc.type = 'triangle';
            osc.frequency.setValueAtTime(80, now);
            osc.frequency.linearRampToValueAtTime(20, now + 0.4);
            
            oscGain.gain.setValueAtTime(0.3, now);
            oscGain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
            
            osc.connect(oscGain);
            oscGain.connect(audioCtx.destination);
            osc.start(now);
            osc.stop(now + 0.4);
        }
    } catch (e) {}
}



function playSoundLoot() {
    if (!audioCtx) return;
    try {
        const now = audioCtx.currentTime;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        
        osc.type = 'sine';
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.setValueAtTime(880, now + 0.08);
        
        gain.gain.setValueAtTime(0.08, now);
        gain.gain.linearRampToValueAtTime(0.08, now + 0.08);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.22);
        
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        
        osc.start(now);
        osc.stop(now + 0.25);
    } catch (e) {}
}

function playSoundMask() {
    if (!audioCtx) return;
    try {
        const now = audioCtx.currentTime;
        const bufferSize = audioCtx.sampleRate * 0.8;
        const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            data[i] = Math.random() * 2 - 1;
        }
        const noise = audioCtx.createBufferSource();
        noise.buffer = buffer;
        
        const filter = audioCtx.createBiquadFilter();
        filter.type = 'bandpass';
        filter.frequency.setValueAtTime(200, now);
        filter.frequency.linearRampToValueAtTime(600, now + 0.4);
        filter.frequency.linearRampToValueAtTime(150, now + 0.8);
        
        const gain = audioCtx.createGain();
        gain.gain.setValueAtTime(0.08, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.8);
        
        noise.connect(filter);
        filter.connect(gain);
        gain.connect(audioCtx.destination);
        
        noise.start(now);
        noise.stop(now + 0.8);
    } catch (e) {}
}

function playSoundDrink() {
    if (!audioCtx) return;
    try {
        const now = audioCtx.currentTime;
        for (let i = 0; i < 3; i++) {
            const time = now + i * 0.22;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            
            osc.type = 'sine';
            osc.frequency.setValueAtTime(220, time);
            osc.frequency.exponentialRampToValueAtTime(120, time + 0.12);
            
            gain.gain.setValueAtTime(0.12, time);
            gain.gain.exponentialRampToValueAtTime(0.001, time + 0.12);
            
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            
            osc.start(time);
            osc.stop(time + 0.18);
        }
    } catch (e) {}
}

function playSoundShot() {
    if (!audioCtx) return;
    try {
        const now = audioCtx.currentTime;
        
        // Шум пороховых газов
        const bufferSize = audioCtx.sampleRate * 0.5;
        const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            data[i] = Math.random() * 2 - 1;
        }
        const noise = audioCtx.createBufferSource();
        noise.buffer = buffer;
        
        const filter = audioCtx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.value = 1200;
        
        const gain = audioCtx.createGain();
        gain.gain.setValueAtTime(0.8, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
        
        noise.connect(filter);
        filter.connect(gain);
        gain.connect(audioCtx.destination);
        
        noise.start(now);
        noise.stop(now + 0.5);
        
        // Низкий хлопок выстрела
        const osc = audioCtx.createOscillator();
        const oscGain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(140, now);
        osc.frequency.linearRampToValueAtTime(30, now + 0.25);
        
        oscGain.gain.setValueAtTime(0.6, now);
        oscGain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
        
        osc.connect(oscGain);
        oscGain.connect(audioCtx.destination);
        osc.start(now);
        osc.stop(now + 0.35);
    } catch (e) {}
}

function playSoundStep() {
    if (!audioCtx) return;
    try {
        const now = audioCtx.currentTime;
        const duration = 0.16;
        
        // Low frequency thump (boot impact)
        const osc = audioCtx.createOscillator();
        const oscGain = audioCtx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(90, now);
        osc.frequency.exponentialRampToValueAtTime(30, now + duration);
        oscGain.gain.setValueAtTime(0.12, now);
        oscGain.gain.exponentialRampToValueAtTime(0.001, now + duration);
        osc.connect(oscGain);
        oscGain.connect(audioCtx.destination);
        osc.start(now);
        osc.stop(now + duration);
        
        // High frequency friction (rubber on concrete)
        const bufferSize = audioCtx.sampleRate * 0.08;
        const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            data[i] = Math.random() * 2 - 1;
        }
        const noise = audioCtx.createBufferSource();
        noise.buffer = buffer;
        
        const filter = audioCtx.createBiquadFilter();
        filter.type = 'bandpass';
        filter.frequency.setValueAtTime(400, now);
        filter.Q.value = 1.0;
        
        const noiseGain = audioCtx.createGain();
        noiseGain.gain.setValueAtTime(0.015, now);
        noiseGain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
        
        noise.connect(filter);
        filter.connect(noiseGain);
        noiseGain.connect(audioCtx.destination);
        
        noise.start(now);
        noise.stop(now + 0.08);
    } catch (e) {}
}

function startSoundSiren() {
    if (!audioCtx) return;
    try {
        stopSoundSiren();
        
        const sirenFunc = () => {
            if (!audioCtx || !state.samosborStatus || state.samosborStatus === 'normal') return;
            const now = audioCtx.currentTime;
            const osc1 = audioCtx.createOscillator();
            const osc2 = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            
            osc1.type = 'sawtooth';
            osc2.type = 'sine';
            
            osc1.frequency.setValueAtTime(280, now);
            osc1.frequency.linearRampToValueAtTime(380, now + 0.7);
            osc1.frequency.linearRampToValueAtTime(280, now + 1.4);
            
            osc2.frequency.setValueAtTime(285, now);
            osc2.frequency.linearRampToValueAtTime(385, now + 0.7);
            osc2.frequency.linearRampToValueAtTime(285, now + 1.4);
            
            gainNode.gain.setValueAtTime(0.01, now);
            gainNode.gain.linearRampToValueAtTime(0.12, now + 0.2);
            gainNode.gain.linearRampToValueAtTime(0.12, now + 1.2);
            gainNode.gain.exponentialRampToValueAtTime(0.001, now + 1.5);
            
            osc1.connect(gainNode);
            osc2.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            
            osc1.start(now);
            osc2.start(now);
            osc1.stop(now + 1.5);
            osc2.stop(now + 1.5);
        };
        
        sirenFunc();
        alarmInterval = setInterval(sirenFunc, 1600);
        
        const canvas = document.getElementById('canvas-holder');
        if (canvas) {
            canvas.requestPointerLock = canvas.requestPointerLock || canvas.mozRequestPointerLock;
            canvas.requestPointerLock();
        }
    } catch (e) {}
}

function stopSoundSiren() {
    if (alarmInterval) {
        clearInterval(alarmInterval);
        alarmInterval = null;
    }
}

// --- ИНТЕГРАЦИЯ YANDEX GAMES SDK ---
let ysdk = null;

function initYandexSDK() {
    console.log("Initializing Yandex Games SDK...");
    const loadingBar = document.getElementById('loading-bar');
    const loadingText = document.getElementById('loading-text');
    const btnStart = document.getElementById('btn-start-game');
    
    // Плавная анимация загрузки (фейковая загрузка до 90% пока инициализируется SDK)
    let progress = 0;
    const progressInterval = setInterval(() => {
        if (progress < 90) {
            progress += 5 + Math.random() * 5;
            if (progress > 90) progress = 90;
            if (loadingBar) loadingBar.style.width = `${progress}%`;
        }
    }, 100);
    
    // Функция успешного завершения инициализации
    const completeInitialization = (modeText) => {
        clearInterval(progressInterval);
        if (loadingBar) loadingBar.style.width = '100%';
        if (loadingText) loadingText.innerText = modeText;
        
        setTimeout(() => {
            const container = document.getElementById('loading-bar-container');
            if (container) {
                container.style.transition = 'opacity 0.5s ease';
                container.style.opacity = '0';
                setTimeout(() => {
                    container.style.display = 'none';
                }, 500);
            }
            if (btnStart) {
                btnStart.removeAttribute('disabled');
                btnStart.classList.remove('btn-disabled');
            }
        }, 600);
    };

    // Таймаут безопасности 3 секунды
    let sdkTimeout = setTimeout(() => {
        console.warn("Yandex Games SDK load timed out. Running in Offline Demo Mode.");
        completeInitialization("РЕЖИМ: ОФФЛАЙН (ДЕМО)");
    }, 3000);

    if (typeof YaGames !== 'undefined') {
        YaGames.init()
            .then(initializedSdk => {
                clearTimeout(sdkTimeout);
                ysdk = initializedSdk;
                console.log("Yandex Games SDK successfully initialized.");
                
                // Сообщаем Yandex SDK, что игра готова к старту
                if (ysdk.features && ysdk.features.LoadingProgress) {
                    ysdk.features.LoadingProgress.ready();
                }
                
                completeInitialization("SDK ГОТОВ");
            })
            .catch(err => {
                clearTimeout(sdkTimeout);
                console.error("Yandex Games SDK init failed:", err);
                completeInitialization("РЕЖИМ: ДЕМО");
            });
    } else {
        clearTimeout(sdkTimeout);
        console.warn("YaGames global object is undefined. Running in Demo Mode.");
        completeInitialization("РЕЖИМ: ДЕМО");
    }
}

function showInterstitialAd() {}

document.addEventListener('DOMContentLoaded', () => {
    loadKeyBindings();
    loadAchievements();
    initYandexSDK();
    
    if (ACHIEVEMENTS.awakened && ACHIEVEMENTS.awakened.unlocked) {
        enableMenuWakeupTheme();
        const startMenuMusicOnInteract = () => {
            initAudio();
            window.removeEventListener('click', startMenuMusicOnInteract);
            window.removeEventListener('keydown', startMenuMusicOnInteract);
        };
        window.addEventListener('click', startMenuMusicOnInteract);
        window.addEventListener('keydown', startMenuMusicOnInteract);
    }
    
    document.getElementById('btn-start-game').addEventListener('click', () => {
        initAudio();
        restartGame();
    });
    
    // Start menu additional buttons
    document.getElementById('btn-open-settings').addEventListener('click', () => {
        populateRebindList();
        document.getElementById('settings-modal').classList.remove('modal-hidden');
    });
    
    document.getElementById('btn-open-about').addEventListener('click', () => {
        document.getElementById('about-modal').classList.remove('modal-hidden');
    });
    
    document.getElementById('btn-open-achievements').addEventListener('click', openAchievementsModal);
    
    document.getElementById('about-close').addEventListener('click', () => {
        document.getElementById('about-modal').classList.add('modal-hidden');
    });
    
    document.getElementById('achievements-close').addEventListener('click', closeAchievementsModal);
    
    document.getElementById('btn-true-ending-restart').addEventListener('click', () => {
        const wakeupScreen = document.getElementById('true-ending-wakeup');
        const whiteout = document.getElementById('true-ending-whiteout');
        const credits = document.getElementById('true-ending-credits');
        if (wakeupScreen) {
            wakeupScreen.style.opacity = '0';
            setTimeout(() => { 
                wakeupScreen.style.display = 'none'; 
                wakeupScreen.classList.add('screen-inactive');
            }, 500);
        }
        if (whiteout) {
            whiteout.style.opacity = '0';
        }
        if (credits) {
            credits.style.opacity = '0';
        }
        if (trueEndingAudioInterval) {
            clearInterval(trueEndingAudioInterval);
            trueEndingAudioInterval = null;
        }
        
        isGamePaused = false;
        if (gameInterval) clearInterval(gameInterval);
        stopSoundSiren();
        stopAtmosphere();
        
        document.getElementById('main-interface').className = 'screen-inactive';
        document.getElementById('splash-screen').className = 'panel screen-active';
        
        if (ACHIEVEMENTS.awakened && ACHIEVEMENTS.awakened.unlocked) {
            enableMenuWakeupTheme();
            playTrueEndingMusic();
        }
        
        const holder = document.getElementById('canvas-holder');
        if (holder) holder.innerHTML = '';
        
        isGamePaused = false;
    });
    
    document.getElementById('settings-close').addEventListener('click', () => {
        document.getElementById('settings-modal').classList.add('modal-hidden');
    });
    
    document.getElementById('btn-rebind-reset').addEventListener('click', () => {
        state.keyBindings = Object.assign({}, DEFAULT_KEY_BINDINGS);
        populateRebindList();
    });
    
    document.getElementById('btn-rebind-save').addEventListener('click', () => {
        saveKeyBindings();
        document.getElementById('settings-modal').classList.add('modal-hidden');
        logToConsole("Настройки управления сохранены.", "sys");
    });
    
    // Pause menu buttons
    document.getElementById('btn-resume-game').addEventListener('click', () => {
        togglePauseGame(false);
    });
    
    document.getElementById('btn-pause-settings').addEventListener('click', () => {
        populateRebindList();
        document.getElementById('settings-modal').classList.remove('modal-hidden');
    });
    
    document.getElementById('btn-exit-menu').addEventListener('click', () => {
        togglePauseGame(false);
        if (gameInterval) clearInterval(gameInterval);
        stopSoundSiren();
        stopAtmosphere();
        
        document.getElementById('main-interface').className = 'screen-inactive';
        document.getElementById('splash-screen').className = 'panel screen-active';
        
        if (ACHIEVEMENTS.awakened && ACHIEVEMENTS.awakened.unlocked) {
            enableMenuWakeupTheme();
            playTrueEndingMusic();
        }
        
        const holder = document.getElementById('canvas-holder');
        if (holder) holder.innerHTML = '';
        
        isGamePaused = false;
    });
    
    document.getElementById('btn-restart').addEventListener('click', restartGame);
    document.getElementById('btn-mask').addEventListener('click', toggleGasMask);
    document.getElementById('btn-drink').addEventListener('click', drinkWater);
    document.getElementById('btn-bag').addEventListener('click', () => openNotesModal());
    
    document.getElementById('btn-listen').addEventListener('click', listenToFocused);
    document.getElementById('btn-open-door').addEventListener('click', interactWithFocused);
    
    document.getElementById('btn-search-room').addEventListener('click', searchRoom);
    document.getElementById('btn-lock-room').addEventListener('click', lockRoom);
    document.getElementById('btn-exit-room').addEventListener('click', exitRoom);
    
    document.getElementById('btn-enter-transition').addEventListener('click', enterTransition);
    document.getElementById('btn-cancel-transition').addEventListener('click', exitRoom);
    
    document.getElementById('modal-close').addEventListener('click', closeNotesModal);
    
    for (let i = 0; i < LORE_NOTES.length; i++) {
        document.getElementById(`note-tab-${i}`).addEventListener('click', () => selectNoteInModal(i));
    }
    
    // Hacking controls
    document.getElementById('hack-tuner-slider').addEventListener('input', updateHackSliderTuner);
    document.getElementById('btn-hack-submit').addEventListener('click', submitHackTuning);
    document.getElementById('btn-hack-cancel').addEventListener('click', () => {
        document.getElementById('hack-modal').classList.add('modal-hidden');
        hackActive = false;
        logToConsole("Взлом прерван игроком.", "warn");
    });
    
    // 3D FPS клавиатура и мышь оглядка
    window.addEventListener('keydown', (e) => {
        if (window.devConsoleOpen) return;
        
        if (hackActive) {
            const pauseKey = state.keyBindings['Pause'] || 'Escape';
            if (e.code === pauseKey) {
                e.preventDefault();
                document.getElementById('hack-modal').classList.add('modal-hidden');
                hackActive = false;
                logToConsole("Взлом прерван игроком.", "warn");
            }
            return;
        }
        
        // Intercept for rebinding
        if (rebindingAction) {
            e.preventDefault();
            e.stopPropagation();
            state.keyBindings[rebindingAction] = e.code;
            const btn = document.querySelector(`.rebind-btn[data-action="${rebindingAction}"]`);
            if (btn) {
                btn.innerText = e.code;
                btn.classList.remove('waiting');
            }
            rebindingAction = null;
            return;
        }
        
        keys[e.code] = true;
        
        // Pause key toggle
        const pauseKey = state.keyBindings['Pause'] || 'Escape';
        if (e.code === pauseKey) {
            e.preventDefault();
            togglePauseGame();
            return;
        }
        
        if (isGamePaused) return;
        
        // Быстрые клавиши взаимодействия
        const interactKey = state.keyBindings['Interact'] || 'KeyR';
        const searchKey = state.keyBindings['Search'] || 'KeyZ';
        const maskKey = state.keyBindings['GasMask'] || 'KeyT';
        const waterKey = state.keyBindings['Water'] || 'KeyQ';
        const bagKey = state.keyBindings['Bag'] || 'KeyG';
        const flashKey = state.keyBindings['Flashlight'] || 'KeyF';
        const listenKey = state.keyBindings['Listen'] || 'KeyE';
        const hackerKey = state.keyBindings['HackerTool'] || 'KeyB';
        
        if (e.code === 'Space') {
            e.preventDefault();
            performPlayerKick();
        }
        
        if (e.code === interactKey) {
            if (state.location === 'hallway') {
                interactWithFocused();
            } else if (state.location === 'room') {
                lockRoom();
            }
        }
        if (e.code === searchKey) {
            if (state.location === 'room' && !state.isSearching) {
                const layout = DOOR_LAYOUT[state.focusedDoorIndex];
                if (layout) {
                    const dirX = layout.x < 0 ? -1 : 1;
                    const cabPos = new THREE.Vector3(layout.x + (5.5 * dirX), 0, layout.z - 2.0);
                    const tablePos = new THREE.Vector3(layout.x + (3.7 * dirX), 0, layout.z);
                    
                    if (playerPos.distanceTo(cabPos) < 3.5 || playerPos.distanceTo(tablePos) < 3.0) {
                        searchRoom();
                    } else {
                        logToConsole("Подойдите ближе к мебели.", "warn");
                    }
                }
            }
        }
        if (e.code === maskKey) {
            toggleGasMask();
        }
        if (e.code === waterKey) {
            drinkWater();
        }
        if (e.code === bagKey) {
            toggleBag();
        }
        if (e.code === flashKey) {
            toggleFlashlight();
        }
        if (e.code === listenKey) {
            listenToFocused();
        }
        if (e.code === hackerKey) {
            useHackerTool();
        }
    });
    
    window.addEventListener('keyup', (e) => {
        if (window.devConsoleOpen) return;
        keys[e.code] = false;
    });
    
    // Выстрел на левую кнопку мыши (ЛКМ) в 3D режиме
    window.addEventListener('mousedown', (e) => {
        if (window.devConsoleOpen || isGamePaused || hackActive) return;
        if (document.pointerLockElement === canvasHolder || pointerLocked) {
            if (e.button === 0 && !state.isSearching) {
                shootPistol();
            }
        }
    });
    
    // Pointer Lock для оглядывания мышей в 3D
    const canvasHolder = document.getElementById('canvas-holder');
    window.addEventListener('click', (e) => {
        if (document.getElementById('main-interface').classList.contains('screen-inactive')) return;
        if (e.target.closest && e.target.closest('.overlay-panel')) return;
        if (e.target.closest && e.target.closest('.hud-overlay')) return;
        if (window.devConsoleOpen || isGamePaused || hackActive) return;
        
        if (!state.isSearching && state.location !== 'notes') {
            canvasHolder.requestPointerLock = canvasHolder.requestPointerLock || canvasHolder.mozRequestPointerLock;
            canvasHolder.requestPointerLock();
        }
    });
    
    document.addEventListener('pointerlockchange', () => {
        pointerLocked = (document.pointerLockElement === canvasHolder);
    });
    
    document.addEventListener('mousemove', (e) => {
        if (hackActive) return;
        if (pointerLocked && !isGamePaused) {
            playerYaw -= e.movementX * sensitivity;
            playerPitch -= e.movementY * sensitivity;
            playerPitch = Math.max(-Math.PI / 2.5, Math.min(Math.PI / 2.5, playerPitch));
        }
    });
    
    // Запасной огляд перетаскиванием мыши / свайпом (для мобилок и ПК без лока)
    let isDragging = false;
    canvasHolder.addEventListener('mousedown', (e) => {
        if (hackActive) return;
        if (!pointerLocked && !isGamePaused) isDragging = true;
    });
    window.addEventListener('mouseup', () => {
        isDragging = false;
    });
    canvasHolder.addEventListener('mousemove', (e) => {
        if (hackActive) return;
        if (isDragging && !pointerLocked && !isGamePaused) {
            playerYaw -= e.movementX * sensitivity * 1.5;
            playerPitch -= e.movementY * sensitivity * 1.5;
            playerPitch = Math.max(-Math.PI / 2.5, Math.min(Math.PI / 2.5, playerPitch));
        }
    });
    
    // Мобильные тач-свайпы для оглядки
    canvasHolder.addEventListener('touchstart', (e) => {
        if (isGamePaused || hackActive) return;
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
    });
    canvasHolder.addEventListener('touchmove', (e) => {
        if (isGamePaused || hackActive) return;
        e.preventDefault();
        const dx = e.touches[0].clientX - touchStartX;
        const dy = e.touches[0].clientY - touchStartY;
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
        
        playerYaw -= dx * 0.008;
        playerPitch -= dy * 0.008;
        playerPitch = Math.max(-Math.PI / 2.5, Math.min(Math.PI / 2.5, playerPitch));
    }, { passive: false });
    
    // Назначение кнопок виртуального D-pad движения
    const setupMobileMoveBtn = (id, flagSetter) => {
        const btn = document.getElementById(id);
        if (!btn) return;
        btn.addEventListener('touchstart', (e) => { e.preventDefault(); flagSetter(true); });
        btn.addEventListener('touchend', (e) => { e.preventDefault(); flagSetter(false); });
        // Для мышки
        btn.addEventListener('mousedown', () => flagSetter(true));
        btn.addEventListener('mouseup', () => flagSetter(false));
        btn.addEventListener('mouseleave', () => flagSetter(false));
    };
    
    setupMobileMoveBtn('btn-v-up', (val) => mvUp = val);
    setupMobileMoveBtn('btn-v-down', (val) => mvDown = val);
    setupMobileMoveBtn('btn-v-left', (val) => mvLeft = val);
    setupMobileMoveBtn('btn-v-right', (val) => mvRight = val);
    
    // Мобильные кнопки взаимодействий
    document.getElementById('btn-v-listen').addEventListener('click', listenToFocused);
    document.getElementById('btn-v-open').addEventListener('click', interactWithFocused);
    document.getElementById('btn-v-shoot').addEventListener('click', shootPistol);
    document.getElementById('btn-v-flash').addEventListener('click', toggleFlashlight);
});

function toggleFlashlight() {
    if (playerFlashlight) {
        playerFlashlight.intensity = playerFlashlight.intensity > 0 ? 0 : 2.5;
        playSoundSwitch();
    }
}

// Клик поstairs на Истинную концовку
const originalDescend = triggerFloorDescent;
document.getElementById('btn-descend').removeEventListener('click', triggerFloorDescent);
// В FPS режиме кнопка HUD "Спуститься на этаж ниже" активна только при собранных записках во время Самосбора для истинной концовки!
// В остальных случаях игрок должен идти на лестницу физически.
setInterval(() => {
    const btnDescend = document.getElementById('btn-descend');
    if (!btnDescend) return;
    
    const allNotesRead = state.notesRead && state.notesRead.every(x => x);
    if (state.notesCount === 10 && allNotesRead && (state.samosborStatus === 'warning' || state.samosborStatus === 'active') && state.location === 'hallway') {
        btnDescend.innerHTML = 'Застыть на месте и ждать';
        btnDescend.className = "btn btn-action glow-blue animate-blink";
        btnDescend.removeAttribute('disabled');
        btnDescend.classList.remove('btn-disabled');
    } else {
        // Выключаем ее, так как идти надо ножками
        btnDescend.innerHTML = 'Идите на лестницу в конце коридора';
        btnDescend.className = "btn btn-action btn-disabled";
        btnDescend.setAttribute('disabled', 'true');
    }
}, 500);

document.getElementById('btn-descend').addEventListener('click', () => {
    const allNotesRead = state.notesRead && state.notesRead.every(x => x);
    if (state.notesCount === 10 && allNotesRead && (state.samosborStatus === 'warning' || state.samosborStatus === 'active')) {
        disableAllControls(true);
        logToConsole("Вы закрыли глаза, расслабились и решили остаться на месте...", "danger");
        
        let tColor = new THREE.Color(0xffffff);
        let tFog = new THREE.FogExp2(0xffffff, 0.05);
        scene.fog = tFog;
        scene.background = tColor;
        renderer.setClearColor(0xffffff);
        
        let flashProgress = 0.05;
        const flashAnim = setInterval(() => {
            flashProgress += 0.05;
            scene.fog.density = flashProgress;
            if (flashProgress >= 1.0) {
                clearInterval(flashAnim);
                triggerGameOver("ending_1");
            }
        }, 100);
        
        if (audioCtx) {
            const now = audioCtx.currentTime;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(220, now);
            osc.frequency.exponentialRampToValueAtTime(880, now + 2.5);
            gain.gain.setValueAtTime(0.01, now);
            gain.gain.linearRampToValueAtTime(0.4, now + 1.0);
            gain.gain.linearRampToValueAtTime(0.4, now + 2.0);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 2.9);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start(now);
            osc.stop(now + 3.0);
        }
    }
});

// Адаптивное поведение при изменении размеров экрана
window.addEventListener('resize', () => {
    if (renderer && camera) {
        const holder = document.getElementById('canvas-holder');
        if (holder) {
            renderer.setSize(holder.clientWidth, holder.clientHeight);
            camera.aspect = holder.clientWidth / holder.clientHeight;
            camera.updateProjectionMatrix();
        }
    }
});

// === DEVELOPER CONSOLE ===
(function() {
    let devConsoleOpen = false;
    const devConsole = document.getElementById('dev-console');
    const devLog = document.getElementById('dev-console-log');
    const devInput = document.getElementById('dev-console-input');
    if (!devConsole || !devLog || !devInput) return;

    const cmdHistory = [];
    let historyIndex = -1;

    function devPrint(text, color) {
        const line = document.createElement('div');
        line.style.color = color || '#00ff00';
        line.style.whiteSpace = 'pre-wrap';
        line.textContent = text;
        devLog.appendChild(line);
        devLog.scrollTop = devLog.scrollHeight;
    }

    function toggleDevConsole() {
        devConsoleOpen = !devConsoleOpen;
        window.devConsoleOpen = devConsoleOpen;
        devConsole.style.display = devConsoleOpen ? 'block' : 'none';
        if (devConsoleOpen) {
            devInput.focus();
            if (document.pointerLockElement) {
                document.exitPointerLock();
            }
            // Clear keys to prevent walking/inputs stuck
            Object.keys(keys).forEach(k => keys[k] = false);
        }
    }

    // Ctrl+Shift+` (Backquote) to toggle
    window.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.shiftKey && (e.code === 'Backquote' || e.key === '~' || e.key === '`')) {
            e.preventDefault();
            e.stopPropagation();
            toggleDevConsole();
            return;
        }
        // Escape closes console
        if (e.code === 'Escape' && devConsoleOpen) {
            e.preventDefault();
            e.stopPropagation();
            toggleDevConsole();
            return;
        }
    }, true);

    // (Capture blockers removed to allow devInput events to pass normally)

    devInput.addEventListener('keydown', (e) => {
        e.stopPropagation();
        if (e.key === 'Enter' || e.code === 'Enter' || e.keyCode === 13) {
            const cmd = devInput.value.trim();
            if (cmd) {
                devPrint('> ' + cmd, '#88ff88');
                cmdHistory.unshift(cmd);
                historyIndex = -1;
                executeDevCommand(cmd);
            }
            devInput.value = '';
        }
        if (e.code === 'ArrowUp') {
            e.preventDefault();
            if (historyIndex < cmdHistory.length - 1) {
                historyIndex++;
                devInput.value = cmdHistory[historyIndex];
            }
        }
        if (e.code === 'ArrowDown') {
            e.preventDefault();
            if (historyIndex > 0) {
                historyIndex--;
                devInput.value = cmdHistory[historyIndex];
            } else {
                historyIndex = -1;
                devInput.value = '';
            }
        }
    });

    function executeDevCommand(raw) {
        const parts = raw.toLowerCase().split(/\s+/);
        const cmd = parts[0];
        const arg1 = parts[1];
        const arg2 = parts[2];

        switch(cmd) {
            case 'help':
                devPrint('=== SAMOSBOR DEV CONSOLE ===');
                devPrint('tp <floor>        - Teleport to floor');
                devPrint('god               - Toggle god mode (no damage)');
                devPrint('heal              - Restore health to max');
                devPrint('give ammo [n]     - Give ammo (default: max)');
                devPrint('give water [n]    - Give water (default: max)');
                devPrint('give filter [n]   - Give filter (default: max)');
                devPrint('give notes        - Collect all lore notes');
                devPrint('noclip            - Toggle noclip mode');
                devPrint('speed <val>       - Set player speed (default 4)');
                devPrint('samosbor          - Trigger samosbor warning');
                devPrint('samosbor stop     - Stop samosbor');
                devPrint('monster           - Spawn stairs monster');
                devPrint('kill              - Kill player');
                devPrint('pos               - Show player position');
                devPrint('doors             - List doors on current floor');
                devPrint('openall           - Open all doors on floor');
                devPrint('rebuild           - Force rebuild 3D scene');
                devPrint('hacker            - Hack tool, 999 batts & infinite batteries');
                devPrint('achievement unlock <id> - Unlock specific achievement');
                devPrint('achievement progress <id> <val> - Progress achievement');
                devPrint('achievement reset - Reset all achievements');
                devPrint('clear             - Clear console');
                break;

            case 'hacker':
                state.hasHackerTool = true;
                state.batteries = 999;
                window._infBatteries = true;
                updateInventoryUI();
                devPrint('Hacker mode enabled! Hacker tool granted, batteries set to 999, infinite battery enabled.');
                break;

            case 'achievement':
                if (arg1 === 'unlock') {
                    if (ACHIEVEMENTS[arg2]) {
                        unlockAchievement(arg2);
                        devPrint('Unlocked achievement: ' + arg2, '#00ff00');
                    } else {
                        devPrint('Unknown achievement ID: ' + arg2, '#ff4444');
                    }
                } else if (arg1 === 'progress') {
                    if (ACHIEVEMENTS[arg2]) {
                        const val = parseInt(parts[3]) || 1;
                        progressAchievement(arg2, val);
                        devPrint('Progressed achievement ' + arg2 + ' by ' + val, '#00ff00');
                    } else {
                        devPrint('Unknown achievement ID: ' + arg2, '#ff4444');
                    }
                } else if (arg1 === 'reset') {
                    for (let id in ACHIEVEMENTS) {
                        ACHIEVEMENTS[id].unlocked = false;
                        ACHIEVEMENTS[id].progress = 0;
                    }
                    saveAchievements();
                    updateAchievementsModalUI();
                    disableMenuWakeupTheme();
                    if (trueEndingAudioInterval) {
                        clearInterval(trueEndingAudioInterval);
                        trueEndingAudioInterval = null;
                    }
                    devPrint('All achievements reset.');
                } else {
                    devPrint('Usage: achievement unlock <id> | progress <id> <val> | reset');
                }
                break;

            case 'tp':
                if (arg1) {
                    const floor = parseInt(arg1);
                    if (!isNaN(floor) && floor >= 1 && floor <= 1324) {
                        state.floor = floor;
                        playerPos.set(0, 0, -1.0);
                        playerYaw = 0;
                        playerPitch = 0;
                        state.location = 'hallway';
                        state.focusedDoorIndex = null;
                        build3DScene();
                        updateHUD();
                        devPrint('Teleported to floor ' + floor, '#00ffff');
                    } else {
                        devPrint('Invalid floor. Range: 1-1324');
                    }
                } else {
                    devPrint('Usage: tp <floor_number>');
                }
                break;

            case 'god':
                window._godMode = !window._godMode;
                if (window._godMode) {
                    // Patch damage functions
                    window._origHealth = state.health;
                    Object.defineProperty(state, 'health', {
                        get: function() { return MAX_HEALTH; },
                        set: function(v) { },
                        configurable: true
                    });
                    devPrint('God mode ON');
                } else {
                    Object.defineProperty(state, 'health', {
                        value: MAX_HEALTH,
                        writable: true,
                        configurable: true
                    });
                    devPrint('God mode OFF');
                }
                updateHUD();
                break;

            case 'heal':
                state.health = MAX_HEALTH;
                updateHUD();
                devPrint('Health restored to ' + MAX_HEALTH, '#00ff00');
                break;

            case 'give':
                if (arg1 === 'ammo') {
                    const n = arg2 ? parseInt(arg2) : MAX_AMMO;
                    state.ammo = Math.min(MAX_AMMO, isNaN(n) ? MAX_AMMO : n);
                    updateHUD();
                    devPrint('Ammo set to ' + state.ammo, '#ffff00');
                } else if (arg1 === 'water') {
                    const n = arg2 ? parseInt(arg2) : MAX_WATER;
                    state.water = Math.min(MAX_WATER, isNaN(n) ? MAX_WATER : n);
                    state.bottleWater = 100;
                    updateHUD();
                    devPrint('Water set to ' + state.water, '#4488ff');
                } else if (arg1 === 'filter') {
                    const n = arg2 ? parseInt(arg2) : MAX_FILTER;
                    state.filter = Math.min(MAX_FILTER, isNaN(n) ? MAX_FILTER : n);
                    updateHUD();
                    devPrint('Filter set to ' + state.filter, '#88ff88');
                } else if (arg1 === 'notes') {
                    const markAsRead = (arg2 === 'read');
                    for (let i = 0; i < LORE_NOTES.length; i++) {
                        state.notesCollected[i] = true;
                        if (markAsRead) {
                            state.notesRead[i] = true;
                        }
                        const tab = document.getElementById('note-tab-' + i);
                        if (tab) {
                            tab.classList.remove('btn-note-locked');
                            tab.innerText = LORE_NOTES[i].title;
                        }
                    }
                    state.notesCount = LORE_NOTES.length;
                    updateHUD();
                    devPrint('All ' + LORE_NOTES.length + ' notes collected' + (markAsRead ? ' and read!' : '!'), '#ffaa00');
                } else {
                    devPrint('Usage: give ammo|water|filter|notes [amount/read]');
                }
                break;

            case 'noclip':
                window._noclip = !window._noclip;
                devPrint('Noclip ' + (window._noclip ? 'ON' : 'OFF'), window._noclip ? '#00ff00' : '#ffaa00');
                break;

            case 'speed':
                if (arg1) {
                    const s = parseFloat(arg1);
                    if (!isNaN(s) && s > 0 && s <= 50) {
                        // We need to modify the const, so we use a workaround
                        window._customSpeed = s;
                        devPrint('Speed set to ' + s + ' (applied next frame)', '#00ffff');
                    } else {
                        devPrint('Invalid speed. Range: 0.1-50');
                    }
                } else {
                    devPrint('Current speed: ' + (window._customSpeed || playerSpeed), '#cccccc');
                }
                break;

            case 'samosbor':
                if (arg1 === 'stop') {
                    state.samosborStatus = 'normal';
                    state.samosborTimeLeft = 999;
                    updateHUD();
                    devPrint('Samosbor stopped');
                } else {
                    state.samosborStatus = 'warning';
                    state.samosborCountdown = 20;
                    updateHUD();
                    devPrint('Samosbor WARNING triggered! 20s until active phase.');
                }
                break;

            case 'monster':
                if (typeof triggerStairsMonster === 'function') {
                    triggerStairsMonster();
                    devPrint('Stairs monster spawned!');
                } else {
                    devPrint('triggerStairsMonster not found');
                }
                break;

            case 'kill':
                state.health = 0;
                if (typeof triggerGameOver === 'function') {
                    triggerGameOver('console_kill');
                }
                devPrint('Player killed.');
                break;

            case 'pos':
                devPrint('Position: X=' + playerPos.x.toFixed(2) + ' Y=' + playerPos.y.toFixed(2) + ' Z=' + playerPos.z.toFixed(2), '#cccccc');
                devPrint('Yaw=' + playerYaw.toFixed(3) + ' Pitch=' + playerPitch.toFixed(3), '#cccccc');
                devPrint('Location: ' + state.location + ' | Floor: ' + state.floor, '#cccccc');
                break;

            case 'doors':
                if (state.doors) {
                    state.doors.forEach((d, i) => {
                        devPrint('[' + i + '] ' + d.name + ' | type=' + d.type + ' | opened=' + d.opened + ' | searched=' + d.searched, '#cccccc');
                    });
                }
                break;

            case 'openall':
                if (state.doors) {
                    state.doors.forEach((d, i) => {
                        if (d.type !== 'empty' && d.type !== 'monster') {
                            d.opened = true;
                        }
                    });
                    build3DScene();
                    updateHUD();
                    devPrint('All safe doors opened.');
                }
                break;

            case 'rebuild':
                build3DScene();
                devPrint('Scene rebuilt.');
                break;

            case 'clear':
                devLog.innerHTML = '';
                break;

            default:
                // Try eval as fallback for advanced debugging
                try {
                    const result = eval(raw);
                    if (result !== undefined) {
                        devPrint(String(result), '#aaaaaa');
                    }
                } catch(err) {
                    devPrint('Unknown command: ' + cmd + '. Type "help" for list.', '#ff4444');
                }
                break;
        }
    }

    devPrint('Developer Console initialized. Type "help" for commands.');
})();

// Patch handleFPSMovement to support noclip and custom speed
const _origHandleFPS = handleFPSMovement;
handleFPSMovement = function(deltaTime) {
    if (hackActive) return;
    // Custom speed override
    if (window._customSpeed) {
        const savedSpeed = playerSpeed;
        // Temporarily override (playerSpeed is const, so we patch moveVector scaling)
        const origFunc = _origHandleFPS;
        
        // Simple noclip: skip collision, allow free movement
        if (window._noclip) {
            if (state.stairsMonsterActive) return;
            const moveVector = new THREE.Vector3();
            if (keys['KeyW'] || keys['ArrowUp'] || mvUp) moveVector.z -= 1;
            if (keys['KeyS'] || keys['ArrowDown'] || mvDown) moveVector.z += 1;
            if (keys['KeyA'] || keys['ArrowLeft'] || mvLeft) moveVector.x -= 1;
            if (keys['KeyD'] || keys['ArrowRight'] || mvRight) moveVector.x += 1;
            if (moveVector.lengthSq() > 0) {
                moveVector.normalize();
                moveVector.applyAxisAngle(new THREE.Vector3(0, 1, 0), playerYaw);
                moveVector.multiplyScalar((window._customSpeed || playerSpeed) * deltaTime);
                playerPos.x += moveVector.x;
                playerPos.z += moveVector.z;
            }
            return;
        }
        
        return origFunc(deltaTime);
    }
    
    if (window._noclip) {
        if (state.stairsMonsterActive) return;
        const moveVector = new THREE.Vector3();
        if (keys['KeyW'] || keys['ArrowUp'] || mvUp) moveVector.z -= 1;
        if (keys['KeyS'] || keys['ArrowDown'] || mvDown) moveVector.z += 1;
        if (keys['KeyA'] || keys['ArrowLeft'] || mvLeft) moveVector.x -= 1;
        if (keys['KeyD'] || keys['ArrowRight'] || mvRight) moveVector.x += 1;
        if (moveVector.lengthSq() > 0) {
            moveVector.normalize();
            moveVector.applyAxisAngle(new THREE.Vector3(0, 1, 0), playerYaw);
            moveVector.multiplyScalar(playerSpeed * deltaTime);
            playerPos.x += moveVector.x;
            playerPos.z += moveVector.z;
        }
        return;
    }
    
    return _origHandleFPS(deltaTime);
};


function playScaryMusic() {
    if (!audioCtx) return;
    const now = audioCtx.currentTime;
    
    // Глубокий, давящий бас (Drone)
    const droneOsc = audioCtx.createOscillator();
    droneOsc.type = 'sawtooth';
    droneOsc.frequency.value = 35; 
    droneOsc.frequency.exponentialRampToValueAtTime(25, now + 10);
    
    const droneGain = audioCtx.createGain();
    droneGain.gain.setValueAtTime(0, now);
    droneGain.gain.linearRampToValueAtTime(0.3, now + 3);
    
    const filter = audioCtx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(150, now);
    filter.frequency.linearRampToValueAtTime(50, now + 10);
    
    droneOsc.connect(filter);
    filter.connect(droneGain);
    droneGain.connect(audioCtx.destination);
    
    droneOsc.start(now);
    
    // Диссонансные аккорды
    [100, 105, 210, 215].forEach(freq => {
        const osc = audioCtx.createOscillator();
        osc.type = 'triangle';
        osc.frequency.value = freq;
        
        const gain = audioCtx.createGain();
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(0.05, now + 4);
        
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        
        osc.start(now);
    });
}
