from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from translator import translate_text
from speech_to_text import transcribe_audio_stream

app = FastAPI()

@app.get("/")
async def get():
    return HTMLResponse("<h1>Traductor en Tiempo Real</h1>")

@app.websocket("/ws/translate")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            text = transcribe_audio_stream(data)
            if text:
                translated_text = translate_text(text, target_language="en")
                await websocket.send_json({"translated_text": translated_text})
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {str(e)}")
        await websocket.close()
