import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

with open('temp_cutscene.txt', 'r', encoding='utf-8') as f:
    old_cutscene_block = f.read()

# We just want to replace up to "// Visually shift environment"
s = old_cutscene_block.find('// Visually shift environment')
if s != -1:
    old_target = old_cutscene_block[:s] + '// Visually shift environment'
    
    new_target = """function triggerSpawnSamosbor() {
    state.spawnSamosborActive = true;
    state.cutsceneActive = true;
    state.cutscenePitch = playerPitch;
    state.cutsceneYaw = playerYaw;
    disableAllControls(true);

    // Hide HUD elements
    document.querySelectorAll('.overlay-ui, #crosshair, #mobile-controls-container, #listening-indicator, #room-overlay, #hud-container, #action-prompt, #interaction-prompt').forEach(el => {
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

    if old_target in c:
        c = c.replace(old_target, new_target)
        with open(app_path, 'w', encoding='utf-8') as f:
            f.write(c)
        print("Cutscene patched.")
    else:
        print("Failed to find exact block in app.js")
else:
    print("Could not parse temp_cutscene.txt properly.")
