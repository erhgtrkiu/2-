import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Try the original pistolGroup position values and experiment with rotation
c = c.replace(
    "wrapper.position.set(0.15, -0.12, -0.2);",
    "wrapper.position.set(0.18, -0.15, -0.3);"
)

# Try no rotation first so we can see which way the model is pointing
c = c.replace(
    "wrapper.rotation.set(0, -Math.PI / 2, 0);",
    "wrapper.rotation.set(0, 0, 0);"
)

# Make the model a bit bigger so we can actually see it
c = c.replace(
    "const scale = maxDim > 0 ? 0.12 / maxDim : 1;",
    "const scale = maxDim > 0 ? 0.18 / maxDim : 1;"
)

# Add debug logging so we know what's happening
c = c.replace(
    'console.log("External pistol model auto-scaled, centered, and loaded successfully.");',
    'console.log("Pistol loaded! BBox size:", size, "Scale applied:", scale, "Center:", center);'
)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Adjusted position, rotation, and scale.")
