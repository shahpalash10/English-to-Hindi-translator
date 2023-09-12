import streamlit as st
from transformers import pipeline


pipe = pipeline('translation', model='Helsinki-NLP/opus-mt-en-hi')

text = st.text_area("Enter some English text")
if text:
    out = pipe(text, src_lang='en', tgt_lang='hi')
    st.json(out)
