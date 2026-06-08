from PIL import Image
import os

path = 'C:/Users/m3615/.gemini/antigravity/brain/68589a5c-391d-4fb4-bd7d-f6ad216b12ae/media__1780667832883.png'
if not os.path.exists(path):
    print("File not found")
    exit()

img = Image.open(path)
w, h = img.size
print(f"Image size: {w}x{h}")

# Analyze colors by regions (e.g. 5x5 grid)
grid_w = w // 5
grid_h = h // 5

for gy in range(5):
    for gx in range(5):
        # Average color in this grid cell
        r_sum, g_sum, b_sum = 0, 0, 0
        pixels_count = 0
        
        # Count some key color pixels
        yellow_count = 0
        green_count = 0
        red_count = 0
        
        for y in range(gy * grid_h, (gy + 1) * grid_h):
            for x in range(gx * grid_w, (gx + 1) * grid_w):
                r, g, b = img.getpixel((x, y))[:3]
                r_sum += r
                g_sum += g
                b_sum += b
                pixels_count += 1
                
                # Check for yellow (high R, high G, low B)
                if r > 150 and g > 150 and b < 100:
                    yellow_count += 1
                # Check for green (low R, high G, low B)
                if r < 100 and g > 150 and b < 100:
                    green_count += 1
                # Check for red (high R, low G, low B)
                if r > 150 and g < 100 and b < 100:
                    red_count += 1
                    
        avg_r = int(r_sum / pixels_count)
        avg_g = int(g_sum / pixels_count)
        avg_b = int(b_sum / pixels_count)
        print(f"Grid ({gx}, {gy}): Avg Color=#{avg_r:02x}{avg_g:02x}{avg_b:02x}, Yellow={yellow_count}, Green={green_count}, Red={red_count}")
