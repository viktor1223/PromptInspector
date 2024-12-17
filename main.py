import streamlit as st
from openai_client import OpenAIClient
from ui import display_prompt_testing, display_interactive_chatbot
from utils import fetch_openai_models

def main():
    st.title("Chatbot Prompt Review System")

    # Sidebar for API Key
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    if not openai_api_key:
        st.warning("Please provide your OpenAI API key to proceed.")
        return

    # Sidebar: Layout Selection
    layout_mode = st.sidebar.radio("Choose Layout Mode", ["Prompt Testing", "Interactive Chatbot"])
    client = OpenAIClient(api_key=openai_api_key)

    openai_models = fetch_openai_models(openai_api_key)

    if layout_mode == "Prompt Testing":
        display_prompt_testing(client, openai_models)
    elif layout_mode == "Interactive Chatbot":
        display_interactive_chatbot(client, openai_models)

if __name__ == "__main__":
    main()
