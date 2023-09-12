import streamlit as st
from transformers import pipeline
from gtts import gTTS 


pipe = pipeline('translation', model='Helsinki-NLP/opus-mt-en-hi')

text = st.text_area("Enter some English text")
if text:
    out = pipe(text, src_lang='en', tgt_lang='hi')
    st.json(out)
    
    translation_text = out[0]['translation_text']
    tts = gTTS(translation_text, lang='hi')  
    
  
    tts.save("translated_audio.mp3")

   
    st.audio("translated_audio.mp3")
