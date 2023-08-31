import logging
import os
from typing import Optional

import pytest

from src.main import delete_sections, remove_trailing_spaces, sort_config
from src.utils import read_file

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_files(directory: str = "./tests/inputs") -> list[str]:
    """Return a list of files in a directory."""
    return [
        f
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f)) and f.endswith(".cfg")
    ]


def common_test(
    test_file: str,
    function_to_test: str,
    optional_var: Optional = None,
    override_name: Optional[str] = None,
):
    """Define a common test for all functions."""

    orginal_config_lines = read_file(os.path.join(__location__, "inputs", test_file))
    function = globals()[function_to_test]
    if optional_var is None:
        new_config_lines = function(orginal_config_lines)
    else:
        if override_name is not None:
            function_to_test = override_name

        if override_name == "sort_config_subsections":
            new_config_lines = function(orginal_config_lines, optional_var, "    ", True)
        else:
            new_config_lines = function(orginal_config_lines, optional_var)

    expected_file = os.path.realpath(
        os.path.join(__location__, "expected", function_to_test, test_file)
    )
    try:
        with open(os.path.join(__location__, expected_file), "r") as f:
            expected_config_lines = f.read().split("\n")
    except FileNotFoundError:
        pytest.skip(f"Expected file '{os.path.relpath(expected_file)}' NOT found")
    if expected_config_lines != []:
        logging.info(f"new_config_lines {len(new_config_lines)}")
        logging.info(f"expected_file {len(expected_config_lines)}")
        assert expected_config_lines == new_config_lines
    else:
        pytest.skip("Expected config lines are EMPTY")


@pytest.mark.parametrize("test_file", get_files())
def test_remove_trailing_spaces(test_file: str):
    """Ensure that the function removes trailing spaces."""
    common_test(test_file, remove_trailing_spaces.__name__)


@pytest.mark.parametrize("test_file", get_files())
def test_delete_sections(test_file: str):
    """Ensure that the function removes user specified sections."""
    config_sections_to_delete = ["vpn certificate local"]
    common_test(test_file, delete_sections.__name__, config_sections_to_delete)


@pytest.mark.parametrize("test_file", get_files())
def test_sort_config_sections(test_file: str):
    """Ensure that the function removes user specified sections."""
    config_sections_to_sort = [
        "firewall address",
        "firewall addrgroup",
        "firewall internet-service-name",
        "router community-list",
        "router route-map",
        "system interface",
        "system zone",
    ]
    common_test(
        test_file,
        sort_config.__name__,
        config_sections_to_sort,
        "sort_config_sections",
    )


@pytest.mark.parametrize("test_file", get_files())
def test_sort_config_subsections(test_file: str):
    """Ensure that the function removes user specified sections."""
    config_subsections_to_sort = {"router bgp": ["neighbor", "network"]}
    common_test(
        test_file,
        sort_config.__name__,
        config_subsections_to_sort,
        "sort_config_subsections",
    )
