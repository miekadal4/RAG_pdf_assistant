from pdf_processor import *

def main():
    # Page Setup
    st.set_page_config(page_title="PDF Chat Demo", layout="wide")
    st.title("📄 Open source LLM pdf chatbot")
    st.markdown("`Upload a PDF and chat`")

    # Sidebar Settings
    with st.sidebar:
        st.header("⚙️ Settings")
        model_selection = st.selectbox("Available Models", ["arnold", "qwen3:8b", "gemma3:4b"])
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
        mode = st.toggle(label="Enhanced Mode", value = False)
        uploaded_file = st.file_uploader(label="Upload a File to chat!", type=["pdf"])

    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "last_file_hash" not in st.session_state:
        st.session_state.last_file_hash = None
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "last_settings" not in st.session_state:
        st.session_state.last_settings = {
            "model": model_selection,
            "temperature": temperature,
            "mode": mode
        }

    # PDF and settings handler
    if uploaded_file:
        file_hash = get_file_hash(uploaded_file)

        # Detects if new PDF changed
        is_new_pdf = st.session_state.last_file_hash != file_hash
        # Detects if settings changed:
        settings_changed = (
            st.session_state.last_settings["model"] != model_selection or
            st.session_state.last_settings["temperature"] != temperature or
            st.session_state.last_settings["mode"] != mode
        )

        # Conditions to reinitialize the chain:
        if is_new_pdf or settings_changed:
            st.session_state.last_file_hash = file_hash
            st.session_state.last_settings = {
                "model": model_selection,
                "temperature": temperature,
                "mode": mode
            }
            # Build the model
            model = ChatOllama(model=model_selection, temperature=temperature)

            if is_new_pdf:
                st.session_state.chat_history=[]

            uploaded_file.seek(0)
            st.session_state.conversation = initialize_pdf_rag_chain(uploaded_file, mode, model)

    # Chat UI
    with st.container():
        for i, (q, a) in enumerate(st.session_state.chat_history):
            message(q, is_user=True, key=f"user_{i}", avatar_style="micah")
            message(a, key=f"bot_{i}", avatar_style="identicon")

    # Input + Clear button
    st.text_input("Ask something about the PDF:", key="user_input", on_change=on_input_change)
    st.button("Clear Chat", on_click=on_clear)

if __name__ == "__main__":
    main()