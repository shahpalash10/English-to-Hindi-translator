import streamlit as st
from transformers import pipeline
from gtts import gTTS  # Google Text-to-Speech library
import IPython.display as ipd  # For playing audio in the notebook

# Create a translation pipeline
pipe = pipeline('translation', model='Helsinki-NLP/opus-mt-en-hi')

text = st.text_area("Enter some English text")
if text:
    out = pipe(text, src_lang='en', tgt_lang='hi')
    st.json(out)
    
    # Extract the translated text from the JSON output
    translation_text = out[0]['translation_text']
    
    # Convert the translated text to speech
    tts = gTTS(translation_text, lang='hi')  # You can specify the desired language ('hi' for Hindi)
    
    # Save the generated speech as an audio file (e.g., "translated_audio.mp3")
    audio_path = "translated_audio.mp3"
    tts.save(audio_path)
    
    # Display the audio player for listening to the speech
    st.audio(audio_path, format='audio/mp3')
