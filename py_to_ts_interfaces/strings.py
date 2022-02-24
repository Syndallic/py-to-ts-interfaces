import re
from typing import List


class StringDefinition:
    """Represent a string definition."""
    name: str
    value: str

    def __init__(self, definition: List[str]):
        matches = re.match("([a-zA-Z_]+).* = \"(.*)\"", definition[0])
        if matches:
            self.name = matches.group(1)
            self.value = matches.group(2)

    def get_typescript(self) -> str:
        """Return the string definition in typescript syntax."""
        typescript_string = "export const {0} = '{1}';".format(self.name, self.value)
        return typescript_string
