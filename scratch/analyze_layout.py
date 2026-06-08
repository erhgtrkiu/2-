from PIL import Image
import os

files = {
    'Photo 1': 'C:/Users/m3615/.gemini/antigravity/brain/68589a5c-391d-4fb4-bd7d-f6ad216b12ae/media__1780666865894.png',
    'Photo 2': 'C:/Users/m3615/.gemini/antigravity/brain/68589a5c-391d-4fb4-bd7d-f6ad216b12ae/media__1780666869292.png'
}

for name, path in files.items():
    if not os.path.exists(path):
        print(f"{name} not found.")
        continue
    img = Image.open(path).convert('RGB')
    w, h = img.size
    print(f"\n=== {name} ({w}x{h}) ===")
    
    # 8x8 grid of average colors
    grid_w, grid_h = 8, 8
    cell_w, cell_h = w // grid_w, h // grid_h
    for row in range(grid_h):
        row_str = []
        for col in range(grid_w):
            box = (col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h)
            cell = img.crop(box)
            # calculate average color
            pixels = list(cell.getdata())
            r = sum(p[0] for p in pixels) // len(pixels)
            g = sum(p[1] for p in pixels) // len(pixels)
            b = sum(p[2] for p in pixels) // len(pixels)
            
            # map color to a character/description
            # simple labels: Black (void), Gray (concrete), Green (sky/nature/achievement), Red, etc.
            brightness = (r + g + b) / 3
            if brightness < 20:
                row_str.append("[ V ]") # Void
            elif r > 180 and g > 180 and b > 180:
                row_str.append("[ W ]") # White
            elif g > r + 30 and g > b + 30:
                row_str.append("[ G ]") # Green
            elif r > g + 40 and r > b + 40:
                row_str.append("[ R ]") # Red
            else:
                # Gray shades
                row_str.append(f"[{r:02x}]")
        print(" ".join(row_str))
