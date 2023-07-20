import logging
from pathlib import Path

import coloredlogs

# Logging setup
logging.basicConfig(level=logging.INFO)
logging.getLogger(name="FortiCleaner")
coloredlogs.install(logging=logging)


def read_file(file_path_to_read_from: str) -> str:
    config_file = Path(file_path_to_read_from)
    if config_file.exists():
        logging.info(f"File '{file_path_to_read_from}' opened successfully")
        return config_file.read_text(encoding="utf-8")
    else:
        logging.error(f"Error: File '{file_path_to_read_from}' not found")
        return ""


def write_file(content: list[str], file_path_to_write_to: str):
    out_file = Path(file_path_to_write_to)
    try:
        out_file.write_text("\n".join(content), encoding="utf-8")
        logging.info(f"File '{file_path_to_write_to}' written successfully")
    except PermissionError:
        logging.error(
            f"Error: Permission denied to open file '{file_path_to_write_to}'"
        )
