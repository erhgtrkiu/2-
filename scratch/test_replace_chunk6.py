with open('C:/Users/m3615/samosbor_game/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

target = """function animateMenuNature() {
    if (!menuNatureCanvas) return;
    const ctx = menuNatureCanvas.getContext('2d');
    
    let time = 0;
    const particles = [];
    for (let i = 0; i < 20; i++) {
        particles.push({
            x: Math.random() * 800,
            y: Math.random() * 600,
            vx: 0.2 + Math.random() * 0.5,
            vy: -0.1 - Math.random() * 0.3,
            size: 2 + Math.random() * 4,
            alpha: 0.1 + Math.random() * 0.4,
            wiggleSpeed: 0.002 + Math.random() * 0.005,
            wiggleOffset: Math.random() * 100
        });
    }
    
    function loop() {
        if (!menuNatureCanvas) return;
        const rect = menuNatureCanvas.getBoundingClientRect();
        const w = menuNatureCanvas.width = rect.width || 800;
        const h = menuNatureCanvas.height = rect.height || 600;
        
        time += 16.67;
        ctx.clearRect(0, 0, w, h);
        
        // 1. Sky Gradient
        const skyGrad = ctx.createLinearGradient(0, 0, 0, h);
        skyGrad.addColorStop(0, '#7ec0ee');
        skyGrad.addColorStop(0.6, '#e0f6ff');
        skyGrad.addColorStop(1, '#a8e4a0');
        ctx.fillStyle = skyGrad;
        ctx.fillRect(0, 0, w, h);
        
        // 2. Pulsating Sun
        const sunX = w * 0.25;
        const sunY = h * 0.25;
        const sunRadBase = Math.min(w, h) * 0.15;
        const sunRad = sunRadBase + Math.sin(time * 0.001) * (sunRadBase * 0.1);
        const sunGrad = ctx.createRadialGradient(sunX, sunY, 10, sunX, sunY, sunRad);
        sunGrad.addColorStop(0, 'rgba(255, 255, 220, 0.85)');
        sunGrad.addColorStop(1, 'rgba(255, 255, 255, 0)');
        ctx.fillStyle = sunGrad;
        ctx.fillRect(0, 0, w, h);
        
        // 3. Clouds
        const cloudSpeed = 0.015;
        const drawCloud = (cx, cy, scale) => {
            ctx.fillStyle = 'rgba(255, 255, 255, 0.65)';
            ctx.beginPath();
            ctx.arc(cx, cy, 30 * scale, 0, Math.PI * 2);
            ctx.arc(cx + 40 * scale, cy - 10 * scale, 40 * scale, 0, Math.PI * 2);
            ctx.arc(cx + 80 * scale, cy, 30 * scale, 0, Math.PI * 2);
            ctx.arc(cx + 40 * scale, cy + 15 * scale, 25 * scale, 0, Math.PI * 2);
            ctx.closePath();
            ctx.fill();
        };
        const cloud1X = ((time * cloudSpeed + 100) % (w + 200)) - 100;
        drawCloud(cloud1X, h * 0.18, 1.2);
        
        const cloud2X = (((time * cloudSpeed * 0.7) + w * 0.5) % (w + 200)) - 100;
        drawCloud(cloud2X, h * 0.3, 0.8);
        
        // 4. Grass Hill
        const hillGrad = ctx.createLinearGradient(0, h * 0.75, 0, h);
        hillGrad.addColorStop(0, '#55a630');
        hillGrad.addColorStop(1, '#2b9348');
        ctx.fillStyle = hillGrad;
        ctx.beginPath();
        const hillYOffset = Math.sin(time * 0.0005) * 5;
        ctx.ellipse(w * 0.5, h + 100 + hillYOffset, w * 0.7, h * 0.4, 0, 0, Math.PI * 2);
        ctx.fill();
        
        // 5. Tree
        const treeX = w * 0.75;
        const treeY = h * 0.85;
        const treeSway = Math.sin(time * 0.0008) * 15;
        
        ctx.fillStyle = '#6f4e37';
        ctx.beginPath();
        ctx.moveTo(treeX - 15, treeY);
        ctx.quadraticCurveTo(treeX - 10, treeY - 80, treeX - 30 + treeSway * 0.5, treeY - 180);
        ctx.lineTo(treeX - 5 + treeSway * 0.5, treeY - 180);
        ctx.quadraticCurveTo(treeX + 15, treeY - 80, treeX + 20, treeY);
        ctx.closePath();
        ctx.fill();
        
        const branchX = treeX - 18 + treeSway * 0.5;
        const branchY = treeY - 180;
        
        ctx.fillStyle = 'rgba(56, 176, 0, 0.85)';
        ctx.beginPath();
        ctx.arc(branchX - 50 + treeSway * 0.3, branchY - 20, 55, 0, Math.PI * 2);
        ctx.arc(branchX + 50 + treeSway * 0.3, branchY - 30, 60, 0, Math.PI * 2);
        ctx.arc(branchX + treeSway * 0.3, branchY - 70, 65, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.fillStyle = 'rgba(0, 114, 0, 0.85)';
        ctx.beginPath();
        ctx.arc(branchX - 30 + treeSway * 0.4, branchY + 10, 45, 0, Math.PI * 2);
        ctx.arc(branchX + 40 + treeSway * 0.4, branchY - 10, 45, 0, Math.PI * 2);
        ctx.fill();
        
        // 6. Particles
        particles.forEach(p => {
            p.x += p.vx + Math.sin(time * p.wiggleSpeed + p.wiggleOffset) * 0.4;
            p.y += p.vy;
            if (p.x > w + 20) p.x = -20;
            if (p.y < -20) {
                p.y = h + 20;
                p.x = Math.random() * w;
            }
            ctx.fillStyle = `rgba(180, 240, 150, ${p.alpha})`;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
        });
        
        menuNatureAnimFrame = requestAnimationFrame(loop);
    }
    
    if (menuNatureAnimFrame) {
        cancelAnimationFrame(menuNatureAnimFrame);
    }
    loop();
}"""

if target in content:
    print("Chunk 6 matches perfectly!")
else:
    print("Chunk 6 does NOT match!")
    # Let's print the actual code from line 5725 to 5852
    lines = content.splitlines()
    print("Actual lines 5725 to 5852:")
    for i in range(5725, 5853):
        print(f"{i}: {lines[i-1]}")
