import streamlit as st
from transformers import pipeline
from gtts import gTTS  # Google Text-to-Speech library

# Create a translation pipeline
pipe = pipeline('translation', model='Helsinki-NLP/opus-mt-en-hi')

text = st.text_area("Enter some English text")
if text:
    out = pipe(text, src_lang='en', tgt_lang='hi')
    st.json(out)
    
    # Convert the translated text to speech
    translation_text = out[0]['translation_text']
    tts = gTTS(translation_text, lang='hi')  # You can specify the desired language ('hi' for Hindi)
    
    # Save the generated speech as an audio file
    tts.save("translated_audio.mp3")

    # Display the audio player
    st.audio("translated_audio.mp3")
