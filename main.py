import streamlit as st
from openai import OpenAI
import time

def main():
    st.title("Chatbot Prompt Review System")

    # Sidebar for API Key Inputs
    st.sidebar.header("API Key Configuration")

    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

    if not openai_api_key:
        st.warning("Please provide your OpenAI API key to proceed.")
        return

    # Sidebar Layout Toggle
    layout_mode = st.sidebar.radio("Choose Layout Mode", ["Prompt Testing", "Interactive Chatbot"])

    if layout_mode == "Prompt Testing":
        # Sidebar: Model Selection for Prompt Testing
        st.sidebar.header("Select OpenAI Models for Testing")
        selected_models = []
        models = ["gpt-4", "gpt-4-turbo", "gpt-4o"]  # Add more models if needed
        for model in models:
            if st.sidebar.checkbox(model, value=False):
                selected_models.append(model)

        if not selected_models:
            st.warning("Please select at least one model to proceed.")
            return

        # Sidebar: Reflection Option with Tooltip for Prompt Testing
        st.sidebar.header("Reflection Settings")
        allow_reflection = st.sidebar.checkbox(
            "Enable Reflection", value=False, help="Reflection allows the model to evaluate and improve its response to your prompt."
        )
        reflection_models = []
        if allow_reflection:
            st.sidebar.markdown("Select models for reflection")
            for model in models:
                if st.sidebar.checkbox(f"Reflect on {model}", value=False):
                    reflection_models.append(model)

        # Step 1: Prompt Testing
        st.subheader("Step 1: Test Prompt")
        prompt = st.text_area("Enter your prompt:", "")

        if st.button("Submit Test"):
            if not prompt.strip():
                st.error("Prompt cannot be empty.")
                return

            responses = {}
            reflection_responses = {}

            # Initialize OpenAI Client
            client = OpenAI(api_key=openai_api_key)

            # Process Normal Responses
            all_models = list(set(selected_models + reflection_models))
            for model in all_models:
                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=[{"role": "system", "content": "You are a helpful assistant."},
                                  {"role": "user", "content": prompt}]
                    )
                    responses[model] = response.choices[0].message.content
                except Exception as e:
                    responses[model] = f"Error: {str(e)}"

            # Perform Reflection if enabled
            if allow_reflection:
                for model in reflection_models:
                    try:
                        reflection_prompt = responses.get(model, "") + "\nReflect on this response and improve it."
                        reflection_response = client.chat.completions.create(
                            model=model,
                            messages=[{"role": "system", "content": "You are a helpful assistant."},
                                      {"role": "user", "content": reflection_prompt}]
                        )
                        reflection_responses[model] = reflection_response.choices[0].message.content
                    except Exception as e:
                        reflection_responses[model] = f"Error: {str(e)}"

            # Display Responses in Interactive Tabs
            st.subheader("Chatbot Responses")
            tabs = st.tabs([f"{model} Normal" for model in selected_models] + \
                           [f"{model} Reflection" for model in reflection_models if allow_reflection])

            for i, model in enumerate(selected_models):
                with tabs[i]:
                    st.markdown(f"### {model} (Normal Response)")
                    st.write(responses.get(model, "No response received."))

            if allow_reflection:
                for j, model in enumerate(reflection_models):
                    with tabs[len(selected_models) + j]:
                        st.markdown(f"### {model} (Reflected Response)")
                        st.write(reflection_responses.get(model, "No reflection response received."))

    elif layout_mode == "Interactive Chatbot":
        # Sidebar: Model and Reflection Selection for Chatbot
        st.sidebar.header("Interactive Chatbot Settings")
        selected_chat_model = st.sidebar.selectbox("Select Model for Chatbot Interaction", ["gpt-4", "gpt-4-turbo", "gpt-4o"])
        use_reflection = st.sidebar.checkbox("Enable Reflection for Chatbot", value=False)

        # Main Page: Interactive Chatbot Layout
        st.subheader("Interactive Chatbot")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display Chat History with Styling
        chat_container = st.container()
        with chat_container:
            st.markdown("""
                <style>
                .chat-container {
                    background-color: #f0f0f5;
                    padding: 10px;
                    border-radius: 10px;
                    max-height: 400px;
                    overflow-y: auto;
                }
                .user-bubble {
                    background-color: #e0f7fa;
                    color: black;
                    padding: 10px;
                    border-radius: 10px;
                    margin-bottom: 10px;
                    text-align: right;
                    max-width: 70%;
                    margin-left: auto;
                }
                .bot-bubble {
                    background-color: #c8e6c9;
                    color: black;
                    padding: 10px;
                    border-radius: 10px;
                    margin-bottom: 10px;
                    text-align: left;
                    max-width: 70%;
                }
                </style>
            """, unsafe_allow_html=True)

            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(f"<div class='user-bubble'>{message['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='bot-bubble'>{message['content']}</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # User Input
        user_message = st.text_input("Your message:", "", key="user_message_input")

        if st.button("Send to Chatbot"):
            if not user_message.strip():
                st.error("Message cannot be empty.")
            else:
                client = OpenAI(api_key=openai_api_key)

                # Send user message to chatbot
                try:
                    response = client.chat.completions.create(
                        model=selected_chat_model,
                        messages=st.session_state.chat_history + [{"role": "user", "content": user_message}]
                    )
                    bot_response = response.choices[0].message.content
                    st.session_state.chat_history.append({"role": "user", "content": user_message})

                    if use_reflection:
                        start_time = time.time()
                        reflection_prompt = bot_response + "\nReflect on this response and improve it."
                        reflection_response = client.chat.completions.create(
                            model=selected_chat_model,
                            messages=[{"role": "system", "content": "You are a helpful assistant."},
                                      {"role": "user", "content": reflection_prompt}]
                        )
                        elapsed_time = time.time() - start_time
                        bot_response = reflection_response.choices[0].message.content
                        bot_response = f"{reflection_response.choices[0].message.content}\n\n**Reflection Response (after {elapsed_time:.2f} seconds)**"
                        print(bot_response)
                        print("REFLECTION!!!!")
                   
                    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

                except Exception as e:
                    st.error(f"Error: {str(e)}")

                # Automatically refresh the UI after updating chat history
                st.rerun()

if __name__ == "__main__":
    main()
