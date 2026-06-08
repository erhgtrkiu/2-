from PIL import Image
from collections import Counter
import os

path = 'C:/Users/m3615/.gemini/antigravity/brain/68589a5c-391d-4fb4-bd7d-f6ad216b12ae/media__1780667832883.png'
if not os.path.exists(path):
    print("File not found")
    exit()

img = Image.open(path).convert('RGB')
pixels = list(img.getdata())
counter = Counter(pixels)

print("Top 20 colors:")
for color, count in counter.most_common(20):
    print(f"Color: #{color[0]:02x}{color[1]:02x}{color[2]:02x}, Count: {count} ({count/len(pixels)*100:.2f}%)")

# Let's count some specific ranges:
# Red-ish
red = sum(1 for p in pixels if p[0] > 150 and p[1] < 100 and p[2] < 100)
# Green-ish
green = sum(1 for p in pixels if p[0] < 100 and p[1] > 150 and p[2] < 100)
# Yellow-ish
yellow = sum(1 for p in pixels if p[0] > 150 and p[1] > 150 and p[2] < 100)

print(f"Red pixels: {red}, Green pixels: {green}, Yellow pixels: {yellow}")
