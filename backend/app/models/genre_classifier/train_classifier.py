import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter
from backend.app.services.classification.genre_classifier import GenreClassifier
from backend.scripts.prepare_data import prepare_data

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

            outputs = model(imgs)
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
            outputs = model(imgs)
            preds = outputs.argmax(dim=1).cpu().numpy()
            all_preds.extend(preds)
            all_targets.extend(targets.cpu().numpy())

    precision = precision_score(all_targets, all_preds, average="weighted")
    recall = recall_score(all_targets, all_preds, average="weighted")
    f1 = f1_score(all_targets, all_preds, average="weighted")

    print(f"\n Evaluation:")
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
    model = GenreClassifier(num_classes=5)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)
    writer = SummaryWriter(log_dir='app/logs/tensorboard')

    train_loader, test_loader = prepare_data()

    trained_model = train_model(model, train_loader, optimizer, criterion, device, writer, epochs=10)

    torch.save(trained_model.state_dict(), 'backend/app/models/genre_classifier/genre_classifier.pt')
    print("Model saved to app/models/genre_classifier/genre_classifier.pt")

    evaluate(trained_model, test_loader, train_loader.dataset.classes, device)
