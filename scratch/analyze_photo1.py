from PIL import Image

# Load the image
img_path = r"C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\media__1780650172051.png"
img = Image.open(img_path)
print("Image size:", img.size)

width, height = img.size
green_pixels = []

for y in range(height):
    for x in range(width):
        r, g, b = img.getpixel((x, y))[:3]
        # Check if green-ish
        if g > 120 and r < 120 and b < 120:
            green_pixels.append((x, y, (r, g, b)))

print("Number of green-ish pixels:", len(green_pixels))

if len(green_pixels) > 0:
    xs = [p[0] for p in green_pixels]
    ys = [p[1] for p in green_pixels]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    print(f"Bounding box of green pixels: X: [{x_min}, {x_max}], Y: [{y_min}, {y_max}]")
    
    pad = 10
    crop_x_min = max(0, x_min - pad)
    crop_x_max = min(width, x_max + pad)
    crop_y_min = max(0, y_min - pad)
    crop_y_max = min(height, y_max + pad)
    
    cropped = img.crop((crop_x_min, crop_y_min, crop_x_max, crop_y_max))
    cropped.save("scratch/green_crop.png")
    print("Saved cropped region to scratch/green_crop.png")
else:
    # Try looser: G > R + 30 and G > B + 30 and G > 80
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))[:3]
            if g > r + 30 and g > b + 30 and g > 80:
                green_pixels.append((x, y, (r, g, b)))
    print("Number of loose green pixels:", len(green_pixels))
    if len(green_pixels) > 0:
        xs = [p[0] for p in green_pixels]
        ys = [p[1] for p in green_pixels]
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)
        print(f"Bounding box (loose): X: [{x_min}, {x_max}], Y: [{y_min}, {y_max}]")
        pad = 10
        cropped = img.crop((max(0, x_min-pad), max(0, y_min-pad), min(width, x_max+pad), min(height, y_max+pad)))
        cropped.save("scratch/green_crop_loose.png")
        print("Saved loose cropped region to scratch/green_crop_loose.png")
