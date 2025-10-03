# Demo Flask IoT

Pequeño proyecto educativo para monitorear un sensor simulado (ESP32 en Wokwi) desde un panel Flask. Incluye un endpoint de salud y una cabecera de estado que muestran claramente si la conexión está activa y cuándo llegó el último dato.

## Características

- ✅ **Validación robusta de datos**: Verifica rangos y tipos de datos de sensores
- ✅ **Logging completo**: Registra todas las operaciones y errores
- ✅ **Estados de conexión**: Connected, Stale y Offline basados en timestamps
- ✅ **Dashboard en tiempo real**: Auto-refresh cada 5 segundos
- ✅ **API REST completa**: Endpoints para datos, salud y actualizaciones

## Flujo de datos

- El firmware del ESP32 mide temperatura y humedad y envía un POST con JSON al endpoint `/update` del servidor Flask.
- El backend valida los datos, guarda el último paquete en memoria, registra la hora de llegada y expone `/health` con la información de conexión.
- El dashboard consulta `/health` de forma periódica para actualizar el badge de estado, la marca de tiempo y los valores mostrados.

## Requisitos previos

- **Python 3.10+** instalado localmente
- **pip** (gestor de paquetes de Python)
- Acceso a internet solo para instalar dependencias (el servidor no necesita conexión externa)
- Cuenta gratuita en [https://wokwi.com](https://wokwi.com) si deseas probar el firmware simulado

## Instalación paso a paso

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd Flask-iot-demo
```

### 2. Crear entorno virtual (recomendado)

**En Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**En Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**En Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:
- Flask 3.0.0
- python-dotenv 1.1.1

### 4. Configurar variables de entorno

Copia el archivo de ejemplo y ajusta si es necesario:

```bash
cp .env.example .env
```

**Contenido del archivo `.env`:**
```env
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=true
STATUS_REFRESH_SECONDS=5
```

### 5. Iniciar el servidor

```bash
python app.py
```

Deberías ver en la consola:
```
2025-10-03 11:21:05,372 - __main__ - INFO - Starting Flask IoT server on 0.0.0.0:5000 (debug=True)
2025-10-03 11:21:05,373 - __main__ - INFO - Dashboard refresh interval: 5 seconds
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.0.7:5000
```

### 6. Acceder al dashboard

Abre tu navegador y visita: **http://localhost:5000**

Verás el panel con:
- Badge de estado (rojo/Offline al inicio)
- Última actualización
- Toggle de auto-refresh
- Valores de temperatura y humedad

## Prueba rápida sin hardware

### Opción 1: PowerShell (Windows)

```powershell
# Enviar datos válidos
$body = '{"temperature": 23.5, "humidity": 60}'
Invoke-RestMethod -Uri "http://localhost:5000/update" -Method POST -ContentType "application/json" -Body $body
```

### Opción 2: Bash/curl (Linux/macOS/Git Bash)

```bash
curl -X POST http://localhost:5000/update \
  -H "Content-Type: application/json" \
  -d '{"temperature": 23.4, "humidity": 55}'
```

### Opción 3: Script de pruebas automatizado

```bash
python test_validation.py
```

Este script ejecuta 13 casos de prueba incluyendo:
- ✅ Datos válidos
- ❌ Datos fuera de rango
- ❌ Tipos de datos incorrectos
- ❌ Campos faltantes
- ✅ Casos límite (edge cases)

### Resultados esperados

Después de enviar datos válidos:
1. El badge cambia a **verde (Connected)**
2. La marca de tiempo se actualiza
3. Los valores de temperatura y humedad se muestran
4. Los logs muestran: `INFO - Sensor data updated: temp=23.5°C, humidity=60%`

## API Endpoints

### `GET /`
Renderiza el dashboard HTML principal.

### `POST /update`
Recibe datos del sensor ESP32.

**Body (JSON):**
```json
{
  "temperature": 23.5,
  "humidity": 60
}
```

**Validaciones:**
- Temperatura: -40°C a 85°C
- Humedad: 0% a 100%
- Ambos campos requeridos
- Valores numéricos

**Respuesta exitosa (200):**
```json
{
  "status": "success",
  "connection": "connected",
  "data": {
    "temperature": 23.5,
    "humidity": 60
  },
  "last_update": "2025-10-03T16:21:05.123456+00:00"
}
```

**Respuesta error (400):**
```json
{
  "error": "Temperature out of valid range (-40 to 85°C)"
}
```

### `GET /data`
Obtiene las últimas lecturas del sensor.

**Respuesta:**
```json
{
  "data": {
    "temperature": 23.5,
    "humidity": 60
  },
  "last_update": "2025-10-03T16:21:05.123456+00:00",
  "connection": "connected"
}
```

### `GET /health`
Endpoint de monitoreo con información detallada.

**Respuesta:**
```json
{
  "status": "connected",
  "data": {
    "temperature": 23.5,
    "humidity": 60
  },
  "last_update": "2025-10-03T16:21:05.123456+00:00",
  "seconds_since_update": 2.5,
  "uptime_seconds": 120.8
}
```

**Estados posibles:**
- `connected`: ≤10 segundos desde última actualización
- `stale`: 10-30 segundos desde última actualización
- `offline`: >30 segundos o sin datos

## Firmware ESP32 (Wokwi)
1. Copia `firmware/config.h.example` a `config.h` dentro de tu sketch y coloca SSID, contrase�a y URL del backend (`API_BASE_URL`).
2. Aseg�rate de usar `POST_INTERVAL_SECONDS` similar a `STATUS_REFRESH_SECONDS` para que la UI y el firmware est�n sincronizados.
3. En Wokwi, usa `host.docker.internal` (o tu IP local) como base para llegar al servidor Flask en tu m�quina.
4. Observa la consola serial: cada POST deber�a responder con `200 OK`. El panel web debe reflejar los valores y marcar la conexi�n como activa.

## Capturas y evidencia
- `docs/screenshots/dashboard-after.png`: placeholder del panel actualizado. Sustituye por una captura real tras probarlo.
- `docs/screenshots/connection-flow.gif`: placeholder de la secuencia de conexi�n. Actualiza con un GIF corto si grabas la prueba.

## Soluci�n de problemas
- **Badge en rojo**: revisa credenciales Wi-Fi en `config.h` y que `API_BASE_URL` apunte al servidor correcto.
- **"Sin datos" permanente**: el backend a�n no recibi� POSTs. Usa el comando curl de prueba.
- **Wokwi sin acceso**: abre el puerto en tu firewall o usa la IP LAN si est�s en hardware real.

## Historial de cambios
Consulta `CHANGELOG.md` para ver qu� se modific� y por qu�.