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
