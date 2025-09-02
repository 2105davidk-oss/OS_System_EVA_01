# Hier kommt der Code für das Spielobjekt hin
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Webcam Multiplayer-Spiel</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js" crossorigin="anonymous"></script>
    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #e5e7eb;
        }
        .blinking {
            animation: blinker 1s linear infinite;
        }
        @keyframes blinker {
            50% { opacity: 0; }
        }
    </style>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center p-4">
    <div class="bg-white rounded-xl shadow-lg p-6 max-w-4xl w-full text-center">
        <h1 class="text-3xl font-bold mb-4 text-gray-800">Webcam Multiplayer-Spiel</h1>
        <p class="text-sm text-gray-600 mb-6">
            Erlaube den Webcam-Zugriff. Deine Handbewegungen steuern einen Avatar.
            <br>Verbindungsstatus: <span id="connectionStatus" class="font-bold text-red-500 blinking">Getrennt</span>
        </p>
        <div class="relative w-full aspect-video rounded-xl overflow-hidden mb-4 border-4 border-gray-400">
            <!-- Canvas für das Spiel -->
            <canvas id="gameCanvas" class="absolute w-full h-full top-0 left-0 bg-gray-200"></canvas>
            <!-- Video-Element für den Webcam-Feed (optional, kann ausgeblendet werden) -->
            <video id="webcamVideo" class="absolute top-0 left-0 w-1/4 h-1/4 object-cover" autoplay playsinline style="display: none;"></video>
            <div id="statusMessage" class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-gray-900 bg-opacity-75 text-white py-2 px-4 rounded-lg text-lg">
                Lade KI-Modell...
            </div>
        </div>
        <div class="flex justify-center space-x-4 mt-4">
            <button id="spawn-table-btn" class="px-6 py-3 bg-blue-500 text-white rounded-lg font-bold shadow-md hover:bg-blue-600 transition-colors">Tisch platzieren</button>
        </div>
    </div>

    <script>
        const videoElement = document.getElementById('webcamVideo');
        const gameCanvas = document.getElementById('gameCanvas');
        const canvasCtx = gameCanvas.getContext('2d');
        const statusMessage = document.getElementById('statusMessage');
        const connectionStatus = document.getElementById('connectionStatus');
        const spawnTableBtn = document.getElementById('spawn-table-btn');
        let camera;
        let socket;
        let myId;
        const players = {};
        const objects = {}; // Speicher für interaktive Objekte
        const objectSize = 60; // Größe des Tisches

        function setupCanvas() {
            gameCanvas.width = videoElement.videoWidth || 1280;
            gameCanvas.height = videoElement.videoHeight || 720;
        }

        // Zeichnet den polygonalen Avatar
        function drawPlayerAvatar(player) {
            canvasCtx.fillStyle = player.color;
            canvasCtx.strokeStyle = 'black';
            canvasCtx.lineWidth = 2;

            const size = 40;
            const handSize = 10;
            const headSize = 15;

            // Zeichne den Körper (Rechteck)
            canvasCtx.fillRect(player.x - size / 2, player.y - size / 2, size, size);
            canvasCtx.strokeRect(player.x - size / 2, player.y - size / 2, size, size);

            // Zeichne den Kopf (Kreis)
            canvasCtx.beginPath();
            canvasCtx.arc(player.x, player.y - size / 2 - headSize, headSize, 0, 2 * Math.PI);
            canvasCtx.fillStyle = 'white';
            canvasCtx.fill();
            canvasCtx.stroke();

            // Zeichne die Hände (Kreise)
            // Linke Hand
            canvasCtx.beginPath();
            canvasCtx.arc(player.x - size / 2 - handSize, player.y, handSize, 0, 2 * Math.PI);
            canvasCtx.fillStyle = player.color;
            canvasCtx.fill();
            canvasCtx.stroke();
            // Rechte Hand
            canvasCtx.beginPath();
            canvasCtx.arc(player.x + size / 2 + handSize, player.y, handSize, 0, 2 * Math.PI);
            canvasCtx.fillStyle = player.color;
            canvasCtx.fill();
            canvasCtx.stroke();

            // Spieler-ID anzeigen
            canvasCtx.fillStyle = 'white';
            canvasCtx.font = '12px Inter';
            canvasCtx.textAlign = 'center';
            canvasCtx.fillText(player.id.substring(0, 4), player.x, player.y + 5);
        }

        // Zeichnet einen Tisch
        function drawTable(object) {
            canvasCtx.fillStyle = '#8b4513';
            canvasCtx.strokeStyle = '#654321';
            canvasCtx.lineWidth = 3;

            const halfSize = objectSize / 2;
            canvasCtx.fillRect(object.x - halfSize, object.y - halfSize, objectSize, objectSize);
            canvasCtx.strokeRect(object.x - halfSize, object.y - halfSize, objectSize, objectSize);
        }

        // Einfache AABB-Kollisionserkennung
        function checkCollision(player, object) {
            const playerHalfSize = 20; // Halbe Größe des Avatars
            const objectHalfSize = objectSize / 2;
            return player.x < object.x + objectHalfSize &&
                   player.x + playerHalfSize > object.x &&
                   player.y < object.y + objectHalfSize &&
                   player.y + playerHalfSize > object.y;
        }

        const hands = new Hands({
            locateFile: (file) => {
                return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
            }
        });

        hands.setOptions({
            maxNumHands: 1,
            modelComplexity: 1,
            minDetectionConfidence: 0.7,
            minTrackingConfidence: 0.7
        });

        hands.onResults((results) => {
            canvasCtx.clearRect(0, 0, gameCanvas.width, gameCanvas.height);
            canvasCtx.fillStyle = '#E5E7EB';
            canvasCtx.fillRect(0, 0, gameCanvas.width, gameCanvas.height);

            const myPlayer = players[myId];
            if (!myPlayer) return;

            // Lokalen Avatar-Status aktualisieren und an Server senden
            if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
                const landmark = results.multiHandLandmarks[0][9]; // Mittelpunkt der Hand
                const playerX = landmark.x * gameCanvas.width;
                const playerY = landmark.y * gameCanvas.height;

                const dx = playerX - myPlayer.x;
                const dy = playerY - myPlayer.y;

                myPlayer.x = playerX;
                myPlayer.y = playerY;

                // Kollisionserkennung und Stoß-Logik
                for (const id in objects) {
                    if (objects.hasOwnProperty(id)) {
                        const object = objects[id];
                        if (checkCollision(myPlayer, object)) {
                            // Verschiebe das Objekt
                            object.x += dx;
                            object.y += dy;
                            // Sende die neue Position des Objekts an den Server
                            socket.emit('object_move', { id: id, x: object.x, y: object.y });
                        }
                    }
                }

                if (socket && socket.connected) {
                    socket.emit('player_move', { x: myPlayer.x, y: myPlayer.y });
                }
            }

            // Alle Spieler-Avatare zeichnen (einschließlich des eigenen)
            for (const id in players) {
                if (players.hasOwnProperty(id)) {
                    drawPlayerAvatar(players[id]);
                }
            }

            // Alle Objekte zeichnen
            for (const id in objects) {
                if (objects.hasOwnProperty(id)) {
                    drawTable(objects[id]);
                }
            }
        });

        function setupSocket() {
            socket = io('http://localhost:3000');

            socket.on('connect', () => {
                myId = socket.id;
                connectionStatus.textContent = 'Verbunden';
                connectionStatus.classList.remove('text-red-500', 'blinking');
                connectionStatus.classList.add('text-green-500');
            });

            socket.on('disconnect', () => {
                connectionStatus.textContent = 'Getrennt';
                connectionStatus.classList.remove('text-green-500');
                connectionStatus.classList.add('text-red-500', 'blinking');
                delete players[myId];
            });

            socket.on('player_update', (data) => {
                players[data.id] = data;
            });

            socket.on('player_disconnect', (id) => {
                delete players[id];
            });

            socket.on('object_update', (data) => {
                objects[data.id] = data;
            });
        }

        spawnTableBtn.addEventListener('click', () => {
            if (socket && socket.connected) {
                const randomX = Math.random() * gameCanvas.width;
                const randomY = Math.random() * gameCanvas.height;
                socket.emit('spawn_object', { type: 'table', x: randomX, y: randomY });
            }
        });

        async function startWebcam() {
            try {
                camera = new Camera(videoElement, {
                    onFrame: async () => {
                        await hands.send({ image: videoElement });
                    },
                    width: 1280,
                    height: 720
                });
                await camera.start();
                videoElement.addEventListener('loadeddata', () => {
                    setupCanvas();
                    statusMessage.style.display = 'none';
                    setupSocket();
                });
            } catch (error) {
                statusMessage.textContent = 'Fehler: Webcam nicht gefunden oder Zugriff verweigert.';
                statusMessage.classList.add('bg-red-500');
            }
        }

        window.addEventListener('load', startWebcam);
    </script>
</body>
</html>
