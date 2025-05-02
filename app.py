import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator

text = " "

def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)

st.set_page_config(page_title="OCR Traductor 🔍🗣️", page_icon="🧡")

st.markdown(
    """
    <style>
        html, body, .stApp {
            background-color: #FFF3E0 !important;
        }
        h1, h2, h3, h4, p {
            text-align: center;
            color: #E65100;
            font-family: 'Comic Sans MS', cursive, sans-serif;
        }
        .stButton>button {
            background-color: #FB8C00;
            color: #fff;
            border-radius: 12px;
            padding: 10px 20px;
            font-weight: bold;
            margin: auto;
            display: block;
        }
        .stSelectbox, .stTextInput, .stTextArea, .stCheckbox, .stRadio, .stFileUploader {
            margin-left: auto;
            margin-right: auto;
            display: block;
        }
        .stImage, .stAudio {
            display: flex;
            justify-content: center;
        }
        .block-container {
            padding-left: 10%;
            padding-right: 10%;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1>🧡 Traductor de Imágenes con Voz</h1>", unsafe_allow_html=True)
st.markdown("<h3>📸 Extrae texto de imágenes y escúchalo en otro idioma 🌍</h3>", unsafe_allow_html=True)

st.subheader("📷 Elige la fuente de la imagen:")
cam_ = st.checkbox("Usar Cámara")

if cam_:
    img_file_buffer = st.camera_input("Toma una Foto")
else:
    img_file_buffer = None

with st.sidebar:
    st.subheader("🎨 Procesamiento de Imagen")
    filtro = st.radio("¿Aplicar filtro negativo?", ('Sí', 'No'))

bg_image = st.file_uploader("📁 Cargar Imagen desde tu dispositivo:", type=["png", "jpg"])
if bg_image is not None:
    uploaded_file = bg_image
    st.image(uploaded_file, caption='Imagen cargada.', use_column_width=True)

    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.read())

    st.success(f"✅ Imagen guardada como {uploaded_file.name}")
    img_cv = cv2.imread(f'{uploaded_file.name}')
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)

    st.markdown("<h4>📝 Texto detectado:</h4>", unsafe_allow_html=True)
    st.write(text)

if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if filtro == 'Sí':
        cv2_img = cv2.bitwise_not(cv2_img)

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)

    st.markdown("<h4>📝 Texto detectado:</h4>", unsafe_allow_html=True)
    st.write(text)

with st.sidebar:
    st.subheader("🌐 Parámetros de Traducción")
    try:
        os.mkdir("temp")
    except:
        pass

    translator = Translator()

    in_lang = st.selectbox("🗣️ Lenguaje de Entrada",
        ("Ingles", "Español", "Bengali", "koreano", "Mandarin", "Japones"))

    if in_lang == "Ingles":
        input_language = "en"
    elif in_lang == "Español":
        input_language = "es"
    elif in_lang == "Bengali":
        input_language = "bn"
    elif in_lang == "koreano":
        input_language = "ko"
    elif in_lang == "Mandarin":
        input_language = "zh-cn"
    elif in_lang == "Japones":
        input_language = "ja"

    out_lang = st.selectbox("🌍 Lenguaje de Salida",
        ("Ingles", "Español", "Bengali", "koreano", "Mandarin", "Japones"))

    if out_lang == "Ingles":
        output_language = "en"
    elif out_lang == "Español":
        output_language = "es"
    elif out_lang == "Bengali":
        output_language = "bn"
    elif out_lang == "koreano":
        output_language = "ko"
    elif out_lang == "Mandarin":
        output_language = "zh-cn"
    elif out_lang == "Japones":
        output_language = "ja"

    english_accent = st.selectbox("🔈 Acento del Audio",
        ("Default", "India", "United Kingdom", "United States", "Canada", "Australia", "Ireland", "South Africa"))

    if english_accent == "Default":
        tld = "com"
    elif english_accent == "India":
        tld = "co.in"
    elif english_accent == "United Kingdom":
        tld = "co.uk"
    elif english_accent == "United States":
        tld = "com"
    elif english_accent == "Canada":
        tld = "ca"
    elif english_accent == "Australia":
        tld = "com.au"
    elif english_accent == "Ireland":
        tld = "ie"
    elif english_accent == "South Africa":
        tld = "co.za"

    display_output_text = st.checkbox("📋 Mostrar texto traducido")

    if st.button("🎧 Convertir a Audio"):
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown("<h4>🔊 Tu audio:</h4>", unsafe_allow_html=True)
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        if display_output_text:
            st.markdown("<h4>📝 Texto de salida:</h4>", unsafe_allow_html=True)
            st.write(output_text)
