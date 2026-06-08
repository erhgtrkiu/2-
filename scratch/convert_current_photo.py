from PIL import Image
import os

path = 'C:/Users/m3615/.gemini/antigravity/brain/68589a5c-391d-4fb4-bd7d-f6ad216b12ae/media__1780667832883.png'
out_path = 'C:/Users/m3615/samosbor_game/scratch/Photo_current_ascii.txt'

chars = "@#S%?*+;:-. "

def to_ascii(path, width=80):
    if not os.path.exists(path):
        return f"{path} not found."
    img = Image.open(path)
    # Calculate height to preserve aspect ratio
    aspect = img.height / img.width
    height = int(width * aspect * 0.55) # 0.55 corrects for font aspect ratio
    img = img.resize((width, height)).convert('L')
    
    pixels = img.getdata()
    ascii_str = ""
    for i, pixel in enumerate(pixels):
        if i > 0 and i % width == 0:
            ascii_str += "\n"
        ascii_str += chars[pixel * len(chars) // 256]
    return ascii_str

ascii_art = to_ascii(path)
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(ascii_art)
print("Wrote ASCII art to Photo_current_ascii.txt")
print("Dimensions:", Image.open(path).size)
