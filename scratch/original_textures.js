function generateProceduralTextures() {
    const createNoiseTexture = (baseColor, noiseColor, scale = 1, isConcrete = false) => {
        const canvas = document.createElement('canvas');
        canvas.width = 256;
        canvas.height = 256;
        const ctx = canvas.getContext('2d');
        
        ctx.fillStyle = baseColor;
        ctx.fillRect(0, 0, 256, 256);
        
        ctx.fillStyle = noiseColor;
        for (let i = 0; i < 6000; i++) {
            const size = Math.random() * 2 + 1;
            const x = Math.random() * 256;
            const y = Math.random() * 256;
            ctx.globalAlpha = Math.random() * 0.18;
            ctx.fillRect(x, y, size, size);
        }
        
        if (isConcrete) {
            ctx.fillStyle = 'rgba(74, 52, 32, 0.15)';
            for (let i = 0; i < 18; i++) {
                ctx.beginPath();
                ctx.arc(Math.random() * 256, Math.random() * 256, Math.random() * 60 + 20, 0, Math.PI * 2);
                ctx.fill();
            }
            ctx.strokeStyle = 'rgba(10, 10, 10, 0.4)';
            ctx.lineWidth = 1;
            for (let i = 0; i < 4; i++) {
                ctx.beginPath();
                ctx.moveTo(Math.random() * 256, Math.random() * 256);
                ctx.lineTo(Math.random() * 256, Math.random() * 256);
                ctx.stroke();
            }
        }
21
<truncated 2180 bytes>

        
        ctx.strokeStyle = '#181109';
        ctx.lineWidth = 2;
        for (let x = 16; x < 128; x += 32) {
            ctx.beginPath();
            ctx.moveTo(x, 0); ctx.lineTo(x, 128);
            ctx.stroke();
        }
        ctx.globalAlpha = 0.25;
        ctx.strokeStyle = '#e6b800';
        ctx.lineWidth = 1;
        for (let y = 0; y < 128; y += 16) {
            for (let x = 0; x < 128; x += 16) {
                ctx.beginPath();
                ctx.moveTo(x, y + 8);
                ctx.lineTo(x + 8, y);
                ctx.lineTo(x + 16, y + 8);
                ctx.lineTo(x + 8, y + 16);
                ctx.closePath();
                ctx.stroke();
            }
        }
        ctx.globalAlpha = 1.0;
        const tex = new THREE.CanvasTexture(canvas);
        tex.wrapS = THREE.RepeatWrapping;
        tex.wrapT = THREE.RepeatWrapping;
        tex.repeat.set(4, 4);
        return tex;
    };
    
    proceduralTextures.concrete = createNoiseTexture('#424750', '#1c1f24', 3, true);
    proceduralTextures.ceiling = createNoiseTexture('#25282e', '#090a0c', 4, false);
    proceduralTextures.rust = createNoiseTexture('#4a3325', '#160e0a', 1, false);
    proceduralTextures.door = createDoorTexture();
    proceduralTextures.wallpaper = createWallpaperTexture();
}

