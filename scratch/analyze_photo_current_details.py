from PIL import Image
import os

path = 'C:/Users/m3615/.gemini/antigravity/brain/68589a5c-391d-4fb4-bd7d-f6ad216b12ae/media__1780667832883.png'
out_path = 'C:/Users/m3615/samosbor_game/scratch/Photo_detailed_ascii.txt'

if not os.path.exists(path):
    print("File not found")
    exit()

img = Image.open(path)
w, h = img.size

# We want 120 columns wide
width = 120
aspect = img.height / img.width
height = int(width * aspect * 0.5)
img_resized = img.resize((width, height)).convert('L')

# Characters by density
chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
num_chars = len(chars)

ascii_str = ""
for y in range(height):
    for x in range(width):
        pixel = img_resized.getpixel((x, y))
        ascii_str += chars[pixel * num_chars // 256]
    ascii_str += "\n"

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(ascii_str)

print("Wrote detailed ASCII to Photo_detailed_ascii.txt")
print("Original size:", w, h)
print("ASCII size:", width, height)
