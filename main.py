import streamlit as st
from google import genai
from google.genai import types

GEMINI_API_KEY = "AIzaSyDV8b5PSmOy1zp2cieG7_NLD-M788T7euU"

SYSTEM_PROMPT = """
You are environmental specialist to advise during power transmission lines building. 
You will be provided with a database in form of geojson file including names of areas (villages), list of
neighboring areas, and map layers with corresponding value of environmental impact.
First, provide a thorough analysis of the user's input. You can recieve a user document with proposed route of the power line.
This power line will cross several areas, and you need to analyze the environmental impact of this power line on these areas.
You should asses the impact on each area, considering how can a change of proposed route improve or worsen the environmental impact.
If the proposed route  can be shortened (achieved goal with crossing less areas ) you can also suggest shortening, but respect the original route.
Thus, you provide a detailed analysis of the environmental impact of the power line on each area, proposing alternative
routes while telling how these alternatives will affect the environment. If you were able to shorten the path,
in the next section, you can provide a suggested shortened path with the same goal achieved, but with less environmental impact.
The output you provide is well structured, with clear sections for analysis and suggestions, using caps or bold for headings.
Then, continue the conversation based on your analysis.
"""

with open("D:/Desktop/VSE/GreenHack/jihocesky.txt", "r", encoding="utf-8") as f:
    DATABASE = f.read()

client = genai.Client(api_key=GEMINI_API_KEY)

def call_llm(messages):
    # Build prompt from messages (skip system)
    prompt = ""
    for msg in messages:
        if msg["role"] == "system":
            continue
        prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=2048,
            temperature=0.3,
        ),
    )
    return response.text

st.set_page_config(page_title="AI Environmental assistant", layout="centered")
st.title("AI Environmental assistant")

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
    if document_text:
        st.session_state.messages.append({
            "role": "user document",
            "content": f"Document provided by user:\n{document_text}"
        })
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    st.session_state.messages.append({"role": "database", "content": DATABASE})

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
