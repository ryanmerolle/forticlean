import logging
from pathlib import Path

import coloredlogs

CONFIG_SECTIONS_TO_SORT = (
    "config firewall address",
    "config firewall addrgroup",
    "config firewall internet-service-name",
    "config router community-list",
    "config router route-map",
    "config system interface",
    "config system zone",
)
CONFIG_SUBSECTIONS_TO_SORT = {
    "config router bgp": ["config neighbor", "config network"],
}
FILE_PATH = "config.cfg"
NEW_FILE_PATH = "sorted_config.cfg"

CONFIG_SECTIONS_TO_DELETE = ("config vpn certificate local",)

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


def delete_sections(
    config_lines: list[str], sections_to_delete: list[str]
) -> list[str]:
    new_lines = []
    section = ""
    delete_line = False

    for line in config_lines:
        if line in sections_to_delete:
            delete_line = True
            section = line
            continue

        if line == "end" and delete_line:
            delete_line = False
            logging.info(f"Section '{section}' was DELETED.")
            continue

        if not delete_line:
            new_lines.append(line)

    return new_lines


def remove_trailing_spaces(config_lines: list[str]) -> list[str]:
    count = sum(line.rstrip() != line for line in config_lines)
    cleaned_lines = [line.rstrip() for line in config_lines]

    logging.info(f"Removed trailing space(s) from {count} lines.")
    return cleaned_lines


def sort_config_sections(sections: list[str]) -> tuple[list[str], bool]:
    sorted_sections = sorted(sections, key=lambda s: s[0])
    is_sorted = sections != sorted_sections
    return sorted_sections, is_sorted


def read_section(lines: list[str], section_end: str = "    next"):
    section = []
    while lines:
        line = lines[0]
        if line.startswith(section_end):
            lines.pop(0)
            break
        else:
            section.append(lines.pop(0))

    return section


def append_sorted_sections(
    sorted_config: list, sorted_items: list, indentation: str, success_log_msg: str
):
    for item in sorted_items:
        sorted_config.extend(item)
        sorted_config.append(f"{indentation}    next")

    logging.info(success_log_msg)


def sort_section(sorted_config, config, config_section, indentation):
    sections = []
    while config and not config[0].startswith("config ") and config[0] != "end":
        sections.append(read_section(config, f"{indentation}    next"))

    sorted_items, is_sorted = sort_config_sections(sections)

    success_log_msg = (
        f"Section '{config_section}' was {'SORTED' if is_sorted else 'NOT SORTED'}"
    )
    append_sorted_sections(sorted_config, sorted_items,
                           indentation, success_log_msg)


def sort_subsection(sorted_config, config, config_section, indentation):
    while config and not config[0].startswith("config ") and config[0] != "end":
        if config[0].strip() in CONFIG_SUBSECTIONS_TO_SORT[config_section]:
            child_section_name = config.pop(0)
            subsections = []
            while (
                config
                and not config[0].startswith(f"{indentation}config ")
                and config[0] != "    end"
            ):
                subsections.append(read_section(
                    config, f"{indentation}    next"))

            sorted_items, is_sorted = sort_config_sections(subsections)
            sorted_config.append(child_section_name)
            success_log_msg = f"Section '{config_section}' SubSection '{child_section_name.strip()}' was {'SORTED' if is_sorted else 'NOT SORTED'}"
            append_sorted_sections(
                sorted_config, sorted_items, indentation, success_log_msg
            )

        else:
            sorted_config.append(config.pop(0))


def sort_config(
    config: list[str],
    config_sections_to_sort: tuple,
    indentation: str = "",
    is_subsection: bool = False,
) -> list[str]:
    sorted_config = []
    while config:
        line = config[0]
        if line in config_sections_to_sort:
            line = line
            sorted_config.append(line)
            config.pop(0)

            if is_subsection:
                sort_subsection(
                    sorted_config,
                    config,
                    line,
                    indentation,
                )
            else:
                sort_section(sorted_config, config, line, indentation)
        else:
            sorted_config.append(config.pop(0))

    return sorted_config


def main():
    config_lines = read_file(FILE_PATH).split("\n")
    config_lines = delete_sections(config_lines, CONFIG_SECTIONS_TO_DELETE)
    config_lines = remove_trailing_spaces(config_lines)
    config_lines = sort_config(config_lines, CONFIG_SECTIONS_TO_SORT)
    config_lines = sort_config(
        config_lines, CONFIG_SUBSECTIONS_TO_SORT, "    ", True)

    write_file(config_lines, NEW_FILE_PATH)


if __name__ == "__main__":
    main()
