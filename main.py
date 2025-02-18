from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from translator import translate_text
from speech_to_text import transcribe_audio_stream

app = FastAPI()

@app.get("/")
async def get():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Traductor en Tiempo Real</title>
            <style>
                .audio-indicator {
                    width: 20px;
                    height: 20px;
                    background-color: red;
                    border-radius: 50%;
                    display: none;
                    margin: 10px;
                    transition: all 0.3s ease;
                }

                .active {
                    display: inline-block;
                    width: 40px;
                    height: 40px;
                    background-color: #4CAF50;
                    animation: pulse 1.5s infinite;
                }

                @keyframes pulse {
                    0% { transform: scale(1); opacity: 1; }
                    50% { transform: scale(1.5); opacity: 0.7; }
                    100% { transform: scale(1); opacity: 1; }
                }
            </style>
        </head>
        <body>
            <h1>Traductor en Tiempo Real</h1>
            <button id="startButton">Iniciar Traducción</button>
            <div class="audio-indicator" id="audioIndicator"></div>
            <div id="result"></div>

            <script>
                let ws;
                let mediaRecorder;
                let audioChunks = [];
                const startButton = document.getElementById('startButton');
                const result = document.getElementById('result');
                const audioIndicator = document.getElementById('audioIndicator');

                startButton.onclick = async function() {
                    if (!ws) {
                        try {
                            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                            ws = new WebSocket('ws://localhost:8000/ws/translate');
                            startButton.textContent = 'Detener Traducción';
                            audioIndicator.classList.add('active');

                            mediaRecorder = new MediaRecorder(stream);
                            mediaRecorder.ondataavailable = event => {
                                if (event.data.size > 0) {
                                    ws.send(event.data);
                                }
                            };

                            ws.onmessage = function(event) {
                                const data = JSON.parse(event.data);
                                result.innerHTML += `<p>${data.translated_text}</p>`;
                            };

                            mediaRecorder.start(1000);
                        } catch (error) {
                            console.error('Error:', error);
                            alert('Error al acceder al micrófono');
                        }
                    } else {
                        if (mediaRecorder) {
                            mediaRecorder.stop();
                            mediaRecorder.stream.getTracks().forEach(track => track.stop());
                        }
                        ws.close();
                        ws = null;
                        startButton.textContent = 'Iniciar Traducción';
                        audioIndicator.classList.remove('active');
                    }
                };
            </script>
        </body>
    </html>
    """
    return HTMLResponse(html_content)

@app.websocket("/ws/translate")
async def websocket_endpoint(websocket: WebSocket):
    print("Nueva conexión WebSocket establecida")
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            text = transcribe_audio_stream(data)
            if text:
                print(f"Texto detectado: {text}")
                translated_text = translate_text(text, target_language="en")
                print(f"Traducción: {translated_text}")
                await websocket.send_json({"translated_text": translated_text})
    except WebSocketDisconnect:
        print("Cliente desconectado")
    except Exception as e:
        print(f"Error: {str(e)}")
        await websocket.close()
