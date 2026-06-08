import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Increase scale significantly - 0.004 was invisible, first time ~0.01 was huge
# Try 0.008 as middle ground
c = c.replace(
    "model.scale.set(0.004, 0.004, 0.004);",
    "model.scale.set(0.008, 0.008, 0.008);"
)

# No rotation at all first - let's just SEE the model
c = c.replace(
    "model.rotation.set(0, -Math.PI/2, 0);",
    "model.rotation.set(0, 0, 0);"
)

# Also reduce camera near plane so close objects don't get clipped
# Find where camera is created
old_cam = "new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)"
new_cam = "new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.01, 1000)"
if old_cam in c:
    c = c.replace(old_cam, new_cam)
    print("Also reduced camera near plane from 0.1 to 0.01")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Scale set to 0.008, rotation zeroed, near plane reduced.")
