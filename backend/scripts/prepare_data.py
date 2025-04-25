from torchvision import datasets
from torch.utils.data import DataLoader
import torch

def pil_collate_fn(batch):
    images, labels = zip(*batch)
    return list(images), torch.tensor(labels)

def get_dataloader(data_dir, batch_size=32, shuffle=True):
    dataset = datasets.ImageFolder(root=data_dir) 
    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=0,
        collate_fn=pil_collate_fn 
    )
    return dataloader

def prepare_data():
    train_loader = get_dataloader('backend/app/data/poster_genres', batch_size=32)
    test_loader = get_dataloader('backend/app/data/poster_genres', batch_size=32, shuffle=False)
    return train_loader, test_loader
