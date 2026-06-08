from PIL import Image

img_path = "scratch/green_crop.png"
img = Image.open(img_path)
w, h = img.size
print(f"Crop size: {w}x{h}")

# Print ASCII art of the green pixels
grid = [[' ' for _ in range(w)] for _ in range(h)]
for y in range(h):
    for x in range(w):
        r, g, b = img.getpixel((x, y))[:3]
        if g > 120 and r < 120 and b < 120:
            grid[y][x] = '#'

# Print a downscaled version (e.g. 40 columns wide)
scale = max(1, w // 40)
for y in range(0, h, scale * 2):
    row = ""
    for x in range(0, w, scale):
        row += grid[y][x] if y < h and x < w else " "
    print(row)
