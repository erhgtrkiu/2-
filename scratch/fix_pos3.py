import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Wrapper should be at 0,0,0 — pistolGroup already has the correct FPS position
c = c.replace(
    "wrapper.position.set(0.18, -0.15, -0.3);",
    "wrapper.position.set(0, 0, 0);"
)

# No extra rotation on wrapper — pistolGroup already has correct rotation
c = c.replace(
    "wrapper.rotation.set(0, 0, 0);",
    "// rotation will be fine-tuned after seeing the model orientation"
)

# Keep scale reasonable
c = c.replace(
    "const scale = maxDim > 0 ? 0.18 / maxDim : 1;",
    "const scale = maxDim > 0 ? 0.25 / maxDim : 1;"
)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed: wrapper at origin, pistolGroup handles positioning.")
