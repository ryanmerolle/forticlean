import typer

from src.constants import (
    CONFIG_SECTIONS_TO_DELETE,
    CONFIG_SECTIONS_TO_SORT,
    CONFIG_SUBSECTIONS_TO_SORT,
    DST_FILE_PATH,
    SRC_FILE_PATH,
)
from src.utils import logging, read_file, write_file

app = typer.Typer(
    help="Clean & sort FortiOS config files.",
    add_completion=True,
)


def delete_sections(
    config_lines: list[str], sections_to_delete: list[str] = CONFIG_SECTIONS_TO_DELETE
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
    append_sorted_sections(sorted_config, sorted_items, indentation, success_log_msg)


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
                subsections.append(read_section(config, f"{indentation}    next"))

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


@app.command()
def main(
    src_file_path: str = typer.Argument(None),
    dst_file_path: str = typer.Option(DST_FILE_PATH, "--dst_file_path", "-d"),
):
    config_lines = read_file(src_file_path)
    config_lines = delete_sections(config_lines, CONFIG_SECTIONS_TO_DELETE)
    config_lines = remove_trailing_spaces(config_lines)
    config_lines = sort_config(config_lines, CONFIG_SECTIONS_TO_SORT)
    config_lines = sort_config(config_lines, CONFIG_SUBSECTIONS_TO_SORT, "    ", True)

    write_file(config_lines, dst_file_path)


if __name__ == "__main__":
    app()
