import sounddevice as sd
import numpy as np

DEVICE = 30

sample_rate = int(sd.query_devices(DEVICE, "input")["default_samplerate"])


def callback(indata, frames, time, status):
    volumen = np.sqrt(np.mean(indata**2))

    if volumen > 0.01:
        print(f"Audio detectado: {volumen:.4f}")


print("Escuchando VB-Cable... (Ctrl+C para salir)")

with sd.InputStream(
    device=DEVICE,
    channels=1,
    samplerate=sample_rate,
    callback=callback,
):
    while True:
        sd.sleep(100)