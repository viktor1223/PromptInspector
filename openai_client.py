from openai import OpenAI
import time

class OpenAIClient:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def generate_response(self, model, messages):
        """Generate response from OpenAI."""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_reflection(self, model, content):
        """Generate a reflection response."""
        try:
            start_time = time.time()
            reflection_prompt = f"{content}\nReflect on this response and improve it."
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": reflection_prompt}
                ]
            )
            elapsed_time = time.time() - start_time
            return response.choices[0].message.content, elapsed_time
        except Exception as e:
            return f"Error: {str(e)}", None
