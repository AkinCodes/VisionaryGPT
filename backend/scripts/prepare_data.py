from torchvision import datasets, transforms
from torch.utils.data import DataLoader

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  
])

def get_dataloader(data_dir, batch_size=32, shuffle=True):
    dataset = datasets.ImageFolder(root=data_dir, transform=transform)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, num_workers=4)
    return dataloader

def prepare_data():
    train_loader = get_dataloader('backend/app/data/poster_genres', batch_size=32)
    test_loader = get_dataloader('backend/app/data/poster_genres', batch_size=32, shuffle=False)
    return train_loader, test_loader


