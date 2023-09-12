import streamlit as st
from transformers import pipeline
from gtts import gTTS
import speech_recognition as sr

# Create a translation pipeline
pipe = pipeline('translation', model='Helsinki-NLP/opus-mt-en-hi')

# Create a Streamlit input element for text input
text_input = st.text_area("Enter some English text")

# Check if the microphone input is requested
if st.checkbox("Use Microphone for English Input"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.warning("Listening for audio input... Speak in English.")
        audio = recognizer.listen(source)
    st.success("Audio input recorded. Translating...")

    # Recognize the English speech using Google Web Speech API
    try:
        english_text = recognizer.recognize_google(audio, language='en')
        text_input = st.text_area("English Input", english_text)
    except sr.WaitTimeoutError:
        st.warning("No speech detected. Please speak into the microphone.")
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service: {e}")
    except sr.UnknownValueError:
        st.warning("Speech recognition could not understand the audio.")

if text_input:
    # Translate the English text to Hindi
    out = pipe(text_input, src_lang='en', tgt_lang='hi')

    # Extract the translation
    translation_text = out[0]['translation_text']
    st.text(f"English Input: {text_input}")
    st.text(f"Hindi Translation: {translation_text}")

    # Convert the translated text to speech
    tts = gTTS(translation_text, lang='hi')
    tts.save("translated_audio.mp3")

    # Display the audio player for listening to the speech
    st.audio("translated_audio.mp3", format='audio/mp3')
