# Voxen - Real-time Voice Assistant 🎙️

## Description

Voxen is a real-time voice assistant built with Python that makes interacting with technology easier and more intuitive. It uses Sarvam AI’s speech-to-text and text-to-speech features alongside OpenAI’s powerful language understanding to let you talk naturally with an AI assistant.

With Voxen, you can simply speak your requests and get quick, accurate responses without needing to type or click. It’s designed to help you get things done more efficiently while providing a smooth, hands-free experience that feels natural and responsive.

**Watch the short demo video here**: [YouTube Demo](https://youtube.com/shorts/DdS4UqM0gTk?si=e1tervcFaNuPY7wE)

## Key Features

* **Real-time Speech Recognition:** Uses Sarvam AI's `saarika` model to transcribe user speech in real-time.
* **Natural Language Processing:** Employs OpenAI's `gpt-4o` model to understand and respond to user queries.
* **Text-to-Speech:** Utilizes Sarvam AI's `bulbul` model to convert the AI's response into natural-sounding speech.
* **Barge-in Capability:** Allows users to interrupt the AI's speech, providing a more natural conversational flow.
* **WebRTC VAD:** Implements Voice Activity Detection using WebRTC to efficiently process audio input.
* **Streamlit Interface:** Provides a user-friendly web interface for easy interaction.

## Dependencies

The project relies on the following Python libraries:

* `streamlit`
* `openai`
* `sarvamai`
* `sounddevice`
* `numpy`
* `queue`
* `threading`
* `base64`
* `time`
* `dotenv`
* `webrtcvad`
* `soundfile`

##  Project Structure

```text
├── app.py           # Main Streamlit app: handles UI, voice interaction, and GPT responses
├── utils.py         # Utility functions: handles audio capture, VAD (Voice Activity Detection), and playback
├── requirements.txt # Python dependencies
├── .env             # Environment variables (API keys)
└── README.md        # Project documentation
```
## Development Journey

The motivation behind building Voxen was to create a smooth, natural voice assistant experience that allows users to interact hands-free with technology.

The project is developed entirely in Python and combines several powerful technologies:

- **Sarvam AI** for high-quality speech-to-text and text-to-speech processing, enabling seamless voice input and output.
- **OpenAI GPT-4o** for understanding natural language queries and generating intelligent responses.
- **Streamlit** to provide an easy-to-use, interactive web interface.

The architecture is divided mainly into two parts:
- `app.py` manages the UI, handles audio input/output, and orchestrates communication with the AI models.
- `utils.py` contains the supporting functions for audio recording, voice activity detection (using WebRTC VAD), and playback control.

One of the key challenges I faced was implementing the barge-in feature, which allows users to interrupt the assistant’s speech, creating a more natural conversational flow. This involved managing real-time audio streams and ensuring responsive interaction.

Throughout this project, I gained valuable experience in audio processing, asynchronous programming, and integrating multiple AI services to work cohesively.

In the future, I plan to add features such as multi-language support, improved context awareness, and personalized user profiles to enhance the assistant’s usability further.

