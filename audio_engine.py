import numpy as np
import queue
import sounddevice
import sys
import time

AUDIO_QUEUE = queue.Queue(maxsize=1)
callback_count = 0

def audio_callback(indata, frames, time, status):
    global callback_count
    callback_count += 1
    
    if status:
        print(f"[Callback #{callback_count}] Status: {status}", file=sys.stderr, flush=True)

    try:
        AUDIO_QUEUE.put(indata.copy(), block=False)
    except queue.Full:
        AUDIO_QUEUE.get_nowait()  # Discard the oldest frame
        AUDIO_QUEUE.put(indata.copy(), block=False)


def start_stream():
    print(f"[INFO] Creating InputStream with device=15 (Stereo Mix)", flush=True)
    input_stream = sounddevice.InputStream(device=15, channels=1, samplerate=44100, blocksize=2048, callback=audio_callback, dtype='float32')
    print(f"[INFO] Stream created, calling start()...", flush=True)
    input_stream.start()
    print(f"[INFO] Stream started. Waiting for callbacks...", flush=True)
    # Give the stream a moment to stabilize
    time.sleep(0.5)
    return input_stream

def stop_stream(input_stream):
    try:
        input_stream.stop()
        input_stream.close()
    except Exception as e:
        print(f"Error stopping stream: {e}")
    finally:
        while not AUDIO_QUEUE.empty():
            AUDIO_QUEUE.get()

