import os
import io
import base64
import time
import streamlit as st
from dotenv import load_dotenv
import sounddevice as sd
import openai
import sarvamai
import soundfile as sf

from utils import (
    sample_rate, channels, block_size, recording_queue,
    flush_queue, audio_callback, get_audio_data,
    play_audio_with_barge_in_memory
)


load_dotenv(override= True)
sarvam_api_key = os.getenv("SARVAMAI_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

client = sarvamai.SarvamAI(api_subscription_key= sarvam_api_key)
openai.api_key = openai_api_key

st.set_page_config(page_title= "Voxen", page_icon= "🎙️")
st.title("🎙️ Voxen - Real-time Voice Assistant")

if "running" not in st.session_state:
    st.session_state.running = False

start_button = st.button("Start Voxen" if not st.session_state.running else "Stop Voxen")

if start_button:
    st.session_state.running = not st.session_state.running

status_placeholder = st.empty()
user_placeholder = st.empty()
assistant_placeholder = st.empty()

if st.session_state.running:
    status_placeholder.info("Voxen is running. Speak into your mic.")

    try:
        with sd.InputStream(samplerate= sample_rate, channels= channels, dtype= 'float32',
                            blocksize= block_size, callback= audio_callback):

            while st.session_state.running:
                flush_queue(recording_queue)
                status_placeholder.info("Listening for your speech...")

                audio_buffer = get_audio_data()

                if not audio_buffer:
                    status_placeholder.warning("No speech detected.")
                    continue

                status_placeholder.info("Transcribing...")
                user_text = client.speech_to_text.transcribe(
                    file=("input.wav", audio_buffer, "audio/wav"),
                    model="saarika:v2.5",
                    language_code="en-IN"
                ).transcript

                if not user_text.strip():
                    status_placeholder.warning("Transcription empty. Try speaking again.")
                    continue

                user_placeholder.success(f"🧑‍💼 You: {user_text}")

                response_text = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": user_text}
                    ]
                ).choices[0].message.content

                assistant_placeholder.success(f"🤖 Voxen: {response_text}")

                tts_response = client.text_to_speech.convert(
                    text= response_text,
                    model= "bulbul:v2",
                    target_language_code= "en-IN",
                    speaker= "hitesh"
                )

                audio_data = base64.b64decode(tts_response.audios[0])
                audio_np, fs = sf.read(io.BytesIO(audio_data), dtype= 'float32')

                play_audio_with_barge_in_memory(audio_np, fs)
                time.sleep(0.3)

    except KeyboardInterrupt:
        status_placeholder.warning("Stopped manually.")

    except Exception as e:
        st.error(f"Error: {e}")

else:
    status_placeholder.warning("Voxen is stopped.")
