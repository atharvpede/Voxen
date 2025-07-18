import io
import queue
import threading
import time
import numpy as np
import sounddevice as sd
import webrtcvad
import soundfile as sf


sample_rate = 16000
channels = 1
block_duration_ms = 30
block_size = int(sample_rate * block_duration_ms / 1000)

vad = webrtcvad.Vad(3) 
recording_queue = queue.Queue()
barge_in_queue = queue.Queue()
barge_in_event = threading.Event()
is_listening_for_barge_in = False

def flush_queue(q):
    try:
        while True:
            q.get_nowait()
    except queue.Empty:
        pass

def audio_callback(indata, frames, time_info, status):
    global is_listening_for_barge_in
    pcm = (indata[:, 0] * 32768).astype(np.int16)
    pcm_bytes = pcm.tobytes()
    if vad.is_speech(pcm_bytes, sample_rate):
        if is_listening_for_barge_in:
            barge_in_queue.put(pcm_bytes)
        else:
            recording_queue.put(pcm_bytes)
    else:
        if is_listening_for_barge_in:
            barge_in_queue.put(None)
        else:
            recording_queue.put(None)

def monitor_barge_in():
    buffer = []
    while not barge_in_event.is_set():
        try:
            chunk = barge_in_queue.get(timeout= 0.1)
            if chunk:
                buffer.append(chunk)
                if len(buffer) * len(chunk) >= sample_rate * 0.2:
                    barge_in_event.set()
                    break
        except queue.Empty:
            continue

def play_audio_with_barge_in_memory(audio_np, fs):
    global is_listening_for_barge_in
    flush_queue(barge_in_queue)
    is_listening_for_barge_in = True
    barge_in_event.clear()

    def playback():
        sd.play(audio_np, fs)
        sd.wait()

    play_thread = threading.Thread(target= playback)
    play_thread.start()

    monitor_thread = threading.Thread(target= monitor_barge_in, daemon= True)
    monitor_thread.start()

    while play_thread.is_alive():
        if barge_in_event.is_set():
            sd.stop()
            break
        time.sleep(0.05)

    play_thread.join()
    is_listening_for_barge_in = False

def get_audio_data():
    collected_audio = []
    silence_chunks = 0
    speaking = False

    while True:
        try:
            chunk = recording_queue.get(timeout= 5)
        except queue.Empty:
            if speaking:
                break
            else:
                continue

        if chunk:
            collected_audio.append(np.frombuffer(chunk, dtype= np.int16))
            silence_chunks = 0
            speaking = True
        else:
            if speaking:
                silence_chunks += 1
                if silence_chunks > 20:
                    break

    if collected_audio:
        final_audio = np.concatenate(collected_audio)
        audio_buffer = io.BytesIO()
        sf.write(audio_buffer, final_audio, sample_rate, format= "WAV")
        audio_buffer.seek(0)
        return audio_buffer
    return None
