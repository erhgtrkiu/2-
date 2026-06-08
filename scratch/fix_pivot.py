import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

old_block = """    loader.load('source/USPS.glb', (gltf) => {
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
        
        // Rotate: barrel was pointing +Y, rotate to point -Z (forward)
        model.rotation.set(-Math.PI / 2, 0, Math.PI);"""

new_block = """    loader.load('source/USPS.glb', (gltf) => {
        const model = gltf.scene;
        
        // 1. Scale, rotate, then center (in that order!)
        const rawBox = new THREE.Box3().setFromObject(model);
        const rawSize = rawBox.getSize(new THREE.Vector3());
        const maxDim = Math.max(rawSize.x, rawSize.y, rawSize.z);
        const autoScale = maxDim > 0 ? 0.25 / maxDim : 1;
        
        // Put model in a pivot group so we can rotate cleanly
        const pivot = new THREE.Group();
        pivot.add(model);
        
        // Scale and rotate the pivot
        pivot.scale.set(autoScale, autoScale, autoScale);
        pivot.rotation.set(-Math.PI / 2, 0, Math.PI);
        
        // Force matrix update so bounding box is correct
        pivot.updateMatrixWorld(true);
        
        // Now measure the rotated+scaled model and center it
        const finalBox = new THREE.Box3().setFromObject(pivot);
        const finalCenter = finalBox.getCenter(new THREE.Vector3());
        const finalSize = finalBox.getSize(new THREE.Vector3());
        pivot.position.set(-finalCenter.x, -finalCenter.y, -finalCenter.z);
        
        console.log("PISTOL size after transform:", finalSize.x.toFixed(3), finalSize.y.toFixed(3), finalSize.z.toFixed(3));"""

c = c.replace(old_block, new_block)

# Also update pistolGroup.add to add pivot instead of model
c = c.replace("pistolGroup.add(model);", "pistolGroup.add(pivot);")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Rewrote: scale -> rotate -> center using pivot group.")
