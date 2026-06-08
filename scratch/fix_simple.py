import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Find and replace the entire model loading block
old_start = '// --- Asynchronous Model Loading ---'
old_end = '// Laser module removed'

s = c.find(old_start)
e = c.find(old_end)

if s != -1 and e != -1:
    e = e + len(old_end)
    
    new_block = """// --- Load 3D Pistol Model ---
if (typeof THREE.GLTFLoader !== 'undefined') {
    const loader = new THREE.GLTFLoader();
    loader.load('source/USPS.glb', (gltf) => {
        const model = gltf.scene;
        
        // Simple approach: just scale and add directly
        model.scale.set(0.004, 0.004, 0.004);
        model.rotation.set(0, -Math.PI/2, 0);
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
        console.log("pistolGroup children:", pistolGroup.children.length);
    }, 
    (progress) => {
        console.log("Loading USPS.glb:", Math.round(progress.loaded / progress.total * 100) + "%");
    },
    (error) => {
        console.error("PISTOL LOAD ERROR:", error);
    });
} else {
    console.error("GLTFLoader not available!");
}
// --- End pistol model ---"""

    c = c[:s] + new_block + c[e:]
    
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Replaced with simplified loader.")
else:
    print(f"Could not find block. start={s}, end={e}")
