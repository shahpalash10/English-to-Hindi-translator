import streamlit as st
from transformers import pipeline
from gtts import gTTS
import speech_recognition as sr
import pyaudio

# Create a translation pipeline
pipe = pipeline('translation', model='Helsinki-NLP/opus-mt-en-hi')

# Initialize the SpeechRecognition recognizer
recognizer = sr.Recognizer()

# Create a Streamlit input element for microphone input
audio_input = st.empty()

# Initialize PyAudio and stream variables
p = pyaudio.PyAudio()
stream = None

# Check if the microphone input is requested
if st.checkbox("Use Microphone for English Input"):
    with audio_input:
        st.warning("Listening for audio input... Speak in English.")
        try:
            with sr.Microphone() as source:
                # Open the audio stream
                stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

                audio = b""
                for _ in range(0, int(16000 / 1024 * 5)):  # Adjust the recording duration as needed
                    audio += stream.read(1024)

                # Recognize the English speech
                english_text = recognizer.recognize_google(audio, language='en')

            st.success("Audio input recorded. Translating...")

            # Translate the English text to Hindi
            out = pipe(english_text, src_lang='en', tgt_lang='hi')

            # Extract the translation
            translation_text = out[0]['translation_text']
            st.text(f"English Input: {english_text}")
            st.text(f"Hindi Translation: {translation_text}")

            # Convert the translated text to speech
            tts = gTTS(translation_text, lang='hi')
            tts.save("translated_audio.mp3")

            # Display the audio player for listening to the speech
            st.audio("translated_audio.mp3", format='audio/mp3')

        except sr.WaitTimeoutError:
            st.warning("No speech detected. Please speak into the microphone.")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service: {e}")
        except sr.UnknownValueError:
            st.warning("Speech recognition could not understand the audio.")
        finally:
            # Clean up audio resources
            if stream:
                stream.stop_stream()
                stream.close()
            p.terminate()
