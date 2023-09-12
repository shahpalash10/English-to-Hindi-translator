import streamlit as st
from transformers import pipeline
from gtts import gTTS
import speech_recognition as sr


pipe = pipeline('translation', model='Helsinki-NLP/opus-mt-en-hi')


recognizer = sr.Recognizer()


audio_input = st.empty()

if st.checkbox("Use Microphone for English Input"):
    with audio_input:
        st.warning("Listening for audio input... Speak in English.")
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
            st.success("Audio input recorded. Translating...")

          
            english_text = recognizer.recognize_google(audio, language='en')

       
            out = pipe(english_text, src_lang='en', tgt_lang='hi')

            
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
