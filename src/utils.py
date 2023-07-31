"""Support functions for the FortiCleaner script."""
import logging
from enum import Enum
from pathlib import Path

import yaml
from rich.logging import RichHandler

# Logging setup
logging.basicConfig(
    level=logging.WARN, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger("FortiCleaner")


class DefaultConfigKey(Enum):
    """Enum to define the default keys and values."""

    CONFIG_SECTIONS_TO_DELETE = []
    CONFIG_SECTIONS_TO_SORT = []
    CONFIG_SUBSECTIONS_TO_SORT = []
    DESTINATION_PATH = "sorted_config.cfg"
    FORTIOS_CONFIG_FILENAME_REGEX = "(.*).cfg"


def read_file(file_path_to_read_from: str) -> list[str]:
    """Read files."""
    config_file = Path(file_path_to_read_from)
    if config_file.exists():
        logger.debug(f"File '{file_path_to_read_from}' opened successfully")
        config = config_file.read_text(encoding="utf-8")
        return config.split("\n")
    else:
        logger.error(f"Error: File '{file_path_to_read_from}' not found")
        exit(1)


def write_file(content: list[str], file_path_to_write_to: str):
    """Write files."""
    out_file = Path(file_path_to_write_to)
    try:
        out_file.write_text("\n".join(content), encoding="utf-8")
        logger.debug(f"File '{file_path_to_write_to}' written successfully")
    except PermissionError:
        logger.error(f"Error: Permission denied to open file '{file_path_to_write_to}'")


def load_app_config() -> dict[str, str]:
    """Load the forticlean config file."""
    # Load the config file if found in the path the script is being called from
    if Path(".forticleaner").exists():
        config_path = Path(".forticleaner")
    # Load the config file if found in the user's home directory
    elif Path("~/.forticleaner").exists():
        config_path = Path("~/.forticleaner")
    # Load the default config file if not found anywhere else
    else:
        config_path = Path("src/conf/default.yaml")

    with open(config_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    logger.debug(f"Config '{config_path}' opened successfully")

    # use an enum to define the default keys and values

    for key in DefaultConfigKey:
        if key.name.lower() not in config:
            logging.debug(f"Key '{key.name}' NOT in the config file. Defaulting to {key.value}.")
            config[key.name.lower()] = key.value

    return config
