function buildFloor(floorNum, baseY) {

    const wallMat = new THREE.MeshStandardMaterial({ 
        map: proceduralTextures.concrete, 
        normalMap: proceduralTextures.concreteNormal, 
        roughness: 0.8,
        metalness: 0.05
    });
    const floorMat = new THREE.MeshStandardMaterial({ 
        map: proceduralTextures.concrete, 
        normalMap: proceduralTextures.concreteNormal, 
        roughness: 0.9
    });
    const ceilingMat = new THREE.MeshStandardMaterial({ 
        map: proceduralTextures.ceiling, 
        normalMap: proceduralTextures.ceilingNormal, 
        roughness: 0.95
    });
    
    // 1. Пол и потолок коридора (BoxGeometry для устранения засветов)
    const floorGeo = new THREE.BoxGeometry(6, 0.2, 42);
    const fMesh = new THREE.Mesh(floorGeo, floorMat);
    fMesh.position.set(0, baseY - 0.1, -21);
    fMesh.receiveShadow = true;
    scene.add(fMesh);
    roomMeshes.push(fMesh);
    
    const ceilingGeo = new THREE.BoxGeometry(6, 0.2, 42);
    const cMesh = new THREE.Mesh(ceilingGeo, ceilingMat);
    cMesh.position.set(0, baseY + 5.0 + 0.1, -21);
    cMesh.receiveShadow = true;
    scene.add(cMesh);
    roomMeshes.push(cMesh);
    
    // 2. Сегментированные толстые стены коридора
    const segments = [
        { zStart: 0, zEnd: -9.4 },
        { zStart: -10.6, zEnd: -21.4 },
        { zStart: -22.6, zEnd: -33.4 },
        { zStart: -34.6, zEnd: -42.0 }
    ];
    
    const buildWallSide = (xPos) => {
        const wallGroup = new THREE.Group();
        segments.forEach(seg => {
            const len = Math.abs(seg.zStart - seg.zEnd);
            const zCenter = (seg.zStart + seg.zEnd) / 2;
            const mesh = new THREE.Mesh(new THREE.BoxGeometry(0.2, 5.0, len), wallMat);
            mesh.position.set(0, 2.5, zCenter);
            mesh.receiveShadow = true;
            mesh.castShadow = true;
            wallGroup.add(mesh);
        });
        [-10, -22, -34].forEach(zDoor => {
            const meshTop = new THREE.Mesh(new THREE.BoxGeometry(0.2, 2.4, 1.2), wallMat);
            meshTop.position.set(0, 3.8, zDoor);
            meshTop.receiveShadow = true;
            meshTop.castShadow = true;
            wallGroup.add(meshTop);
        });
        wallGroup.position.set(xPos, baseY, 0);
        wallGroup.rotation.y = 0;
        scene.add(wallGroup);
        roomMeshes.push(wallGroup);
        return wallGroup;
    };
    
    leftWallMesh = buildWallSide(-3.1);
    rightWallMesh = buildWallSide(3.1);
    
    // Задняя стена коридора
    const backWall = new THREE.Mesh(new THREE.BoxGeometry(6, 5, 0.2), wallMat);
    backWall.position.set(0, baseY + 2.5, 0.1);
    backWall.receiveShadow = true;
    backWall.castShadow = true;
    scene.add(backWall);
    roomMeshes.push(backWall);
    
    // Перегородка с лестничным проемом на Z = -42
    const stairsHoleWallL = new THREE.Mesh(new THREE.BoxGeometry(1.5, 5, 0.2), wallMat);
    stairsHoleWallL.position.set(-2.25, baseY + 2.5, -42);
    stairsHoleWallL.receiveShadow = true;
    stairsHoleWallL.castShadow = true;
    scene.add(stairsHoleWallL);
    staircaseMeshes.push(stairsHoleWallL);
    
    const stairsHoleWallR = new THREE.Mesh(new THREE.BoxGeometry(1.5, 5, 0.2), wallMat);
    stairsHoleWallR.position.set(2.25, baseY + 2.5, -42);
    stairsHoleWallR.receiveShadow = true;
    stairsHoleWallR.castShadow = true;
    scene.add(stairsHoleWallR);
    staircaseMeshes.push(stairsHoleWallR);
    
    // 3. Физическая П-образная лестница вниз (к baseY - 5.0)
    const stepWidth = 1.5;
    const stepHeight = 0.3125;
    const stepDepth = 0.625;
    const stepsCount = 8;
    
    // Левый пролет (вниз от baseY до Y = baseY - 2.5)
    for (let i = 0; i < stepsCount; i++) {
        const stepGeo = new THREE.BoxGeometry(stepWidth, stepHeight, stepDepth);
        const step = new THREE.Mesh(stepGeo, wallMat);
        step.position.set(-0.75, baseY - stepHeight * i - stepHeight / 2, -42.0 - stepDepth * i - stepDepth / 2);
        step.receiveShadow = true;
        scene.add(step);
        staircaseMeshes.push(step);
    }
    
    // Разворотная площадка на Y = baseY - 2.5
    const landing = new THREE.Mesh(new THREE.BoxGeometry(3.0, 0.2, 2.5), wallMat);
    landing.position.set(0, baseY - 2.5 - 0.1, -48.25);
    landing.receiveShadow = true;
    landing.castShadow = true;
    scene.add(landing);
    staircaseMeshes.push(landing);
    
    // Правый пролет (вниз от Y = baseY - 2.5 до Y = baseY - 5.0)
    for (let i = 0; i < stepsCount; i++) {
        const stepGeo = new THREE.BoxGeometry(stepWidth, stepHeight, stepDepth);
        const step = new THREE.Mesh(stepGeo, wallMat);
        step.position.set(0.75, baseY - 2.5 - stepHeight * i - stepHeight / 2, -47.0 + stepDepth * i + stepDepth / 2);
        step.receiveShadow = true;
        scene.add(step);
        staircaseMeshes.push(step);
    }
    
    // Разделитель между пролетами
    const partition = new THREE.Mesh(new THREE.BoxGeometry(0.1, 3.5, 5.0), wallMat);
    partition.position.set(0, baseY - 1.25, -44.5);
    partition.receiveShadow = true;
    partition.castShadow = true;
    scene.add(partition);
    staircaseMeshes.push(partition);
    
    // Стены лестничного колодца
    const shaftL = new THREE.Mesh(new THREE.BoxGeometry(0.2, 5.0, 7.5), wallMat);
    shaftL.position.set(-1.6, baseY - 2.5, -45.75);
    shaftL.receiveShadow = true;
    shaftL.castShadow = true;
    scene.add(shaftL);
    staircaseMeshes.push(shaftL);
    
    const shaftR = new THREE.Mesh(new THREE.BoxGeometry(0.2, 5.0, 7.5), wallMat);
    shaftR.position.set(1.6, baseY - 2.5, -45.75);
    shaftR.receiveShadow = true;
    shaftR.castShadow = true;
    scene.add(shaftR);
    staircaseMeshes.push(shaftR);
    
    const shaftB = new THREE.Mesh(new THREE.BoxGeometry(3.2, 5.0, 0.2), wallMat);
    shaftB.position.set(0, baseY - 2.5, -49.6);
    shaftB.receiveShadow = true;
    shaftB.castShadow = true;
    scene.add(shaftB);
    staircaseMeshes.push(shaftB);
    
    // Stairs blast doors at Z = -47.0
    const sdState = getOrGenerateStairsDoor(floorNum);
    const sdGroup = new THREE.Group();
    sdGroup.name = `stairsDoor_${floorNum}`;
    sdGroup.position.set(0, baseY - 2.5, -47.0);
    
    const sdPanelMat = new THREE.MeshStandardMaterial({
        map: proceduralTextures.stairsDoor,
        normalMap: proceduralTextures.stairsDoorNormal,
        roughness: 0.6,
        metalness: 0.8
    });
    
    const sdLeftMesh = new THREE.Mesh(new THREE.BoxGeometry(1.5, 5.0, 0.15), sdPanelMat);
    sdLeftMesh.name = "left_panel";
    sdLeftMesh.receiveShadow = true;
    sdLeftMesh.castShadow = true;
    sdGroup.add(sdLeftMesh);
    
    const sdRightMesh = new THREE.Mesh(new THREE.BoxGeometry(1.5, 5.0, 0.15), sdPanelMat);
    sdRightMesh.name = "right_panel";
    sdRightMesh.receiveShadow = true;
    sdRightMesh.castShadow = true;
    sdGroup.add(sdRightMesh);
    
    if (sdState.opened) {
        sdLeftMesh.position.set(-2.25, 2.5, 0); // slid open
        sdRightMesh.position.set(2.25, 2.5, 0);
    } else {
        sdLeftMesh.position.set(-0.75, 2.5, 0); // closed
        sdRightMesh.position.set(0.75, 2.5, 0);
    }
    
    // Door Frame details (outlines)
    const frameMat = new THREE.MeshStandardMaterial({
        map: proceduralTextures.rust,
        normalMap: proceduralTextures.rustNormal,
        roughness: 0.5,
        metalness: 0.8
    });
    const sdFrameTop = new THREE.Mesh(new THREE.BoxGeometry(3.2, 0.3, 0.3), frameMat);
    sdFrameTop.position.set(0, 4.85, 0);
    sdGroup.add(sdFrameTop);
    
    const sdFrameL = new THREE.Mesh(new THREE.BoxGeometry(0.3, 5.0, 0.3), frameMat);
    sdFrameL.position.set(-1.65, 2.5, 0);
    sdGroup.add(sdFrameL);
    
    const sdFrameR = new THREE.Mesh(new THREE.BoxGeometry(0.3, 5.0, 0.3), frameMat);
    sdFrameR.position.set(1.65, 2.5, 0);
    sdGroup.add(sdFrameR);
    
    scene.add(sdGroup);
    staircaseMeshes.push(sdGroup);
    
    // 4. Потолочные трубы
    const pipeMat = new THREE.MeshStandardMaterial({ 
        map: proceduralTextures.rust, 
        normalMap: proceduralTextures.rustNormal, 
        metalness: 0.8, 
        roughness: 0.3 
    });
    const pipeGeo = new THREE.CylinderGeometry(0.12, 0.12, 42, 8);
    
    const pipeL = new THREE.Mesh(pipeGeo, pipeMat);
    pipeL.rotation.x = Math.PI / 2;
    pipeL.position.set(-2.2, baseY + 4.4, -21);
    scene.add(pipeL);
    ceilingPipes.push(pipeL);
    
    const pipeR = new THREE.Mesh(pipeGeo, pipeMat);
    pipeR.rotation.x = Math.PI / 2;
    pipeR.position.set(2.2, baseY + 4.4, -21);
    scene.add(pipeR);
    ceilingPipes.push(pipeR);
    
    // 5. Освещение (PointLight тени ОТКЛЮЧЕНЫ во избежание лагов)
    const lightGeo = new THREE.BoxGeometry(0.8, 0.1, 1.4);
    const lightEmissiveMat = new THREE.MeshBasicMaterial({ color: 0xccffcc });
    const zLights = [-2, -10, -22, -34, -44];
    zLights.forEach(z => {
        const lamp = new THREE.Mesh(lightGeo, lightEmissiveMat);
        lamp.position.set(0, baseY + 4.95, z);
        scene.add(lamp);
        ceilingLights.push(lamp);
        
        if (Math.abs(floorNum - state.floor) <= 1) {
            const pl = new THREE.PointLight(0xd5ffd0, 0.65, 16);
            pl.position.set(0, baseY + 4.5, z);
            pl.castShadow = false;
            scene.add(pl);
            ceilingLights.push(pl);
        }
    });
    
    // Сигнальный маяк Самосбора на Z = -38
    const beacon = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.3, 8), new THREE.MeshBasicMaterial({ color: 0x440000 }));
    beacon.position.set(0, baseY + 4.8, -38);
    scene.add(beacon);
    warningBeacons.push(beacon);
    
    if (Math.abs(floorNum - state.floor) <= 1) {
        const wl = new THREE.PointLight(0xff0000, 0, 15);
        wl.position.set(0, baseY + 4.4, -38);
        wl.castShadow = false;
        scene.add(wl);
        warningLights.push(wl);
    }
    
    // 6. Двери и интерьеры комнат
    const doorGeo = new THREE.BoxGeometry(1.2, 2.6, 0.1);
    const doorMat = new THREE.MeshStandardMaterial({ 
        map: proceduralTextures.door, 
        normalMap: proceduralTextures.doorNormal, 
        roughness: 0.5 
    });
    const roomWallMat = new THREE.MeshStandardMaterial({ 
        map: proceduralTextures.wallpaper, 
        normalMap: proceduralTextures.wallpaperNormal, 
        roughness: 0.8, 
        side: THREE.DoubleSide 
    });
    const roomFloorMat = new THREE.MeshStandardMaterial({ 
        map: proceduralTextures.concrete, 
        normalMap: proceduralTextures.concreteNormal, 
        roughness: 0.9, 
        side: THREE.DoubleSide 
    });
    const transWallMat = new THREE.MeshStandardMaterial({ 
        map: proceduralTextures.rust, 
        normalMap: proceduralTextures.rustNormal, 
        roughness: 0.7, 
        side: THREE.DoubleSide 
    });
    const roomCeilMat = new THREE.MeshStandardMaterial({ 
        map: proceduralTextures.ceiling, 
        normalMap: proceduralTextures.ceilingNormal, 
        roughness: 0.95, 
        side: THREE.DoubleSide 
    });
    
    const floorDoors = getOrGenerateFloorDoors(floorNum);
    
    DOOR_LAYOUT.forEach((layout, idx) => {
        const doorObj = floorDoors[idx];
        
        const doorPivot = new THREE.Group();
        // Размещаем петлю двери сбоку проема для правильной стыковки и анимации
        const zPivot = layout.x < 0 ? layout.z + 0.6 : layout.z - 0.6;
        doorPivot.position.set(layout.x, baseY + 1.3, zPivot);
        doorPivot.rotation.y = layout.rot;
        doorPivot.userData = { floor: floorNum, doorIndex: idx };
        
        const doorMesh = new THREE.Mesh(doorGeo, doorMat);
        doorMesh.name = `door_${idx}`;
        doorMesh.position.set(0.6, 0, 0); // Смещение от петли
        doorMesh.userData = { doorIndex: idx };
        doorMesh.castShadow = true;
        doorMesh.receiveShadow = true;
        
        // Add volumetric handles to both sides of the door
        addVolumetricHandle(doorMesh);
        
        doorPivot.add(doorMesh);
        
        if (doorObj && doorObj.opened) {
            doorPivot.rotation.y = layout.rot + Math.PI / 2;
        }
        
        scene.add(doorPivot);
        doorPivots.push(doorPivot);
        
        if (doorObj) {
            const roomGroup = new THREE.Group();
            const isLeft = layout.x < 0;
            const dirX = isLeft ? -1 : 1;
            
            if (doorObj.type === 'apartment') {
                // Сдвиг комнат глубже наружу, чтобы предотвратить пересечения со стенами коридора
                const roomCenterX = layout.x + (3.7 * dirX);
                const roomCenterZ = layout.z;
                const wallOffsetX = layout.x + (0.3 * dirX);
                const backWallX = layout.x + (7.1 * dirX);
                
                const rFloor = new THREE.Mesh(new THREE.BoxGeometry(7.0, 0.1, 7.0), roomFloorMat);
                rFloor.position.set(roomCenterX, baseY - 0.05, roomCenterZ);
                rFloor.receiveShadow = true;
                roomGroup.add(rFloor);
                
                const rCeil = new THREE.Mesh(new THREE.BoxGeometry(7.0, 0.1, 7.0), roomCeilMat);
                rCeil.position.set(roomCenterX, baseY + 5.0 + 0.05, roomCenterZ);
                rCeil.receiveShadow = true;
                roomGroup.add(rCeil);
                
                const rBackWall = new THREE.Mesh(new THREE.BoxGeometry(0.2, 5.0, 7.0), roomWallMat);
                rBackWall.position.set(backWallX, baseY + 2.5, roomCenterZ);
                rBackWall.castShadow = true;
                rBackWall.receiveShadow = true;
                roomGroup.add(rBackWall);
                
                const rSideWall1 = new THREE.Mesh(new THREE.BoxGeometry(7.0, 5.0, 0.2), roomWallMat);
                rSideWall1.position.set(roomCenterX, baseY + 2.5, roomCenterZ - 3.5 - 0.1);
                rSideWall1.castShadow = true;
                rSideWall1.receiveShadow = true;
                roomGroup.add(rSideWall1);
                
                const rSideWall2 = new THREE.Mesh(new THREE.BoxGeometry(7.0, 5.0, 0.2), roomWallMat);
                rSideWall2.position.set(roomCenterX, baseY + 2.5, roomCenterZ + 3.5 + 0.1);
                rSideWall2.castShadow = true;
                rSideWall2.receiveShadow = true;
                roomGroup.add(rSideWall2);
                
                const rFrontWall1 = new THREE.Mesh(new THREE.BoxGeometry(0.2, 5.0, 2.9), roomWallMat);
                rFrontWall1.position.set(wallOffsetX, baseY + 2.5, roomCenterZ - 2.05);
                rFrontWall1.castShadow = true;
                rFrontWall1.receiveShadow = true;
                roomGroup.add(rFrontWall1);
                
                const rFrontWall2 = new THREE.Mesh(new THREE.BoxGeometry(0.2, 5.0, 2.9), roomWallMat);
                rFrontWall2.position.set(wallOffsetX, baseY + 2.5, roomCenterZ + 2.05);
                rFrontWall2.castShadow = true;
                rFrontWall2.receiveShadow = true;
                roomGroup.add(rFrontWall2);
                
                const rFrontWallTop = new THREE.Mesh(new THREE.BoxGeometry(0.2, 2.4, 1.2), roomWallMat);
                rFrontWallTop.position.set(wallOffsetX, baseY + 3.8, roomCenterZ);
                rFrontWallTop.castShadow = true;
                rFrontWallTop.receiveShadow = true;
                roomGroup.add(rFrontWallTop);
                
                const cab = createDetailedCabinet(dirX);
                cab.position.set(layout.x + (5.5 * dirX), baseY, roomCenterZ - 2.0);
                roomGroup.add(cab);
                
                const table = createDetailedTable();
                table.position.set(roomCenterX, baseY, roomCenterZ);
                roomGroup.add(table);
                
                if (Math.abs(floorNum - state.floor) <= 1) {
                    const roomLight = new THREE.PointLight(0xffeedd, doorObj.opened ? 0.3 : 0, 8);
                    roomLight.position.set(roomCenterX, baseY + 4, roomCenterZ);
                    roomLight.castShadow = false;
                    roomGroup.add(roomLight);
                    doorLights[floorNum + '_' + idx] = roomLight;
                }
                
            } else if (doorObj.type === 'transition') {
                const roomCenterX = layout.x + (2.7 * dirX);
                const roomCenterZ = layout.z;
                const wallOffsetX = layout.x + (0.3 * dirX);
                const backWallX = layout.x + (5.1 * dirX);
                
                const rFloor = new THREE.Mesh(new THREE.BoxGeometry(5.0, 0.1, 5.0), transWallMat);
                rFloor.position.set(roomCenterX, baseY - 0.05, roomCenterZ);
                rFloor.receiveShadow = true;
                roomGroup.add(rFloor);
                
                const rCeil = new THREE.Mesh(new THREE.BoxGeometry(5.0, 0.1, 5.0), transWallMat);
                rCeil.position.set(roomCenterX, baseY + 5.0 + 0.05, roomCenterZ);
                rCeil.receiveShadow = true;
                roomGroup.add(rCeil);
                
                const rBackWall = new THREE.Mesh(new THREE.BoxGeometry(0.2, 5.0, 5.0), transWallMat);
                rBackWall.position.set(layout.x + (5.0 * dirX) + (0.1 * dirX), baseY + 2.5, roomCenterZ);
                rBackWall.castShadow = true;
                rBackWall.receiveShadow = true;
                roomGroup.add(rBackWall);
                
                const rSideWall1 = new THREE.Mesh(new THREE.BoxGeometry(5.0, 5.0, 0.2), transWallMat);
                rSideWall1.position.set(roomCenterX, baseY + 2.5, roomCenterZ - 2.5 - 0.1);
                rSideWall1.castShadow = true;
                rSideWall1.receiveShadow = true;
                roomGroup.add(rSideWall1);
                
                const rSideWall2 = new THREE.Mesh(new THREE.BoxGeometry(5.0, 5.0, 0.2), transWallMat);
                rSideWall2.position.set(roomCenterX, baseY + 2.5, roomCenterZ + 2.5 + 0.1);
                rSideWall2.castShadow = true;
                rSideWall2.receiveShadow = true;
                roomGroup.add(rSideWall2);
                
                const rFrontWall1 = new THREE.Mesh(new THREE.BoxGeometry(0.2, 5.0, 1.9), transWallMat);
                rFrontWall1.position.set(wallOffsetX, baseY + 2.5, roomCenterZ - 1.55);
                rFrontWall1.castShadow = true;
                rFrontWall1.receiveShadow = true;
                roomGroup.add(rFrontWall1);
                
                const rFrontWall2 = new THREE.Mesh(new THREE.BoxGeometry(0.2, 5.0, 1.9), transWallMat);
                rFrontWall2.position.set(wallOffsetX, baseY + 2.5, roomCenterZ + 1.55);
                rFrontWall2.castShadow = true;
                rFrontWall2.receiveShadow = true;
                roomGroup.add(rFrontWall2);
                
                const rFrontWallTop = new THREE.Mesh(new THREE.BoxGeometry(0.2, 2.4, 1.2), transWallMat);
                rFrontWallTop.position.set(wallOffsetX, baseY + 3.8, roomCenterZ);
                rFrontWallTop.castShadow = true;
                rFrontWallTop.receiveShadow = true;
                roomGroup.add(rFrontWallTop);
                
                const panel = createDetailedPanel(dirX);
                panel.position.set(layout.x + (4.5 * dirX), baseY, roomCenterZ);
                roomGroup.add(panel);
                
                if (Math.abs(floorNum - state.floor) <= 1) {
                    const transLight = new THREE.PointLight(0x00aaff, doorObj.opened ? 0.5 : 0, 6);
                    transLight.position.set(roomCenterX, baseY + 4, roomCenterZ);
                    transLight.castShadow = (floorNum === state.floor);
                    roomGroup.add(transLight);
                    doorLights[floorNum + '_' + idx] = transLight;
                }
                
            } else {
                const blankWall = new THREE.Mesh(new THREE.BoxGeometry(0.2, 5.0, 1.2), wallMat);
                blankWall.position.set(layout.x + (0.5 * dirX), baseY + 2.5, layout.z);
                blankWall.castShadow = true;
                blankWall.receiveShadow = true;
                roomGroup.add(blankWall);
            }
            
            scene.add(roomGroup);
            roomMeshes.push(roomGroup);
        }
    });
}