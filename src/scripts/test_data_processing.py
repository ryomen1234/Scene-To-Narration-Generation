from src.data.data_preprocessing import DataPreprocessing
from src.utils.logger import get_logger
from src.utils.common import load_config

from pathlib import Path 

logger = get_logger(__name__)

def data_preprocessing_pipeline():
    logger.info("Starting DataPreprocessing pipeline....")

    config = load_config()

    processor = DataPreprocessing(config=config)
    processor.run_data_processing()


if __name__ == "__main__":
    data_preprocessing_pipeline()

