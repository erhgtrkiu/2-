import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Fix 1: Slider initial value
bad_slider_code = "typeof mouseSensMultiplier !== 'undefined' ? sensitivity :"
good_slider_code = "typeof mouseSensMultiplier !== 'undefined' ? mouseSensMultiplier :"
if bad_slider_code in c:
    c = c.replace(bad_slider_code, good_slider_code)

# Fix 2: triggerSpawnSamosbor cutscene logic
old_cutscene_block = """function triggerSpawnSamosbor() {
    state.spawnSamosborActive = true;
    state.cutsceneActive = true;
    state.cutscenePitch = playerPitch;
    state.cutsceneYaw = playerYaw;
    disableAllControls(true);

    // Visually shift environment"""

new_cutscene_block = """function triggerSpawnSamosbor() {
    state.spawnSamosborActive = true;
    state.cutsceneActive = true;
    state.cutscenePitch = playerPitch;
    state.cutsceneYaw = playerYaw;
    disableAllControls(true);

    // Hide HUD elements
    document.querySelectorAll('.overlay-ui, #crosshair, #mobile-controls-container, #listening-indicator, #room-overlay').forEach(el => {
        if (el) el.style.display = 'none';
    });
    
    // Drop pistol
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

if old_cutscene_block in c:
    c = c.replace(old_cutscene_block, new_cutscene_block)
else:
    print("WARNING: Could not find old_cutscene_block")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Patch applied.")
