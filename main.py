import sounddevice as sd
import numpy as np
import queue
import sys
import whisper
import ollama  # <-- Usamos la librería oficial nativa

# ==========================================
# CONFIGURACIÓN DEL COPILOT (CALIBRADA)
# ==========================================
DEVICE = 30           
UMBRAL = 0.010        
SAMPLE_RATE = 48000   
CHANNELS = 2          
OLLAMA_MODEL = "llama3"   # <-- Cambiamos Qwen por Llama 3

PUESTO_IT = "Soporte IT Avanzado y Administrador de Sistemas (SysAdmin)"

SYSTEM_PROMPT = f"""
Actúas como un Interview Copilot experto para un candidato al puesto de {PUESTO_IT}.
REGLA CRÍTICA: NO pienses en voz alta. NO uses procesos de pensamiento internos ni etiquetas <think>.
Responde SIEMPRE directamente en ESPAÑOL.
Estructura tu salida estrictamente en 2 partes:
1. Resume lo que dijo el entrevistador en una sola línea corta.
2. Da una respuesta técnica y fluida en primera persona ("Yo..."), de máximo 2 párrafos cortos.
"""

print("⚙️ Cargando Whisper en tu RTX 4060 con CUDA...")
try:
    model = whisper.load_model("small", device="cuda") 
except Exception as e:
    print(f"⚠️ Error CUDA, usando CPU: {e}")
    model = whisper.load_model("small", device="cpu")

audio_queue = queue.Queue()
audio_buffer = []
silence_counter = 0
SILENCE_TIMEOUT = 100  

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    audio_queue.put(indata.copy())

def consultar_copilot_ollama(texto_pregunta):
    try:
        # Unificamos todo en un único mensaje de usuario para que Qwen no se confunda con las instrucciones
        prompt_unico = (
            f"Instrucción: Actúa como mi Interview Copilot para un puesto de Soporte IT Avanzado / SysAdmin. "
            f"No pienses en voz alta ni escribas análisis técnicos internos. Responde directamente en español.\n\n"
            f"Paso 1: Resume brevemente en una sola línea lo que dijo el entrevistador.\n"
            f"Paso 2: Dame una sugerencia de respuesta técnica y fluida en primera persona ('Yo...'), máximo 2 párrafos cortos.\n\n"
            f"Lo que dijo el entrevistador: \"{texto_pregunta}\"\n\n"
            f"Respuesta sugerida:"
        )

        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "user", "content": prompt_unico}
            ],
            stream=True,
            options={
                "temperature": 0.1,
                "num_predict": 150
            }
        )
        
        for chunk in response:
            text_chunk = chunk['message']['content']
            if "<think>" in text_chunk or "</think>" in text_chunk:
                continue
            print(text_chunk, end="", flush=True)
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error nativo de Ollama: {e}")

print(f"\n🚀 INTERVIEW COPILOT ACTIVO | Rol: {PUESTO_IT}")
print("🎙️ Escuchando la reunión... Dale play al video de prueba.")
print("-" * 60)

try:
    with sd.InputStream(samplerate=SAMPLE_RATE, device=DEVICE, channels=CHANNELS, callback=callback):
        while True:
            data = audio_queue.get()
            volumen = np.sqrt(np.mean(data**2))
            
            if volumen > UMBRAL:
                audio_mono = np.mean(data, axis=1)
                audio_buffer.extend(audio_mono)
                silence_counter = 0
                print(f"\r🎤 Escuchando voz... (Vol: {volumen:.4f})", end="", flush=True)
            else:
                if len(audio_buffer) > 0:
                    silence_counter += 1
                    print(f"\r🤫 Procesando pausa... ({silence_counter}/{SILENCE_TIMEOUT})", end="", flush=True)
                    
                    if silence_counter >= SILENCE_TIMEOUT:
                        if len(audio_buffer) > SAMPLE_RATE * 1.0: 
                            print("\n\n🎯 Analizando lo que dijo...")
                            
                            audio_np = np.array(audio_buffer, dtype=np.float32)
                            paso = SAMPLE_RATE // 16000
                            audio_16k = audio_np[::paso]
                            
                            result = model.transcribe(audio_16k, fp16=True) 
                            texto = result.get("text", "").strip()
                            
                            if texto and len(texto) > 4: 
                                print(f"📝 ENTRADA: '{texto}'")
                                print("🤖 COPILOT SUGIERE: ", end="", flush=True)
                                consultar_copilot_ollama(texto)
                                print("="*60 + "\n")
                            else:
                                print(" [Ruido descartado]")
                        
                        audio_buffer = []
                        silence_counter = 0

except KeyboardInterrupt:
    print("\n👋 Copilot apagado.")
