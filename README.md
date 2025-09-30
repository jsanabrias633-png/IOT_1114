# Demo Flask IoT

Pequeño proyecto educativo para monitorear un sensor simulado (ESP32 en Wokwi) desde un panel Flask. Incluye un endpoint de salud y una cabecera de estado que muestran claramente si la conexión está activa y cuándo llegó el último dato.

## Flujo de datos
- El firmware del ESP32 mide temperatura y humedad y envía un POST con JSON al endpoint `/update` del servidor Flask.
- El backend guarda el último paquete en memoria, registra la hora de llegada y expone `/health` con la información de conexión.
- El dashboard consulta `/health` de forma periódica para actualizar el badge de estado, la marca de tiempo y los valores mostrados.

## Requisitos
- Python 3.10+ instalado localmente.
- Acceso a internet solo para instalar dependencias (el servidor no necesita conexión externa).
- Cuenta gratuita en [https://wokwi.com](https://wokwi.com) si deseas probar el firmware simulado.

## Configuración rápida
1. Clona el repositorio y entra en la carpeta del proyecto.
2. (Opcional) Crea un entorno virtual: `python -m venv .venv` y actívalo.
3. Instala dependencias: `pip install -r requirements.txt`.
4. Copia `.env.example` a `.env` y ajusta las opciones si quieres cambiar host, puerto o intervalo de refresco.
5. Ejecuta el servidor: `python app.py` (carga automática de `.env`).
6. Abre `http://localhost:5000` en el navegador; verás el panel con el badge de conexión.

## Prueba rápida sin hardware
1. Arranca el servidor como se indicó arriba.
2. En otra terminal, envía un dato de prueba:  
   `curl -X POST http://localhost:5000/update -H "Content-Type: application/json" -d '{"temperature": 23.4, "humidity": 55}'`
3. La cabecera debe cambiar a verde (Connected) y mostrar la hora actualizada.
4. Comprueba `/health`: `curl http://localhost:5000/health` para ver el JSON con estado, último update y uptime.

## Firmware ESP32 (Wokwi)
1. Copia `firmware/config.h.example` a `config.h` dentro de tu sketch y coloca SSID, contraseña y URL del backend (`API_BASE_URL`).
2. Asegúrate de usar `POST_INTERVAL_SECONDS` similar a `STATUS_REFRESH_SECONDS` para que la UI y el firmware estén sincronizados.
3. En Wokwi, usa `host.docker.internal` (o tu IP local) como base para llegar al servidor Flask en tu máquina.
4. Observa la consola serial: cada POST debería responder con `200 OK`. El panel web debe reflejar los valores y marcar la conexión como activa.

## Capturas y evidencia
- `docs/screenshots/dashboard-after.png`: placeholder del panel actualizado. Sustituye por una captura real tras probarlo.
- `docs/screenshots/connection-flow.gif`: placeholder de la secuencia de conexión. Actualiza con un GIF corto si grabas la prueba.

## Solución de problemas
- **Badge en rojo**: revisa credenciales Wi-Fi en `config.h` y que `API_BASE_URL` apunte al servidor correcto.
- **"Sin datos" permanente**: el backend aún no recibió POSTs. Usa el comando curl de prueba.
- **Wokwi sin acceso**: abre el puerto en tu firewall o usa la IP LAN si estás en hardware real.

## Historial de cambios
Consulta `CHANGELOG.md` para ver qué se modificó y por qué.