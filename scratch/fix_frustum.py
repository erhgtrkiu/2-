import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the entire loading callback with a much more robust version
old_callback = """loader.load('source/USPS.glb', (gltf) => {
        const model = gltf.scene;
        
        // Simple approach: just scale and add directly
        model.scale.set(0.008, 0.008, 0.008);
        model.rotation.set(0, 0, 0);
        model.position.set(0, 0, 0);
        
        model.traverse((child) => {
            if (child.isMesh) {
                child.castShadow = true;
                child.receiveShadow = true;
            }
        });
        
        pistolGroup.add(model);
        
        // Debug: log bounding box so we can fine-tune
        const box = new THREE.Box3().setFromObject(model);
        const size = box.getSize(new THREE.Vector3());
        console.log("PISTOL LOADED. Size after scale:", size);
        console.log("pistolGroup position:", pistolGroup.position);
        console.log("pistolGroup children:", pistolGroup.children.length);"""

new_callback = """loader.load('source/USPS.glb', (gltf) => {
        const model = gltf.scene;
        
        // 1. Measure the raw model BEFORE scaling
        const rawBox = new THREE.Box3().setFromObject(model);
        const rawSize = rawBox.getSize(new THREE.Vector3());
        const rawCenter = rawBox.getCenter(new THREE.Vector3());
        console.log("RAW model size:", rawSize.x, rawSize.y, rawSize.z);
        console.log("RAW model center:", rawCenter.x, rawCenter.y, rawCenter.z);
        
        // 2. Auto-scale: fit longest axis to 0.25 (25cm in game units)
        const maxDim = Math.max(rawSize.x, rawSize.y, rawSize.z);
        const autoScale = maxDim > 0 ? 0.25 / maxDim : 1;
        model.scale.set(autoScale, autoScale, autoScale);
        
        // 3. Center the model on pistolGroup origin
        model.position.set(
            -rawCenter.x * autoScale,
            -rawCenter.y * autoScale, 
            -rawCenter.z * autoScale
        );
        
        // 4. Force all meshes to use a visible material if original fails
        model.traverse((child) => {
            if (child.isMesh) {
                child.castShadow = true;
                child.receiveShadow = true;
                child.frustumCulled = false; // CRITICAL: prevent Three.js from hiding it
                // If material has no map, force a fallback color
                if (child.material && !child.material.map) {
                    child.material.color = new THREE.Color(0x333333);
                    child.material.metalness = 0.7;
                    child.material.roughness = 0.4;
                }
                child.material.needsUpdate = true;
            }
        });
        
        pistolGroup.add(model);
        
        // Also disable frustum culling on pistolGroup itself
        pistolGroup.traverse((child) => {
            child.frustumCulled = false;
        });
        
        // Debug
        const box = new THREE.Box3().setFromObject(pistolGroup);
        const size = box.getSize(new THREE.Vector3());
        console.log("PISTOL FINAL size:", size.x.toFixed(4), size.y.toFixed(4), size.z.toFixed(4));
        console.log("PISTOL autoScale:", autoScale);
        console.log("pistolGroup world pos:", pistolGroup.getWorldPosition(new THREE.Vector3()));"""

c = c.replace(old_callback, new_callback)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Injected robust loader with frustumCulled=false and detailed debug.")
