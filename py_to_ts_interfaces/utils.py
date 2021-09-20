def to_camel_case(snake_str: str) -> str:
    """
    Convert a snake_case string to camelCase.

    :param snake_str: The input in snake_case
    :return: The input, but in camelCase
    """
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])
