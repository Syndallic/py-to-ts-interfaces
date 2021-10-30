python_to_typescript_type_map = {
    "str": "string",
    "int": "number",
    "float": "number",
    "complex": "number",
    "bool": "boolean",
    "List[int]": "number[]",
    "List[str]": "string[]",
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
