from typing import List, Tuple

from py_to_ts_interfaces.type_converting import python_to_typescript_type
from py_to_ts_interfaces.utils import to_camel_case


class InterfaceField:
    """Represent a dataclass field."""
    name: str
    python_type: str
    is_nullable: bool

    def __init__(self, line: str):
        self.is_nullable = line.endswith(" = None") or "Union[" in line
        line = line.removesuffix(" = None")

        self.name, self.python_type = self.get_name_and_type(line)

    @staticmethod
    def get_name_and_type(line: str) -> Tuple[str, str]:
        """Take a line like "field_name: Union[None, int]" and return ("fieldName", "int")"""
        name, python_type = line.strip().split(": ")
        name = to_camel_case(name)
        if "Union[" in python_type:
            python_type = python_type.removeprefix("Union[None, ").removeprefix("Union[")
            python_type = python_type.removesuffix("]").removesuffix(", None")
        return name, python_type

    def get_typescript(self) -> str:
        """Return the field in typescript syntax (including indentation)."""
        ts_name = self.name
        if self.is_nullable:
            ts_name += "?"
        return "    {0}: {1};".format(ts_name, python_to_typescript_type(self.python_type))


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
