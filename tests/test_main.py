import os
import pytest
from forticlean.main import delete_sections, remove_trailing_spaces, sort_config
from forticlean.utils import read_file


def get_files(directory: str) -> list[str]:
    """Returns a list of files in a directory"""
    return [
        f
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f)) and f.endswith(".cfg")
    ]


def get_test_files(expected_dir: str) -> list[tuple[str, str]]:
    """Returns a list of tuples with input and expected files"""
    input_files = get_files("./tests/inputs")
    excepted_files = get_files(f"./tests/expected/{expected_dir}")
    return [
        (
            f"./tests/inputs/{input_file}",
            f"./tests/expected/{expected_dir}/{expected_file}",
        )
        for input_file, expected_file in zip(input_files, excepted_files)
    ]


@pytest.mark.parametrize(
    (
        "input_file",
        "expected_file",
    ),
    get_test_files("remove_trailing_spaces"),
)
def test_remove_trailing_spaces(input_file: str, expected_file: str):
    """
    Ensure that the function removes trailing spaces
    """
    orginal_config_lines = read_file(input_file)
    new_config_lines = remove_trailing_spaces(orginal_config_lines)
    expected_config_lines = read_file(expected_file)
    assert new_config_lines == expected_config_lines


@pytest.mark.parametrize(
    (
        "input_file",
        "expected_file",
    ),
    get_test_files("delete_sections"),
)
def test_delete_sections(input_file: str, expected_file: str):
    """
    Ensure that the function removes intended sections
    """
    CONFIG_SECTIONS_TO_DELETE = ["config vpn certificate local"]
    orginal_config_lines = read_file(input_file)
    new_config_lines = delete_sections(orginal_config_lines, CONFIG_SECTIONS_TO_DELETE)
    expected_config_lines = read_file(expected_file)
    assert new_config_lines == expected_config_lines


@pytest.mark.parametrize(
    (
        "input_file",
        "expected_file",
    ),
    get_test_files("sort_config_sections"),
)
def test_sort_config_sections(input_file: str, expected_file: str):
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
    orginal_config_lines = read_file(input_file)
    new_config_lines = sort_config(orginal_config_lines, CONFIG_SECTIONS_TO_SORT)
    expected_config_lines = read_file(expected_file)
    assert new_config_lines == expected_config_lines


@pytest.mark.parametrize(
    (
        "input_file",
        "expected_file",
    ),
    get_test_files("sort_config_subsections"),
)
def test_sort_config_subsections(input_file: str, expected_file: str):
    """
    Ensure that the function sorts intended subsections
    """
    CONFIG_SUBSECTIONS_TO_SORT = {
        "config router bgp": ["config neighbor", "config network"],
    }
    orginal_config_lines = read_file(input_file)
    new_config_lines = sort_config(
        orginal_config_lines, CONFIG_SUBSECTIONS_TO_SORT, "    ", True
    )
    expected_config_lines = read_file(expected_file)
    assert new_config_lines == expected_config_lines
