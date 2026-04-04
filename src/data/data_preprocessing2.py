import json
from pathlib import Path
from src.utils.logger import get_logger
from src.data.vocabulary_utils import Vocabulary

logger = get_logger(__name__)


def convert_to_posix(path: str):
    return str(Path(path).as_posix())


class DataProcessing2:
    def __init__(self, config):
        self.config = config

        self.interim_path = Path(config["data_path"]["interim_data_path"]) / "processed_data.json"
        self.processed_dir = Path(config["data_path"]["process_data_path"])

        self.processed_path = self.processed_dir / "dataset_encoded.json"
        self.vocab_path = self.processed_dir / "vocab.json"

    def load_data(self):
        if not self.interim_path.exists():
            logger.error(f"File not found: {self.interim_path}")
            raise FileNotFoundError()

        with open(self.interim_path, "r") as f:
            data = json.load(f)

        logger.info(f"Loaded data from {self.interim_path}")
        return data

    def build_vocab(self, data):
        vocab = Vocabulary(min_freq=2)

        logger.info("Building vocabulary...")

        for obj in data:
            story = obj["story"]
            vocab.build_vocab(story)

        logger.info(f"Vocab size: {len(vocab)}")
        return vocab

    def encode_dataset(self, data, vocab):
        processed_data = []

        logger.info("Encoding dataset...")

        for obj in data:
            images = obj["images"]
            story = obj["story"]

            token_ids = vocab.encode(story)

            processed_data.append({
                "images": [convert_to_posix(img) for img in images],
                "tokens": token_ids
            })

        return processed_data

    def save_outputs(self, processed_data, vocab):
        self.processed_dir.mkdir(parents=True, exist_ok=True)

        # save dataset
        with open(self.processed_path, "w") as f:
            json.dump(processed_data, f, indent=4)

        logger.info(f"Saved encoded dataset at: {self.processed_path}")

        # save vocab
        with open(self.vocab_path, "w") as f:
            json.dump(vocab.word2idx, f, indent=4)

        logger.info(f"Saved vocab at: {self.vocab_path}")
    
    def run(self):
        logger.info("Starting DataProcessing2 pipeline...")

        data = self.load_data()
        vocab = self.build_vocab(data)
        processed_data = self.encode_dataset(data, vocab)

        self.save_outputs(processed_data, vocab)

        logger.info("Data processing completed successfully.")

