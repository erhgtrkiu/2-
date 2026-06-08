import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the wrapper position/rotation that references undefined MODEL_* variables
c = c.replace(
    "wrapper.position.set(MODEL_OFFSET_X, MODEL_OFFSET_Y, MODEL_OFFSET_Z);",
    "wrapper.position.set(0, -0.05, 0);"
)
c = c.replace(
    "wrapper.rotation.set(MODEL_ROTATION_X, MODEL_ROTATION_Y, MODEL_ROTATION_Z);",
    "wrapper.rotation.set(0, Math.PI, 0);"
)

# Also remove the old laser/lens since the new model has its own barrel
# and the laser cylinder is the ugly thing showing on screen
c = c.replace(
    """// Keep the laser module
const laserGeo = new THREE.CylinderGeometry(0.007, 0.007, 0.07, 8);
const laser = new THREE.Mesh(laserGeo, new THREE.MeshStandardMaterial({ color: 0x22252a }));
laser.rotation.x = Math.PI / 2;
laser.position.set(0, -0.022, -0.05);
pistolGroup.add(laser);

const lensGeo = new THREE.CylinderGeometry(0.004, 0.004, 0.002, 8);
const lens = new THREE.Mesh(lensGeo, laserSightMat);
lens.rotation.x = Math.PI / 2;
lens.position.set(0, -0.022, -0.086);
pistolGroup.add(lens);""",
    "// Laser module removed — using full 3D model instead"
)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed: removed undefined MODEL_ variables, removed old laser mesh.")
