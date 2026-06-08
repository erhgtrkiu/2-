import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the material traversal to force bright red BasicMaterial + DoubleSide
old_traverse = """        // 4. Force all meshes to use a visible material if original fails
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
        });"""

new_traverse = """        // 4. Force ALL meshes visible with debug material
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

c = c.replace(old_traverse, new_traverse)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Applied DoubleSide + mesh debug logging.")
