from torch.utils.data import Dataset
from PIL import Image
import torch

def pad_sequence(tokens, max_len: int, pad_idx: int):
    tokens = list(tokens)  # safety

    if len(tokens) > max_len:
        return tokens[:max_len]
    else:
        return tokens + [pad_idx] * (max_len - len(tokens))

class StoryDataset(Dataset):
    def __init__(self, data, transformer: None, max_len=256, pad_idx: int= 0) -> None:
        self.data = data 
        self.transformer = transformer
        self.max_len = max_len
        self.pad_idx = pad_idx
  
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, key):
        img_paths, story = self.data[key]["images"], self.data[key]["tokens"]

        images = []
        for img_path in img_paths:
            img = Image.open(img_path)
            if self.transformer:
                img = self.transformer(img)
            images.append(img)
        
        images = torch.stack(images)

        token = pad_sequence(story, self.max_len, self.pad_idx)
        token = torch.tensor(token)
     
        return images, token

        

