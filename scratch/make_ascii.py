from PIL import Image
import os

files = {
    'Photo_1': 'C:/Users/m3615/.gemini/antigravity/brain/68589a5c-391d-4fb4-bd7d-f6ad216b12ae/media__1780666865894.png',
    'Photo_2': 'C:/Users/m3615/.gemini/antigravity/brain/68589a5c-391d-4fb4-bd7d-f6ad216b12ae/media__1780666869292.png'
}

chars = "@#S%?*+;:-. "

def to_ascii(path, width=80):
    if not os.path.exists(path):
        return f"{path} not found"
    img = Image.open(path).convert('L')
    w, h = img.size
    aspect = h / w
    height = int(width * aspect * 0.55)
    img = img.resize((width, height))
    pixels = img.getdata()
    
    ascii_str = []
    for i in range(height):
        row = []
        for j in range(width):
            val = pixels[i * width + j]
            char_idx = int(val / 256 * len(chars))
            row.append(chars[char_idx])
        ascii_str.append("".join(row))
    return "\n".join(ascii_str)

for name, path in files.items():
    ascii_art = to_ascii(path, width=80)
    with open(f'C:/Users/m3615/samosbor_game/scratch/{name}_ascii.txt', 'w', encoding='utf-8') as out:
        out.write(ascii_art)
    print(f"Saved ASCII art for {name}")
