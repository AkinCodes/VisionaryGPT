import torch
from PIL import Image
import os
from transformers import CLIPProcessor, CLIPModel
from diffusers import StableDiffusionPipeline

class CLIPEmbedder:
    def __init__(self, model_name="openai/clip-vit-base-patch32"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = CLIPModel.from_pretrained(model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_name)

        # Text-to-image model
        self.sd_pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            safety_checker=None 
        ).to(self.device)

    def generate_image_from_description(self, prompt: str, save_path: str):
        print(f"[generate] Creating image from prompt: '{prompt}'")
        image = self.sd_pipe(prompt).images[0]
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        image.save(save_path)
        return image

    def get_image_embedding(self, image_path: str, description: str = None) -> torch.Tensor:
        if not os.path.exists(image_path):
            if description:
                image = self.generate_image_from_description(description, image_path)
            else:
                print("[get_image_embedding] No file or description provided, creating blank image.")
                image = Image.new("RGB", (224, 224), color="white")
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                image.save(image_path)
        else:
            image = Image.open(image_path).convert("RGB")

        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        outputs = self.model.get_image_features(**inputs)
        return outputs / outputs.norm(p=2, dim=-1, keepdim=True) 

