import os
from dotenv import load_dotenv
from google import genai
from PIL import Image, ImageDraw, ImageFont
import textwrap
import logging
from fastapi.responses import FileResponse
from fastapi import HTTPException

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
    
    print("Full response object:", response)
    print("Response text:", response.text)
    if response.text:
        captioned_image_path = create_captioned_image(image_path, response.text.split('Meme:')[-1])
        return response.text, FileResponse(
            captioned_image_path,
            media_type="image/jpeg",
            filename=os.path.basename(captioned_image_path)
        )
    else:
        logging.warning(f"Empty translation.")
        return "Failed to extract the text from your meme", None


def create_captioned_image(original_image_path, caption_text):
    try:
        # Open the original image
        original_img = Image.open(original_image_path)
        width = original_img.width
        
        # Create a white image for the caption
        caption_height = max(int(original_img.height * 0.1), len(caption_text) // 50 * 60)
        caption_img = Image.new('RGB', (width, caption_height), 'white')
        
        # Add text to the white image
        draw = ImageDraw.Draw(caption_img)
        
        # Larger font size
        font = ImageFont.load_default()
        font_size = 100
        
        # Wrap text using image width
        margin = 20
        chars_per_line = width // 10
        wrapper = textwrap.TextWrapper(width=chars_per_line)
        wrapped_text = wrapper.fill(caption_text)
        
        # Draw the text with larger size
        draw.text(
            (margin, margin),
            wrapped_text,
            font=font,
            fill='black',
            spacing=10
        )
        
        # Concatenate the images vertically
        final_height = original_img.height + caption_img.height
        final_image = Image.new('RGB', (width, final_height), 'white')
        
        final_image.paste(original_img, (0, 0))
        final_image.paste(caption_img, (0, original_img.height))
        
        # Create output path in the same directory as input
        output_path = os.path.splitext(original_image_path)[0] + '_captioned.jpg'
        
        # Save with error handling
        final_image.save(output_path, 'JPEG')
        return output_path
        
    except Exception as e:
        logging.error(f"Error in create_captioned_image: {str(e)}")
        raise Exception(f"Failed to create captioned image: {str(e)}")
