import streamlit as st
from transformers import pipeline
from gtts import gTTS
import speech_recognition as sr
import pyaudio

# Create a translation pipeline
pipe = pipeline('translation', model='Helsinki-NLP/opus-mt-en-hi')

# Initialize the SpeechRecognition recognizer
recognizer = sr.Recognizer()

# Find the microphone device index
def find_microphone_index():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if "microphone" in device_info["name"].lower():
            return i
    return None

# Get the microphone device index
microphone_index = find_microphone_index()

audio_input = st.empty()

# Check if the microphone input is requested
if st.checkbox("Use Microphone for English Input"):
    with audio_input:
        if microphone_index is None:
            st.warning("No microphone found. Please make sure your microphone is connected.")
        else:
            st.warning("Listening for audio input... Speak in English.")
            try:
                with sr.Microphone(device_index=microphone_index) as source:
                    audio = recognizer.listen(source)
                st.success("Audio input recorded. Translating...")

                # Recognize the English speech
                english_text = recognizer.recognize_google(audio, language='en')

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
