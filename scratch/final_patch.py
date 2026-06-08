import os
import re

app_path = r'C:\Users\m3615\samosbor_game\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Fix Cutscene to hide main-interface completely
old_cutscene_block = """    // Hide HUD elements
    document.querySelectorAll('.overlay-ui, #crosshair, #mobile-controls-container, #listening-indicator, #room-overlay, #hud-container, #action-prompt, #interaction-prompt').forEach(el => {
        if (el) el.style.display = 'none';
    });"""

new_cutscene_block = """    // Hide ALL HUD elements by fading out the main interface
    const mainUI = document.getElementById('main-interface');
    const hud = document.getElementById('hud');
    const crosshair = document.getElementById('crosshair');
    if (mainUI) mainUI.style.opacity = '0';
    if (hud) hud.style.opacity = '0';
    if (crosshair) crosshair.style.opacity = '0';"""

c = c.replace(old_cutscene_block, new_cutscene_block)

# Fix Sensitivity Event Listeners
# Replace the old bounded listener with document level event delegation
old_slider_logic = """    // Sensitivity
    const sensSlider = document.getElementById('sens-slider');
    if (sensSlider) {
        sensSlider.value = typeof mouseSensMultiplier !== 'undefined' ? mouseSensMultiplier : (parseFloat(localStorage.getItem('samosbor_sensitivity')) || 1.0);
        sensSlider.addEventListener('input', (e) => {
            if (typeof mouseSensMultiplier !== 'undefined') {
                mouseSensMultiplier = parseFloat(e.target.value);
            }
            localStorage.setItem('samosbor_sensitivity', e.target.value);
        });
    }"""

new_slider_logic = """    // Sensitivity (Event Delegation for reliability)
    const sensSlider = document.getElementById('sens-slider');
    if (sensSlider) {
        sensSlider.value = typeof mouseSensMultiplier !== 'undefined' ? mouseSensMultiplier : (parseFloat(localStorage.getItem('samosbor_sensitivity')) || 1.0);
    }
    document.addEventListener('input', (e) => {
        if (e.target && e.target.id === 'sens-slider') {
            if (typeof mouseSensMultiplier !== 'undefined') mouseSensMultiplier = parseFloat(e.target.value);
            localStorage.setItem('samosbor_sensitivity', e.target.value);
        }
    });
    document.addEventListener('change', (e) => {
        if (e.target && e.target.id === 'sens-slider') {
            if (typeof mouseSensMultiplier !== 'undefined') mouseSensMultiplier = parseFloat(e.target.value);
            localStorage.setItem('samosbor_sensitivity', e.target.value);
        }
    });"""

c = c.replace(old_slider_logic, new_slider_logic)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)


# Fix Translation label in index.html
index_path = r'C:\Users\m3615\samosbor_game\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    idx_content = f.read()

idx_content = idx_content.replace('<label data-i18n="sens_label">Mouse Sensitivity:</label>', '<label data-i18n="sens_slider_label">Mouse Sensitivity:</label>')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(idx_content)

print("Final patch applied.")
