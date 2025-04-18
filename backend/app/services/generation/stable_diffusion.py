# Stable Diffusion generation logic

from fastapi import UploadFile
from pathlib import Path
import torch
from diffusers import StableDiffusionPipeline
import logging
from io import BytesIO
from PIL import Image

class StableDiffusionGenerator:
    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else (
            "mps" if torch.backends.mps.is_available() else "cpu"
        )
        dtype = torch.float16 if device in ["cuda", "mps"] else torch.float32

        try:
            self.pipe = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5", torch_dtype=dtype
            )
            self.pipe.to(device)
            logging.info(f"Stable Diffusion model loaded to {device}.")
        except Exception as e:
            logging.error(f"Error loading Stable Diffusion model: {e}")
            raise

        self.output_dir = Path("app/static/generated")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, prompt: str, file: UploadFile) -> str:
        try:
            # Optional: Handle the image file (if needed)
            image = Image.open(BytesIO(file.file.read()))
            image.save(self.output_dir / "input_image.png")  # Save the input file (for any reason, like debugging)

            # Generate image from the prompt
            result = self.pipe(prompt, guidance_scale=8.5).images[0]

            # Generate a filename based on the prompt hash
            filename = f"{hash(prompt)}.png"
            save_path = self.output_dir / filename

            # Save the generated image to disk
            result.save(save_path)

            return f"http://localhost:8000/static/generated/{filename}"
        except Exception as e:
            logging.error(f"Error generating image: {e}")
            raise