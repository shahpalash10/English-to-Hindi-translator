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

if st.checkbox("Use Microphone for English Input"):
    with audio_input:
        st.warning("Listening for audio input... Speak in English.")
        try:
            # Create a PyAudio object
            pa = pyaudio.PyAudio()

            # Use PyAudio for microphone input
            with pa.open(format=pyaudio.paInt16,
                         channels=1,
                         rate=44100,
                         input=True,
                         frames_per_buffer=1024) as stream:
                audio_data = stream.read(44100)  # Adjust the number of frames as needed

            # Close the PyAudio object
            pa.terminate()

            st.success("Audio input recorded. Translating...")

            # Recognize the English speech
            english_text = recognizer.recognize_google(audio_data, language='en')

            # Translate the English text to Hindi
            out = pipe(english_text, src_lang='en', tgt_lang='hi')

            # Extract the translation
            translation_text = out[0]['translation_text']
            st.text(f"English Input: {english_text}")
            st.text(f"Hindi Translation: {translation_text}")

            tts = gTTS(translation_text, lang='hi')
            tts.save("translated_audio.mp3")

            st.audio("translated_audio.mp3", format='audio/mp3')

        except sr.WaitTimeoutError:
            st.warning("No speech detected. Please speak into the microphone.")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service: {e}")
        except sr.UnknownValueError:
            st.warning("Speech recognition could not understand the audio.")
