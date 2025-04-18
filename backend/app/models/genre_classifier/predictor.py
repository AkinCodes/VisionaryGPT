import torch
from app.models.genre_classifier.genre_classifier import GenreClassifier
from PIL import Image
from torchvision import transforms

# Load the model
model = GenreClassifier(num_classes=5)
model.load_state_dict(torch.load('app/models/genre_classifier/genre_classifier.pt'))
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def predict_genre(image_path):
    img = Image.open(image_path).convert("RGB")
    img_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        outputs = model(img_tensor)
        probs = torch.nn.functional.softmax(outputs, dim=1)[0]
        genre_idx = torch.argmax(probs).item()
        genre = ["Action", "Comedy", "Drama", "Horror", "Romance"][genre_idx]
        confidence = probs[genre_idx].item()

    return {
        "genre": genre,
        "confidence": round(confidence, 3)
    }

# Testing testing: python predict_genre.py
image_path = 'path_to_poster.jpg'
result = predict_genre(image_path)
print(f"Predicted Genre: {result['genre']}, Confidence: {result['confidence']}")
