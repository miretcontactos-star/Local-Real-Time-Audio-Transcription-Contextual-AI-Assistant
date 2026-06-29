📝 Resumen del Proyecto: Interview Assistant Copilot
Este proyecto es un asistente de IA local en tiempo real diseñado para capturar el audio de una reunión, entrevista o video técnico, transcribirlo automáticamente e inmediatamente generar sugerencias de respuestas profesionales y contextualizadas en español.

Aspectos Técnicos Clave:
Captura de Audio Local: Utiliza sounddevice para escuchar el canal de audio del sistema (configurado mediante cables virtuales como VB-Audio).

Procesamiento de Voz (STT): Implementa el modelo Whisper de OpenAI (small) corriendo de manera nativa en la GPU (Nvidia RTX 4060) mediante CUDA para una transcripción instantánea.

Segmentación por Silencio: Un búfer inteligente acumula el audio mientras detecta voz por encima del umbral calibrado (0.010) y dispara el análisis de forma automática tras 1.5 segundos de silencio continuo.

Inferencia de IA Local: Se comunica mediante el SDK oficial de Ollama con el modelo Llama 3 (8B) de Meta, garantizando privacidad absoluta (sin llamadas a APIs externas como OpenAI) y velocidad de respuesta local.

📘 Estructura del Manual Práctico para tu Portafolio
Podés guardar esto en un archivo llamado README.md dentro de la carpeta de tu proyecto en GitHub:

Markdown
# Real-Time Interview Assistant Copilot 🎙️🤖

Este proyecto es un asistente de IA local diseñado para profesionales de IT. Captura el audio del sistema en tiempo real, realiza la transcripción de voz a texto (STT) mediante Whisper corriendo en GPU y genera de forma automática sugerencias de respuestas técnicas contextualizadas utilizando modelos de lenguaje locales (LLMs) vía Ollama.

## 🚀 Características principales
- **Procesamiento en Tiempo Real:** Segmentación inteligente de audio basada en el volumen del micrófono/canal virtual y detección de pausas de voz.
- **Inferencia 100% Local:** Privacidad absoluta de datos al ejecutar Whisper y Llama 3 localmente sin dependencias en la nube.
- **Aceleración por Hardware:** Optimizado para GPUs NVIDIA mediante ejecución nativa con CUDA.
- **Formateo Contextual:** Respuestas inmediatas divididas en un resumen de la pregunta y una propuesta de respuesta en primera persona.

## 🛠️ Stack Tecnológico
- **Lenguaje:** Python 3.10+
- **Procesamiento de Audio:** `sounddevice`, `numpy`
- **Transcripción de Voz (STT):** OpenAI Whisper (Modelo: `small` con soporte CUDA)
- **Motor de LLM Local:** Ollama (Modelo: `llama3:8b`)

---

## 🔧 Guía de Instalación y Configuración

### 1. Requisitos Previos
- **Python:** Tener instalado Python (3.10 o superior recomendado).
- **Controladores de Audio:** Dispositivo de audio virtual (ej. VB-Audio Virtual Cable) para redirigir el audio del sistema o del reproductor de video hacia el script.
- **Ollama:** Instalar Ollama en el sistema y descargar el modelo base:
  ```powershell
  ollama pull llama3
2. Configuración del Entorno Virtual e Instalación
Clona el repositorio, crea tu entorno virtual e instala las dependencias necesarias:

PowerShell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\activate

# Instalar librerías requeridas (Omitiendo verificaciones SSL si es necesario)
.\venv\Scripts\pip.exe install sounddevice numpy openai-whisper ollama --trusted-host pypi.org --trusted-host files.pythonhosted.org
3. Calibración del Umbral de Audio
Antes de iniciar, se debe identificar el índice del dispositivo de entrada de audio virtual (ej. Dispositivo 30) y ajustar las variables en el script según los niveles de ruido del hardware:

Silencio absoluto: 0.0000

Umbral de activación (UMBRAL): 0.010

💻 Arquitectura del Código (main.py)
El script se compone de tres bloques fundamentales:

Captura del flujo de entrada: Un hilo continuo (sd.InputStream) lee el flujo de audio en formato estéreo a 48000Hz y calcula el volumen cuadrático medio (RMS) en tiempo real.

Procesamiento de voz: Al detectarse una pausa (100 frames por debajo del umbral), los datos acumulados se normalizan y submuuestrean a 16000Hz para ser procesados por la GPU mediante whisper.load_model("small", device="cuda").

Generación de respuestas: El texto transcrito se inyecta directamente al SDK oficial de Ollama utilizando una estructura de prompt plano para evitar la fuga de tokens de razonamiento o textos de configuración:

Python
response = ollama.chat(
    model="llama3",
    messages=[{"role": "user", "content": prompt_unico}],
    stream=True
)
📊 Demostración de Funcionamiento (Logs reales)
Plaintext
🎯 Analizando lo que dijo...
📝 ENTRADA: 'Processes are structured workloads designed to ensure consistency and efficiency.'
🤖 COPILOT SUGIERE: 
Paso 1: El entrevistador mencionó la importancia de los procesos estructurados en el trabajo para garantizar consistencia y eficiencia.

Paso 2: Yo entiendo que los procesos estructurados son fundamentales para un equipo de soporte IT avanzado como el nuestro, ya que nos permiten establecer patrones de trabajo consistentes y automatizar tareas repetitivas. Esto nos permite enfocarnos en solucionar problemas más complejos y mejorar la eficiencia en general.
============================================================
