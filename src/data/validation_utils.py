from pathlib import Path
from PIL import Image


def get_images(img_dir: Path):
    return set([img.name for img in img_dir.glob("*.jpg")])


def load_captions(cap_file: Path):
    caption_map = {}
    invalid_lines = 0

    with open(cap_file, "r") as f:
        next(f)  # skip header

        for line in f:
            try:
                img, cap = line.strip().split(",", 1)

                if not cap.strip():
                    raise ValueError("Empty caption")

                caption_map.setdefault(img, []).append(cap)

            except Exception:
                invalid_lines += 1

    return caption_map, invalid_lines


def check_corrupted_images(img_dir: Path, images, limit=500):
    corrupted = []

    for img in list(images)[:limit]:
        try:
            with Image.open(img_dir / img) as im:
                im.verify()
        except Exception:
            corrupted.append(img)

    return corrupted