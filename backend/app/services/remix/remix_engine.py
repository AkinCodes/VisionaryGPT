# Poster remix fusion logic

from PIL import Image
from backend.app.services.embeddings.clip_embedder import CLIPEmbedder
from backend.app.services.generation.stable_diffusion import StableDiffusionGenerator


class PosterRemixEngine:
    def __init__(self):
        self.embedder = CLIPEmbedder()
        self.generator = StableDiffusionGenerator()

    def remix(self, anchor_path: str, add_path: str, subtract_path: str) -> str:
        a = self.embedder.get_image_embedding(anchor_path)
        b = self.embedder.get_image_embedding(add_path)
        c = self.embedder.get_image_embedding(subtract_path)

        fused = a + b - c
        fused = fused / fused.norm(p=2, dim=-1, keepdim=True)  

        # Turn embedding into prompt (optional — or use placeholder)
        prompt = "A new movie that combines the themes of these two posters and removes the third."

        return self.generator.generate(prompt)
