import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

old_rot = "pivot.rotation.set(Math.PI, -Math.PI, 0);"
new_rot = "pivot.rotation.set(-Math.PI / 2, -Math.PI / 2, 0);"

c = c.replace(old_rot, new_rot)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Set rotation to X: -90, Y: -90")
