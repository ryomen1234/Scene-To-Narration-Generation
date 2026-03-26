from pathlib import Path
from src.utils.logger import get_logger
from src.data.validation_utils import (
    get_images,
    load_captions,
    check_corrupted_images,
)

logger = get_logger(__name__)


class DataValidation:
    def __init__(self, config):
        self.raw_path = Path(config["data_path"]["raw_data_path"])
        self.img_dir = self.raw_path / "Images"
        self.cap_file = self.raw_path / "captions.txt"

    def check_paths(self):
        if not self.raw_path.exists():
            raise FileNotFoundError(f"Raw path not found: {self.raw_path}")

        if not self.img_dir.exists():
            raise FileNotFoundError(f"Images folder not found: {self.img_dir}")

        if not self.cap_file.exists():
            raise FileNotFoundError(f"Captions file not found: {self.cap_file}")

        logger.info("All paths exist")

    def validate(self):
        logger.info("Starting data validation...")

        self.check_paths()

        # Images
        images = get_images(self.img_dir)
        logger.info(f"Total images: {len(images)}")

        # Captions
        caption_map, invalid_lines = load_captions(self.cap_file)
        logger.info(f"Captioned images: {len(caption_map)}")
        logger.warning(f"Invalid lines: {invalid_lines}")

        # Missing checks
        missing_captions = [img for img in images if img not in caption_map]
        missing_images = [img for img in caption_map if img not in images]

        if missing_captions:
            logger.warning(f"Images without captions: {len(missing_captions)}")

        if missing_images:
            logger.warning(f"Captions without images: {len(missing_images)}")

        # Caption count check
        wrong_caption_count = [
            img for img, caps in caption_map.items() if len(caps) < 5
        ]

        if wrong_caption_count:
            logger.warning(f"Images with <5 captions: {len(wrong_caption_count)}")

        # Corruption check
        corrupted = check_corrupted_images(self.img_dir, images)

        if corrupted:
            logger.warning(f"Corrupted images: {len(corrupted)}")

        logger.info("Data validation completed")

        return {
            "total_images": len(images),
            "captioned_images": len(caption_map),
            "invalid_lines": invalid_lines,
            "missing_captions": len(missing_captions),
            "missing_images": len(missing_images),
            "corrupted_images": len(corrupted),
        }