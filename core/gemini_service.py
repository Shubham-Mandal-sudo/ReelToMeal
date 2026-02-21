# core/gemini_service.py
import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List
from django.conf import settings

class Ingredient(BaseModel):
    name: str
    quantity_si: str = Field(description="Quantity strictly in SI units (e.g., grams, ml)")

class RecipeSchema(BaseModel):
    recipe_name: str
    ingredients: List[Ingredient]
    instruments: List[str] = Field(description="Cooking instruments visually used or mentioned")
    instructions: List[str]
    serving_size: str

def extract_recipe_from_video(youtube_url):
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    prompt = "Watch this cooking video. Extract the recipe, convert all measurements to SI units, and list the cooking instruments used."
    
    # FIX 1: Explicitly define the YouTube URL as a video part
    video_part = types.Part.from_uri(
        file_uri=youtube_url,
        mime_type="video/mp4" # This tells Gemini to treat the YouTube link as a video file
    )
    
    # FIX 2: Fallback to gemini-2.5-flash to ensure model availability
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=[
            prompt, 
            video_part # Pass the specially formatted video part here
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RecipeSchema,
            temperature=0.2 
        )
    )
    
    return json.loads(response.text)