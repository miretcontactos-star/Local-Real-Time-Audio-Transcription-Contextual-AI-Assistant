# Local Real-Time Audio Transcription & Contextual AI Assistant 🎙️🤖

Este proyecto es una solución de ingeniería de automatización diseñada para capturar flujos de audio en tiempo real, transcribirlos mediante aceleración por hardware (GPU) y generar análisis contextuales de forma **100% local**. 

Fue desarrollado para resolver desafíos corporativos como la generación de minutas automatizadas en reuniones de infraestructura, asistencia en *troubleshooting* técnico en vivo y análisis de datos de audio sin exponer información confidencial a servicios en la nube de terceros.

## 🚀 Características Principales

*   🔒 **Privacidad Total (Offline/Air-Gapped Ready):** Toda la inferencia de inteligencia artificial (STT y LLM) se ejecuta localmente. No hay dependencias de APIs externas (como OpenAI o Anthropic), garantizando la seguridad de los datos corporativos.
*   ⚡ **Aceleración Nativa por GPU:** Utiliza núcleos CUDA (testeado en NVIDIA RTX 4060) para procesar modelos de Whisper, logrando transcripciones de voz a texto casi instantáneas.
*   🎛️ **Segmentación Inteligente de Audio:** Implementa un algoritmo dinámico basado en el volumen cuadrático medio (RMS) y buffers de memoria para detectar pausas naturales en la conversación y aislar ráfagas de voz con precisión milimétrica.
*   🧠 **Análisis Contextual Automatizado:** Integración directa con el motor de Ollama para estructurar la información técnica utilizando el modelo Llama 3, generando resúmenes, minutas o planes de acción en tiempo real.

## 🛠️ Stack Tecnológico y Entorno

*   **Lenguaje:** Python 3.10+
*   **Procesamiento de Audio Estéreo:** `sounddevice`, `numpy`
*   **Motor STT (Speech-to-Text):** OpenAI Whisper (Modelo: `small` | Backend: `PyTorch` + `CUDA`)
*   **Motor LLM (Local Language Model):** Ollama (Modelo: `llama3:8b` nativo)
*   **Hardware de Desarrollo:** Optimizaciones orientadas a arquitecturas NVIDIA.

---

## 🔧 Guía de Instalación y Despliegue

### 1. Requisitos Previos
*   Tener **Python 3.10+** instalado y configurado en el PATH.
*   Disponer de un dispositivo de enrutamiento de audio (ej. VB-Audio Virtual Cable) para capturar el sonido del sistema operativo o software de conferencias (Teams, Zoom, Meet).
*   Instalar [Ollama](https://ollama.com/) en el sistema host y descargar el modelo Llama 3:
    ```powershell
    ollama pull llama3
    ```

### 2. Configuración del Entorno Virtual
Se recomienda aislar las dependencias utilizando un entorno virtual. Clona este repositorio y ejecuta:

```powershell
# Crear y activar entorno virtual
python -m venv venv
.\venv\Scripts\activate

# Instalar librerías requeridas (Eludiendo proxies corporativos o bloqueos SSL si aplica)
pip install sounddevice numpy openai-whisper ollama --trusted-host pypi.org --trusted-host files.pythonhosted.org
3. Calibración de Umbrales
En el archivo main.py, ajusta las constantes según el hardware de captura y el nivel de ruido de fondo de tu entorno corporativo:

DEVICE: Índice del hardware de audio (ej. 30).

UMBRAL: Sensibilidad de captura (Valor por defecto: 0.010).

💻 Arquitectura del Sistema
El flujo de procesamiento (Pipeline) opera en tres etapas continuas sin bloquear el hilo principal:

Captura y Buffering: Se abre un stream de audio (48kHz, estéreo). El script calcula el volumen RMS y acumula frames únicamente cuando se supera el umbral de ruido de fondo.

Submuestreo y Transcripción (STT): Al detectar 1.5 segundos de silencio (fin de la intervención), el buffer se unifica, se normaliza y se realiza un downsampling a 16kHz para alimentar la red neuronal de Whisper en la GPU.

Inferencia y Formateo (LLM): El texto limpio se inyecta mediante el SDK oficial de Ollama al modelo Llama 3, el cual está instruido mediante un System Prompt estricto para generar una síntesis técnica y un plan de respuesta en español, todo en menos de 3 segundos.

📊 Demostración de Salida (Logs de Consola)
Ejemplo de cómo el sistema captura un debate sobre estandarización de soporte IT y genera un análisis estructurado:

Plaintext
🎤 Escuchando voz... (Vol: 0.0520)
🤫 Procesando pausa... (100/100)

🎯 Analizando flujo de audio...
📝 ENTRADA DETECTADA: 'Processes are structured workloads designed to ensure consistency and efficiency in IT operations.'

🤖 SISTEMA DE ANÁLISIS SUGIERE: 
> Resumen del Contexto: El locutor destacó que los procesos estructurados son vitales para garantizar la consistencia y eficiencia operativa.

> Propuesta de Acción / Análisis Técnico: 
Implementar procesos estructurados es el pilar de un área de Soporte IT avanzado. Al definir flujos de trabajo claros y automatizar tareas repetitivas mediante sistemas de ticketing, mitigamos el riesgo humano y nos enfocamos en el escalamiento de incidentes críticos, mejorando la disponibilidad del servicio y los SLAs.
============================================================
🤝 Contribuciones
Este proyecto fue desarrollado bajo una visión de SysAdmin para optimizar flujos de trabajo locales. Los Pull Requests para optimizar el manejo de memoria en la GPU o incluir soporte para modelos RAG (Retrieval-Augmented Generation) son bienvenidos.
