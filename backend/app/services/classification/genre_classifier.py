import os
import torch
import torch.nn as nn
import logging
from torchvision import transforms
from PIL import Image
from transformers import ViTForImageClassification

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("GenreClassifier")

class GenreClassifier(nn.Module):
    def __init__(self, num_classes=5, checkpoint=None):
        super(GenreClassifier, self).__init__()

        self.model = ViTForImageClassification.from_pretrained(
            "google/vit-base-patch16-224-in21k",
            num_labels=num_classes
        )

        if checkpoint and os.path.exists(checkpoint):
            log.info(f"✅ Loading trained model from: {checkpoint}")
            state_dict = torch.load(checkpoint, map_location="cpu")
            self.model.load_state_dict(state_dict)
        else:
            log.warning("❌ No checkpoint loaded. The model may not be trained yet.")

        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])

    def forward(self, x):
        return self.model(x)

    def predict(self, image_path: str):
        img = Image.open(image_path).convert("RGB")
        tensor = self.transform(img).unsqueeze(0)

        labels = ["Action", "Comedy", "Drama", "Horror", "Romance"]

        with torch.no_grad():
            logits = self.model(tensor).logits
            probs = torch.nn.functional.softmax(logits, dim=1)[0]

        best_idx = torch.argmax(probs).item()
        confidence = probs[best_idx].item()
        prob_dict = {labels[i]: round(probs[i].item(), 3) for i in range(len(labels))}

        log.info(f"Class probabilities: {prob_dict}")

        return {
            "label": labels[best_idx],
            "confidence": round(confidence, 3),
            "predictions": prob_dict
        }


if __name__ == "__main__":
    checkpoint_path = "backend/app/models/genre_classifier/vit_genre_classifier.pt"

    classifier = GenreClassifier(checkpoint=checkpoint_path)

    sample_path = "spiderman.jpeg" 
    result = classifier.predict(sample_path)

    log.info(f"\n✅ Final Prediction: {result}")    