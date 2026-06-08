import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Add configuration variables at the top of the file
config_str = """
// ==========================================
// 3D MODEL CONFIGURATION (USPS PISTOL)
// Tweak these values if the pistol looks too big, too small, or misaligned.
// ==========================================
const MODEL_SCALE = 0.01; // Change to 1.0 if exported in meters, 0.01 for cm, 0.001 for mm
const MODEL_OFFSET_X = 0; 
const MODEL_OFFSET_Y = -0.05; // Drop it slightly so it sits in hand
const MODEL_OFFSET_Z = 0;
const MODEL_ROTATION_X = 0;
const MODEL_ROTATION_Y = Math.PI; // Usually 3D models point towards +Z, but camera looks at -Z, so rotate 180 degrees
const MODEL_ROTATION_Z = 0;
// ==========================================
"""

if "3D MODEL CONFIGURATION" not in c:
    c = c.replace('"use strict";', '"use strict";' + config_str)
    
    # Now replace the hardcoded values in createPistol
    c = c.replace("model.scale.set(0.01, 0.01, 0.01);", "model.scale.set(MODEL_SCALE, MODEL_SCALE, MODEL_SCALE);")
    c = c.replace("model.position.set(0, 0, 0);", "model.position.set(MODEL_OFFSET_X, MODEL_OFFSET_Y, MODEL_OFFSET_Z);")
    c = c.replace("model.rotation.set(0, Math.PI, 0);", "model.rotation.set(MODEL_ROTATION_X, MODEL_ROTATION_Y, MODEL_ROTATION_Z);")

    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Added configuration block for 3D model.")
else:
    print("Configuration block already exists.")
