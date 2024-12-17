import streamlit as st
import time


def load_css(file_path):
    with open(file_path, "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def display_prompt_testing(client, models):

    # Sidebar for Model Selection
    st.sidebar.header("Select Models for Prompt Testing")
    selected_models = [model for model in models if st.sidebar.checkbox(model)]
    if not selected_models:
        st.warning("Please select at least one model to proceed.")
        return

    # Sidebar for Reflection Settings
    allow_reflection = st.sidebar.checkbox(
        "Enable Reflection",
        help="Allows the model to evaluate and improve its response."
    )
    reflection_models = [
        model for model in selected_models if allow_reflection and st.sidebar.checkbox(f"Reflect on {model}")
    ]

    # Prompt Input
    st.subheader("Test Prompt")
    prompt = st.text_area("Enter your prompt:")

    if st.button("Submit Test"):
        if not prompt.strip():
            st.error("Prompt cannot be empty.")
            return

        responses = {}
        reflection_responses = {}

        # Process Normal Responses
        for model in selected_models:
            response = client.generate_response(
                model,
                [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}]
            )
            responses[model] = response
            if model in reflection_models:
                reflection, elapsed_time = client.generate_reflection(model, response)
                reflection_responses[model] = f"{reflection}\n\n**Reflection Response (after {elapsed_time:.2f} seconds)**"

        # Display Results in Tabs
        st.subheader("Chatbot Responses")
        tabs = st.tabs([f"{model} Normal" for model in selected_models] + 
                       [f"{model} Reflection" for model in reflection_models])

        # Normal Responses
        for i, model in enumerate(selected_models):
            with tabs[i]:
                st.markdown(f"### {model} (Normal Response)")
                st.write(responses.get(model, "No response received."))

        # Reflection Responses
        for j, model in enumerate(reflection_models):
            with tabs[len(selected_models) + j]:
                st.markdown(f"### {model} (Reflected Response)")
                st.write(reflection_responses.get(model, "No reflection response received."))

def display_interactive_chatbot(client, models):
    st.subheader("Interactive Chatbot")

    # Sidebar for Chatbot Settings
    selected_model = st.sidebar.selectbox("Select Model", models)
    use_reflection = st.sidebar.checkbox("Enable Reflection")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Load external CSS
    load_css("styles.css")

    # Render chat history
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"<div class='user-bubble'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-bubble'>{message['content']}</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # User Input at the Bottom
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    user_message = st.text_input("", placeholder="Type your message here...", key="chat_input", label_visibility="collapsed")
    if st.button("Send", key="send_button"):
        if not user_message.strip():
            st.error("Message cannot be empty.")
            return

        response = client.generate_response(
            selected_model,
            st.session_state.chat_history + [{"role": "user", "content": user_message}]
        )
        if use_reflection:
            reflection, elapsed_time = client.generate_reflection(selected_model, response)
            response = f"{reflection}\n\n**Reflection Response (after {elapsed_time:.2f} seconds):**"

        st.session_state.chat_history.append({"role": "user", "content": user_message})
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
