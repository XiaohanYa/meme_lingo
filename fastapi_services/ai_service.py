import os
from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()

def generate_response(image_path: str, target_language: str) -> str:
    """
    Generate a response from the Gemini API for the given prompt.
    """
    # Load API key from environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")
    # Initialize Gemini API client
    client = genai.Client(api_key=api_key)
    
    image = Image.open(image_path)
    
    if not target_language:
        target_language = 'English'    
    prompt = f"""You are a translator. Please first identify if there is text in the image. If there is, please output the translation of the following format: 
    Meme: The text in {target_language}. If there is no text, you can say 'This is a free meme' """
    # Generate content
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents=[
            image,
            prompt
    ]
        )
    
    print(response.text)
    return response.text
