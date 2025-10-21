# 🌡️ Demo Flask IoT - Monitor de Sensores ESP32

Proyecto educativo para aprender a monitorear sensores IoT en tiempo real usando Flask y ESP32 (simulado en Wokwi).

---

## 📋 ¿Qué hace este proyecto?

Este sistema te permite:
1. **Simular un sensor ESP32** que mide temperatura y humedad
2. **Enviar los datos** a un servidor web Flask
3. **Visualizar en tiempo real** los valores en un dashboard web
4. **Monitorear el estado** de conexión del dispositivo

---

## 🎯 Características principales

- ✅ Dashboard web en tiempo real
- ✅ Indicador visual de conexión (verde/amarillo/rojo)
- ✅ Validación automática de datos del sensor
- ✅ Sistema de logs para debugging
- ✅ API REST para integración con otros sistemas
- ✅ Compatible con Windows, Linux y macOS

---

## 📦 Requisitos previos

Antes de comenzar, asegúrate de tener instalado:

### 1. Python 3.10 o superior
Verifica tu versión de Python:

**Windows (PowerShell):**
```powershell
python --version
```

**Linux/macOS:**
```bash
python3 --version
```

Si no tienes Python instalado, descárgalo desde: https://www.python.org/downloads/

### 2. Git (opcional, pero recomendado)
Para clonar el repositorio. Descarga desde: https://git-scm.com/downloads

### 3. Navegador web moderno
Chrome, Firefox, Edge o Safari

---

## 🚀 Instalación y configuración

### PASO 1: Obtener el código

#### Opción A: Clonar con Git
```bash
git clone https://github.com/henryor/Flask-iot-demo.git
cd Flask-iot-demo
```

#### Opción B: Descargar ZIP
1. Ve a https://github.com/henryor/Flask-iot-demo
2. Click en "Code" → "Download ZIP"
3. Extrae el archivo
4. Abre la terminal en la carpeta extraída

---

### PASO 2: Crear entorno virtual (Recomendado)

Un entorno virtual mantiene las dependencias aisladas de otros proyectos Python.

#### En Windows (PowerShell):
```powershell
# Crear el entorno virtual
python -m venv .venv

# Activarlo
.venv\Scripts\Activate.ps1
```

**Si aparece error de permisos:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### En Windows (CMD):
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

#### En Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**✅ Sabrás que está activo cuando veas** `(.venv)` al inicio de tu línea de comandos.

---

### PASO 3: Instalar dependencias

Con el entorno virtual activado:

```bash
pip install -r requirements.txt
```

Esto instalará:
- **Flask 3.0.0**: Framework web para Python
- **python-dotenv 1.1.1**: Gestor de variables de entorno

---

### PASO 4: Configurar el servidor

#### 4.1. Copiar el archivo de configuración

**En Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**En Linux/macOS:**
```bash
cp .env.example .env
```

#### 4.2. (Opcional) Editar configuración

Abre el archivo `.env` con tu editor de texto favorito:

```env
FLASK_HOST=0.0.0.0          # Permite conexiones desde cualquier IP
FLASK_PORT=5000             # Puerto del servidor (puedes cambiarlo)
FLASK_DEBUG=true            # Modo desarrollo (muestra errores detallados)
STATUS_REFRESH_SECONDS=5    # Cada cuántos segundos se actualiza el dashboard
```

**💡 Nota:** Para uso en clase, puedes dejar los valores por defecto.

---

### PASO 5: Iniciar el servidor

```bash
python app.py
```

**✅ Si todo está correcto, verás:**

```
2025-10-03 11:21:05,372 - __main__ - INFO - Starting Flask IoT server on 0.0.0.0:5000 (debug=True)
2025-10-03 11:21:05,373 - __main__ - INFO - Dashboard refresh interval: 5 seconds
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.0.7:5000
```

**🎉 ¡El servidor está funcionando!**

**Para detener el servidor:** Presiona `Ctrl + C`

---

### PASO 6: Abrir el dashboard

1. Abre tu navegador web
2. Ve a: **http://localhost:5000**

**Deberías ver:**
- 🔴 Badge rojo con "Offline" (es normal, aún no hay datos)
- Panel con temperatura y humedad vacíos
- Mensaje "Esperando datos del microcontrolador..."

---

## 🧪 Probar sin hardware (simulación)

Ahora enviaremos datos simulados al servidor para ver cómo funciona.

### Opción 1: PowerShell (Windows) ⭐ MÁS FÁCIL

Abre una **nueva terminal PowerShell** (sin cerrar la del servidor):

```powershell
# Copiar y pegar todo junto
$body = '{"temperature": 23.5, "humidity": 60}'
Invoke-RestMethod -Uri "http://localhost:5000/update" -Method POST -ContentType "application/json" -Body $body
```

### Opción 2: Bash (Linux/macOS/Git Bash)

Abre una **nueva terminal**:

```bash
curl -X POST http://localhost:5000/update \
  -H "Content-Type: application/json" \
  -d '{"temperature": 23.5, "humidity": 60}'
```

### Opción 3: Script de pruebas automatizado

Este script prueba múltiples escenarios (datos válidos, inválidos, fuera de rango):

```bash
python test_validation.py
```

---

### 🎊 ¿Qué deberías ver?

**En el navegador (http://localhost:5000):**
1. 🟢 Badge cambia a verde con "Connected"
2. La temperatura muestra: **23.5°C**
3. La humedad muestra: **60%**
4. La marca de tiempo se actualiza

**En la terminal del servidor:**
```
INFO - Sensor data updated: temp=23.5°C, humidity=60%
```

**💡 Prueba enviar diferentes valores:**

```powershell
# Temperatura alta
$body = '{"temperature": 35.8, "humidity": 75}'
Invoke-RestMethod -Uri "http://localhost:5000/update" -Method POST -ContentType "application/json" -Body $body

# Temperatura fría
$body = '{"temperature": 10.2, "humidity": 45}'
Invoke-RestMethod -Uri "http://localhost:5000/update" -Method POST -ContentType "application/json" -Body $body
```

---

## 🎮 Usar con Wokwi (ESP32 simulado)

### PASO 1: Configurar el firmware

1. Ve a tu proyecto en Wokwi
2. Copia el archivo `firmware/config.h.example` a `config.h`
3. Edita los valores:

```cpp
#define WIFI_SSID "Wokwi-GUEST"
#define WIFI_PASSWORD ""

// Usa la IP de tu computadora (la que aparece en "Running on http://192.168.X.X:5000")
#define API_BASE_URL "http://host.docker.internal:5000"
#define API_UPDATE_PATH "/update"

// Debe coincidir con STATUS_REFRESH_SECONDS del .env
#define POST_INTERVAL_SECONDS 5
```

### PASO 2: Ejecutar en Wokwi

1. Inicia el servidor Flask en tu computadora
2. Inicia la simulación en Wokwi
3. Observa la consola serial (debería mostrar `200 OK`)
4. Refresca el dashboard en tu navegador

**✅ El badge debe cambiar a verde y mostrar los valores del sensor simulado**

---

## 🔍 Solución de problemas

### ❌ Error: "python: command not found"

**Solución Windows:**
```powershell
py app.py
```

**Solución Linux/macOS:**
```bash
python3 app.py
```

---

### ❌ Error: "No module named 'flask'"

**Causa:** No instalaste las dependencias o el entorno virtual no está activado.

**Solución:**
1. Activa el entorno virtual (ver PASO 2)
2. Ejecuta: `pip install -r requirements.txt`

---

### ❌ Badge permanece en rojo

**Posibles causas:**

1. **No has enviado datos:** Envía datos con PowerShell/curl (ver sección "Probar sin hardware")

2. **Pasaron más de 30 segundos desde el último dato:**
   - El sistema marca como "offline" si no hay datos en 30 segundos
   - Envía nuevos datos

3. **Problema con Wokwi:**
   - Verifica que `API_BASE_URL` en `config.h` sea correcto
   - Revisa la consola serial para errores
   - Comprueba que el firewall permita conexiones al puerto 5000

---

### ❌ Error de validación: "Temperature out of range"

**Causa:** El sensor está enviando valores fuera del rango permitido.

**Rangos válidos:**
- Temperatura: -40°C a 85°C
- Humedad: 0% a 100%

**Solución:** Verifica que el sensor DHT11/DHT22 esté funcionando correctamente.

---

### ❌ El dashboard no se actualiza automáticamente

**Solución:**
1. Verifica que el toggle "Auto refresco" esté activado (✅)
2. Abre la consola del navegador (F12) y busca errores
3. Refresca la página (F5)

---

## 📡 Referencia de API

### Endpoints disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Dashboard HTML |
| `/update` | POST | Recibir datos del sensor |
| `/data` | GET | Obtener últimas lecturas |
| `/health` | GET | Estado del sistema |

---

### POST `/update` - Enviar datos del sensor

**Requisitos:**
- Content-Type: `application/json`
- Body: JSON con temperatura y humedad

**Ejemplo de petición:**
```json
{
  "temperature": 23.5,
  "humidity": 60
}
```

**Validaciones automáticas:**
- ✅ Temperatura: debe estar entre -40°C y 85°C
- ✅ Humedad: debe estar entre 0% y 100%
- ✅ Ambos campos son obligatorios
- ✅ Los valores deben ser números

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

**Respuesta de error (400):**
```json
{
  "error": "Temperature out of valid range (-40 to 85°C)"
}
```

---

### GET `/data` - Obtener lecturas actuales

No requiere parámetros.

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

---

### GET `/health` - Estado del servidor

Útil para monitoreo y debugging.

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
- 🟢 `connected`: Recibió datos hace ≤10 segundos
- 🟡 `stale`: Recibió datos hace 10-30 segundos (conexión débil)
- 🔴 `offline`: No hay datos o pasaron >30 segundos

---

## 📚 Para profundizar

### Estructura del proyecto

```
Flask-iot-demo/
├── app.py                      # Servidor Flask principal
├── requirements.txt            # Dependencias Python
├── .env.example               # Plantilla de configuración
├── test_validation.py         # Script de pruebas
├── templates/
│   └── index.html            # Dashboard HTML
├── static/
│   └── style.css             # Estilos CSS
└── firmware/
    └── config.h.example      # Configuración ESP32
```

### Tecnologías utilizadas

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Firmware:** Arduino C++ (ESP32)
- **Simulador:** Wokwi

### Ideas para extender el proyecto

1. **Base de datos:** Guardar histórico de lecturas con SQLite
2. **Gráficas:** Agregar Chart.js para visualizar tendencias
3. **Alertas:** Notificaciones cuando temperatura/humedad excedan límites
4. **Multi-sensor:** Soportar múltiples ESP32 simultáneamente
5. **Autenticación:** Login para proteger el dashboard
6. **PWA:** Convertir en Progressive Web App para usar en móvil

---

## 📞 Soporte

**¿Encontraste un error?** Abre un issue en GitHub: https://github.com/henryor/Flask-iot-demo/issues

**¿Tienes preguntas?** Consulta con tu profesor o revisa la documentación de Flask: https://flask.palletsprojects.com/

---

## 📄 Licencia

Este proyecto es de código abierto para fines educativos.

---

## 📝 Historial de cambios

Consulta `CHANGELOG.md` para ver todas las actualizaciones del proyecto.
#   I O T _ 1 1 1 4  
 