# Manually supporting dict types scales pretty badly, so the python_to_typescript_type function handles them
# programmatically for the sake of sanity.
python_to_typescript_type_map = {
    "str": "string",
    "int": "number",
    "float": "number",
    "complex": "number",
    "bool": "boolean",
    "List[str]": "string[]",
    "List[int]": "number[]",
    "List[float]": "number[]",
    "List[complex]": "number[]",
    "List[bool]": "boolean[]",
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
        if python_type.startswith("Dict["):
            python_type = python_type.removeprefix("Dict[").removesuffix("]").replace(" ", "")
            # This part handles nested dicts
            py_type_1, py_type_2 = python_type.split(",", 1)
            ts_type_1 = python_to_typescript_type(py_type_1)
            ts_type_2 = python_to_typescript_type(py_type_2)
            return f"Record<{ts_type_1}, {ts_type_2}>"
        elif python_type.startswith("List["):
            # This means the list contains an unknown type - likely an enum
            python_type = python_type.removeprefix("List[").removesuffix("]")
            return f"{python_type}[]"
        else:
            # This should mean it is an enum
            return python_type
