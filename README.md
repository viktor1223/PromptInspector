# PromptInspector

PromptInspector is an advanced tool designed to streamline testing and refining AI-generated conversations and prompts. By enabling users to interact with OpenAI’s GPT models, evaluate their outputs, and leverage a unique **Reflection Mechanism**, it empowers researchers, developers, and educators to enhance the quality and performance of AI responses. PromptInspector also provides insights into cost-performance trade-offs by comparing older models with newer ones using the Reflection Mechanism.

---

## Features

- **Prompt Testing**: Compare custom prompts across multiple OpenAI GPT models.
- **Interactive Chatbot**: Engage in real-time conversations to test prompt and response quality.
- **Reflection Mechanism**: Enhance AI outputs by allowing the model to refine its own responses.
- **Model Comparison**: Evaluate cost-effectiveness by testing if older models with reflection can match the performance of newer, more expensive models.
- **Customizable Settings**: Fine-tune model selection, reflection capabilities, and prompt behavior.

---

## Getting Started

### 1. Create an OpenAI API Key
To use PromptInspector, you need an OpenAI API key. Follow these steps to create one:

1. Sign in to your [OpenAI account](https://platform.openai.com/signup/).
2. Navigate to the **API Keys** section in the [OpenAI dashboard](https://platform.openai.com/account/api-keys).
3. Click **Create New Secret Key** and copy the generated key.  
   *Keep this key secure as it provides access to your OpenAI account.*

### 2. Access PromptInspector
Visit the live demo of PromptInspector:  
👉 [promptinspector.streamlit.app](https://promptinspector.streamlit.app)

### 3. Using PromptInspector
- Enter your OpenAI API key in the sidebar input field to unlock the tool.
- Choose between:
  - **Prompt Testing**: Test a prompt on one or more models and optionally enable reflection for enhanced results.
  - **Interactive Chatbot**: Interact with a model in real-time for conversational testing.

---

## Why We Added the Reflection Mechanism

The Reflection Mechanism is a unique feature that allows a model to evaluate its own responses and refine them. This serves several purposes:

### 1. **Comparing Older and Newer Models**
- **Problem**: Newer models like GPT-4 are powerful but come at a higher cost. Older models like GPT-3.5 or GPT-4-turbo may still perform well for specific tasks, especially with some refinement.
- **Solution**: Reflection enables users to see if older models can achieve comparable performance to newer models by refining their outputs. This helps make **cost-effective decisions** when choosing a model.

### 2. **Optimizing Cost-Performance Trade-offs**
- Reflected responses from older models might provide results that are "good enough" compared to newer models, making them a viable alternative in scenarios where cost is a significant factor.

### 3. **Improving Output Quality**
- Reflection prompts the model to reconsider its initial response and refine it. This ensures the most coherent, accurate, and well-thought-out results, regardless of the model used.

### 4. **Enhancing Model Versatility**
- Reflection allows models to adapt better to complex tasks, making them more reliable for applications like customer support, creative writing, and educational tools.

---

## What Can It Be Used For?

### 1. Chatbot Development
- Test prompts for customer service bots to ensure natural, empathetic, and accurate responses.

### 2. AI Research
- Compare different models and assess how reflection improves their outputs.

### 3. Cost Optimization
- Evaluate if older models with reflection can replace newer, more expensive models without sacrificing quality.

### 4. Education
- Use reflection to explain model reasoning or to refine outputs for educational content.

---

## Example Use Cases

### 1. **Cost-Efficient Chatbot Development**
- Use GPT-4 for initial testing and compare its performance to GPT-3.5-turbo with reflection enabled. 
- Determine whether the cheaper GPT-3.5-turbo provides satisfactory results after refinement.

### 2. **Creative Writing with Enhanced Coherence**
- Feed a story prompt to the models, then refine the responses using the Reflection Mechanism to ensure logical consistency and depth.

### 3. **Model Decision-Making**
- Test complex tasks like multi-turn conversations or creative content generation on both older and newer models.
- Use results to decide which model offers the best balance of quality and cost for the application.

---

## Architecture Decisions

PromptInspector was designed with the following principles in mind:

### 1. **Scalability**
- **Streamlit Framework**: Provides a lightweight, interactive, and scalable front-end for rapid prototyping.
- **Modular Design**: Divides functionality into components (`main.py`, `openai_client.py`, `ui.py`) to ensure flexibility and maintainability.

### 2. **Cost-Performance Trade-Off Analysis**
- **Reflection Mechanism**: Enables older models to refine their responses, allowing users to compare their performance with newer models.

### 3. **Seamless User Experience**
- **Custom CSS Styling**: Enhances readability and creates an intuitive chat interface.
- **Session State Management**: Retains user inputs and chat history for a smooth conversational experience.

**Component Overview**:
- **API Integration**: `openai_client.py` handles communication with the OpenAI API.
- **UI Design**: `ui.py` defines both the Prompt Testing and Interactive Chatbot interfaces.
- **Main Controller**: `main.py` orchestrates user navigation and ties the UI to the backend.

---

## Live Demo

Ready to try PromptInspector?  
👉 [promptinspector.streamlit.app](https://promptinspector.streamlit.app)

---

PromptInspector bridges the gap between cost and performance, giving you the tools to make informed decisions about AI model selection while enhancing the quality of AI-generated content. Whether you’re a developer, researcher, or educator, PromptInspector helps you harness the full potential of OpenAI’s GPT models efficiently and effectively.