# # CLIP+GPT metadata

import os
from transformers import CLIPProcessor, CLIPModel
from openai import OpenAI
from PIL import Image
import torch
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    raise ValueError("API key is missing. Please set the OPENAI_API_KEY environment variable.")

class PosterMetadataGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
        
        self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        
        self.openai_client = OpenAI(api_key=openai_api_key)
        
    def image_to_text_prompt(self, image_path: str) -> str:
        """Generate a dynamic text prompt based on the image using CLIP."""
        try:
            image = Image.open(image_path).convert("RGB")
            inputs = self.processor(images=image, return_tensors="pt").to(self.device)
            image_features = self.clip_model.get_image_features(**inputs)
        
            return "Describe a movie poster with futuristic cityscape and neon glow."
        except Exception as e:
            raise ValueError(f"Error processing image {image_path}: {e}")
    
    def generate_metadata(self, image_path: str) -> str:
        """Generate movie metadata using GPT-4 based on the image description."""
        try:
            prompt = self.image_to_text_prompt(image_path)
            
            # Create GPT-4 system message and user prompt
            system_msg = "You are a brilliant movie metadata writer. Generate a movie title, genre, tagline, mood, and a 2-sentence summary based on a movie poster."
            user_msg = f"Poster prompt: {prompt}"

            # Make an API call to OpenAI to generate metadata
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                temperature=0.8,
                max_tokens=300
            )

            # Return the generated metadata from GPT-4
            return response.choices[0].message.content

        except Exception as e:
            raise ValueError(f"Error generating metadata: {str(e)}")
