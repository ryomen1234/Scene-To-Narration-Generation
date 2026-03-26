from src.utils.common import load_config
from src.data.data_validation import DataValidation
from src.utils.logger import get_logger
from pathlib import Path
import json

logger = get_logger(__name__)


def data_validation_pipeline():
    logger.info("Starting validation pipeline...")

    config = load_config()

    validator = DataValidation(config)
    stats = validator.validate()

    # Save report
    report_path = Path("artifacts/reports/data_validation_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, "w") as f:
        json.dump(stats, f, indent=4)

    logger.info(f"Validation report saved at: {report_path}")


if __name__ == "__main__":
    data_validation_pipeline()