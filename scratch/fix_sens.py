import os

app_path = r'C:\Users\m3615\samosbor_game\app.js'

with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace variables
c = c.replace("let sensitivity = parseFloat(localStorage.getItem('samosbor_sensitivity')) || 1.0;", "let mouseSensMultiplier = parseFloat(localStorage.getItem('samosbor_sensitivity')) || 1.0;")
c = c.replace("// const sensitivity = 0.0025; // Replaced by dynamic sensitivity", "const sensitivity = 0.0025;")

# Replace calculations
c = c.replace("playerYaw -= e.movementX * sensitivity;", "playerYaw -= e.movementX * sensitivity * mouseSensMultiplier;")
c = c.replace("playerPitch -= e.movementY * sensitivity;", "playerPitch -= e.movementY * sensitivity * mouseSensMultiplier;")
c = c.replace("playerYaw -= e.movementX * sensitivity * 1.5;", "playerYaw -= e.movementX * sensitivity * mouseSensMultiplier * 1.5;")
c = c.replace("playerPitch -= e.movementY * sensitivity * 1.5;", "playerPitch -= e.movementY * sensitivity * mouseSensMultiplier * 1.5;")

# Replace slider logic variables
c = c.replace("typeof sensitivity !== 'undefined'", "typeof mouseSensMultiplier !== 'undefined'")
c = c.replace("sensitivity = parseFloat(e.target.value);", "mouseSensMultiplier = parseFloat(e.target.value);")
c = c.replace("typeof sensitivity !== \"undefined\"", "typeof mouseSensMultiplier !== \"undefined\"")
c = c.replace("typeof sensitivity !== `undefined`", "typeof mouseSensMultiplier !== `undefined`")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed sensitivity math.")
