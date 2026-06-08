import sys

with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

chunks = [
    # Chunk 1
    ("""// Глобальные переменные света
let doorLights = {};
let playerFlashlight = null;
let warningBeacons = [];
let warningLights = [];

// --- РАЗНООБРАЗИЕ ГЕЙМПЛЕЯ: НОВЫЕ ПЕРЕМЕННЫЕ ---""", 13, 20),
    # Chunk 2
    ("""    // Стены лестничного колодца
    const shaftL = new THREE.Mesh(new THREE.BoxGeometry(0.2, 10.0, 7.5), wallMat);
    shaftL.position.set(-1.6, baseY, -45.75);
    shaftL.receiveShadow = true;
    shaftL.castShadow = true;
    scene.add(shaftL);
    staircaseMeshes.push(shaftL);
    
    const shaftR = new THREE.Mesh(new THREE.BoxGeometry(0.2, 10.0, 7.5), wallMat);
    shaftR.position.set(1.6, baseY, -45.75);
    shaftR.receiveShadow = true;
    shaftR.castShadow = true;
    scene.add(shaftR);
    staircaseMeshes.push(shaftR);
    
    const shaftB = new THREE.Mesh(new THREE.BoxGeometry(3.2, 10.0, 0.2), wallMat);
    shaftB.position.set(0, baseY, -49.6);
    shaftB.receiveShadow = true;
    shaftB.castShadow = true;
    scene.add(shaftB);
    staircaseMeshes.push(shaftB);
    
    // Потолок лестничного колодца
    const stairsCeiling = new THREE.Mesh(new THREE.BoxGeometry(3.4, 0.2, 7.6), ceilingMat);
    stairsCeiling.position.set(0, baseY + 5.1, -45.8);
    stairsCeiling.receiveShadow = true;
    stairsCeiling.castShadow = true;
    scene.add(stairsCeiling);
    staircaseMeshes.push(stairsCeiling);""", 2790, 2818),
    # Chunk 3
    ("""        if (distMoved > 0.01) {
            footstepTimeAccumulator += deltaTime;
            const finalSpd = window._customSpeed || currentSpeed;
            const stepInterval = Math.max(0.2, 1.5 / finalSpd);
            if (footstepTimeAccumulator >= stepInterval) {
                playSoundStep();
                footstepTimeAccumulator = 0;
            }""", 3835, 3843),
    # Chunk 4
    ("""function openNotesModal(autoSelectId = null) {
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
}""", 5524, 5543),
    # Chunk 5
    ("""        menuNatureCanvas.style.opacity = '0.55';
        menuNatureCanvas.style.filter = 'blur(10px)';""", 5661, 5663),
    # Chunk 7 (skip 6 for now or keep in order)
    ("""function playSoundDoor(isSlam = false) {
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
}""", 6721, 6771),
    # Chunk 8
    ("""function playSoundShot() {
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
}""", 6855, 6900),
    # Chunk 9
    ("""function playSoundStep() {
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
}""", 6902, 6947),
    # Chunk 10
    ("""    window.addEventListener('click', (e) => {
        if (document.getElementById('main-interface').classList.contains('screen-inactive')) return;
        if (e.target.closest && e.target.closest('.overlay-panel')) return;
        if (e.target.closest && e.target.closest('.hud-overlay')) return;
        if (window.devConsoleOpen || isGamePaused || hackActive) return;
        
        if (!state.isSearching && state.location !== 'notes') {
            canvasHolder.requestPointerLock = canvasHolder.requestPointerLock || canvasHolder.mozRequestPointerLock;
            canvasHolder.requestPointerLock();
        }
    });""", 7357, 7367)
]

for idx, (target, start, end) in enumerate(chunks):
    if target not in content:
        print(f"Chunk {idx+1} not found in file content!")
        # Print a snippet of where it might be
        lines = content.splitlines()
        print("Lines near expected range:")
        for l_num in range(max(1, start - 5), min(len(lines), end + 5)):
            print(f"{l_num}: {lines[l_num-1]}")
        sys.exit(1)
    else:
        print(f"Chunk {idx+1} matches perfectly!")

print("All chunks validated successfully!")
