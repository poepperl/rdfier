from pathlib import Path
from typing import List


def get_all_files_in_path(
    path: str, file_type: str = "*", recursive: bool = True
) -> List[str]:
    """
    Creates a list of file pathes of all files found in the provided path.     

    Args:
        path (str): The base path to search files in.
        file_type (str, optional): The file type to search for. Defaults to "*".
        recursive (bool, optional): If all subdirectories serached recursively. Defaults to True.

    Returns:
        List[str]: List of files with there corresponding path
    """
    pattern = "**/*"
    if not recursive:
        pattern = "*"

    glob = f"{pattern}.{file_type}"
    return list(Path(path).glob(glob))
