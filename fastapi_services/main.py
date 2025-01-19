from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import os
from ai_service import generate_response
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Ensure temp directory exists
os.makedirs("temp", exist_ok=True)


class PromptRequest(BaseModel):
    prompt: str


@app.post("/translate")
async def translate(
    file: UploadFile = File(...),
    target_language: str = Form(...)
):
    """
    Endpoint to translate text from an uploaded image.
    """
    try:
        logger.info(f"Received file: {file.filename}, size: {file.size} bytes")
        logger.info(f"Target language: {target_language}")

        # Save the uploaded file locally
        file_location = f"temp/{file.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
        
        # Call the generate function
        translation, image_response = generate_response(file_location, target_language)
        logger.info(f"Generated translation in target_language: {translation}")
        os.remove(file_location)
        
        if image_response:
            return image_response
        # Clean up the temp file
        
        return {"translation": translation}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))