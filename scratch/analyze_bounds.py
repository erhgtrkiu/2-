from PIL import Image
import os

path = 'C:/Users/m3615/.gemini/antigravity/brain/68589a5c-391d-4fb4-bd7d-f6ad216b12ae/media__1780667832883.png'
if not os.path.exists(path):
    print("File not found")
    exit()

img = Image.open(path).convert('RGB')
pixels = list(img.getdata())

max_r = max(p[0] for p in pixels)
max_g = max(p[1] for p in pixels)
max_b = max(p[2] for p in pixels)

min_r = min(p[0] for p in pixels)
min_g = min(p[1] for p in pixels)
min_b = min(p[2] for p in pixels)

print(f"Max R: {max_r}, G: {max_g}, B: {max_b}")
print(f"Min R: {min_r}, G: {min_g}, B: {min_b}")
