import sounddevice as sd
for i, d in enumerate(sd.query_devices()):
    if "CABLE" in d["name"] or "Voice" in d["name"]:
        print(f"Índice {i}: {d['name']} | Entradas: {d['max_input_channels']} | Salidas: {d['max_output_channels']}")