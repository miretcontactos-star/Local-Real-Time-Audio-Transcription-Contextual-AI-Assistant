# Local Real-Time Audio Transcription & Contextual AI Assistant 🎙️🤖

This project is an automation engineering solution designed to capture real-time audio streams, transcribe them using hardware acceleration (GPU), and generate contextual analysis **100% locally**. 

It was developed to solve corporate challenges such as automated minute generation in infrastructure meetings, live technical troubleshooting assistance, and audio data analysis without exposing confidential information to third-party cloud services.

## 🚀 Key Features

* 🔒 **Total Privacy (Offline/Air-Gapped Ready):** All artificial intelligence inference (STT and LLM) runs locally. There are no dependencies on external APIs (such as OpenAI or Anthropic), guaranteeing corporate data security.
* ⚡ **Native GPU Acceleration:** Leverages CUDA cores (tested on NVIDIA RTX 4060) to process Whisper models, achieving near-instantaneous speech-to-text transcriptions.
* 🎛️ **Intelligent Audio Segmentation:** Implements a dynamic algorithm based on Root Mean Square (RMS) volume and memory buffers to detect natural conversational pauses and isolate speech bursts with pinpoint accuracy.
* 🧠 **Automated Contextual Analysis:** Direct integration with the Ollama engine to structure technical information using the Llama 3 model, generating summaries, minutes, or action plans in real time.

## 🛠️ Tech Stack & Environment

* **Language:** Python 3.10+
* **Stereo Audio Processing:** `sounddevice`, `numpy`
* **STT Engine (Speech-to-Text):** OpenAI Whisper (Model: `small` | Backend: `PyTorch` + `CUDA`)
* **LLM Engine (Local Language Model):** Ollama (Model: `llama3:8b` native)
* **Development Hardware:** Optimizations targeted for NVIDIA architectures.

---

## 🔧 Installation & Deployment Guide

### 1. Prerequisites
* **Python 3.10+** installed and configured in your PATH.
* An audio routing device (e.g., VB-Audio Virtual Cable) to capture sound from the operating system or conferencing software (Teams, Zoom, Meet).
* Install [Ollama](https://ollama.com/) on the host system and download the Llama 3 model:
    ```powershell
    ollama pull llama3
    ```

### 2. Virtual Environment Configuration
It is recommended to isolate dependencies using a virtual environment. Clone this repository and run:

```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install required libraries (Bypassing corporate proxies or SSL blocks if applicable)
pip install sounddevice numpy openai-whisper ollama --trusted-host pypi.org --trusted-host files.pythonhosted.org
