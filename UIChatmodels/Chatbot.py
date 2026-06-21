# app.py

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="GeoChatBot",
    page_icon="🌍",
    layout="centered",
)

# -------------------- DARK THEME --------------------
st.markdown(
    """
    <style>
    .stApp{
        background-color:#0e1117;
        color:white;
    }

    .stChatMessage{
        border-radius:12px;
        padding:10px;
    }

    button[kind="secondary"]{
        width:100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- LLM --------------------
@st.cache_resource
def load_llm():
    return ChatMistralAI(
        model="mistral-medium-3-5",
        temperature=0.9
    )

llm = load_llm()

# -------------------- SESSION STATE --------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(
            content=(
                "Act as a Geopolitical Teacher and you will be teaching "
                "each and every information asked very concisely."
            )
        )
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------- HEADER --------------------
st.title("GeoChatBot ->")

col1, col2 = st.columns([5, 1])

with col2:
    if st.button("Reset"):
        st.session_state.messages = [
            SystemMessage(
                content=(
                    "Act as a Geopolitical Teacher and you will be teaching "
                    "each and every information asked very concisely."
                )
            )
        ]
        st.session_state.chat_history = []
        st.rerun()

# -------------------- DISPLAY CHATS --------------------
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------- INPUT --------------------
prompt = st.chat_input("Ask anything about geopolitics...")

if prompt:

    # show user
    st.session_state.chat_history.append(
        {"role": "user", "content": prompt}
    )

    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm.invoke(st.session_state.messages)

            answer = response.content

            st.markdown(answer)

    st.session_state.messages.append(
        AIMessage(content=answer)
    )

    st.session_state.chat_history.append(
        {"role": "assistant", "content": answer}
    )