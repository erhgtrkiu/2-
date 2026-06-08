import shutil

original = r'C:\Users\m3615\samosbor_game\scratch\app_original.js'
target = r'C:\Users\m3615\samosbor_game\app.js'

shutil.copy(original, target)
print("Copied app_original.js to app.js successfully.")
