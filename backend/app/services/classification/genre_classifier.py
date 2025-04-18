import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

class GenreClassifier(nn.Module):
    def __init__(self, num_classes=5, checkpoint=None):
        super(GenreClassifier, self).__init__()
        
        # Load the pretrained ResNet-18 model
        self.model = models.resnet18(pretrained=True)
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)  # Action, Comedy, Drama, Horror, Romance

        if checkpoint:
            self.model.load_state_dict(torch.load(checkpoint, map_location="cpu"))
        
        self.model.eval()  

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)), 
            transforms.ToTensor(),  
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), 
        ])

    def forward(self, x):
        return self.model(x)


    def predict(self, image_path: str):
      """Make prediction on the input image"""
      img = Image.open(image_path).convert("RGB") 
      tensor = self.transform(img).unsqueeze(0) 
      with torch.no_grad():  
        logits = self.model(tensor) 
        probs = torch.nn.functional.softmax(logits, dim=1)[0]  

      best_idx = torch.argmax(probs).item() 
      confidence = probs[best_idx].item() 
      labels = ["Action", "Comedy", "Drama", "Horror", "Romance"]

      print("Class probabilities:", {labels[i]: round(probs[i].item(), 3) for i in range(len(probs))})

      if confidence < 0.5:
        return {"error": "Classification confidence too low", "all_probabilities": {labels[i]: round(probs[i].item(), 3) for i in range(len(probs))}}

      return {
        "label": labels[best_idx],
        "confidence": round(confidence, 3),
        "all_probabilities": {labels[i]: round(probs[i].item(), 3) for i in range(len(probs))}
      }



if __name__ == "__main__":
    classifier = GenreClassifier(checkpoint=None)

    checkpoint_path = "backend/app/models/genre_classifier.pt"
    
    os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)

    torch.save(classifier.state_dict(), checkpoint_path)
    print(f"Model saved at {checkpoint_path}")
