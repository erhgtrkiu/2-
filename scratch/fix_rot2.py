import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Add rotation right after the position.set block
old_pos = """        model.position.set(
            -rawCenter.x * autoScale,
            -rawCenter.y * autoScale, 
            -rawCenter.z * autoScale
        );"""

new_pos = """        model.position.set(
            -rawCenter.x * autoScale,
            -rawCenter.y * autoScale, 
            -rawCenter.z * autoScale
        );
        
        // Rotate: barrel was pointing +Y, rotate to point -Z (forward)
        model.rotation.set(-Math.PI / 2, 0, Math.PI);"""

c = c.replace(old_pos, new_pos)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Added rotation after position set.")
