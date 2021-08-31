import os
import sys
from typing import List, Union
import argparse

python_to_typescript_type_map = {
    "str": "string",
    "int": "number",
    "float": "number",
    "complex": "number",
    "bool": "bool",
    "List[int]": "Array[number]",
    "List[str]": "Array[string]"
}


def python_to_typescript_type(python_type: str) -> str:
    """
    Map python type to an equivalent typescript type.

    :param python_type: A python type like 'str' or 'int'.
    :return: An equivalent typescript type. If there is no known mapping for the input, then it is returned as-is for
    enum support.
    """
    try:
        return python_to_typescript_type_map[python_type]
    except KeyError:
        # This should mean it is an enum
        return python_type


class InterfaceField:
    """Represent a dataclass field."""
    name: str
    python_type: str

    def __init__(self, line: str):
        self.name, self.python_type = line.strip().split(": ")

    def get_typescript(self) -> str:
        """Return the field in typescript syntax (including indentation)."""
        return "    {0}: {1};".format(self.name, python_to_typescript_type(self.python_type))


class InterfaceDefinition:
    """Represent a python dataclass/typescript interface."""
    name: str
    fields: List[InterfaceField]

    def __init__(self, definition: List[str]):
        self.name = definition[0].removeprefix("class ").strip(":")
        self.fields = [InterfaceField(line) for line in definition[1:]]

    def get_typescript(self) -> str:
        """Return the entire interface in typescript syntax (including indentation)."""
        typescript_string = "export interface {0} {{\n".format(self.name)
        for field in self.fields:
            typescript_string += "{}\n".format(field.get_typescript())
        typescript_string += "}"
        return typescript_string


class EnumElement:
    """Represent one element of an enum."""
    name: str
    value: str

    def __init__(self, line: str):
        name_and_value = line.strip().split(" = ")
        self.name = name_and_value[0]
        self.value = name_and_value[1].strip("\"")

    def get_typescript(self) -> str:
        """Return the element in typescript syntax (including indentation)."""
        return "    {0} = \'{1}\',".format(self.name, self.value)


class EnumDefinition:
    """Represent a python/typescript enum."""
    name: str
    elements: List[EnumElement]

    def __init__(self, definition: List[str]):
        self.name = definition[0].removeprefix("class ").removesuffix("(Enum):")
        self.elements = [EnumElement(line) for line in definition[1:]]

    def get_typescript(self) -> str:
        """Return the enum in typescript syntax (including indentation)."""
        typescript_string = "enum {0} {{\n".format(self.name)
        for element in self.elements:
            typescript_string += "{}\n".format(element.get_typescript())
        typescript_string += "}"
        return typescript_string


def read_file(file_path: str) -> str:
    """Read content of file provided."""
    with open(file_path, "r", encoding="utf-8") as reader:
        return reader.read()


def write_file(to_write: str, file_path: str) -> None:
    """Write input string to file."""
    folder_path = os.path.dirname(file_path)
    if folder_path and not os.path.isdir(folder_path):
        os.makedirs(folder_path)
    with open(file_path, "w+", encoding="utf-8") as writer:
        writer.write(to_write)


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
    typescript_output = "/* eslint-disable no-unused-vars */\n"
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
