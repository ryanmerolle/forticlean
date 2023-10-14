# FORTICLEAN

[![Build Tests](https://github.com/ryanmerolle/forticlean/actions/workflows/build-tests.yml/badge.svg?event=push)](https://github.com/ryanmerolle/forticlean/actions/workflows/build-tests.yml)
[![CodQL Analysis](https://github.com/ryanmerolle/forticlean/actions/workflows/codeql-analysis.yml/badge.svg?event=push)](https://github.com/ryanmerolle/forticlean/actions/workflows/codeql-analysis.yml)
[![Dependency Review](https://github.com/ryanmerolle/forticlean/actions/workflows/dependency-review.yml/badge.svg?event=push)](https://github.com/ryanmerolle/forticlean/actions/workflows/dependency-review.yml)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/forticlean)](https://pypi.org/project/forticlean)

## Description

FortiClean is a CLI tool designed for FortiOS configuration file management for better readability and comparision.
Built with Python & leverages the power of the typer library, this utility streamlines the process of:

- **Trimming Trailing Spaces**: Say goodbye to unwanted spaces at the end of your config lines that complicate diffs, but do not affect the configuration.
- **Removing Specific Sections**: Clean up your config file by specifying & deleting sections do not wish to save. A handy feature for decluttering and maintaining a streamlined configuration setup.
- **Sorting Config Sections & Subsections**: Enhance readability & structure by sorting specified config sections for enhanced readbility. It is recommended you do not sort config sections like firewall policy where order matters.

Unlike other network operatin systems, sections where config order does not matter is hapazardly saved in the order the config was entered making automated & manual diff operations challenging

## Features

- Trim spaces at the end of a line
- Delete config sections
- Sort config sections
- Sort config sections 1 level down
- Colored Logs
- Use jsonschemea to warn of config file errors
- Use jsonschema in tests
- Command line arguments to specify config, path, etc **COMING SOON**
- Prevent or WARN on the sorting of sections where order matters **COMING SOON**

## Getting Started

Clone the repo, move to the directory & run one of the below:

### Configuration

In order of precedence:
1.) .forticleaner in the directory you are running the script from
2.) .forticleaner in your home directory
3.) Default config file included with the package

### Usage

```console
main [OPTIONS] [SRC_FILE_PATH]
```

### Arguments

- `[SRC_FILE_PATH]`: Path to the source file

### Options

- `-d, --dst_file_path TEXT`: Path to the write file  [default: sorted_config.cfg]
- `-v, --verbose`: Enable level of verbose mode  [default: 0]
- `--install-completion`: Install completion for the current shell.
- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
- `--help`: Show this message and exit.

```bash
python3 src/main.py config.cfg
```

### Verbose Mode (1 level)

```bash
$ python3 src/main.py config.cfg -v
[13:42:07] INFO     Section 'config vpn certificate local' was DELETED.                                                                               main.py:27
           INFO     Removed trailing space(s) from 0 lines.                                                                                           main.py:40
           INFO     Section 'config system zone' was NOT SORTED                                                                                       main.py:70
           INFO     Section 'config system interface' was NOT SORTED                                                                                  main.py:70
           INFO     Section 'config firewall internet-service-name' was SORTED                                                                        main.py:70
```

## Verbose Mode (2 levels)

```bash
$ python3 src/main.py config.cfg -vv
[13:42:48] DEBUG    Config 'src/conf/default.yaml' opened successfully                                                                               utils.py:57
           DEBUG    Key 'FORTIOS_CONFIG_FILENAME_REGEX' NOT in the config file. Defaulting to (.*).cfg.                                              utils.py:63
           DEBUG    File 'config.cfg' opened successfully                                                                                            utils.py:26
           INFO     Section 'config vpn certificate local' was DELETED.                                                                               main.py:27
           INFO     Removed trailing space(s) from 0 lines.                                                                                           main.py:40
           INFO     Section 'config system zone' was NOT SORTED                                                                                       main.py:70
           INFO     Section 'config system interface' was NOT SORTED                                                                                  main.py:70
           INFO     Section 'config firewall internet-service-name' was SORTED                                                                        main.py:70
           DEBUG    File 'sorted_config.cfg' written successfully                                                                                    utils.py:38
```
