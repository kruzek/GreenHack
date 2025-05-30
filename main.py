import streamlit as st
import openai


API_URL = "https://api.featherless.ai/v1"
API_KEY = "rc_9ec513e6f29404913286239a973df723dcac4328faf23964a3d28e6369dfa995"
MODEL = "meta-llama/Meta-Llama-3-70B-Instruct"
SYSTEM_PROMPT = "You are a helpful assistant. First, provide a thorough analysis of the user's input. Then, continue the conversation based on your analysis."

client = openai.OpenAI(
    base_url=API_URL,
    api_key=API_KEY,
)

def call_llm(messages):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    return response.model_dump()['choices'][0]['message']['content']

st.set_page_config(page_title="LLM Chat Interface", layout="centered")
st.title("LLM Chat Interface")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

chat_history = st.container()

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area("Your message:", key="user_input", height=80)
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    with st.spinner("Assistant is typing..."):
        assistant_reply = call_llm(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    st.session_state.analysis_done = True

with chat_history:
    for msg in st.session_state.messages:
        if msg["role"] == "system":
            continue
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**Assistant:** {msg['content']}")
