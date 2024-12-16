import streamlit as st
from openai import OpenAI

def main():
    st.title("Chatbot Prompt Review System")

    # Sidebar for API Key Inputs
    st.sidebar.header("API Key Configuration")

    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

    if not openai_api_key:
        st.warning("Please provide your OpenAI API key to proceed.")
        return

    # Model Selection
    st.sidebar.header("Select OpenAI Models")
    selected_models = []
    models = ["gpt-4", "gpt-4-turbo", "gpt-4o"]  # Add more models if needed
    for model in models:
        if st.sidebar.checkbox(model, value=False):
            selected_models.append(model)

    if not selected_models:
        st.warning("Please select at least one model to proceed.")
        return

    # Reflection Option with Tooltip
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

    # Prompt Input
    prompt = st.text_area("Enter your prompt:", "")

    # Submit Button
    if st.button("Submit"):
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

if __name__ == "__main__":
    main()
