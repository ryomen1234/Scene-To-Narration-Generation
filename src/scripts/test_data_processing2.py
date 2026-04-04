from src.utils.logger import get_logger
from src.utils.common import load_config
from pathlib import Path 

from src.data.data_preprocessing2 import DataProcessing2

logger = get_logger(__name__)

def data_processing_pipelin2():
    logger.info("Starting DataPreprocessing2 pipeline....")

    config = load_config()

    processor2 = DataProcessing2(config)
    processor2.run()

if __name__ == "__main__":
    data_processing_pipelin2()
