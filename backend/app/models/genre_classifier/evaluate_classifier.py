import torch
import torch.nn as nn
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from app.models.genre_classifier.genre_classifier import GenreClassifier
from app.scripts.prepare_data import test_loader

# Load the trained model
model = GenreClassifier(num_classes=5)
model.load_state_dict(torch.load('app/models/genre_classifier/genre_classifier.pt'))
model.eval()

def evaluate(model, test_loader):
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for imgs, labels in test_loader:
            outputs = model(imgs)
            preds = outputs.argmax(dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    precision = precision_score(all_labels, all_preds, average='weighted')
    recall = recall_score(all_labels, all_preds, average='weighted')
    f1 = f1_score(all_labels, all_preds, average='weighted')

    print(f"Precision: {precision:.3f}")
    print(f"Recall: {recall:.3f}")
    print(f"F1 Score: {f1:.3f}")

    cm = confusion_matrix(all_labels, all_preds)
    sns.heatmap(cm, annot=True, fmt='d', cmap="Blues")
    plt.title("Confusion Matrix")
    plt.savefig("app/logs/confusion_matrix.png")
    plt.show()

# Evaluate the model
evaluate(model, test_loader)
