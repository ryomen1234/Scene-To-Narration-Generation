from src.features.dataset import StoryDataset
from src.features.transformer import get_transform
from torch.utils.data import DataLoader
from src.utils.logger import get_logger

from pathlib import Path
import json

logger = get_logger(__name__)

class _DataLoader:
    def __init__(self, config, transform) -> None:
        self.config = config 
        self.transform = transform
        self.processed_dir = Path(config["data_path"]["process_data_path"])
        self.data_path = self.processed_dir / "dataset_encoded.json"
        self.max_len = config["parameters"]["max_len"]
        self.batch_size = config["parameters"]["batch_size"]
        self.pad_idx = config["parameters"]["pad_idx"]
        self.num_workers = config["parameters"]["num_worker"]
    
    def load_data(self):
        if not self.data_path.exists():
            logger.error(f"{self.data_path} file not found.")
            raise
        
        try:
            with open(self.data_path, "r") as f:
                data = json.load(f)
            
            logger.info(f"Data loaded successfully from {self.data_path}")
        except Exception as e:
            logger.exception(f"Some unexpected error {e}")
            raise

        return data
        

    def get_dataloader(self):

        logger.info("DataLoader loading.....")

        data = self.load_data()
       
        story_data = StoryDataset(data, transformer=self.transform, max_len=self.max_len, pad_idx=self.pad_idx)

        dataloader = DataLoader(
            dataset=story_data,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=self.num_workers
        )
        
        return dataloader