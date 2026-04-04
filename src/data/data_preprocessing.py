from pathlib import Path 
from collections import defaultdict
import random
import json

from src.utils.logger import get_logger

logger = get_logger(__name__)

class DataPreprocessing:

    def __init__(self, config):
        self.config = config 
        self.raw_dir = Path(config["data_path"]["raw_data_path"])
        self.interim_dir = Path(config["data_path"]["interim_data_path"])
        self.images = self.raw_dir / "Images"
        self.captions = self.raw_dir / "captions.txt"
    
    def check_paths(self):
        if not self.raw_dir.exists():
            logger.error(f"Directory path not found: {self.raw_dir}")
            raise FileNotFoundError()
        
        if not self.interim_dir.exists():
            logger.error(f"Directory path not found: {self.raw_dir}")
            raise FileNotFoundError()

        if not self.images.exists():
            logger.error(f"{self.images} dir don't exists")
            raise Exception(f"Images dir don't exists")
        
        if not self.captions.exists():
            logger.error(f"file don't exists {self.captions}")
            raise FileNotFoundError()
    
    def genearte_caption_map(self, cap_file: Path):

        caption_map = defaultdict(list)

        with  open(cap_file, "r") as f:
            next(f)
            for line in f:
                img, cap = line.strip().split(",",1)
                caption_map[img].append(cap)
        
        return caption_map
    
    def story_dataset(self, sequence, caption_map):
        dataset = []

        for seq in sequence:

            if len(seq) < 5:
                continue
            
            caps = []

            for img in seq:
                cap = random.choice(caption_map[img])
                caps.append(cap)
            
            story = " ".join(caps)

            dataset.append({
                "images" : [str(self.images / img) for img in seq],
                "story": story
            })

        return dataset
        
    def run_data_processing(self):

        logger.info("Starting data processing.....")
        logger.info("Check for paths existence")
        
        self.check_paths()
        logger.info("all paths exists")

        caption_map = self.genearte_caption_map(self.captions)

        images = list(caption_map.keys())
        random.shuffle(images)

        sequence = [images[i:i+5] for i in range(0, len(images), 5)]

        dataset = self.story_dataset(sequence=sequence, caption_map=caption_map)

        # store the dataset
        save_path = self.interim_dir / "processed_data.json"
        try:

            with open(save_path, "w") as f:
                json.dump(dataset, f, indent=4)
            
            logger.info(f"Dataset saved at: {save_path}")
        except Exception as e:
            logger.exception("Failed to save dataset")
            raise


        









        
       
        

        
                            