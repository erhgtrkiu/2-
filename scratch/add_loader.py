import sys

idx_path = r'C:\Users\m3615\samosbor_game\index.html'
with open(idx_path, 'r', encoding='utf-8') as f:
    c = f.read()

target = '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>'
replacement = target + '\n    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>'

if target in c:
    c = c.replace(target, replacement)
    with open(idx_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Injected GLTFLoader successfully.")
else:
    print("Could not find three.js script tag!")
