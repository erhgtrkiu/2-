import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'

js_code = """
// --- Added automatically: Localization & Sensitivity Bindings ---
function applyLanguage(lang) {
    if (typeof LANGUAGES === 'undefined' || !LANGUAGES[lang]) return;
    const t = LANGUAGES[lang];
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (t[key]) {
            if (el.tagName === 'INPUT' && (el.type === 'button' || el.type === 'submit')) {
                el.value = t[key];
            } else if (key.includes('_html')) {
                el.innerHTML = t[key];
            } else {
                el.innerText = t[key];
            }
        }
    });
}

window.addEventListener('DOMContentLoaded', () => {
    // Language
    const langSelect = document.getElementById('settings-language-select');
    if (langSelect) {
        langSelect.value = localStorage.getItem('samosbor_lang') || 'ru';
        langSelect.addEventListener('change', (e) => {
            const l = e.target.value;
            localStorage.setItem('samosbor_lang', l);
            applyLanguage(l);
        });
        // Initial apply
        applyLanguage(langSelect.value);
    }
    
    // Sensitivity
    const sensSlider = document.getElementById('sens-slider');
    if (sensSlider) {
        sensSlider.value = typeof sensitivity !== 'undefined' ? sensitivity : (parseFloat(localStorage.getItem('samosbor_sensitivity')) || 1.0);
        sensSlider.addEventListener('input', (e) => {
            if (typeof sensitivity !== 'undefined') {
                sensitivity = parseFloat(e.target.value);
            }
            localStorage.setItem('samosbor_sensitivity', e.target.value);
        });
    }
});
// --------------------------------------------------------------
"""

with open(app_path, 'a', encoding='utf-8') as f:
    f.write(js_code)

print("Appended UI bindings to app.js")
