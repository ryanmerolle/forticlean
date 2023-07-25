import logging
from pathlib import Path

from rich.logging import RichHandler

# Logging setup
logging.basicConfig(
    level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger("FortiCleaner")


def read_file(file_path_to_read_from: str) -> list[str]:
    config_file = Path(file_path_to_read_from)
    if config_file.exists():
        logger.info(f"File '{file_path_to_read_from}' opened successfully")
        config = config_file.read_text(encoding="utf-8")
        return config.split("\n")
    else:
        logger.error(f"Error: File '{file_path_to_read_from}' not found")
        return []


def write_file(content: list[str], file_path_to_write_to: str):
    out_file = Path(file_path_to_write_to)
    try:
        out_file.write_text("\n".join(content), encoding="utf-8")
        logger.info(f"File '{file_path_to_write_to}' written successfully")
    except PermissionError:
        logger.error(f"Error: Permission denied to open file '{file_path_to_write_to}'")
