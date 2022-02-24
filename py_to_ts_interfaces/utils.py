import re


def to_camel_case(snake_str: str) -> str:
    """
    Convert a snake_case string to camelCase.

    :param snake_str: The input in snake_case.
    :return: The input, but in camelCase.
    """
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])


def is_class_definition(line: str) -> bool:
    """
    Check if the given string is a class definition, e.g. "class MyInterface:"

    :param line: The string to check (should be one line of code).
    :return: True if the given string is a class definition.
    """
    return line.startswith("class ")


def is_string_definition(line: str) -> bool:
    """
    Check if the given string is a string definition. Ignores type hints such as Final.
    e.g. CONSTANT_STRING: Final = "example"

    :param line: The string to check (should be one line of code).
    :return: True if the given string is a string definition.
    """
    return re.match("[a-zA-Z_]+.* = \".*\"", line) is not None
