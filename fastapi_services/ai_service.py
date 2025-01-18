import os
from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()

def generate_response(prompt: str) -> str:
    """
    Generate a response from the Gemini API for the given prompt.
    """
    # Load API key from environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")

    # Initialize Gemini API client
    client = genai.Client(api_key=api_key)
    
    image = Image.open('/Users/xiaohanyang/Downloads/IMG_9083.jpg')

    # Generate content
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents=[
            image,
            "Write a short and engaging blog post based on this picture."
    ]
        )
    
    print(response.text)
    return response.text
