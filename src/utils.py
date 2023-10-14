"""Support functions for the FortiCleaner script."""
import logging
from enum import Enum
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft7Validator
from rich.logging import RichHandler

# Constants
BASE_DIR = Path(__file__).parent
CONFIG_SCHEMA_PATH = BASE_DIR / "conf/config_schema.yaml"

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


def load_config_schema(path: Path) -> dict:
    try:
        with path.open("r") as schema_file:
            return yaml.safe_load(schema_file)
    except FileNotFoundError:
        logger.error(f"Schema file '{path}' not found.")
        exit(1)
    except Exception as e:
        logger.error(f"Error reading schema file '{path}': {e}")
        exit(1)


def log_validation_error(error):
    """Log the validation error."""
    data_path = ".".join(map(str, error.path))
    invalid_value = error.instance

    if error.validator == "type":
        expected_type = error.schema["type"].upper()
        invalid_type = type(invalid_value).__name__.upper()
        logger.error(
            f"Config validation error at '{data_path}': Invalid value '{invalid_value}' "
            f"of type '{invalid_type}' when '{expected_type}' was expected"
        )
    elif error.validator == "pattern":
        pattern = error.schema["pattern"]
        logger.error(
            f"Config validation error at '{data_path}': Value '{invalid_value}' "
            f"should match the pattern '{pattern}'"
        )
    elif error.validator == "not":
        not_pattern = error.schema["not"]["pattern"]
        logger.error(
            f"Config validation error at '{data_path}': Value '{invalid_value}' "
            f"should NOT match the pattern '{not_pattern}'"
        )
    else:
        logger.error(error)


def validate_config(config: dict[str, Any]) -> None:
    """Validate the configuration against a JSON schema."""
    schema = load_config_schema(CONFIG_SCHEMA_PATH)
    validator = Draft7Validator(schema)
    errors = validator.iter_errors(config)

    has_errors = False
    for error in errors:
        log_validation_error(error)
        has_errors = True

    if has_errors:
        exit(1)

    logger.debug("Configuration is valid")


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

    validate_config(config)

    return config
