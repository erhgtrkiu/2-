import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'

if not os.path.exists(app_path):
    print("app.js does not exist!")
    exit(1)

size = os.path.getsize(app_path)
print(f"Size of app.js: {size} bytes")

with open(app_path, 'rb') as f:
    content = f.read()

print(f"Read {len(content)} bytes")
# Check for null bytes
null_count = content.count(b'\x00')
print(f"Number of null bytes: {null_count}")

# Print first 200 chars and last 200 chars
try:
    text = content.decode('utf-8')
    print("First 200 chars:")
    print(text[:200])
    print("\nLast 200 chars:")
    print(text[-200:])
except Exception as e:
    print(f"Decode error: {e}")
