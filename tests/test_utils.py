import os

from src.utils import load_app_config, read_file, write_file


def test_read_file(tmp_path):
    # Create a temporary file with some content
    file_path = tmp_path / "test.txt"
    file_path.write_text("Hello, world!\nHow are you?\n")

    # Test that the file is read correctly
    assert read_file(file_path) == ["Hello, world!", "How are you?", ""]


def test_write_file(tmp_path):
    # Create a temporary file and write some content to it
    file_path = tmp_path / "test.txt"
    write_file(["Hello, world!", "How are you?"], file_path)

    # Test that the file was written correctly
    assert file_path.read_text() == "Hello, world!\nHow are you?"


def test_load_app_config(tmp_path):
    # Change the working directory to the temporary directory
    os.chdir(tmp_path)
    # Create a temporary config file with some content
    config_path = tmp_path / ".forticleaner"
    config_path.write_text(
        "config_sections_to_delete:\n  - section1\nconfig_sections_to_sort:\n  - section2\nconfig_subsections_to_sort: []\n"
    )

    file_contents = config_path.read_text()
    print(f"Contents of the config file:\n{file_contents}")
    print(tmp_path)
    current_path = os.getcwd()
    print(f"Current Path: {current_path}")

    # Test that the config is loaded correctly
    assert load_app_config() == {
        "config_sections_to_delete": ["section1"],
        "config_sections_to_sort": ["section2"],
        "config_subsections_to_sort": [],
        "destination_path": "sorted_config.cfg",
        "fortios_config_filename_regex": "(.*).cfg",
    }


# def test_validate_config(tmp_path):
#    # Create a temporary config file with some content
#    config_path = tmp_path / "test.yaml"
#    config_path.write_text("config_sections_to_delete:\n  - section1\n  - section2\n")
#
#    # Test that the config is validated correctly
#    assert validate_config({"config_sections_to_delete": ["section1", "section2"]}) is None
#    with pytest.raises(SystemExit):
#        validate_config({"config_sections_to_delete": "not a list"})    with pytest.raises(SystemExit):
#            validate_config({"config_sections_to_delete": "not a list"})
#            validate_config({"config_sections_to_delete": "not a list"})
