import os
import torch
import torch.nn as nn
import logging
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from transformers import ViTForImageClassification, ViTImageProcessor
from backend.scripts.prepare_data import prepare_data


os.makedirs("backend/app/logs", exist_ok=True)
logging.basicConfig(
    filename="backend/app/logs/metrics.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224-in21k', num_labels=5)
model.load_state_dict(torch.load("backend/app/models/genre_classifier/vit_genre_classifier.pt", map_location=device))
model.to(device)
model.eval()

# Load image processor
image_processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224-in21k')

def evaluate(model, test_loader):
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for imgs, labels in test_loader:
            # Process images using ViTImageProcessor
            inputs = image_processor(images=imgs, return_tensors="pt")
            inputs = {k: v.to(device) for k, v in inputs.items()}
            labels = labels.to(device)

            outputs = model(**inputs)
            logits = outputs.logits
            preds = torch.argmax(logits, dim=-1)

            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    # Metrics
    precision = precision_score(all_labels, all_preds, average='weighted')
    recall = recall_score(all_labels, all_preds, average='weighted')
    f1 = f1_score(all_labels, all_preds, average='weighted')

    logging.info(f"Precision: {precision:.3f}")
    logging.info(f"Recall: {recall:.3f}")
    logging.info(f"F1 Score: {f1:.3f}")

    print(f"Precision: {precision:.3f}")
    print(f"Recall: {recall:.3f}")
    print(f"F1 Score: {f1:.3f}")

    # Save predictions, labels, and metrics to CSV
    results_df = pd.DataFrame({
        'True Label': all_labels,
        'Predicted Label': all_preds,
    })

    results_df.to_csv('backend/app/logs/predictions.csv', index=False)

    # Confusion matrix
    cm = confusion_matrix(all_labels, all_preds)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap="Blues")
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()
    plt.savefig("backend/app/logs/confusion_matrix.png")
    plt.close()

def main():
    train_loader, test_loader = prepare_data()
    evaluate(model, test_loader)

if __name__ == "__main__":
    main()
