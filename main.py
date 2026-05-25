import whisper
import tempfile
import soundfile as sf
import streamlit as st
from langchain_helper import get_llm_chain, ask
from streamlit_mic_recorder import mic_recorder


st.title("AFRiQ T-shirts: Database Q&A")

#load whisper model once(important for performance)
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

chain = get_llm_chain()

st.write("Ask a question using voice or text")

# -----------------------------
# 🎤 MICROPHONE INPUT
# -----------------------------

audio = mic_recorder(
    start_prompt="🎤 Click to record",
    stop_prompt="⏹ Stop recording",
    just_once=True
)

question = None

if audio:
    #save audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        #st.write(tmp_file.name, audio['bytes'], audio['sample_rate'])
        tmp_file.write(audio["bytes"])
        tmp_path = tmp_file.name

    with st.spinner("Transcribing speech..."):
        #speech to text
        result = model.transcribe(tmp_file.name)
        question = result['text']

    st.success(f'you said: {question}')


# -----------------------------
# 💬 TEXT FALLBACK INPUT
# -----------------------------
text_input = st.text_input("Type your question here:")

if text_input:
    question = text_input

# -----------------------------
# 🧠 RUN CHAIN
# -----------------------------

if question:
    answer = ask(question, chain)

    st.header("Answer:")
    st.write(answer)