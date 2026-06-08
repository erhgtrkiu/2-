import subprocess
import os
import shutil

extractor = r"C:\Program Files\7-Zip\7z.exe"
rar_path = r"C:\Users\m3615\samosbor_game.rar"

archive_path = "samosbor_game\\index.html"
dest_path = "scratch\\index_original.html"

res = subprocess.run([
    extractor, "x", rar_path, archive_path, "-y"
], capture_output=True, text=True, errors='ignore')
print(f"Extracted {archive_path}: status={res.returncode}")

src1 = archive_path
src2 = os.path.join("samosbor_game", "index.html")

real_src = None
if os.path.exists(src1):
    real_src = src1
elif os.path.exists(src2):
    real_src = src2
    
if real_src:
    if os.path.exists(dest_path):
        os.remove(dest_path)
    shutil.move(real_src, dest_path)
    print(f"Moved {real_src} to {dest_path}")
else:
    print(f"Could not find extracted file")

if os.path.exists("samosbor_game"):
    shutil.rmtree("samosbor_game")
