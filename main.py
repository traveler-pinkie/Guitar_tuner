import numpy as np
import sys
from audio_engine import start_stream, stop_stream, AUDIO_QUEUE, callback_count

print("Starting audio stream...", flush=True)
stream = start_stream()
print("Audio stream started. Make noise near the microphone...", flush=True)

try:
    count = 0
    while True:
        if not AUDIO_QUEUE.empty():
            data = AUDIO_QUEUE.get()
            rms = np.sqrt(np.mean(data**2))
            count += 1
            print(f"[{count}] RMS Level: {rms:.6f}", flush=True)
except KeyboardInterrupt:
    print(f"\nStopping audio stream...", flush=True)

finally:
    stop_stream(stream)
    print("Audio stream stopped.", flush=True)