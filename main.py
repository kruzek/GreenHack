import streamlit as st
import openai


API_URL = "https://api.featherless.ai/v1"
API_KEY = "rc_9ec513e6f29404913286239a973df723dcac4328faf23964a3d28e6369dfa995"
MODEL = "meta-llama/Meta-Llama-3-70B-Instruct"
SYSTEM_PROMPT = """
You are a helpful assistant. First, provide a thorough analysis of the user's input. 
Then, continue the conversation based on your analysis.
"""

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

st.set_page_config(page_title="AI Environmental assistant", layout="centered")
st.title("AI Environmental assistant")

# New: Document upload
document_text = ""
with st.expander("Optional: Upload a document to include in the prompt"):
    uploaded_file = st.file_uploader("Choose a text file", type=["txt"])
    if uploaded_file is not None:
        document_text = uploaded_file.read().decode("utf-8")
        st.text_area("Document content", value=document_text, height=150, disabled=True)

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
    # Add document as a message if present
    if document_text:
        st.session_state.messages.append({
            "role": "system",
            "content": f"Document provided by user:\n{document_text}"
        })
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})

    # Print out the prompt sent to the model for development
    with st.expander("Prompt sent to model"):
        for msg in st.session_state.messages:
            st.write(f"**{msg['role']}**: {msg['content']}")

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
