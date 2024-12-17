import requests
import os

def fetch_openai_models(api_key):
    """
    Fetch all available models from OpenAI's API and return a list of model names.

    Args:
        api_key (str): Your OpenAI API key.

    Returns:
        list: A list of model names available for use with the Chatbot API.
    """
    url = "https://api.openai.com/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        models_data = response.json()

        # Extract model names from the response
        model_names = [model['id'] for model in models_data.get('data', [])]
        return model_names

    except requests.exceptions.RequestException as e:
        print(f"Error fetching models: {e}")
        return []

 