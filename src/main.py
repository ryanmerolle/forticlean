"""Main file that gets called my forticlean."""
from typing import Union

import typer

from src.utils import load_app_config, logging, read_file, write_file

CONFIG_LINE_PREFIX = "config "

app_config = load_app_config()

app = typer.Typer(
    help="Clean & sort FortiOS config files.",
    add_completion=True,
)


def delete_sections(config_lines: list[str], sections_to_delete: list[str]) -> list[str]:
    """Delete sections from the FortiOS config file."""
    new_lines = []
    section = ""
    delete_line = False

    for line in config_lines:
        if (
            line.startswith(CONFIG_LINE_PREFIX)
            and line[len(CONFIG_LINE_PREFIX):] in sections_to_delete
        ):
            delete_line = True
            section = line
            continue

        if line == "end" and delete_line:
            delete_line = False
            logging.info(f"Section config '{section}' was DELETED.")
            continue

        if not delete_line:
            new_lines.append(line)

    return new_lines


def remove_trailing_spaces(config_lines: list[str]) -> list[str]:
    """Remove trailing spaces from the FortiOS config file."""
    count = sum(line.rstrip() != line for line in config_lines)
    cleaned_lines = [line.rstrip() for line in config_lines]

    logging.info(f"Removed trailing space(s) from {count} lines.")
    return cleaned_lines


def sort_config_sections(sections: list[str]) -> tuple[list[str], bool]:
    """Sort the sections of the FortiOS config file."""
    sorted_sections = sorted(sections, key=lambda s: s[0])
    is_sorted = sections != sorted_sections
    return sorted_sections, is_sorted


def read_section(lines: list[str], section_end: str = "    next"):
    """Read a section from the FortiOS config file."""
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
    sorted_config: list[str], sorted_items: list[str], indentation: str, success_log_msg: str
):
    """Append the sorted sections to the FortiOS config file."""
    for item in sorted_items:
        sorted_config.extend(item)
        sorted_config.append(f"{indentation}    next")

    logging.info(success_log_msg)


def sort_section(
    sorted_config: list[str], config: list[str], config_section: str, indentation: str
):
    """Sort a section from the FortiOS config file."""
    sections = []
    while config and not config[0].startswith("config ") and config[0] != "end":
        sections.append(read_section(config, f"{indentation}    next"))

    sorted_items, is_sorted = sort_config_sections(sections)

    success_log_msg = (
        f"Section config '{config_section}' was {'SORTED' if is_sorted else 'NOT SORTED'}"
    )
    append_sorted_sections(sorted_config, sorted_items, indentation, success_log_msg)


def sort_subsection(
    sorted_config: list[str],
    config: list[str],
    config_section: str,
    indentation: str,
    subsections: list[str],
):
    """Sort a subsection from the FortiOS config file."""
    while config and not config[0].startswith("config ") and config[0] != "end":
        logging.info(f"TEST {subsections}")
        line = config[0]
        if (
            line.strip().startswith(CONFIG_LINE_PREFIX)
            and line.strip()[len(CONFIG_LINE_PREFIX):] in subsections
        ):
            child_section_name = config.pop(0)
            sorted_subsections = []
            while (
                config
                and not config[0].startswith(f"{indentation}config ")
                and config[0] != "    end"
            ):
                sorted_subsections.append(read_section(config, f"{indentation}    next"))

            sorted_items, is_sorted = sort_config_sections(sorted_subsections)
            sorted_config.append(child_section_name)
            success_log_msg = (
                f"Section config '{config_section}' SubSection '{child_section_name.strip()}' ",
                f"was {'SORTED' if is_sorted else 'NOT SORTED'}",
            )
            append_sorted_sections(sorted_config, sorted_items, indentation, success_log_msg)

        else:
            sorted_config.append(config.pop(0))


def sort_config(
    config: list[str],
    config_sections_to_sort: Union[dict[str, list[str]], list[str]],
    indentation: str = "",
    is_subsection: bool = False,
) -> list[str]:
    """Sort the FortiOS config file."""
    sorted_config = []
    while config:
        line = config[0]
        if (
            line.startswith(CONFIG_LINE_PREFIX)
            and line[len(CONFIG_LINE_PREFIX):] in config_sections_to_sort
        ):
            sorted_config.append(line)
            config.pop(0)

            if is_subsection:
                sort_subsection(
                    sorted_config,
                    config,
                    line,
                    indentation,
                    config_sections_to_sort[line[len(CONFIG_LINE_PREFIX):]],
                )
            else:
                sort_section(sorted_config, config, line, indentation)
        else:
            sorted_config.append(config.pop(0))

    return sorted_config


@app.command()
def main(
    src_file_path: str = typer.Argument(None, help="Path to the source file"),
    dst_file_path: str = typer.Option(
        app_config["destination_path"],
        "--dst_file_path",
        "-d",
        help="Path to the write file",
    ),
    verbosity: int = typer.Option(
        0, "-v", "--verbose", count=True, help="Enable level of verbose mode"
    ),
):
    """Clean & sort FortiOS config files."""
    if verbosity >= 2:
        logging.getLogger().setLevel(logging.DEBUG)
    elif verbosity >= 1:
        logging.getLogger().setLevel(logging.INFO)

    config_lines = read_file(src_file_path)
    config_lines = delete_sections(config_lines, app_config["config_sections_to_delete"])
    config_lines = remove_trailing_spaces(config_lines)
    config_lines = sort_config(config_lines, app_config["config_sections_to_sort"])
    config_lines = sort_config(config_lines, app_config["config_subsections_to_sort"], "    ", True)
    write_file(config_lines, dst_file_path)


if __name__ == "__main__":
    app()
