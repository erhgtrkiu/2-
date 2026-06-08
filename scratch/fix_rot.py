import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Rotate the model so barrel points forward (-Z) instead of up (+Y)
# The Y axis is the longest = barrel. Rotate -90deg on X to point it forward.
c = c.replace(
    "model.rotation.set(0, 0, 0);",
    "model.rotation.set(-Math.PI / 2, 0, 0);"
)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Rotated model -90deg on X axis.")
