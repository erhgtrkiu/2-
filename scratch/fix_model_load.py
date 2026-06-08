import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

s = c.find('// --- Asynchronous Model Loading ---')
e = c.find('// Keep the laser module')

if s != -1 and e != -1:
    new_code = """// --- Asynchronous Model Loading ---
if (typeof THREE.GLTFLoader !== 'undefined') {
    const loader = new THREE.GLTFLoader();
    loader.load('source/USPS.glb', (gltf) => {
        const model = gltf.scene;
        
        // 1. Calculate bounding box to find the true size and center of the model
        const box = new THREE.Box3().setFromObject(model);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());
        
        // 2. Auto-scale: Make the longest dimension exactly 0.3 units (30 cm)
        const maxDim = Math.max(size.x, size.y, size.z);
        const scale = maxDim > 0 ? 0.3 / maxDim : 1;
        model.scale.set(scale, scale, scale);
        
        // 3. Auto-center: Move the model so its center aligns with (0,0,0)
        model.position.set(-center.x * scale, -center.y * scale, -center.z * scale);
        
        // 4. Wrap it in a group so user offsets apply cleanly on top of the centered model
        const wrapper = new THREE.Group();
        wrapper.add(model);
        wrapper.position.set(MODEL_OFFSET_X, MODEL_OFFSET_Y, MODEL_OFFSET_Z);
        wrapper.rotation.set(MODEL_ROTATION_X, MODEL_ROTATION_Y, MODEL_ROTATION_Z);
        
        // Ensure shadows are enabled
        model.traverse((child) => {
            if (child.isMesh) {
                child.castShadow = true;
                child.receiveShadow = true;
            }
        });
        
        pistolGroup.add(wrapper);
        console.log("External pistol model auto-scaled, centered, and loaded successfully.");
    }, undefined, (error) => {
        console.error("Failed to load USPS.glb.", error);
        
        // Show visible error on screen so the user knows it failed!
        const errDiv = document.createElement('div');
        errDiv.style.position = 'absolute';
        errDiv.style.top = '10%';
        errDiv.style.left = '50%';
        errDiv.style.transform = 'translate(-50%, -50%)';
        errDiv.style.color = '#ff4444';
        errDiv.style.fontSize = '20px';
        errDiv.style.background = 'rgba(0,0,0,0.8)';
        errDiv.style.padding = '15px';
        errDiv.style.border = '2px solid red';
        errDiv.style.zIndex = '9999';
        errDiv.style.fontFamily = 'monospace';
        errDiv.innerHTML = '<b>ОШИБКА ЗАГРУЗКИ МОДЕЛИ PISTOL!</b><br>USPS.glb не загрузился.<br>Скорее всего вы открыли игру без локального сервера (CORS error).<br>Запустите через Live Server!';
        document.body.appendChild(errDiv);
    });
} else {
    console.error("GLTFLoader not found!");
}

"""
    c = c[:s] + new_code + c[e:]
    
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Auto-scale and error handling injected.")
else:
    print("Could not find the insertion points.")
