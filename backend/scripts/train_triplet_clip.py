# Triplet loss training for CLIP
from torch.utils.data import Dataset, DataLoader
from PIL import Image
from torchvision import transforms


class PosterTripletDataset(Dataset):
    def __init__(self, triplet_json):
        import json

        with open(triplet_json) as f:
            self.triplets = json.load(f)

        self.transform = transforms.Compose(
            [transforms.Resize((224, 224)), transforms.ToTensor()]
        )

    def __len__(self):
        return len(self.triplets)

    def __getitem__(self, idx):
        t = self.triplets[idx]
        a = self.transform(Image.open(t["anchor"]).convert("RGB"))
        p = self.transform(Image.open(t["positive"]).convert("RGB"))
        n = self.transform(Image.open(t["negative"]).convert("RGB"))
        return a, p, n
