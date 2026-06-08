import sys

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

s = c.find('// Slide/Barrel')
e = c.find('pistolGroup.position.set(0.18, -0.16, -0.32);')

if s != -1 and e != -1:
    new_code = """
// --- Asynchronous Model Loading ---
if (typeof THREE.GLTFLoader !== 'undefined') {
    const loader = new THREE.GLTFLoader();
    loader.load('source/USPS.glb', (gltf) => {
        const model = gltf.scene;
        
        // Setup scaling, position, and rotation
        // NOTE: These values might need tuning depending on the 3D model's origin and scale.
        model.scale.set(0.01, 0.01, 0.01);
        model.position.set(0, 0, 0);
        model.rotation.set(0, Math.PI, 0); // Pointing forward usually requires 180 deg turn on Y
        
        // Set shadows and materials
        model.traverse((child) => {
            if (child.isMesh) {
                child.castShadow = true;
                child.receiveShadow = true;
            }
        });
        
        // Add to pistolGroup so recoil and movements apply automatically
        pistolGroup.add(model);
        console.log("External pistol model loaded successfully.");
    }, undefined, (error) => {
        console.error("Failed to load USPS.glb. Make sure you are running via a local web server (CORS error) or check file path.", error);
    });
} else {
    console.error("GLTFLoader not found!");
}

// Keep the laser module
const laserGeo = new THREE.CylinderGeometry(0.007, 0.007, 0.07, 8);
const laser = new THREE.Mesh(laserGeo, new THREE.MeshStandardMaterial({ color: 0x22252a }));
laser.rotation.x = Math.PI / 2;
laser.position.set(0, -0.022, -0.05);
pistolGroup.add(laser);

const lensGeo = new THREE.CylinderGeometry(0.004, 0.004, 0.002, 8);
const lens = new THREE.Mesh(lensGeo, laserSightMat);
lens.rotation.x = Math.PI / 2;
lens.position.set(0, -0.022, -0.086);
pistolGroup.add(lens);

"""
    c = c[:s] + new_code + c[e:]
    
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Replaced createPistol logic with GLTFLoader.")
else:
    print("Could not find insertion points in app.js!")
