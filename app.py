import streamlit as st
import requests
from PyPDF2 import PdfReader
import os

# Configuración
st.set_page_config(page_title="Chat con PDF (Hugging Face)", layout="wide")
st.title("📘 Chat simple con PDF usando Hugging Face API")

# Token de Hugging Face
hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    st.error("No se encontró el token de Hugging Face. Configúralo en Streamlit Secrets.")

# Subir PDF
uploaded_file = st.file_uploader("Sube tu manual en PDF", type="pdf")

if uploaded_file and hf_token:
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    st.success("Texto extraído ✅")

    st.subheader("💬 Haz tu pregunta")
    question = st.text_input("Escribe tu pregunta:")

    if question:
        with st.spinner("Consultando IA..."):
            prompt = f"Responde la siguiente pregunta usando el texto del manual:\n\nTexto:\n{text}\n\nPregunta:\n{question}"
            headers = {"Authorization": f"Bearer {hf_token}"}
            payload = {
                "inputs": prompt,
                "parameters": {"max_new_tokens": 500, "temperature": 0.2}
            }
            response = requests.post(
                "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
                headers=headers,
                json=payload
            )
            if response.status_code == 200:
                answer = response.json()[0]["generated_text"]
                st.write("**Respuesta:**", answer)
            else:
                st.error(f"Error en la API: {response.status_code}")
