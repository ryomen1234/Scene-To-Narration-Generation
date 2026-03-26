import yaml
from pathlib import Path
from functools import lru_cache
from src.utils.logger import get_logger

logger = get_logger(__name__)


@lru_cache()
def load_config(config_path: Path | str | None = None) -> dict:
    """
    Load YAML configuration file.

    Args:
        config_path (Path | str | None): Optional custom config path

    Returns:
        dict: Parsed configuration

    Raises:
        FileNotFoundError: If config file does not exist
        ValueError: If YAML is empty or invalid
    """

    # Resolve path safely
    if config_path is None:
        project_root = Path(__file__).resolve().parents[2]
        config_path = project_root / "config" / "config.yaml"
    else:
        config_path = Path(config_path)

    # Check existence
    if not config_path.exists():
        logger.error(f"Config file not found: {config_path}")
        raise FileNotFoundError(f"{config_path} not found")

    # Load YAML
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        if not config:
            raise ValueError("Config file is empty or invalid YAML")

        logger.info(f"Config loaded successfully from: {config_path}")

    except Exception as e:
        logger.exception(f"Failed to load config: {e}")
        raise

    return config