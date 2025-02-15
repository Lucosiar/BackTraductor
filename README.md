Arrancar la app

```bash
uvicorn main:app --reload
```

Para probar el servidor:

1. Abre un navegador web y visita `http://127.0.0.1:8000`
2. Deberías ver el mensaje "Traductor en Tiempo Real"

Para detener el servidor:
- Presiona `CTRL+C` en la terminal

Para permitir conexiones desde otros dispositivos en la red local, puedes iniciar el servidor con:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

El servidor está configurado para:
- Reconocimiento de voz en español (es-ES)
- Traducción de español a inglés
- Comunicación en tiempo real mediante WebSockets


ver los logs:
uvicorn main:app --reload --log-level debug