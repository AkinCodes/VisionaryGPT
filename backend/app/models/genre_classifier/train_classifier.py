import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter
from transformers import ViTForImageClassification
from backend.scripts.prepare_data import prepare_data
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Evaluation imports
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt


def train_model(model, train_loader, optimizer, criterion, device, writer, epochs=10):
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        correct = 0
        total = 0

        for imgs, labels in train_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            optimizer.zero_grad()

            # Forward pass
            outputs = model(imgs).logits  # For ViT, the output logits are in the 'logits' attribute
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            pred = outputs.argmax(dim=1)
            correct += (pred == labels).sum().item()
            total += len(labels)

        avg_loss = total_loss / len(train_loader)
        accuracy = correct / total
        writer.add_scalar('Loss/train', avg_loss, epoch)
        writer.add_scalar('Accuracy/train', accuracy, epoch)

        print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}, Accuracy: {accuracy:.4f}")

    return model


def evaluate(model, test_loader, labels, device):
    model.eval()
    all_preds = []
    all_targets = []

    with torch.no_grad():
        for imgs, targets in test_loader:
            imgs = imgs.to(device)
            outputs = model(imgs).logits  # ViT's logits
            preds = outputs.argmax(dim=1).cpu().numpy()
            all_preds.extend(preds)
            all_targets.extend(targets.cpu().numpy())

    precision = precision_score(all_targets, all_preds, average="weighted")
    recall = recall_score(all_targets, all_preds, average="weighted")
    f1 = f1_score(all_targets, all_preds, average="weighted")

    print(f"\nEvaluation:")
    print(f"Precision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")
    print(f"F1-score:  {f1:.3f}")

    cm = confusion_matrix(all_targets, all_preds)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(xticks_rotation=45)

    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.savefig("app/logs/confusion_matrix.png")
    print("Saved: app/logs/confusion_matrix.png")


if __name__ == '__main__':
    # Initialize the ViT model with 5 output classes (Action, Comedy, Drama, Horror, Romance)
    model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224-in21k", num_labels=5)

    # Move model to device (GPU if available)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    # Define loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)
    writer = SummaryWriter(log_dir='app/logs/tensorboard')

    # Prepare data (train_loader, test_loader)
    train_loader, test_loader = prepare_data()

    # Train the model
    trained_model = train_model(model, train_loader, optimizer, criterion, device, writer, epochs=10)

    # Save the model weights after training
    torch.save(trained_model.state_dict(), 'backend/app/models/genre_classifier/vit_genre_classifier.pt')
    print("Model saved to app/models/genre_classifier/vit_genre_classifier.pt")

    # Evaluate the model
    evaluate(trained_model, test_loader, train_loader.dataset.classes, device)