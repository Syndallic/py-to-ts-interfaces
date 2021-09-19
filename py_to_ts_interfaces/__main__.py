import os
import sys
from typing import Union
import argparse

from py_to_ts_interfaces.enums import EnumDefinition
from py_to_ts_interfaces.file_io import write_file, read_file
from py_to_ts_interfaces.interfaces import InterfaceDefinition


def python_to_typescript_file(python_code: str) -> str:
    """
    Convert python enum and dataclass definitions to equivalent typescript code.

    :param python_code: Python code containing only enums and dataclasses.
    :return: Equivalent typescript code.
    """
    # initial processing (remove superfluous lines)
    lines = python_code.splitlines()
    lines = [line for line in lines if line and not line.isspace() and not line.startswith(("from ", "#", "@"))]

    # group the lines for each enum/class definition together
    definition_groups: list[list[str]] = []
    for line in lines:
        if line.startswith("class "):
            definition_groups.append([])
        definition_groups[-1].append(line)

    # convert each group into either an EnumDefinition or InterfaceDefinition object
    processed_definitions: list[Union[EnumDefinition, InterfaceDefinition]] = []
    for definition in definition_groups:
        if definition[0].endswith("(Enum):"):
            processed_definitions.append(EnumDefinition(definition))
        else:
            processed_definitions.append(InterfaceDefinition(definition))

    # construct final output
    typescript_output = "/* eslint-disable @typescript-eslint/no-unused-vars */\n"
    for processed_definition in processed_definitions:
        typescript_output += "\n{}\n".format(processed_definition.get_typescript())
    typescript_output.strip("\n")

    return typescript_output


def python_to_typescript_folder(input_path: str, output_path: str) -> None:
    """
    Convert all python files in input directory to typescript files in output directory. Each output file has the
    same name as its python source (with the file extension changed to 'ts').

    :param input_path: A full or relative path to a folder containing .py files.
    :param output_path: A full or relative path to a folder which may not exist.
    """
    for file in os.listdir(input_path):
        if file.endswith(".py") and file != "__init__.py":
            file_contents = read_file(os.path.join(input_path, file))

            typescript_output = python_to_typescript_file(file_contents)

            write_file(typescript_output, os.path.join(output_path, file[:-3] + ".ts"))


def main():
    """Main script."""
    parser = argparse.ArgumentParser()
    parser.add_argument("input_folder", help="The path to the folder of python files to be converted")
    parser.add_argument("output_folder", help="The path to the folder to output the typescript files to")
    args = parser.parse_args()

    python_to_typescript_folder(args.input_folder, args.output_folder)


if __name__ == "__main__":
    sys.exit(main())
