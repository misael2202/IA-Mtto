import streamlit as st
import openai
from PyPDF2 import PdfReader
import os

# Configuración
st.set_page_config(page_title="Chat con PDF", layout="wide")
st.title("📘 IA Mtto")

# Configurar API Key (desde Secrets)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("No se encontró la API Key. Configúrala en Streamlit Secrets.")
else:
    openai.api_key = api_key

# Subir PDF
uploaded_file = st.file_uploader("Sube tu manual en PDF", type="pdf")

if uploaded_file and api_key:
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    st.success("Texto extraído ✅")

    st.subheader("💬 Que duda o problema tienes?")
    question = st.text_input("Escribe tu pregunta:")

    if question:
        with st.spinner("Consultando IA..."):
            prompt = f"Responde la siguiente pregunta usando el texto del manual:\n\nTexto:\n{text}\n\nPregunta:\n{question}"
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            st.write("**Respuesta:**", response.choices[0].message.content)
