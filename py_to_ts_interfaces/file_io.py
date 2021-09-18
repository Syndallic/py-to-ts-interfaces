import os


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
