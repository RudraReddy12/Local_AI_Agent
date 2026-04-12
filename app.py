import streamlit as st
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from transformers import pipeline
import sounddevice as sd
import scipy.io.wavfile as wav

# ----------------------------
# Setup
# ----------------------------
load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = groq_key

llm = ChatGroq(model="qwen/qwen3-32b")

pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small"
)

# ----------------------------
# Functions
# ----------------------------

def detect_intent(text):
    prompt = f"""
    Classify the user intent into one word:
    create_file, write_code, summarize, chat.

    Text: {text}
    """
    
    response = llm.invoke(prompt)
    result = response.content.lower()

    if "write" in result or "code" in result:
        return "write_code"
    elif "create" in result:
        return "create_file"
    elif "summarize" in result:
        return "summarize"
    else:
        return "chat"


def create_file(filename):
    os.makedirs("output", exist_ok=True)
    path = os.path.join("output", filename)

    with open(path, "w") as f:
        f.write("")

    return f"File created: {path}"


def generate_code(prompt):
    response = llm.invoke(
        f"Write clean Python code for: {prompt}. Only code no further content or explanation needed."
    )
    code = response.content
    code = code.replace("```python", "").replace("```", "")
    return code.strip()


def write_code(filename, code):
    os.makedirs("output", exist_ok=True)
    path = os.path.join("output", filename)
    if not isinstance(code, str):
        code = str(code)

    with open(path, "w",encoding="utf-8", errors="ignore") as f:
        f.write(code)

    return f"Code written to {path}"


def summarize_text(text):
    response = llm.invoke(f"Summarize this:\n{text}")
    return response.content


def chat_response(text):
    response = llm.invoke(text)
    return response.content


def process_command(text):
    intent = detect_intent(text)

    if intent == "create_file":
        return intent, create_file("new_file.txt")

    elif intent == "write_code":
        code = generate_code(text)
        return intent, write_code("generated_code.py", code)

    elif intent == "summarize":
        return intent, summarize_text(text)

    else:
        return intent, chat_response(text)


# ----------------------------
# Mic Recording Function
# ----------------------------
def record_audio(filename="mic_input.wav", duration=5, fs=16000):
    st.write("🎤 Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wav.write(filename, fs, recording)
    st.success("Recording done!")
    return filename


# ----------------------------
# UI
# ----------------------------

st.title("🎙️ Voice AI Agent")

option = st.radio("Choose Input Method:", ["Upload File", "Record Audio"])

if "audio_path" not in st.session_state:
    st.session_state.audio_path = None


# 📁 File Upload
if option == "Upload File":
    uploaded_file = st.file_uploader("Upload Files" , type=["wav", "mp3"])

    if uploaded_file:
        with open("input.wav", "wb") as f:
            f.write(uploaded_file.read())
        st.session_state.audio_path = "input.wav"

# 🎤 Mic Input
elif option == "Record Audio":
    if st.button("Record Audio"):
        st.session_state.audio_path = record_audio()

# ▶️ Run Pipeline
if st.session_state.audio_path:
    if st.button("Run Agent"):
        result = pipe(st.session_state.audio_path)
        text = result["text"]

        intent, output = process_command(text)

        st.subheader("🧾 Transcription")
        st.write(text)

        st.subheader("🧠 Intent")
        st.write(intent)

        st.subheader("⚙️ Output")
        st.write(output)