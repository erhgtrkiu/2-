function handleFPSMovement(deltaTime) {
    if (state.stairsMonsterActive || hackActive) return; // Locked when monster attacks or hacking
    
    const prevX = playerPos.x;
    const prevZ = playerPos.z;
    
    const moveVector = new THREE.Vector3();
    
    // Get custom keybindings
    const bindFwd = state.keyBindings['MoveForward'] || 'KeyW';
    const bindBwd = state.keyBindings['MoveBackward'] || 'KeyS';
    const bindLft = state.keyBindings['MoveLeft'] || 'KeyA';
    const bindRgt = state.keyBindings['MoveRight'] || 'KeyD';
    const bindSprint = state.keyBindings['Sprint'] || 'ShiftLeft';
    
    // Считываем WASD / Стрелки клавиатуры или виртуальные кнопки D-pad
    if (keys[bindFwd] || keys['ArrowUp'] || mvUp) moveVector.z -= 1;
    if (keys[bindBwd] || keys['ArrowDown'] || mvDown) moveVector.z += 1;
    if (keys[bindLft] || keys['ArrowLeft'] || mvLeft) moveVector.x -= 1;
    if (keys[bindRgt] || keys['ArrowRight'] || mvRight) moveVector.x += 1;
    
    let currentSpeed = playerSpeed;
    let isSprinting = keys[bindSprint] || keys['ShiftLeft'] || keys['ShiftRight'];
    
    if (isSprinting && moveVector.lengthSq() > 0 && state.stamina > 0) {
        currentSpeed = 6.5;
        state.stamina = Math.max(0, state.stamina - 30 * deltaTime);
    } else {
        if (moveVector.lengthSq() > 0) {
            state.stamina = Math.min(100, state.stamina + 15 * deltaTime);
        } else {
            state.stamina = Math.min(100, state.stamina + 25 * deltaTime);
        }
    }
    
    if (moveVector.lengthSq() > 0) {
        // Переводим вектор движения относительно взгляда игрока (yaw)
        moveVector.normalize();
        moveVector.applyAxisAngle(new THREE.Vector3(0, 1, 0), playerYaw);
        
        // Умножаем на скорость
        const finalSpeed = window._customSpeed || currentSpeed;
        moveVector.multiplyScalar(finalSpeed * deltaTime);
        
        // Новые предлагаемые координаты
        const nextX = playerPos.x + moveVector.x;
        const nextZ = playerPos.z + moveVector.z;
        
        // Обработка границ и коллизий (Бесшовный мир)
        // 1. Коридор и Лестница
        if (nextZ < -42) {
            // Лестничная шахта
            let allowed = false;
            
            // Проверка границ в лестничной шахте
            if (nextZ >= -49.5) {
                if (nextZ >= -47.0) {
                    // Коридоры лестниц
                    if (playerPos.x < 0) {
                        // Левая лестница
                        if (nextX >= -1.4 && nextX <= -0.1) {
                            allowed = true;
                        }
                    } else {
                        // Правая лестница
                        if (nextX >= 0.1 && nextX <= 1.4) {
                            allowed = true;
                        }
                    }
                } else {
                    // Разворотная площадка
                    if (nextX >= -1.4 && nextX <= 1.4) {
                        allowed = true;
                    }
                }
            }
            
            if (allowed) {
                // Stairs doors collision check at Z = -47.0
                const sdState = getOrGenerateStairsDoor(state.floor);
                let finalNextZ = nextZ;
                if (!sdState.opened) {
                    if (playerPos.z >= -47.0 && nextZ < -47.0) {
                        finalNextZ = -46.95;
                    } else if (playerPos.z < -47.0 && nextZ >= -47.0) {
                        finalNextZ = -47.05;
                    }
                }
                
                playerPos.x = nextX;
                playerPos.z = finalNextZ;
                
                // Вычисляем высоту
                playerPos.y = getStepsY(playerPos.x, playerPos.y, playerPos.z);
                
                // Смена этажей по высоте Y
                if (playerPos.y < -4.7) {
                    state.floor = state.floor - 1;
                    playerPos.y += 5.0;
                    
                    if (state.floor < END_FLOOR) { // Allow floor 1
                        triggerGameOver("ending_2");
                        return;
                    }
                    
                    if (Math.random() < 0.1 && !state.stairsMonsterActive) {
                        triggerStairsMonster();
                    } else {
                        logToConsole(`Вы спустились на этаж ${state.floor}.`, "sys");
                    }
                    
                    build3DScene();
                    updateHUD();
                } else if (playerPos.y > 4.7) {
                    if (state.floor >= state.spawnFloor) {
                        // Clamp floor ascension
                        playerPos.y = 4.7;
                        logToConsole("Верхние этажи заблокированы гермозатвором. Прохода нет.", "warn");
                    } else {
                        state.floor = state.floor + 1;
                        playerPos.y -= 5.0;
                        
                        logToConsole(`Вы поднялись на этаж ${state.floor}.`, "sys");
                        
                        build3DScene();
                        updateHUD();
                    }
                }
                
                if (state.location !== 'hallway') {
                    state.location = 'hallway';
                    updateHUD();
                }
            }
        } else if (nextZ > 0.5) {
            // Задний тупик
            playerPos.z = 0.5;
        } else {
            // КОРИДОР И КОМНАТЫ (Z от 0 до -42) — AABB Collision System
            playerPos.y = 0; // На этаже
            
            // Build AABB colliders for walls and doors
            const colliders = [];
            const PR = 0.3; // Player radius
            
            // Corridor walls (left and right) — segments between doors
            // Left wall
            colliders.push({ minX: -3.2, maxX: -2.9, minZ: -9.4, maxZ: 0.0 });
            colliders.push({ minX: -3.2, maxX: -2.9, minZ: -21.4, maxZ: -10.6 });
            colliders.push({ minX: -3.2, maxX: -2.9, minZ: -33.4, maxZ: -22.6 });
            colliders.push({ minX: -3.2, maxX: -2.9, minZ: -42.0, maxZ: -34.6 });
            // Right wall
            colliders.push({ minX: 2.9, maxX: 3.2, minZ: -9.4, maxZ: 0.0 });
            colliders.push({ minX: 2.9, maxX: 3.2, minZ: -21.4, maxZ: -10.6 });
            colliders.push({ minX: 2.9, maxX: 3.2, minZ: -33.4, maxZ: -22.6 });
            colliders.push({ minX: 2.9, maxX: 3.2, minZ: -42.0, maxZ: -34.6 });
            // Back wall (spawn end)
            colliders.push({ minX: -3.2, maxX: 3.2, minZ: 0.0, maxZ: 0.3 });
            
            // Door and room colliders
            DOOR_LAYOUT.forEach((layout, idx) => {
                const doorObj = state.doors[idx];
                if (!doorObj) return;
                
                const isLeft = layout.x < 0;
                
                // Closed door or empty slot — block the doorway
                if (!doorObj.opened || doorObj.type === 'empty') {
                    if (isLeft) {
                        colliders.push({ minX: -3.2, maxX: -2.9, minZ: layout.z - 0.6, maxZ: layout.z + 0.6 });
                    } else {
                        colliders.push({ minX: 2.9, maxX: 3.2, minZ: layout.z - 0.6, maxZ: layout.z + 0.6 });
                    }
                }
                
                // Room walls (if door exists and is not empty)
                if (doorObj.type !== 'empty') {
                    const roomWidth = doorObj.type === 'apartment' ? 3.5 : (doorObj.type === 'monster' ? 4.0 : 2.5);
                    const roomDepth = doorObj.type === 'apartment' ? 7.0 : 5.0;
                    const dirX = isLeft ? -1 : 1;
                    
                    const backWallX = layout.x + roomDepth * dirX;
                    const zMin = layout.z - roomWidth;
                    const zMax = layout.z + roomWidth;
                    
                    // Back wall of room
                    colliders.push({ minX: backWallX - 0.15, maxX: backWallX + 0.15, minZ: zMin, maxZ: zMax });
                    
                    // Side walls of room
                    colliders.push({ minX: Math.min(layout.x, backWallX), maxX: Math.max(layout.x, backWallX), minZ: zMin - 0.15, maxZ: zMin + 0.15 });
                    colliders.push({ minX: Math.min(layout.x, backWallX), maxX: Math.max(layout.x, backWallX), minZ: zMax - 0.15, maxZ: zMax + 0.15 });
                    
                    // Front wall segments (around doorway)
                    const frontDoorHalf = 0.6;
                    if (isLeft) {
                        colliders.push({ minX: -3.2, maxX: -2.9, minZ: zMin, maxZ: layout.z - frontDoorHalf });
                        colliders.push({ minX: -3.2, maxX: -2.9, minZ: layout.z + frontDoorHalf, maxZ: zMax });
                    } else {
                        colliders.push({ minX: 2.9, maxX: 3.2, minZ: zMin, maxZ: layout.z - frontDoorHalf });
                        colliders.push({ minX: 2.9, maxX: 3.2, minZ: layout.z + frontDoorHalf, maxZ: zMax });
                    }
                    
                    // Furniture colliders inside rooms
                    if (doorObj.type === 'apartment') {
                        const cabX = layout.x + 5.5 * dirX;
                        const cabZ = layout.z - 2.0;
                        colliders.push({ minX: cabX - 1.0, maxX: cabX + 1.0, minZ: cabZ - 0.5, maxZ: cabZ + 0.5 });
                        
                        const tableX = layout.x + 3.7 * dirX;
                        const tableZ = layout.z;
                        colliders.push({ minX: tableX - 0.9, maxX: tableX + 0.9, minZ: tableZ - 0.6, maxZ: tableZ + 0.6 });
                    } else if (doorObj.type === 'transition') {
                        const panelX = layout.x + 4.5 * dirX;
                        colliders.push({ minX: panelX - 0.4, maxX: panelX + 0.4, minZ: layout.z - 0.8, maxZ: layout.z + 0.8 });
                    }
                }
            });
            
            // AABB vs circle collision check
            function checkAABBCollision(px, pz, radius) {
                for (const box of colliders) {
                    const closestX = Math.max(box.minX, Math.min(px, box.maxX));
                    const closestZ = Math.max(box.minZ, Math.min(pz, box.maxZ));
                    const distX = px - closestX;
                    const distZ = pz - closestZ;
                    if ((distX * distX + distZ * distZ) < (radius * radius)) {
                        return true;
                    }
                }
                return false;
            }
            
            // Try X movement independently
            if (!checkAABBCollision(nextX, playerPos.z, PR)) {
                playerPos.x = nextX;
            }
            // Try Z movement independently
            if (!checkAABBCollision(playerPos.x, nextZ, PR)) {
                playerPos.z = nextZ;
            }
            
            // Determine location (hallway vs room)
            let insideRoomIdx = -1;
            DOOR_LAYOUT.forEach((layout, idx) => {
                const doorObj = state.doors[idx];
                if (!doorObj || doorObj.type === 'empty') return;
                
                const isLeft = layout.x < 0;
                const roomWidth = doorObj.type === 'apartment' ? 3.5 : (doorObj.type === 'monster' ? 4.0 : 2.5);
                const roomDepth = doorObj.type === 'apartment' ? 7.0 : 5.0;
                const dirX = isLeft ? -1 : 1;
                const backWallX = layout.x + roomDepth * dirX;
                
                const pxInRoom = isLeft ? 
                    (playerPos.x <= layout.x && playerPos.x >= backWallX) :
                    (playerPos.x >= layout.x && playerPos.x <= backWallX);
                const pzInRoom = (playerPos.z >= layout.z - roomWidth && playerPos.z <= layout.z + roomWidth);
                
                if (pxInRoom && pzInRoom) {
                    insideRoomIdx = idx;
                }
            });
            
            if (insideRoomIdx >= 0) {
                const newLoc = state.doors[insideRoomIdx].type === 'apartment' ? 'room' : 
                               (state.doors[insideRoomIdx].type === 'transition' ? 'transition' : 'room');
                if (state.location !== newLoc || state.focusedDoorIndex !== insideRoomIdx) {
                    const oldLoc = state.location;
                    state.location = newLoc;
                    state.focusedDoorIndex = insideRoomIdx;
                    updateHUD();
                    
                    // Выводим описание атмосферы при входе в новую комнату
                    if (newLoc === 'room' && oldLoc === 'hallway') {
                        const door = state.doors[insideRoomIdx];
                        if (door.roomType === 'armory') {
                            logToConsole(`Вы вошли в ${door.name}. На стене висит знак Ликвидаторов. Под ногами рассыпаны гильзы.`, "sys");
                        } else if (door.roomType === 'contaminated') {
                            logToConsole(`Вы вошли в ${door.name}. Воздух здесь едкий и желтоватый. Счетчик Гейгера тихо потрескивает! (Фильтр тратится быстрее)`, "danger");
                        } else if (door.roomType === 'nest') {
                            logToConsole(`Вы вошли в ${door.name}. В углу копошится склизкая биомасса. Старайтесь не шуметь!`, "warn");
                        } else {
                            logToConsole(`Вы вошли в квартиру. Вокруг обычная серая обстановка советской квартиры-хрущевки.`, "sys");
                        }
                    }
                }
            } else {
                if (state.location !== 'hallway') {
                    state.location = 'hallway';
                    state.focusedDoorIndex = null;
                    updateHUD();
                }
            }
        }
        
        state.water = Math.max(0, state.water - 0.002); // Slower water consumption when moving
        
        // Footstep sound system: trigger steps at walking rate if actually moved
        const distMoved = Math.sqrt((playerPos.x - prevX) * (playerPos.x - prevX) + (playerPos.z - prevZ) * (playerPos.z - prevZ));
        if (distMoved > 0.01) {
            footstepTimeAccumulator += deltaTime;
            const finalSpd = window._customSpeed || currentSpeed;
            const stepInterval = Math.max(0.2, 1.5 / finalSpd);
            if (footstepTimeAccumulator >= stepInterval) {
                playSoundStep();
                footstepTimeAccumulator = 0;
            }
        } else {
            footstepTimeAccumulator = 0;
        }
    }
}