import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# The model loaded but is way too big. Reduce auto-scale target from 0.3 to 0.12
c = c.replace(
    "const scale = maxDim > 0 ? 0.3 / maxDim : 1;",
    "const scale = maxDim > 0 ? 0.12 / maxDim : 1;"
)

# Reposition wrapper: push it to the right, down, and forward like a proper FPS gun
c = c.replace(
    "wrapper.position.set(0, -0.05, 0);",
    "wrapper.position.set(0.15, -0.12, -0.2);"
)

# Keep rotation pointing forward
c = c.replace(
    "wrapper.rotation.set(0, Math.PI, 0);",
    "wrapper.rotation.set(0, -Math.PI / 2, 0);"
)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Adjusted scale and position.")
