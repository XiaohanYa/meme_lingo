from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_service import generate_response

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate(prompt_request: PromptRequest):
    """
    Endpoint to generate AI responses using the Gemini API.
    """
    try:
        prompt = prompt_request.prompt
        response = generate_response(prompt)
        return {"response": response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while generating the response.")
