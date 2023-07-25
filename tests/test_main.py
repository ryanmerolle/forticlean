import os
import pytest
from src.main import delete_sections, remove_trailing_spaces, sort_config
from src.utils import read_file


def get_files(directory: str) -> list[str]:
    """Returns a list of files in a directory"""
    return [
        f
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f)) and f.endswith(".cfg")
    ]


def get_test_files(expected_dir: str) -> list[tuple[str, str]]:
    """Returns a list of tuples with input and expected files"""
    test_files = get_files("./tests/inputs")
    return [
        (
            f"./tests/inputs/{test_file}",
            f"./tests/expected/{expected_dir}/{test_file}",
        )
        for test_file in test_files
    ]


def common_test(expected_file: str, new_config_lines: list[str]):
    """Defines a common test for all functions"""
    expected_config_lines = read_file(expected_file)
    if expected_config_lines != []:
        assert new_config_lines == expected_config_lines
    else:
        pytest.skip("Expected config lines are empty")


@pytest.mark.parametrize(
    (
        "test_file",
        "expected_file",
    ),
    get_test_files("remove_trailing_spaces"),
)
def test_remove_trailing_spaces(test_file: str, expected_file: str):
    """
    Ensure that the function removes trailing spaces
    """
    orginal_config_lines = read_file(test_file)
    new_config_lines = remove_trailing_spaces(orginal_config_lines)
    common_test(expected_file, new_config_lines)


@pytest.mark.parametrize(
    (
        "test_file",
        "expected_file",
    ),
    get_test_files("delete_sections"),
)
def test_delete_sections(test_file: str, expected_file: str):
    """
    Ensure that the function removes intended sections
    """
    CONFIG_SECTIONS_TO_DELETE = ["config vpn certificate local"]
    orginal_config_lines = read_file(test_file)
    new_config_lines = delete_sections(orginal_config_lines, CONFIG_SECTIONS_TO_DELETE)
    common_test(expected_file, new_config_lines)


@pytest.mark.parametrize(
    (
        "test_file",
        "expected_file",
    ),
    get_test_files("sort_config_sections"),
)
def test_sort_config_sections(test_file: str, expected_file: str):
    """
    Ensure that the function sorts intended sections
    """
    CONFIG_SECTIONS_TO_SORT = {
        "config firewall address",
        "config firewall addrgroup",
        "config firewall internet-service-name",
        "config router community-list",
        "config router route-map",
        "config system interface",
        "config system zone",
    }
    orginal_config_lines = read_file(test_file)
    new_config_lines = sort_config(orginal_config_lines, CONFIG_SECTIONS_TO_SORT)
    common_test(expected_file, new_config_lines)


@pytest.mark.parametrize(
    (
        "test_file",
        "expected_file",
    ),
    get_test_files("sort_config_subsections"),
)
def test_sort_config_subsections(test_file: str, expected_file: str):
    """
    Ensure that the function sorts intended subsections
    """
    CONFIG_SUBSECTIONS_TO_SORT = {
        "config router bgp": ["config neighbor", "config network"],
    }
    orginal_config_lines = read_file(test_file)
    new_config_lines = sort_config(
        orginal_config_lines, CONFIG_SUBSECTIONS_TO_SORT, "    ", True
    )
    common_test(expected_file, new_config_lines)
