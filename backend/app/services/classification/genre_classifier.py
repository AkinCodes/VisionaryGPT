import os
import torch
from torch import nn
from torchvision import transforms
from PIL import Image
from transformers import ViTForImageClassification

class GenreClassifier(nn.Module):
    def __init__(self, num_classes=5, checkpoint=None):
        super(GenreClassifier, self).__init__()

        # Load the pretrained Vision Transformer (ViT) model
        self.model = ViTForImageClassification.from_pretrained(
            "google/vit-base-patch16-224-in21k", 
            num_labels=num_classes
        )

        # If a checkpoint is provided, load the weights
        if checkpoint:
            self.model.load_state_dict(torch.load(checkpoint, map_location="cpu"))

        self.model.eval()  # Set the model to evaluation mode

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])

    def forward(self, x):
        return self.model(x)

    def predict(self, image_path: str):
        """Make prediction on the input image"""
        img = Image.open(image_path).convert("RGB")
        tensor = self.transform(img).unsqueeze(0)
        labels = ["Action", "Comedy", "Drama", "Horror", "Romance"]

        with torch.no_grad():
            logits = self.model(tensor)
            probs = torch.nn.functional.softmax(logits.logits, dim=1)[0]

        best_idx = torch.argmax(probs).item()
        confidence = probs[best_idx].item()

        # Build a dictionary of all probabilities
        prob_dict = {labels[i]: round(probs[i].item(), 3) for i in range(len(labels))}

        print("Class probabilities:", prob_dict)

        return {
            "label": labels[best_idx],
            "confidence": round(confidence, 3),
            "predictions": prob_dict
        }



if __name__ == "__main__":
    classifier = GenreClassifier(checkpoint=None)

    checkpoint_path = "backend/app/models/genre_classifier.pt"
    
    os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)

    torch.save(classifier.state_dict(), checkpoint_path)
    print(f"Model saved at {checkpoint_path}")