from PIL import Image
import os

files = [
    'C:/Users/m3615/.gemini/antigravity/brain/68589a5c-391d-4fb4-bd7d-f6ad216b12ae/media__1780666865894.png',
    'C:/Users/m3615/.gemini/antigravity/brain/68589a5c-391d-4fb4-bd7d-f6ad216b12ae/media__1780666869292.png'
]

for f in files:
    if os.path.exists(f):
        img = Image.open(f)
        print(f"File: {os.path.basename(f)}, Size: {img.size}, Format: {img.format}, Mode: {img.mode}")
    else:
        print(f"File {f} does not exist!")
