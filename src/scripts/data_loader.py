from src.utils.logger import get_logger
from src.utils.common import load_config
from src.features.transformer import get_transform
from src.features.dataloader import _DataLoader

from pathlib import Path
import json

logger = get_logger(__name__)

def data_loader_pipeline():
    logger.info("DataLoader pipeline started....")
   
    config = load_config()
    transform = get_transform()

    d_obj = _DataLoader(config=config, transform=transform)
    data_loader = d_obj.get_dataloader()

    sample = next(iter(data_loader))
    images, tokens = sample[0], sample[1]

    logger.info("loader loaded successfully.")
    logger.info(f"sample len: {len(sample)}")
    logger.info(f"images shape: {images.shape}")
    logger.info(f"tokens shape: {tokens.shape}")
    
if __name__ == "__main__":
    data_loader_pipeline()