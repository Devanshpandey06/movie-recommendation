import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import pyttsx3
import os
import tempfile

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="TTS & STT App",
    page_icon="🎤",
    layout="centered"
)

# ----------------- Sidebar -----------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Text to Speech", "Speech to Text", "About"])

# ----------------- Home -----------------
if page == "Home":
     st.title("🎤 Text to Speech & Speech to Text Application")
     st.markdown("""
    ### Welcome!
    This application allows users to:
    - Convert **Text into Speech**
    - Convert **Speech into Text**
    
    The system is developed using **Python** and **Streamlit** as part of a college project.
    """)
     st.image(
        "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
        width=250
    )
     st.success("Use the sidebar to navigate through the application.")
     
     st.markdown("""
    ---
    ### Features
    - Simple and user-friendly interface  
    - Fast text-to-speech conversion  
    - Accurate speech-to-text recognition  
    - Works on basic hardware  
    """)

# ==================================================
# ================= TEXT TO SPEECH =================
# ==================================================
elif page == "Text to Speech":
    st.title("🔊 Text to Speech")

    text = st.text_area("Enter text to convert into speech")

    tts_option = st.radio(
        "Select TTS Mode",
        ("Online (gTTS)", "Offline (pyttsx3)")
    )

    if st.button("Convert to Speech"):
        if text.strip() == "":
            st.warning("Please enter some text.")
        else:
            if tts_option == "Online (gTTS)":
                tts = gTTS(text)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    st.audio(fp.name)
                    st.success("Speech generated successfully!")

            else:
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
                st.success("Speech played successfully (offline mode).")

# ==================================================
# ================= SPEECH TO TEXT =================
# ==================================================
elif page == "Speech to Text":
    st.title("🎙️ Speech to Text")

    recognizer = sr.Recognizer()

    st.subheader("Upload Audio File (.wav)")

    audio_file = st.file_uploader("Upload WAV file", type=["wav"])

    if audio_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
            fp.write(audio_file.read())
            audio_path = fp.name

        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
            st.success("Speech converted successfully!")
            st.text_area("Converted Text", text, height=150)
        except sr.UnknownValueError:
            st.error("Could not understand the audio.")
        except sr.RequestError:
            st.error("Speech recognition service error.")

    st.markdown("---")
    st.subheader("Live Speech Input")

    if st.button("Start Recording"):
        with sr.Microphone() as source:
            st.info("Listening... Speak now")
            audio_data = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio_data)
            st.success("Speech converted successfully!")
            st.text_area("Converted Text", text, height=150)
        except sr.UnknownValueError:
            st.error("Could not understand your speech.")
        except sr.RequestError:
            st.error("Service unavailable.")

# ----------------- About -----------------
elif page == "About":
    st.title("ℹ️ About This Project")

    st.markdown("""
    ### Project Title
    **Text to Speech and Speech to Text Application**

    ### Description
    This project is developed as part of an academic curriculum to demonstrate the
    practical implementation of **speech processing technologies** using Python.

    The application integrates:
    - Text-to-Speech (TTS)
    - Speech-to-Text (STT)

    using open-source Python libraries and a web-based interface built with Streamlit.
    """)

    st.markdown("""
    ---
    ### Technologies Used
    - **Python**
    - **Streamlit**
    - **gTTS / pyttsx3**
    - **SpeechRecognition**
    """)

    st.markdown("""
    ---
    ### Objective
    To provide a simple, efficient, and accessible voice-based application that can
    assist users in converting text and speech easily.
    """)

    st.info("This project is developed for educational purposes.")

    
