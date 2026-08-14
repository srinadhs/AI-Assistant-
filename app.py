import streamlit as st
import os
import asyncio
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

# Handle Streamlit asyncio event loop compatibility
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

load_dotenv()

# Import backend engine
from core.engine import ChatEngine

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize Session States
if "engine" not in st.session_state:
    st.session_state.engine = ChatEngine()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar Controls
with st.sidebar:
    st.header("Files")
    st.caption("Attach text or PDF documents to discuss them.")
    
    uploaded_files = st.file_uploader(
        "Attach documents (Optional)",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.info(f"📎 {len(uploaded_files)} file(s) attached to current context.")

    st.markdown("---")
    if st.button("Clear Conversation", type="secondary", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

st.title("🤖Storm AI")
st.caption("Conversational AI powered by Gemini.")

# Render previous chat history
for message in st.session_state.chat_history:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# Chat Input Handler
if user_prompt := st.chat_input("Type your message here..."):
    # Display user query
    st.chat_message("user").markdown(user_prompt)
    
    # Process attached documents on the fly if provided
    file_context = ""
    if uploaded_files:
        with st.spinner("Reading attached documents..."):
            file_context = st.session_state.engine.extract_file_content(uploaded_files)
            
            # Visual Debugging Alerts
            if not file_context.strip():
                st.warning("⚠️ No text could be found in the PDF. It might be a scanned image.")
            else:
                st.toast("✅ PDF text extracted successfully!")

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response_text = st.session_state.engine.generate_response(
                    user_query=user_prompt,
                    chat_history=st.session_state.chat_history,
                    file_context=file_context
                )
                st.markdown(response_text)
                
                # Update persistent session history
                st.session_state.chat_history.append(HumanMessage(content=user_prompt))
                st.session_state.chat_history.append(AIMessage(content=response_text))
            except Exception as e:
                st.error(f"Error communicating with Gemini: {e}")