import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

old_traverse = """        // 4. Force ALL meshes visible with debug material
        let meshCount = 0;
        model.traverse((child) => {
            if (child.isMesh) {
                meshCount++;
                child.castShadow = true;
                child.receiveShadow = true;
                child.frustumCulled = false;
                // Force double-sided rendering
                if (child.material) {
                    child.material.side = THREE.DoubleSide;
                    child.material.needsUpdate = true;
                }
                console.log("Mesh " + meshCount + ":", child.name, "geo verts:", child.geometry.attributes.position ? child.geometry.attributes.position.count : "NONE");
            }
        });
        console.log("Total meshes in model:", meshCount);"""

new_traverse = """        // 4. FORCE REPLACE all materials with bright visible material
        const debugMat = new THREE.MeshStandardMaterial({ 
            color: 0x222222, 
            roughness: 0.4, 
            metalness: 0.8, 
            side: THREE.DoubleSide 
        });
        let meshCount = 0;
        model.traverse((child) => {
            if (child.isMesh) {
                meshCount++;
                child.material = debugMat;
                child.castShadow = true;
                child.receiveShadow = true;
                child.frustumCulled = false;
                console.log("Mesh " + meshCount + ":", child.name, "verts:", child.geometry.attributes.position.count);
            }
        });
        console.log("Total meshes:", meshCount, "All materials replaced.");"""

c = c.replace(old_traverse, new_traverse)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Forced material replacement with MeshStandardMaterial.")
