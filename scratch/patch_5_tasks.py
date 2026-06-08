import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

app_path = r'C:\Users\m3615\samosbor_game\app.js'
index_path = r'C:\Users\m3615\samosbor_game\index.html'

with open(app_path, 'r', encoding='utf-8') as f:
    app_content = f.read()

with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

# --- 1. Fix index.html SDK and settings ---
# Remove Yandex SDK script tag
index_content = re.sub(r'<script src="https://yandex\.ru/games/sdk/v2"></script>\s*', '', index_content)

# Add sensitivity slider
if 'sens-slider' not in index_content:
    sens_html = """
            <div class="setting-item">
                <label data-i18n="sens_label">Mouse Sensitivity:</label>
                <input type="range" id="sens-slider" min="0.1" max="5.0" step="0.1" value="1.0">
            </div>"""
    index_content = index_content.replace('<div class="setting-item">', sens_html + '\n            <div class="setting-item">', 1)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(index_content)

# --- 2. Fix app.js SDK, Cutscene, Translation, Samosbor distortion, Sensitivity ---

# Sensitivity logic
if 'let sensitivity = parseFloat(localStorage.getItem(\'samosbor_sensitivity\')) || 1.0;' not in app_content:
    app_content = app_content.replace('let playerYaw = 0;', 'let playerYaw = 0;\nlet sensitivity = parseFloat(localStorage.getItem(\'samosbor_sensitivity\')) || 1.0;')

# Update mouse handlers
app_content = app_content.replace('playerYaw -= e.movementX * 0.002;', 'playerYaw -= e.movementX * 0.002 * sensitivity;')
app_content = app_content.replace('playerYaw -= e.movementX * 0.003;', 'playerYaw -= e.movementX * 0.003 * sensitivity;')

# Cutscene fix
cutscene_replacement = """function triggerSpawnSamosbor() {
    state.spawnSamosborActive = true;
    state.cutsceneActive = true;
    state.cutscenePitch = playerPitch;
    state.cutsceneYaw = playerYaw;
    disableAllControls(true);

    // Hide HUD and drop pistol
    document.querySelectorAll('.overlay-ui, #crosshair, #mobile-controls-container, #listening-indicator, #room-overlay').forEach(el => {
        if (el) el.style.display = 'none';
    });
    
    let pistol = camera.getObjectByName('pistol');
    if (pistol) {
        pistol.visible = false;
        let droppedPistol = pistol.clone();
        droppedPistol.visible = true;
        scene.add(droppedPistol);
        let forward = new THREE.Vector3(0, 0, -1).applyQuaternion(camera.quaternion);
        forward.y = 0; forward.normalize();
        let left = new THREE.Vector3().crossVectors(new THREE.Vector3(0,1,0), forward).normalize();
        let dropPos = camera.position.clone().add(forward.multiplyScalar(1.2)).add(left.multiplyScalar(0.4));
        dropPos.y = 0.1;
        droppedPistol.position.copy(dropPos);
        droppedPistol.rotation.set(-Math.PI/2, 0, Math.random() * Math.PI);
    }

    // Visually shift environment"""

app_content = app_content.replace("""function triggerSpawnSamosbor() {
    state.spawnSamosborActive = true;
    state.cutsceneActive = true;
    state.cutscenePitch = playerPitch;
    state.cutsceneYaw = playerYaw;
    disableAllControls(true);

    // Visually shift environment""", cutscene_replacement)

# SDK async
sdk_old = """if (typeof YaGames !== 'undefined') {
        YaGames.init()"""

sdk_new = """let script = document.createElement('script');
    script.src = "https://yandex.ru/games/sdk/v2";
    script.onload = () => {
        if (typeof YaGames !== 'undefined') {
            YaGames.init()"""

sdk_catch_old = """})
            .catch(err => {"""

sdk_catch_new = """})
            .catch(err => {"""

if 'document.createElement(\'script\')' not in app_content and sdk_old in app_content:
    app_content = app_content.replace(sdk_old, sdk_new)
    
    # Close the script tag logic
    catch_block_end = app_content.find('completeInitialization("РЕЖИМ: ОФФЛАЙН (ОШИБКА)");', app_content.find(sdk_catch_new))
    if catch_block_end != -1:
        insert_idx = app_content.find('}', catch_block_end) + 1
        app_content = app_content[:insert_idx] + """
        }
    };
    script.onerror = () => {
        clearTimeout(sdkTimeout);
        console.error("Yandex SDK load failed");
        completeInitialization("РЕЖИМ: ОФФЛАЙН (ОШИБКА СЕТИ)");
    };
    document.head.appendChild(script);""" + app_content[insert_idx:]

# Full translation binding when language changes
if 'function changeLanguage(lang)' in app_content:
    lang_patch = """function changeLanguage(lang) {
    applyLanguage(lang);
    localStorage.setItem('samosbor_lang', lang);"""
    app_content = re.sub(r'function changeLanguage\(lang\)\s*\{', lang_patch, app_content)

# Camera distortion fix during samosbor (if there's screen shake or FOV)
if 'camera.fov = 75 + Math.sin(Date.now() * 0.01) * 5;' in app_content:
    app_content = app_content.replace('camera.fov = 75 + Math.sin(Date.now() * 0.01) * 5;', 
        'if (state.location === "hallway") camera.fov = 75 + Math.sin(Date.now() * 0.01) * 5;')

# Wait, let's just make a generic patch for Samosbor screen shake
shake_old = 'camera.position.y = 1.6 + Math.sin(Date.now() * 0.05) * 0.05;'
shake_new = 'if (state.location === "hallway") camera.position.y = 1.6 + Math.sin(Date.now() * 0.05) * 0.05;'
if shake_old in app_content:
    app_content = app_content.replace(shake_old, shake_new)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(app_content)

print("Patched app.js and index.html successfully.")
